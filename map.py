import re
from rdflib import Graph, Literal
from rdflib.namespace import RDFS, RDF, Namespace
import json


RDF_LIST = ['character', 'conception', 'epidemiology', 'event', 'health', 'medical',
            'prevention', 'research', 'resource', 'wiki']
# RDF_LIST = ['character']

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
goods_s = Namespace("http://www.openkg.cn/COVID-19/goods#")
wiki = Namespace("http://www.openkg.cn/COVID-19/wiki/")

merge = Namespace("http://www.openkg.cn/COVID-19/merge/")
merge_s = Namespace("https://www.openkg.cn/COVID-19/merge#")
code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

resource_counter = 1
class_counter = 1
property_counter = 1



def has_prefix(namespace, uri):
    if str(uri).find(str(namespace)) != -1:
        return True
    else: return False

def has_normal_prefix(uri):
    from rdflib.namespace import RDFS, RDF, OWL, XSD
    nslist = [RDFS, RDF, OWL, XSD, 'http://cnschema.org/', 'http://www.plantdata.ai/ontology/','http://edukb.org/knowledge/0.1/instance/biology/',
              'http://www.platdata.ai/rdf-schema#']
    for ns in nslist:
        if has_prefix(str(ns)[:-1], uri):
            return True
    else: return False


def get_id(subject, pattern='/'):
    return str(subject).split(pattern)[-1]

def trans_to_uri(namespace:Namespace, suffix:str, id_:str, index:int, pattern='/', usepad = False):
    if usepad:
        return str(Namespace(namespace[suffix]+pattern)[id_[0].upper() + code[i] + '0' + id_[1:]])
    else:
        return str(Namespace(namespace[suffix]+pattern)[id_[0].upper() + code[i]+ id_[1:]])


def trans(uri, file, mdict, i):
    
    if len(uri) == 0 or has_normal_prefix(uri) or (str(uri).find('http')==-1 and re.search('p[0-9]+:[0-9]', str(uri)) is None):
        return
    if file == 'character':
        if str(uri) in mdict.keys():
                return
        if str(uri).find(str(cara.resource)) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'resource',id_, i)
            mdict[str(uri)] = trans_uri
        elif str(uri).find(str(cara.property)) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'property',id_, i)
            mdict[str(uri)] = trans_uri
        elif str(uri).find(cara['class']) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'class', id_, i)
            mdict[str(uri)] = trans_uri
        elif re.search('p[1-9]:[0-9]', str(uri)) is not None:
            print(uri)
            id_ = str(uri).replace(':','')
            trans_uri = trans_to_uri(merge, 'property',id_, i, usepad=True)
            mdict[str(uri)] = trans_uri
        else:
            print(uri)
            
    elif file == 'conception':
        if str(uri) in mdict.keys():
            return
        if str(uri).find(str(conp['class'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['class']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        else:
            print(uri)
            
    elif file == 'epidemiology':
        if str(uri) in mdict.keys():
            return
        if str(uri).find(str(epid['class'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['class']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        elif str(uri).find(str(epid['property'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['property']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        else:
            print(uri)
            
    elif file == 'event':
        if str(uri) in mdict.keys():
            return
        if str(uri).find(str(event['property'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(str(merge['property']+'/')+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        elif str(uri).find(str(event['class'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['class']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        else:
            print(uri)

    elif file == 'health':
        if str(uri) in mdict.keys():
            return
        if str(uri).find(str(health['property'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['property']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        elif str(uri).find(str(health['class'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['class']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        elif str(uri).find(str(health['resource'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['resource']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        elif str(uri).find('http://www.openkg.cn/2019-nCoV/medical/resource/') != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['resource']+'/')[id_])
            mdict[str(uri)] = trans_uri
        elif str(uri).find('http://www.openkg.cn/2019-nCoV/ontology/alias') != -1:
            trans_uri = str(Namespace(merge['ontology']+'/')['alias'])
            mdict[str(uri)] = trans_uri
        else:
            print(uri)
                
    elif file == 'medical':
        if str(uri) in mdict.keys():
            return
        if str(uri).find(str(medical['property'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['property']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        elif str(uri).find(str(medical['class'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['class']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        elif str(uri).find(str(medical['resource'])) != -1:
            id_ = get_id(uri)
            trans_uri = str(Namespace(merge['class']+'/')[id_[0] + code[i] + id_[1:]])
            mdict[str(uri)] = trans_uri
        elif re.search('p[0-9]+:[0-9]', str(uri)) is not None:
            id_ = str(uri).replace(':','')
            trans_uri = str(Namespace(merge['property']+'/')[id_[0].upper() + code[i] + '0' + id_[1:]])
            mdict[str(uri)] = trans_uri
        else:
            print(uri)
                
    elif file == 'prevention':
            if str(uri) in mdict.keys():
                return
            if str(uri).find(str(prevention_s)) != -1:
                id_ = get_id(uri, pattern='#')
                trans_uri = str(Namespace(merge_s[id_]))
                mdict[str(uri)] = trans_uri
            elif str(uri).find(str(prevention['resource'])) != -1:
                id_ = get_id(uri)
                trans_uri = str(Namespace(merge['resource']+'/')[id_[0] + code[i] + id_[1:]])
                mdict[str(uri)] = trans_uri
            elif str(uri).find(str(prevention['class'])) != -1:
                id_ = get_id(uri)
                trans_uri = str(Namespace(merge['class']+'/')[id_[0] + code[i] + id_[1:]])
                mdict[str(uri)] = trans_uri
            elif str(uri).find(str(prevention['property']+'/')) != -1:
                id_ = get_id(uri)
                trans_uri = trans_to_uri(merge, 'property', id_, i)
                mdict[str(uri)] = trans_uri
            else:
                print(uri)
                
    elif file == 'research':
        if str(uri) in mdict.keys():
            return
        if str(uri).find(str(research['property'])) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'property' ,id_, i)
            mdict[str(uri)] = trans_uri
        elif str(uri).find(str(research['class'])) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'class', id_, i)
            mdict[str(uri)] = trans_uri
        else:
            print(uri)
        
    elif file=='resource':
        if str(uri) in mdict.keys():
            return
        if str(uri).find(goods['property']) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'property', id_, i)
            mdict[str(uri)] = trans_uri
        elif str(uri).find(goods['class']) != -1:
            id_ =get_id(uri)
            trans_uri = trans_to_uri(merge, 'class', id_, i)
            mdict[str(uri)] = trans_uri
        elif str(uri).find(goods['resource']) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'resource', id_, i)
            mdict[str(uri)] = trans_uri
        # elif str(uri).find(goods_s) != -1:
        #     id_ = get_id(uri, pattern='#')
        #     trans_uri = str(merge_s[id])
        #     mdict[str(uri)] = trans_uri
        else:
            print(uri)
                
    elif file=='wiki':
        if str(uri) in mdict.keys():
            return
        if (str(uri)).find(wiki['resource']) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'resource', id_, i)
            mdict[str(uri)] = trans_uri
        elif str(uri).find(wiki['property']) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'property', id_, i)
            mdict[str(uri)] = trans_uri
        elif str(uri).find(wiki['class']) != -1:
            id_ = get_id(uri)
            trans_uri = trans_to_uri(merge, 'class', id_, i)
            mdict[str(uri)] = trans_uri
        else:
            print(uri)
    
map_dict = {}
for i, file in enumerate(RDF_LIST):
    route = f"D:/Datasets/KG/{file}/{file}.nt"
    g = Graph()
    print(f"importing file {route}")
    g.parse(route)
    
    file_map = {}
    for triple in g:
        for uris in triple:
            for uri in uris.split(','):
                trans(uri, file, file_map, i)
                
    g.remove((None, None, None))
    print(f"{file}.nt map finished")
    map_dict[file] = file_map
        


with open("D:/Datasets/KG/merge_map.json", 'w') as f:
    json.dump(map_dict, f, indent=4, ensure_ascii=False)