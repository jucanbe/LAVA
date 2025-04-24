
def print_entities_and_relations(entities, relations):
    print("\nEntities:")
    for ent in entities:
        print(f" - {ent['word']} ({ent['entity_group']})")
    print("\nRelations:")
    for e1, e2, label in relations:
        print(f" - {e1['word']} -> {e2['word']}: {label}")

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