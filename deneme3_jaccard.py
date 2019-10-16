import networkx as nx
import numpy as np
from minhash import *
from random_walks import *
from zlib import crc32
import matplotlib.pyplot as plt


def my_hash_function(value):
    if isinstance(value, str):
        return float(crc32(value.encode("utf-8")) & 0xffffffff) / 2 ** 32
    else:
        return float(crc32(value) & 0xffffffff) / 2 ** 32

def my_crc32_function(x):
    return crc32(x) & 0xffffffff


def save_embeddings(file_path, emb):
    with open(file_path, 'w') as f:
        f.write("{} {}\n".format(len(emb.values()), len(emb[str(0)])))
        for v in emb.keys():
            f.write("{} {}\n".format(str(v), " ".join(str(e) for e in emb[str(v)])))


def get_nb_list(g):

    nb_list = [[] for _ in range(g.number_of_nodes())]
    for node in g.nodes():
        nb_list[int(node)].append(node)
        for nb in nx.neighbors(g, node):
            nb_list[int(node)].append(nb)

            #for nb_nb in nx.neighbors(g, nb):
            #    if nb_nb not in nb_list[int(node)]:
            #        nb_list[int(node)].append(nb_nb)
        nb_list[int(node)].append(node)

    return nb_list

g = nx.read_gml("../datasets/citeseer_undirected.gml")
dim = 256
#rw = RandomWalks(g=g, method="deepwalk", N=1, L=11, opts={})
mh = MinHash(hash_function=my_crc32_function)

#walks = rw.get_walks()
walks = get_nb_list(g)

embeddings = {str(node): [] for node in range(g.number_of_nodes())}
for d in range(dim):
    mh.renew_hash_function()
    for walk in walks:
        embeddings[walk[0]].append(mh.getMinHashCodeOf(values=walk[1:]))

'''
plt.figure()
plt.plot([embeddings[str(node)][0] for node in range(g.number_of_nodes())],
         [embeddings[str(node)][1] for node in range(g.number_of_nodes())], '.')
plt.show()
'''

save_embeddings(file_path="./citeseer_undirected_minhash_1ego_{}.embedding".format(dim), emb=embeddings)
