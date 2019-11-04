import networkx as nx
import numpy as np
import os
import sys

def compute_jaccard(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    return float(len(set1.intersection(set2))) / float(len( set1.union(set2) ))

def compute_cosine(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    return float(len(set1.intersection(set2))) / np.sqrt(float(len(set1))*float(len(set2)))


dataset_name = "citeseer_undirected"
dataset_path = os.path.join("../datasets/", dataset_name + ".gml")

g = nx.read_gml(dataset_path)
num_of_nodes = nx.number_of_nodes(g)

percentage = 0.1

node2comm = nx.get_node_attributes(g, name='community')


unlabeled_nodes = np.random.choice(a=[str(v) for v in range(num_of_nodes)], size=int(num_of_nodes*percentage) )
labeled_nodes = [str(node) for node in range(num_of_nodes) if node not in unlabeled_nodes]


counter = 0
tcounter = 0
for node in unlabeled_nodes:

    '''
    nb_list= []
    for nb in nx.neighbors(g, node):
        if nb not in nb_list:
            if nb not in unlabeled_nodes:
                nb_list.append(nb)
            for nb_nb in nx.neighbors(g, nb):
                if nb_nb not in unlabeled_nodes:
                    nb_list.append(nb_nb)
    '''
    nb_list= [nb for nb in nx.neighbors(g, node)]

    list1 = [nb for nb in nx.neighbors(g, node)]
    list1.append(node)

    jc_list=[]
    for nb in nb_list:
        list2 = [nbt for nbt in nx.neighbors(g, nb)]
        list2.append(nb)
        jc_list.append((nb, compute_cosine(list1, list2)))

    sorted_jc = sorted(jc_list, key=lambda x: x[1])
    selected = None
    i = 0
    while i < len(sorted_jc) and selected is None:
        temp = sorted_jc[i][0]
        if temp != node:
            selected = temp
        i += 1
    if selected is not None:
        tcounter += 1
        if node2comm[node] == node2comm[selected]:
            counter += 1

print(float(counter)/tcounter)
print(tcounter, len(unlabeled_nodes))
