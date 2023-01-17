from rdflib import Graph, RDFS, URIRef, Literal
from rdflib.namespace import Namespace
class_list = []
conception = Namespace("http://www.openkg.cn/COVID-19/wiki/resource/")
with open("D:/Datasets/KG/conception/conception_schema.csv",'r',encoding='utf8') as f:
    cg = Graph()
    for line in f.readlines():
        Id, _, _, label = line.split(',')
        label = label.replace('\n','')
        cg.add((URIRef(Id), RDFS.label, Literal(label)))
        
        
    cg.serialize("D:/Datasets/KG/conception/conception_class.nt", format='nt')

with open("D:/Datasets/KG/conception/xinguan_entities.csv", 'r', encoding='utf8') as f:
    eg = Graph()
    
    for i, line in enumerate(f.readlines()):
        label = line.replace('\n','')
        
        sbj = URIRef(conception[f'P{i}'])
        eg.add((sbj, RDFS.label, Literal(label)))
        
    eg.serialize("D:/Datasets/KG/conception/conception_entity.nt", format='nt')