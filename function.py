import json
import pandas as pd
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDFS

# def search(g:Graph, q, info):
#     if len(q) == 1:
#         if q[0] == PDC:
#             sbj, obj = info
#             g.predicates(subject=sbj, object=obj)

def get_label(g:Graph):
    uris = []
    labels = []
    for sbj, obj in g.subject_objects(predicate=URIRef("http://www.w3.org/2000/01/rdf-schema#label")):
        mdict[str(sbj)] = str(obj)
    
    with open('D:/Datasets/KG/labels.json','w') as f:
        json.dump(mdict, f)
map_dict = 
{
    
}
        