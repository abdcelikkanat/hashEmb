import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from random_walks import *
from gensim.models import Word2Vec


def compute_score(g, included_list):
    sub_g = nx.subgraph(g, included_list)
    in_edge_count = float(sub_g.number_of_edges())
    out_edge_count = float(np.sum(nx.degree(g, node) for node in included_list)
                           - 2 * sub_g.number_of_edges() )

    try:
        return in_edge_count / out_edge_count
    except ZeroDivisionError:
        return np.inf
        #raise ZeroDivisionError


def assign_label(g, node_labels, node, new_label):
    included_list = [node]
    candidate_list = [nb for nb in nx.neighbors(g, node)]
    current_score = compute_score(g, included_list=included_list)
    cont = True

    while cont:

        # Check scores of all the candidate nodes
        max_score = -1.0
        max_node = None

        for candidate in candidate_list:

            candidate_score = compute_score(g, included_list=included_list + [candidate])

            if candidate_score > max_score:
                max_score = candidate_score
                max_node = candidate


        # If the score of one of the candidates is greater than the current score
        if max_score > current_score:
            included_list.append(max_node)
            current_score = max_score
            candidate_list.remove(max_node)
            for new_candidate in nx.neighbors(g, max_node):
                if new_candidate not in candidate_list:
                    candidate_list.append(new_candidate)
            cont = True
        else:
            cont = False

    # Label each node
    for inc_node in included_list:
        node_labels[int(inc_node)].append(new_label)


def partition(g):

    N = g.number_of_nodes()
    node_list = list(g.nodes())
    np.random.shuffle(node_list)
    node_labels = [[] for _ in range(N)]

    new_label = 0
    for node in node_list:
        if len(node_labels[int(node)]) == 0:

            assign_label(g, node_labels, node, new_label=new_label)
            new_label += 1

    return node_list, node_labels


def plot_graph(g, node_list, node_labels):

    num_of_labels = max(max(m) for m in node_labels) + 1
    node_lists = [[] for _ in range(num_of_labels)]
    for node in node_list:
        for c in node_labels[int(node)]:
            node_lists[c].append(node)
    color_list = ['r', 'b', 'g', 'y', 'm', 'w', 'k', 'c']

    plt.figure()
    pos = nx.spring_layout(g)
    for c in range(num_of_labels):
        nx.draw_networkx_nodes(g, pos, nodelist=node_lists[c], node_color=color_list[c])
    nx.draw_networkx_edges(g, pos, edgelist=g.edges)
    plt.show()


def binary(node_list, node_labels):
    N = len(node_list)
    num_of_labels = max(max(m) for m in node_labels) + 1

    embeddings = np.zeros(shape=(N, num_of_labels), dtype=np.int)
    for node in node_list:
        embeddings[node_labels[int(node)]] = 1

    return embeddings


def logistic_regression(node_list, node_labels, dim=128):
    N = len(node_list)
    num_of_labels = max(max(m) for m in node_labels) + 1

    centers = 10.0*np.random.random(size=(num_of_labels, dim)) - 5.0

    node_lists = [[] for _ in range(num_of_labels)]
    for node in node_list:
        node_lists[node_labels[int(node)]].append(node)

    embeddings = np.zeros(shape=(N, dim), dtype=np.float)
    for c in range(num_of_labels):
        for node in node_lists[c]:
            #embeddings[int(node), :] = np.random.normal(size=(1, dim), loc=centers[c, :])
            embeddings[int(node), :] = centers[c, :]

    return embeddings

def learn_by_walks(g, node_list, node_labels, walk_len, walk_num, dim, output_path):

    num_of_labels = max(max(m) for m in node_labels) + 1

    node_lists = [[] for _ in range(num_of_labels)]
    for node in node_list:
        node_lists[node_labels[int(node)]].append(node)

    walks = []
    for c in range(num_of_labels):
        subg = nx.subgraph(g, node_lists[c])

        for n in range(walk_num):
            np.random.shuffle(node_lists[c])

            for node in node_lists[c]:
                walk = [node]

                while len(walk) < walk_len:
                    nb_list = list(nx.neighbors(subg, walk[-1]))
                    if len(nb_list) > 0:
                        nb = np.random.choice(a=nb_list, size=1)[0]
                    else:
                        nb = walk[-1]
                    walk.append(nb)

                walks.append(walk)

    model = Word2Vec(walks, size=dim, min_count=0, sg=1, hs=0, negative=5, window=20,
                     workers=1)
    model.wv.save_word2vec_format(output_path)

def write_embeddings(embeddings, output_path):
    N, dim = embeddings.shape

    with open(output_path, 'w') as f:
        f.write("{} {}\n".format(N, dim))
        for node in node_list:
            f.write("{} {}\n".format(node, ' '.join(str(v) for v in embeddings[int(node), :])))




g = nx.read_gml("../datasets/cora_undirected.gml")
#####
g = max(nx.connected_component_subgraphs(g), key=len)
g = nx.relabel_nodes(G=g, mapping={node:str(nodeId) for nodeId, node in enumerate(g.nodes())})
g.remove_edges_from(g.selfloop_edges())
####
g = nx.Graph()
g.add_edges_from([[0,1], [1,2], [1,3], [1,4], [1,5], [2,3], [2,4], [2,5], [3,4], [3,5], [4,5], [0,6]])
####
node_list, node_labels = partition(g)
print(node_labels)
num_of_labels = max(max(m) for m in node_labels) + 1
print("Num of nodes: {}".format(g.number_of_nodes()))
print("Num of labels: {}".format(num_of_labels))
# embeddings = logistic_regression(node_list, node_labels, dim=num_of_labels)
# write_embeddings(embeddings=embeddings,
#                  output_path="myalg_citeseer_undirected_logistic.embedding")
# learn_by_walks(g, node_list, node_labels, walk_len=20, walk_num=300, dim=128,
#                output_path="myalg_citeseer_undirected_randomwalk.embedding")



plot_graph(g, node_list, node_labels)