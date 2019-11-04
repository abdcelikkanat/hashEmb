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


dim = 1024
filename = "cora_undirected"
graph_path="../datasets/{}.gml".format(filename)
#output_path="./embeddings/{}_2ego_dim={}_sacma.embedding".format(filename, dim)
output_path="./embeddings/{}_rw_n=10_l=3_dim={}_0=0.embedding".format(filename, dim)


g = nx.read_gml(graph_path)

nb_list = [[] for _ in range(g.number_of_nodes())]
nb_list2 = [[] for _ in range(g.number_of_nodes())]

''' '''
for node in g.nodes():
    nb_list2[int(node)].append(str(node))
    for nb in nx.neighbors(g, node):
        nb_list2[int(node)].append(str(nb))
        if int(node) == 0:
            print(", ", nb)
        for nb_nb in nx.neighbors(g, nb):
            nb_list2[int(node)].append(str(nb_nb))
            if int(node) == 0:
                print("2: ", nb_nb)


rw = RandomWalks(g, method='deepwalk', N=1000, L=3)
walks = rw.get_walks()
for walk in walks:
    if 0 == 0:
        nb_list[int(walk[0])].extend(str(w) for w in walk)
        #print(nb_list[int(walk[0])])
	if len(walk) != 3:
	    raise ValueError("DUR")
    else:
        nb_list[int(walk[0])].extend(walk[1:])

#for node in g.nodes():
#    nb_list[int(node)] = list(set(nb_list[int(node)]))


#srp = SimHashSRP(dim=dim, vocab_size=g.number_of_nodes(), hash_function=_crc32_function)

#emb = np.zeros(shape=(g.number_of_nodes(), dim), dtype=np.float)
#for node in g.nodes():
#    emb[int(node), :] += srp.encode(nb_list[int(node)])

#save_emb(emb=emb, N=g.number_of_nodes(), dim=dim, outputname=output_path)

#print(sorted(nb_list[0]))
#print(sorted(nb_list2[0]))

print(list(set(nb_list[0])))
print(list(set(nb_list2[0])))



print(len(list(set(nb_list[0]))))
print(len(list(set(nb_list2[0]))))

