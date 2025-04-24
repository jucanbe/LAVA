from rdflib import Graph, Namespace, URIRef, Literal, RDF
import os
import re

def make_uri(entity_name):
    tokens = re.findall(r"[a-zA-Z0-9]+", entity_name)
    clean_name = tokens[0].lower() + ''.join(t.capitalize() for t in tokens[1:])
    return URIRef(f"http://example.org/entity/{clean_name}")

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