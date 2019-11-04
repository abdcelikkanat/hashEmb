import networkx as nx
from simhashsrp import *
from learn_embedding import *


def save_emb(emb, N, dim, outputname):
    with open(outputname, 'w') as f:
        f.write("{} {}\n".format(N, dim))
        for node in range(N):
            line = "{} {}\n".format(str(node), " ".join('1' if v else '0' for v in emb[node, :]))
            f.write(line)


def _crc32_function(x):
    return crc32(x) & 0xffffffff


dim = 4096//2
filename = "dblp_new"
graph_path="../NodeSketch/graphs/{}.gml".format(filename)
#output_path="./embeddings/{}_2ego_dim={}_yeni.embedding".format(filename, dim)
N=50
L=3
output_path="./embeddings/{}_rw_n={}_l={}_dim={}_orthogonal_paper.embedding".format(filename,str(N), str(L), dim)


g = nx.read_gml(graph_path)

nb_list = [[] for _ in range(g.number_of_nodes())]


'''
for node in g.nodes():
    nb_list[int(node)].append(str(node))
    for nb in nx.neighbors(g, node):
        nb_list[int(node)].append(str(nb))
        for nb_nb in nx.neighbors(g, nb):
            nb_list[int(node)].append(str(nb_nb))

'''
rw = RandomWalks(g, method='deepwalk', N=N, L=L)
walks = rw.get_walks()
for walk in walks:
    nb_list[int(walk[0])].extend(str(w) for w in walk)


#for node in g.nodes():
#    nb_list[int(node)] = list(set(nb_list[int(node)]))

srp = SimHashSRP(dim=dim, vocab_size=g.number_of_nodes(), hash_function=_crc32_function, hash_method="orthogonal")

emb = np.zeros(shape=(g.number_of_nodes(), dim), dtype=np.float)
for node in g.nodes():
    emb[int(node), :] = srp.encode(nb_list[int(node)])

save_emb(emb=emb, N=g.number_of_nodes(), dim=dim, outputname=output_path)
