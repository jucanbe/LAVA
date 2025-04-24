from BERTController import process_text

id2label = {
    0: 'Agonist', 
    1: 'Antagonist', 
    2: 'Association', 
    3: 'Bind', 
    4: 'Comparison', 
    5: 'Cotreatment', 
    6: 'Downregulator', 
    7: 'Negative_Correlation', 
    8: 'Not', 
    9: 'Part_of', 
    10: 'Positive_Correlation', 
    11: 'Regulator', 
    12: 'Substrate', 
    13: 'Upregulator'
}

def print_entities_and_relations(entities, relations):
    print("\nEntities:")
    for ent in entities:
        print(f" - {ent['word']} ({ent['entity_group']})")
    print("\nRelations:")
    for e1, e2, label in relations:
        print(f" - {e1['word']} → {e2['word']}: {label}")


text = "TP53 regulates MDM2 expression in cancer cells."
entities, relations, graph_file = process_text(text, id2label)
print_entities_and_relations(entities, relations)

text = "Aspirins cures fever."
entities, relations, graph_file = process_text(text, id2label)
print_entities_and_relations(entities, relations)
