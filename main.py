import numpy as np
import networkx as nx
from simhash import *
import matplotlib.pyplot as plt
from sklearn import manifold

'''
g = nx.read_edgelist("./graphs/karate.txt", comments='#', delimiter=' ', nodetype=int, create_using=nx.Graph())

# Relabel nodes
mapping = {node: str(nodeId) for nodeId, node in enumerate(g.nodes())}
g = nx.relabel_nodes(G=g, mapping=mapping)
'''

graph_name = "citeseer_undirected"
dim = 128
suffix="_{}".format(dim)
g = nx.read_gml("../datasets/{}.gml".format(graph_name))
print("# cc: ", nx.number_connected_components(g))

'''
pos = nx.spring_layout(g)
nx.draw(g, pos, with_labels=True)
plt.show()
'''


degree_seq = [nx.degree(g, str(node)) for node in range(g.number_of_nodes())]





# Compute the signatures
sigdict = {}
for node in g.nodes():

    nb_list = [str(nb) for nb in nx.neighbors(g, node)]
    nb_list.append(str(node))  # add the node itself
    sigdict[int(node)] = SimHash(nb_list, dim=dim)
    print(type(sigdict[int(node)].input))

def save_embeddings(output_filename, dim, embed_dict):
    N = len(embed_dict.keys())
    print(N)
    with open(output_filename, 'w') as f:
        f.write("{} {}\n".format(N, dim))
        for node in range(N):
            line = "{} {}\n".format(node, embed_dict[node].input)
            f.write(line)


save_embeddings("./embeddings/{}{}.embedding".format(graph_name, suffix), dim, sigdict)

'''
nndist = np.empty((g.number_of_nodes(), g.number_of_nodes()), dtype=float)
for node1 in range(g.number_of_nodes()):
    for node2 in range(node1, g.number_of_nodes()):
        nndist[node1, node2] = sigdict[node1].hamming_distance(sigdict[node2])
        nndist[node2, node1] = nndist[node1, node2]
        #nndist[node1-1,node2-1] = nndist[node2-1,node1-1] = 1.0 - jaccard_similarity(neigh[node1],neigh[node2])
        #print hammingDistance(sigdict[node1].value,sigdict[node2].value)


seed = np.random.RandomState(seed=42)

mds = manifold.MDS(n_components=2, max_iter=100, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)

mds_coords = mds.fit(nndist).embedding_

colors = ['magenta', 'lightgreen','yellow','lightblue','pink','blue','red','purple','green','gray']

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for i in range(g.number_of_nodes()):
    #ax.scatter(M[i,0],M[i,1], color=colors[i])
    x = mds_coords[i, 0]
    y = mds_coords[i, 1]
    #com = clustering_dict[i+1]
    ax.scatter(x, y, s=200)#, c=colors[com])
    plt.text(x*(1+0.01), y*(1+0.01), i, fontsize=14)
ax.scatter(0, 0, color='black')
plt.xlabel('dim 1')
plt.ylabel('dim 2')
plt.show()
'''
