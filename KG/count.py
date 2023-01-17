import os
import json
import numpy as np
import seaborn as sns
from rdflib import Graph, Literal, URIRef
import matplotlib.pyplot as plt
import pandas as pd
RDF_LIST = ['character', 'conception', 'epidemiology', 'event', 'health', 'medical',
            'prevention', 'resource', 'wiki']
# RDF_LIST = ['character']



def is_resource(uri):
    if str(uri).find("resource") != -1:
        return True
    else:
        return False

def is_class(uri):
    if str(uri).find("class") != -1 or str(uri).find("property"):
        return True
    else:
        return False

def get_id(subject, pattern='/'):
    return str(subject).split(pattern)[-1]

def count_triple():
    for file in RDF_LIST:
        resources = set()
        classes = set()
        route = f"D:/Datasets/KG/{file}/{file}.nt"
        g = Graph()
        g.parse(route)
        print(f"Counting file {file}")
        for sbj in g.subjects(predicate=None, object=None):
            sbj_id = get_id(sbj)
            if is_resource(sbj):
                resources.add(str(sbj))
            elif is_class(sbj):
                classes.add(str(sbj))
            else:
                print(sbj)
        print(f"The total trip in {file} is {len(g)}")
        print(f"The number of Class is {len(classes)}")
        print(f"The number of Resource is {len(resources)}")


def transfer_epi():
    g = Graph()
    gc = Graph()
    g.parse("D:/Datasets/KG/epidemiology/epidemiology.json")
    gc.parse("D:/Datasets/KG/epidemiology/epidemiology.json")
    print(len(gc))
    for triple in g:
        sbj, pdc, obj = triple
        if str(obj).find('file') != -1:
            # print(sbj, pdc, obj)
            obj = str(obj).replace("file:///D:/Datasets/KG/epidemiology/","")
            gc.remove(triple)
            if str(obj) == 'event.json':
                continue
            else:
                gc.add((sbj, pdc, Literal(obj)))
        if str(obj).find("一、各外汇分支机构要启动应急处置机制,对于有关部门和地方政府所需的疫情防控物资进口") != -1:
            obj = Literal(str(obj))
            gc.remove(triple)
            gc.add((sbj, pdc, Literal(obj)))
    # for triple in gc:
    #     sbj, pdc, obj = triple
    #     if str(obj).find('file') != -1:
    #         # print(sbj, pdc, obj)
    #         if str(obj).find("file:///D:/Datasets/KG/event/") != -1:
    #             print('find file')
    #             break

    gc.serialize(destination="D:/Datasets/KG/epidemiology/epidemiology.nt", format='nt')
    
def draw_cross():
    count_dict = {}
    for dir in os.listdir("D:/Datasets/KG/匹配/"):
        with open(f"D:/Datasets/KG/匹配/{dir}/{dir}statistics.json", 'r', encoding='utf8') as f:
            count = json.load(f)
        same = count["outputSizes"]["acceptance"]
        r = count["outputSizes"]['verification']
        count_dict[dir] = same
        print(f"{dir}: {same}, {r}, total:{same+r}")
    mat = np.zeros((len(RDF_LIST), len(RDF_LIST)), dtype=np.int16)
    for key, val in count_dict.items():
        source, target = key.split("_")
        mat[RDF_LIST.index(target)][RDF_LIST.index(source)] =  val
    mask = np.zeros_like(mat)
    for i in range(0, len(mask)):
        for j in range(i, len(mask)):
            mask[j][0] = True
    
    # data = pd.DataFrame(mat, columns=RDF_LIST, index=reversed(RDF_LIST), dtype=int)
    # f,ax = plt.subplots()
    # print(data)
    # sns.heatmap(data, annot=True, ax=ax, mask=mask)
    # plt.matshow(mat,cmap=plt.cm.Blues)
    # plt.show()


if __name__=='__main__':
    draw_cross()
        

    
            
        
