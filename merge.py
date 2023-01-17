import json
import re
from copy import deepcopy
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDFS, RDF, Namespace, OWL, XSD
import os

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

RDF_LIST = ['character', 'conception', 'epidemiology', 'event', 'health', 'medical',
            'prevention', 'research', 'resource', 'wiki']




g = Graph()
# for file in RDF_LIST:
#     route = f"D:/Datasets/KG/{file}/{file}_reform.nt"
#     g.parse(route)
    
with open("D:/Datasets/KG/merge_map.json") as f:
    map_dict = json.load(f)

def transfer(file, uri, strict=False):
    global map_dict
    uri = uri[1:-1]
    
    if uri in map_dict[file].keys():
        return map_dict[file][uri]
    elif file=='conception' and uri.replace('wiki','conception') in map_dict[file].keys():
        uri = uri.replace('wiki', 'conception')
        return map_dict[file][uri]
    elif strict:
        print(uri)
        return False
    else:
        return uri

def generating_map_file():
    print("generating link file")
    matching_route = "D:/Datasets/KG/匹配"
    for dir in os.listdir(matching_route):
        if 'accepted_pair_ori.json' in os.listdir(f"{matching_route}/{dir}"):
            continue
        
        accepted_pair = {}
        trans_accepted_pair = {}
        with open(matching_route+f'/{dir}/belief_pkustatistics.json') as f:
            count_dict = json.load(f)
        if not count_dict['outputSizes']['verification'] and not count_dict['outputSizes']['acceptance']:
            continue
        resource_file, target_file = dir.split('_')
        print(f"The resource file is {resource_file}, the target file is {target_file}")
        if count_dict['outputSizes']['verification'] != 0:
            with open(f"{matching_route}/{dir}/lgd_relaybox_near.nt", 'r') as f:
                for line in f.readlines():
                    reso_uri, target_uri, score = line.replace('\n','').split('\t')
                    if reso_uri.split('/')[-2] != target_uri.split('/')[-2]:
                        break
                    nsource = transfer(resource_file, reso_uri)
                    ntarget = transfer(target_file, target_uri)
                    
                    print('-'*60)
                    print(f'resource:{reso_uri}\n target:{target_uri}\n Please check above uris is the same or not. The confidence is {score}')
                    chos = input("Accept? \n [Y]/N:")
                    if chos is None:
                        chos = 'Y'
                    else:
                        chos = chos.upper()
                    if chos == 'Y':
                        print("accept")
                        accepted_pair[reso_uri] = target_uri
                        trans_accepted_pair[nsource] = ntarget
                    else: continue
        
        if count_dict['outputSizes']['acceptance'] != 0:
            with open(f"{matching_route}/{dir}/lgd_relaybox_verynear.nt", 'r') as f:
                for line in f.readlines():
                    reso_uri, target_uri, _ = line.replace('\n', '').split('\t')
                    accepted_pair[reso_uri] = target_uri
                    nsource = transfer(resource_file, reso_uri, True)
                    ntarget = transfer(target_file, target_uri, True)
                    if bool(nsource) and bool(ntarget):
                        trans_accepted_pair[nsource] = ntarget
                    
        
        with open(f"{matching_route}/{dir}/accepted_pair_ori.json", 'w') as f:
            json.dump(accepted_pair, f, indent=4, ensure_ascii=False)
        
        with open(f"{matching_route}/{dir}/accepted_pair_trans.json", 'w') as f:
            json.dump(trans_accepted_pair, f, indent=4, ensure_ascii=False)
        
def mergering_property():
    matching_route = "D:/Datasets/KG/匹配"
    transfer_triple = []
    for dir in os.listdir(matching_route):
        
        print(dir)
        source_file, target_file = dir.split('_')
        with open(f"{matching_route}/{dir}/accepted_pair_ori.json",'r') as f:
            accepted_pair_dict_1 = json.load(f)
        
        accepted_pair_dict_2 = {}
        with open(f"{matching_route}/{dir}/lgd_relaybox_verynear.nt", 'r') as f:
            for line in f.readlines():
                source, target, _ = line.replace('\n','').split('\t')

                accepted_pair_dict_2[source] = target
        
        acp_dict = [accepted_pair_dict_1, accepted_pair_dict_2]
        for adict in acp_dict:
            for source, target in adict.items():
                nsource, ntarget = '<' + transfer(source_file, source, True)+'>', '<'+transfer(target_file, target, True)+'>'
                if bool(nsource) and bool(ntarget):
                    transfer_triple.append(' '.join([nsource,'<http://www.w3.org/2002/07/owl#sameAs>',ntarget,'.','\n']))
                elif not nsource:
                    print(f"{source} is not in {source_file}, {nsource}")
                else:
                    print(f"{target} is not in {target_file}, {ntarget}")
    
    with open(f"D:/Datasets/KG/sameAs.nt",'w') as f:
        f.writelines(transfer_triple)
        
def mergering_class():
    from xml.dom.minidom import parse
    import os
    triple = []
    for file in os.listdir("D:/Datasets/KG/matching/files_result"):
        print(file)
        dom = parse(f"D:/Datasets/KG/matching/files_result/{file}")
        data = dom.documentElement
        stus = data.getElementsByTagName('Cell')
        sourcef, targetf = file.split('.')[0].split('-')
        
        for stu in stus:
            source = '<'+stu.getElementsByTagName('entity1')[0].getAttribute('rdf:resource')+'>'
            target = '<'+stu.getElementsByTagName('entity2')[0].getAttribute('rdf:resource')+'>'
            if source == target:
                break
            print(source, target)
            if sourcef == '概念':
                source = source.replace('wiki','conception')
            elif targetf == '概念':
                target = target.replace('wiki','conception')
            
            sf, tf = source.split('/')[-3], target.split('/')[-3]
            if sf == 'goods': sf = 'resource'
            if tf == 'goods': tf = 'resource'
            sbj, obj = transfer(sf, source, True), transfer(tf, target, True)
            if sbj is True and obj is True: 
                sbj = '<'+sbj+'>'
                obj = '<'+obj+'>'
                triple.append(' '.join([sbj,'<http://www.w3.org/2002/07/owl#sameAs>',obj,'.','\n']))
     
      
    # with open(f"D:/Datasets/KG/sameAs.nt","a") as f:
    #     f.writelines(triple)
    
if __name__ == "__main__":
    mergering_property()
    mergering_class()

                
                
   
    
    
