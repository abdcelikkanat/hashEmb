import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def my_metric(g, included):

    current_g = nx.subgraph(g, included)
    current_r = current_g.number_of_edges() / float( np.sum(nx.degree(g, node) for node in included) - 2*current_g.number_of_edges() )

    return current_r


edges1 = [[0,1], [1,2], [2,3], [3,0], [0,4], [4,5], [5,6], [6,0]]
edges2 = [[0,1], [1,2], [2,3], [3,0], [0,7], [7,4], [4,5], [5,6], [6,7]]


edges = edges1

g = nx.Graph()
g.add_edges_from(edges)




# Algorithm
initial = 2
included = [initial]
current_r = my_metric(g, included=included)
candidates = [nb for nb in nx.neighbors(g, initial)]
cont = True

while cont:
    if len(included) + 1 == g.number_of_nodes():
        included = [node for node in g.nodes()]
        break

    max_r = -1.0
    max_node = None
    for nb in candidates:
        nb_r = my_metric(g, included=included+[nb])

        if nb_r > max_r:
            max_r = nb_r
            max_node = nb

    if max_r > current_r:
        included.append(max_node)
        current_r = max_r
        candidates.remove(max_node)
        for nb in nx.neighbors(g, max_node):
            if nb not in candidates:
                candidates.append(nb)
        cont = True
    else:
        cont = False

print(included)

plt.figure()
pos = nx.spring_layout(g)
nx.draw_networkx_nodes(g, pos, nodelist=g.nodes, node_color='b',label={node: node for node in g.nodes()})
nx.draw_networkx_nodes(g, pos, nodelist=included, node_color='r', label={node: node for node in g.nodes()})
nx.draw_networkx_edges(g, pos, edgelist=g.edges)
plt.show()
