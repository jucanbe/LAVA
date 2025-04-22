import json
import os
import csv
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

def extract_entity_mentions(passage):
    """Extract entity mentions from a passage."""
    entities = {}
    for ann in passage.get("annotations", []):
        ent_id = ann["infons"]["identifier"]
        ent_text = ann["text"]
        context = passage["text"]
        entities.setdefault(ent_id, []).append(ent_text)
    return entities


def find_sentence_with_entities(text, ent1, ent2):
    """Return the sentence containing both entities."""
    for sentence in sent_tokenize(text):
        if ent1 in sentence and ent2 in sentence:
            return sentence
    return None


def mark_entities(sentence, ent1, ent2):
    """Write labels around the entities in the sentence."""
    if ent1 == ent2:
        first = sentence.find(ent1)
        second = sentence.find(ent2, first + 1)
        if first != -1 and second != -1:
            return (
                sentence[:first] + "<e1>" + ent1 + "</e1>" +
                sentence[first+len(ent1):second] + "<e2>" + ent2 + "</e2>" +
                sentence[second+len(ent2):]
            )
    else:
        sentence = sentence.replace(ent1, f"<e1>{ent1}</e1>", 1)
        sentence = sentence.replace(ent2, f"<e2>{ent2}</e2>", 1)
    return sentence


def process_bioc_file(input_path):
    """Process a file and extract relations."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for doc in data["documents"]:
        for passage in doc["passages"]:
            text = passage["text"]
            entities = extract_entity_mentions(passage)

            for rel in doc.get("relations", []):
                ent1_id = rel["infons"]["entity1"]
                ent2_id = rel["infons"]["entity2"]
                label = rel["infons"]["type"]

                for ent1 in entities.get(ent1_id, []):
                    for ent2 in entities.get(ent2_id, []):
                        sentence = find_sentence_with_entities(text, ent1, ent2)
                        if sentence:
                            marked = mark_entities(sentence, ent1, ent2)
                            results.append([marked, label])
                            break
    return results


def convert_all(input_dir, output_dir, filenames):
    os.makedirs(output_dir, exist_ok=True)

    for in_file, out_file in filenames.items():
        input_path = os.path.join(input_dir, in_file)
        output_path = os.path.join(output_dir, out_file)

        rows = process_bioc_file(input_path)
        with open(output_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["text", "relation"])
            writer.writerows(rows)

        print(f"File {input_path} processed and saved to {output_path}.")


base_input = "Datasets/biored/Original"
base_output = "Datasets/biored/Processed"
files = {
    "Train.BioC.JSON": "biored_train.csv",
    "Dev.BioC.JSON": "biored_dev.csv",
    "Test.BioC.JSON": "biored_test.csv"
}

convert_all(base_input, base_output, files)