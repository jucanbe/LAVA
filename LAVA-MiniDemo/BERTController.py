from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline
import torch
import itertools
from KnowledgeGraphController import store_ner_re_in_rdf
from Utils import print_entities_and_relations
from nltk.tokenize import sent_tokenize
import nltk
nltk.download("punkt")

ner_tokenizer = AutoTokenizer.from_pretrained("models/NER/tokenizer")
ner_model = AutoModelForTokenClassification.from_pretrained("models/NER/model")
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple")

re_tokenizer = AutoTokenizer.from_pretrained("models/RE/tokenizer")
re_model = AutoModelForSequenceClassification.from_pretrained("models/RE/model")
re_model.eval().to("cuda" if torch.cuda.is_available() else "cpu")

def insert_entity_markers(text, entity1, entity2):
    ents = sorted([entity1, entity2], key=lambda x: x['start'])
    marked = (
        text[:ents[0]['start']] + "<e1>" + text[ents[0]['start']:ents[0]['end']] + "</e1>" +
        text[ents[0]['end']:ents[1]['start']] + "<e2>" + text[ents[1]['start']:ents[1]['end']] + "</e2>" +
        text[ents[1]['end']:]
    )
    return marked

def aggregate_entities(ner_output):
    entities = []
    current = None
    for ent in ner_output:
        if current is None:
            current = ent.copy()
        elif ent["entity_group"] == current["entity_group"] and ent["start"] == current["end"]:
            current["word"] += ent["word"].replace("##", "")
            current["end"] = ent["end"]
            current["score"] = max(current["score"], ent["score"])
        else:
            entities.append(current)
            current = ent.copy()
    if current:
        entities.append(current)
    return entities

def predict_relation(marked_text, tokenizer, model, id2label):
    inputs = tokenizer(
        marked_text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=128
    )
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        logits = model(**inputs).logits
        pred = torch.argmax(logits, dim=1).item()
    return id2label[pred]

def process_text(text, id2label, output_file="knowledge_graph.ttl"):
    raw_ner = ner_pipeline(text)
    entities = aggregate_entities(raw_ner)
    if not entities:
        print("No entities found.")
        return [], [], None
    relations = []
    for e1, e2 in itertools.combinations(entities, 2):
        marked_text = insert_entity_markers(text, e1, e2)
        label = predict_relation(marked_text, re_tokenizer, re_model, id2label)
        relations.append((e1, e2, label))
    store_ner_re_in_rdf(entities, relations, output_file)
    print_entities_and_relations(entities, relations)
    return entities, relations, output_file

def process_paragraph_by_index(indices, filepath="Text/test.dat", id2label=None):
    if id2label is None:
        raise ValueError("You must provide the id2label dictionary.")

    if isinstance(indices, int):
        indices = [indices]

    with open(filepath, "r", encoding="utf-8") as f:
        paragraphs = [line.strip() for line in f if line.strip()]

    max_index = len(paragraphs) - 1
    for index in indices:
        if index < 0 or index > max_index:
            print(f"Invalid index {index}. File has {len(paragraphs)} paragraphs.")
            continue

        paragraph = paragraphs[index]
        print(f"\nParagraph {index}:\n{paragraph}\n")

        sentences = sent_tokenize(paragraph)

        for i, sentence in enumerate(sentences):
            print(f"--Sentence {i+1}:\n{sentence}")
            entities, relations, graph_file = process_text(sentence, id2label, output_file="knowledge_graph.ttl")
            print_entities_and_relations(entities, relations)