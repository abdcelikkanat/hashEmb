import networkx as nx
from simhash import *
from learn_embedding import *

dim = 1024
filename = "citeseer_undirected"
graph_path="../datasets/{}.gml".format(filename)
output_path="./embeddings/{}_{}_ego1.embedding".format(filename, dim)

g = nx.read_gml(graph_path)
le = LearnEmb(g, dim)
le.save_emb(output_path)
