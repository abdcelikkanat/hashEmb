import networkx as nx

g = nx.read_gml("../datasets/blogcatalog.gml")


two = 0
three = 0
more = 0
count = 0
for node in g.nodes():
    pos = set()
    for nb in nx.neighbors(g, node):
        for nb_nb in nx.neighbors(g, nb):
            if nb_nb != node:
                pos.add(nb_nb)

    for nb in pos:
        nodel = len(list(nx.neighbors(g, node)))
        nbl = len(list(nx.neighbors(g, nb)))
        if nodel == len(list(nx.common_neighbors(g, node, nb))) and nodel == nbl:
            count += 1
            if nodel == 2:
                two += 1
            if nodel == 3:
                three += 1
            if nodel >= 4:
                more += 1
                # print("---------")
                # print(node, list(nx.neighbors(g, node)))
                # print(nb, list(nx.neighbors(g, nb)))

totalone = 0
totaltwo = 0
totalthree = 0
totalfour = 0
for node in g.nodes():
    if nx.degree(g, node) == 1:
        totalone += 1
    if nx.degree(g, node) == 2:
        totaltwo += 1
    if nx.degree(g, node) == 3:
        totalthree += 1
    if nx.degree(g, node) == 4:
        totalfour += 1


print(g.number_of_nodes())
print(count/2, two/2, three/2, more/2)
print(totalone, totaltwo, totalthree, totalfour)