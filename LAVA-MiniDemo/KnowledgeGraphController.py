from rdflib import Graph, Namespace, URIRef, Literal, RDF
import os

def make_uri(entity_name):
    return URIRef(f"http://example.org/entity/{entity_name.lower()}")

def store_ner_re_in_rdf(entities, relations, output_file="knowledge_graph.ttl"):
    g = Graph()
    if os.path.exists(output_file):
        g.parse(output_file, format="turtle")
    EX = Namespace("http://example.org/")
    g.bind("ex", EX)
    for ent in entities:
        uri = make_uri(ent["word"])
        g.add((uri, RDF.type, EX[ent["entity_group"]]))
        g.add((uri, EX.label, Literal(ent["word"])))
    for e1, e2, rel in relations:
        subj = make_uri(e1["word"])
        obj = make_uri(e2["word"])
        g.add((subj, EX[rel], obj))
    g.serialize(destination=output_file, format="turtle")