import json
import re
from copy import deepcopy
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDFS, RDF, Namespace, OWL, XSD

cara = Namespace("http://www.openkg.cn/COVID-19/character/")
conp = Namespace("http://www.openkg.cn/COVID-19/conception/")
epid = Namespace("http://www.openkg.cn/COVID-19/epidemiology/")
event = Namespace("http://www.openkg.cn/COVID-19/event/")
health = Namespace("http://www.openkg.cn/2019-nCoV/health/")
medical = Namespace("http://www.openkg.cn/COVID-19/medical/")
prevention = Namespace("http://www.openkg.cn/COVID-19/prevention/")
prevention_s = Namespace("http://www.openkg.cn/COVID-19/prevention#")
research = Namespace("http://www.openkg.cn/COVID-19/research/")
goods = Namespace("http://www.openkg.cn/COVID-19/goods/")
wiki = Namespace("http://www.openkg.cn/COVID-19/wiki/")

ns_list = [cara, conp, epid, event, health, medical, prevention, research, goods, wiki]

# RDF_LIST = ['character', 'conception', 'epidemiology', 'event', 'health', 'medical',
#             'prevention', 'research', 'resource', 'wiki']

RDF_LIST = ['prevention']

with open("D:/Datasets/KG/merge_map.json") as f:
    map_dict = json.load(f)

def has_prefix(namespace, uri):
    if str(uri).find(str(namespace)[:-1]) != -1:
        return True
    else: return False

def has_normal_prefix(uri):
    from rdflib.namespace import RDFS, RDF, OWL, XSD
    nslist = [RDFS, RDF, OWL, XSD, 'http://cnschema.org/', 'http://www.plantdata.ai/ontology/', 'http://www.platdata.ai/rdf-schema#']
    for ns in nslist:
        if has_prefix(str(ns)[:-1], uri):
            return True
    else: return False

def locate(uri):
    for ns in ns_list:
        if has_prefix(ns, uri):
            return str(ns)[:-1].split('/')[-1]
    return None


def trans(triple, map_dict, file):
    subjects, predicated, objects = triple
    subjectl = [URIRef(subject) for subject in subjects.split(',')]
    if isinstance(objects, URIRef):
        objectl = [URIRef(object) for object in objects.split(',')]
    else:
        objectl = [objects]
    for subject in subjectl:
        if str(subject).find('http:') == -1:
            continue
        for object in objectl:
            unknow = {}
            if str(subject) in map_dict[file].keys():
                n_subject = URIRef(map_dict[file][str(subject)])
            elif has_normal_prefix(subject):
                n_subject = subject
            else:
                unknow['subject'] = str(subject)
                n_subject = subject
            
            if str(predicated) in map_dict[file].keys():
                n_predicated = URIRef(map_dict[file][str(predicated)])
            elif has_normal_prefix(predicated):
                n_predicated = predicated
            else:
                n_predicated = predicated
                unknow['predicated'] = str(predicated)
            
            
            if isinstance(object, URIRef):
                if str(object) in map_dict[file].keys():
                    n_object = URIRef(map_dict[file][str(object)])
                elif has_normal_prefix(object):
                    n_object = object
                else:
                    unknow['object'] = str(object)
                    n_object = object
            else:
                n_object = object
                    
            yield (n_subject, n_predicated, n_object), unknow


for i, file in enumerate(RDF_LIST):
    route = f"D:/Datasets/KG/{file}/{file}.nt"
    print(f"importing file {route}")
    g = Graph()
    g.parse(route)
    for triple in g:
        for ntriple, unknow in trans(triple, map_dict, file):
            unknow_ = deepcopy(unknow)
            for key,val in unknow.items():
                link_file = locate(val)
                if link_file is not None:
                    if link_file == 'goods':
                        link_file = 'resource'
                    subject, predicated, object = ntriple
                    if key == 'subject':
                        ntriple = (URIRef(map_dict[link_file][val]), predicated, object)
                        unknow_.pop(key)
                    elif key == 'predicated':
                        ntriple = (subject, URIRef(map_dict[link_file][val]), object)
                        unknow_.pop(key)
                    elif key == 'object':
                        ntriple = (subject, predicated, URIRef(map_dict[link_file][val]))
                        unknow_.pop(key)
            if len(unknow_) !=0:
                
                print(unknow_)
            g.add(ntriple)
        g.remove(triple)
    g.serialize(destination=f'D:/Datasets/KG/{file}/{file}_reform.nt',format='nt')