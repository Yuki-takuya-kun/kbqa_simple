from rdflib import Graph, Literal
from rdflib.namespace import RDFS

g = Graph()
cg = Graph()
eg = Graph()
RDF_LIST = ['character', 'epidemiology', 'event', 'health', 'medical',
            'prevention', 'research', 'resource', 'wiki']

for file in RDF_LIST:
    print(file)
    route = f"D:/Datasets/KG/{file}/{file}.nt"
    g.parse(route)
    eset = set()
    cset = set()
    for sbj in g.subjects():
        if str(sbj).find("resource") != -1:
            eset.add(sbj)
        elif str(sbj).find("class") != -1:
            cset.add(sbj)
    for entity in eset:
        for label in g.objects(subject=entity, predicate=RDFS.label):
            if isinstance(label, Literal):
                if label.language is not None and label.language == 'en':
                    continue
                label = Literal(str(label))
                eg.add((entity, RDFS.label, label))
    for cls in cset:
        for label in g.objects(subject=cls, predicate=RDFS.label):
            if isinstance(label, Literal):
                if label.language is not None and label.language == 'en':
                    continue
                label = Literal(str(label))
                cg.add((cls, RDFS.label, label))
    
    eg.serialize(f"D:/Datasets/KG/{file}/{file}_entity.nt", format='nt')
    cg.serialize(f"D:/Datasets/KG/{file}/{file}_class.nt", format='nt')
    g.remove((None, None, None))
    eg.remove((None, None, None))
    cg.remove((None, None, None))