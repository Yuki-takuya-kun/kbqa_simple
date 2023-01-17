import json

# with open('./KG/wiki/wiki.json','r', encoding='utf-8') as f:
#     data = json.load(f)

# graph = data['@graph']


# for dt in graph:
#     for key, val in dt.items():
#         if isinstance(val, str):
#             val = val.replace(' ', '_').replace('\u00a0','_').replace('%','%25').replace('>','%3E').replace('[','%5B').replace(']','5D').replace('\u3000','_')
#             val = val.replace('<','%3C').replace('－','-').replace('|','%7C').replace('"','').replace('`','%27').replace('^','%5E').replace('{','%7B').replace('\\','%5C')
#             dt[key] = val.replace('}','%7D')
            
            
# with open('./KG/wiki/wiki_copy.json', 'w', encoding='utf-8') as fc:
#     json.dump(data, fc, indent=4, ensure_ascii=False)

# from xml.dom.minidom import parse
# import os
# for file in os.listdir("D:/Datasets/KG/matching/files_result"):
#     dom = parse(f"D:/Datasets/KG/matching/files_result/{file}")
#     data = dom.documentElement
#     stus = data.getElementsByTagName('Cell')
#     for stu in stus:
#         source = stu.getElementsByTagName('entity1')[0].getAttribute('rdf:resource')
#         target = stu.getElementsByTagName('entity2')[0].getAttribute('rdf:resource')
        


"""transform to nt"""
from pathlib import Path

import rdflib
from rdflib import Graph, Literal
from rdflib.namespace import RDFS, RDF, Namespace, XSD, OWL
g = Graph()

route_1 = "wiki"
# route_2 = "epidemiology"
# g.parse(f"D:/Datasets/KG/{route_1}/{route_1}.json")
# g.parse(f"./KG/{route_2}/{route_2}.json")
# g.parse("D:/Datasets/Tutorial_Test_Data/interest_triple_actor_final_pku_label.nt")
# g.parse("D:/Datasets/KG/wiki/wiki.json")
# for triple in g:
#     subject, depricated, object = triple
#     if str(object).find("file") != -1:
#         n_object = Literal(str(object).split('/')[-1])
#         g.remove((subject, depricated, object))
#         g.add((subject,depricated, n_object))
        
# g.serialize(format="nt", destination="D:/Datasets/KG/wiki/wiki.nt")
# cara = Namespace("http://www.openkg.cn/COVID-19/character/")
# epid = Namespace("http://www.openkg.cn/COVID-19/epidemiology/")
# conp = Namespace("http://www.openkg.cn/COVID-19/wiki/class/")
# event = Namespace("http://www.openkg.cn/COVID-19/event/")
# health = Namespace("http://www.openkg.cn/2019-nCoV/health/")
# medical = Namespace("http://www.openkg.cn/COVID-19/medical/")
# prevention = Namespace("http://www.openkg.cn/COVID-19/prevention/")
# research = Namespace("http://www.openkg.cn/COVID-19/research/")
# goods = Namespace("http://www.openkg.cn/COVID-19/goods/")
# wiki = Namespace("http://www.openkg.cn/COVID-19/wiki/")
# entity = epid.property
# entity = cara.resource
#entity = conp
#entity = event.property
# entity = health.property
# entity = medical.resource
# entity = prevention.resource
# entity = research.property
# entity = goods.resource
# entity = wiki.resource
# v = g.serialize(format="xml", destination=f"./KG/{route_1}-{route_2}.xml")
# class_uris = [subject for subject in g.subjects(RDF.type, RDFS.Class)]

# attribute_uris = set()
# relation_uris = set()
# for predicate in g.predicates(None,None):
#     if str(predicate).find(str(cara.property)) != -1:
#         attribute_uris.update([predicate])
#     elif str(predicate).find(str(RDFS.label)) == -1:
#         relation_uris.update([predicate])
# attribute_uris = list(attribute_uris)
# relation_uris = list(relation_uris)

# class_label = []
# for class_uri in class_uris:
#     for label in g.objects(class_uri,RDFS.label):
#         class_label.append(label)



"""transfomer"""
# ng = Graph()
# i = 0
# for triple in g.triples((None, RDFS.label, None)):
#     subject = str(triple[0])
    
#     if subject.find(str(entity)) != -1:
#         text = str(triple[2])
#         # text = text.encode("unicode_escape").decode("ascii")
#         literal = Literal(text)
#         ng.add((triple[0], triple[1], literal))
        

# ng.serialize(format="nt", destination=f"D:/Datasets/KG/{route_1}/{route_1}_alab.nt", encoding='UTF-8')

# a = [1,2,3]
# for i, b in enumerate(a):
#     print(i)
    
    
    
# attribute_uris = [subject for subject in g.subjects(rdflib.RDF.type, rdflib.OWL.DatatypeProperty) if namespace in str(subject)]
# for s, p, o in g.triples((None,RDFS.label, None)):
#     print(s,p,o)
#     break
# print(len(g))
# print(len(v))

"""transform to unicode"""
# file_name = 'epidemiology'
# file_path = f"./KG/{file_name}/{file_name}.nt"
# save_path = f"./KG/{file_name}/{file_name}_ascii.nt"

# import chardet
# import codecs
    
# # with codecs.open(file_path, 'r', encoding='utf-8') as f_in:
# #     new_content  = f_in.read()
# #     f_out = codecs.open(save_path, 'w', 'unicode')
# #     f_out.write(new_content)
# #     f_out.close()

# def get_line(file_path):
#     with open(file_path, 'r', encoding='utf8') as f:
#         for line in f:
#             yield line


# with open(save_path, 'w', encoding='ascii') as f:
#     for line in get_line(file_path):
#         aci = line.encode('unicode_escape').decode('ascii')
#         f.write(aci[:-2]+"\n")
        
import jieba
import re
import jieba.posseg as pseg

inpu = "李兰娟的重要成果有什么"
print(list(jieba.cut(inpu)))
pattern = "(.*的.*(是|有)(什么|谁|哪里))|(.*是什么.+)|(.*是哪里人)"
# pattern = "(.*的.*(是|有)(什么|谁|哪里))|(.*是什么.+)|(.*是哪里人)"

a = list(pseg.cut(inpu))
print(a)

print(re.search(pattern, inpu))