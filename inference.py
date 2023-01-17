import os
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDFS, RDF, Namespace, OWL, XSD
import re
import json
import synonyms as syn
from pprint import pprint
from copy import deepcopy
from bidict import bidict
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

SBJ, PDC, OBJ = 'subject', 'predicated', 'object'

PROPERTY_CODE = {
    'PA1':'籍贯',
'PA2':'性别',
'PA3':'死亡时间',
'PA4':'出生日期',
'PA5':'民族',
'PA6':'国籍',
'PA7':'研究方向',
'PA8':'毕业院校',
'PA9':'参与战役',
'PA10':'参与事件',
'PA11':'发表',
'PA12':'事迹',
'PA13':'职责',
'PA14':'死亡原因',
'PA15':'出生地',
'PA16':'履历',
'PA18':'重要成果',
'PA19':'相关疾病',
'PA20':'导致',
'PA21':'顺承',
'PA22':'因果',
'PA23':'爆发地点',
'PA24':'所在城市',
'PA25':'颁布',
'PA26':'出版',
'PA28':'奖项名次',
'PA29':'获奖原因',
'PA30':'发表日期',
'PA31':'结论',
'PA32':'发表_',
'PA33':'第一作者',
'PA34':'共同作者',
'PA35':'发生地点',
'PA36':'职务',
'PA37':'任职机构',
'PA38':'学校所在城市',
'PA39':'获奖事件',
'PA40':'相关奖项',
'PA41':'出版日期',
'PA42':'同事',
'PA43':'合作',
'PA44':'队友',
'PA45':'支援地点',
'PA46':'所属救援队',
'PA48':'现任机构',
'PA49':'出发日期',


}

BIPROPERTY_CODE = bidict(PROPERTY_CODE)

templates = ['.*和.*的关系是什么',
             '.*的.*是什么',
             '.*的.*有什么',
            '.*是什么',
            '.*有什么',
            '.*是谁',
            '.*有什么.*',
            '什么有.*的特点',
            ]


g = Graph()

for file in RDF_LIST:
    print(f"importing {file}")
    g.parse(f"D:/Datasets/KG/{file}/{file}_reform.nt")

g.parse("D:/Datasets/KG/sameAs.nt")

with open('D:/Datasets/KG/labels.json','r', encoding='utf8') as f:
    label_dt = json.load(f)

def has_prefix(uri, prefix):
    if str(uri).find(str(prefix)) != -1:
        return True
    else:
        return False

def is_property(uri):
    if str(uri).find('property') != -1:
        return True
    else: return False

def is_resource(uri):
    if str(uri).find('resource') != -1:
        return True
    else: return False

def is_label(uri):
    if str(uri).find(str(RDFS.label)) != -1:
      return True
    else: return False  
    
def is_rdf(uri):
    if is_property(uri) or is_resource(uri) or is_property(uri) or is_label(uri):
        return False
    else: return True

def get_nearest_uri(words):
    if words in label_dt.values():
        uris = [key for key, val in label_dt.items() if val == words]
        uri = uris[0]
        return uri
    nearw, _ = syn.nearby(words)
    uri = None
    if len(nearw) != 0:
        for w in nearw:
            if w in label_dt.values():
                uris = [key for key, val in label_dt.items() if val == w]
                uri = uris[0]
                break
            
    if uri is None: 
        nearest_w = None
        nearest_a = 0
        
        for key in label_dt.values():
            print(f'compare {sbj},{key}')
            acc = syn.compare(sbj, key, False)
            if acc > nearest_a:
                nearest_a = acc
                nearest_w = key
            if acc > 0.9:
                break
            
        uris = [key for key, val in label_dt.items() if val == nearest_w]
        print(uri)
    return uri

def get_label(uri):
    global g
    if isinstance(uri, Literal):
        return  str(uri)
    elif isinstance(uri, URIRef):
        if is_property(uri) or is_resource(uri):
            label = list(g.objects(uri, RDFS.label))
            if len(label) == 0:
                code = str(uri).split('/')[-1]
                if code in PROPERTY_CODE.keys():
                    return PROPERTY_CODE[code]
                else:
                    return  code
            else:
                return  str(label[0])
        else:
            return  "unknow"
            
    


def search(g:Graph, q, info):

    if len(q) == 1:
        
        if q[0] == PDC:
            sbj, obj = info
            sbj_uri, obj_uri = URIRef(get_nearest_uri(sbj)), URIRef(get_nearest_uri(obj))
            
            return [(predicated) for predicated in g.predicates(subject=sbj_uri, object=obj_uri)]
        elif q[0] == SBJ:
            pdc, obj = info
            pdc_uri, obj_uri = URIRef(get_nearest_uri(pdc)), URIRef(get_nearest_uri(obj))
            
            return [(sbj) for sbj in g.predicate_objects(pdc_uri, obj_uri)]
        elif q[0] == OBJ:
            sbj, pdc = info
            sbj_uri = URIRef(get_nearest_uri(sbj))
            if pdc in PROPERTY_CODE.values():
                code = BIPROPERTY_CODE.inverse[pdc]
                pdc_uri = URIRef(f"http://www.openkg.cn/COVID-19/merge/property/{code}")
            elif pdc in label_dt.values():
                pdc_uri  = [key for key, val in label_dt.items() if val == pdc][0]
            objs = []
            for obj in g.objects(subject=sbj_uri, predicate=pdc_uri):
                label = get_label(obj)
                objs.append(label)
            return objs
            
    else:
        
        if q[0] == PDC and q[1] == OBJ:
            sbj = info[0]
            sbj_uri = URIRef(get_nearest_uri(sbj))
            pairs = {}
            for pdc, obj in g.predicate_objects(subject=sbj_uri):
                if is_rdf(pdc) or is_label(pdc):
                    continue
                
                pdc_data = get_label(pdc)
                
                obj_data = get_label(obj)
                if pdc_data in pairs.keys():
                    pairs[pdc_data].append(obj_data)
                else:
                    pairs[pdc_data] = [obj_data]
            rpairs = deepcopy(pairs)
            for key, val in pairs.items():
                if len(val) == 1:
                    rpairs[key] = val[0]
            return rpairs
            # return [(get_label(pdc), get_label(obj)) for pdc, obj in g.predicate_objects(subject=sbj_uri)]
            # return [(pdc, obj) for pdc, obj in g.predicate_objects(subject=sbj_uri)]

# flag = True
# while flag:
#     question = input("请输入你的问题(q to quit)：")
#     if question == 'q':
#         flag = False
#         break
#     for i, template in enumerate(templates):
#         match =  re.search(template, question)
#         if match is None:
#             continue
#         elif template == '.*和.*的关系是什么':
#             print(f"matching pattern {template}")
#             sbj, obj = question.split('的')[0].split('和')
#             q = [PDC]
#             r = search(g, q, [sbj, obj])
#             print(r)
#             break
#         elif template == '.*的.*是什么' or template == '.*的.*有什么':
#             print(f"matching pattern {template}")
#             sbj, pdc = question.split('是什么')[0].split('的')
#             q = [OBJ]
#             r = search(g,q,[sbj, pdc])
#             print(r)
#             break
#         elif template == '.*是什么' or template == '.*有什么' or template== '.*是谁':
#             print(f"matching pattern {template}")
#             if template == '.*是什么' or template == '.*有什么':
#                 sbj = question.split('什么')[0][:-1]
#             elif template == '.*是谁':
#                 sbj = question.split('是谁')[0]
#             q = (PDC,OBJ)
#             r = search(g, q,[sbj])
#             pprint(r)
#             break
#         else:
#             print("can't matching any template")


tmps = [  "(.*的.*(是|有)(什么|谁|哪里))|(.*是什么.+)|(.*是哪里人)",'.+(是|有)(谁|什么)']
noun = ['n', 'ns', 'nr', 'nt', 'nw', 'nz', 'PER', 'LOC', 'ORG']

import jieba.posseg as pseg   
flag = True
while flag:
    question = input("请输入你的问题(q to quit)：")
    if question == 'q':
        flag = False
        break
    for i, tmp in enumerate(tmps):
        match =  re.search(tmp, question)
        if match is None:
            continue
        elif tmp == "(.*的.*(是|有)(什么|谁|哪里))|(.*是什么.+)|(.*是哪里人)":
            print(f"matching pattern {tmp}")
            sbj,pdc = '',  ''
            j = 0
            for i ,(word, fg) in enumerate(pseg.cut(question)):
                if fg in noun:
                    if sbj == '' or (pdc == '' and i==j+1):
                        sbj +=word
                        j = i 
                    elif pdc == '' or (i==j+1):
                        pdc += word
                        j = i
            if sbj is None and pdc is None:
                print("There hasn't two noun")
                continue
            
            q = [OBJ]
            r = search(g,q,[sbj, pdc])
            print(r)
            break
        elif tmp == '.+(是|有)(谁|什么)':
            print(f"matching pattern {tmp}")
            sbj = ''
            for  word, fg in pseg.cut(question):
                if fg in noun:
                    sbj+=word
                elif sbj != '':
                    break
            print(sbj)
            q = (PDC,OBJ)
            r = search(g, q,[sbj])
            pprint(r)
            break
        
            
            
            
        elif template == '.*是什么' or template == '.*有什么' or template== '.*是谁':
            print(f"matching pattern {template}")
            if template == '.*是什么' or template == '.*有什么':
                sbj = question.split('什么')[0][:-1]
            elif template == '.*是谁':
                sbj = question.split('是谁')[0]
            q = (PDC,OBJ)
            r = search(g, q,[sbj])
            pprint(r)
            break
    

# for triple in g:
#     print(triple)
#     break

# if __name__ == '__main__':
#     mdict = {}
#     for sbj, obj in g.subject_objects(predicate=URIRef("http://www.w3.org/2000/01/rdf-schema#label")):
#         mdict[str(sbj)] = str(obj)
    
#     with open('D:/Datasets/KG/labels.json','w', encoding='utf8') as f:
#         json.dump(mdict, f, indent=4, ensure_ascii=False)
