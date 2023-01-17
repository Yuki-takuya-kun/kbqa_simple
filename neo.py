import py2neo as pn

graph = pn.Graph("http//localhost:7687", auth=('neo4j','neo4j'))
RDF_LIST = ['character', 'conception', 'epidemiology', 'event', 'health', 'medical',
            'prevention', 'research', 'resource', 'wiki']

def graph_init():
    graph.run('match (n) detach delete n')
    graph.run('call n10s.graphconfig.init()')
    graph.run('call n10s.nsprefixes.add("class","http://www.openkg.cn/COVID-19/merge/class/")')
    graph.run('call n10s.nsprefixes.add("property","http://www.openkg.cn/COVID-19/merge/property/")')
    graph.run('call n10s.nsprefixes.add("resource","http://www.openkg.cn/COVID-19/merge/resource/")')
    graph.run('call n10s.nsprefixes.add("ontology","http://www.openkg.cn/COVID-19/merge/ontology/")')
    graph.run('call n10s.nsprefixes.add("platdata","http://www.platdata.ai/rdf-schema#")')
    for file in RDF_LIST:
        route = f"file:///D:/Datasets/KG/{file}/{file}_reform.nt"
        graph.run(f'call n10s.rdf.import.fetch("{route}","N-Triples")')
    
if __name__ == '__main__':
    graph_init()
    graph.close()
    