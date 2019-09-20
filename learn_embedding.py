from simhash import *
import networkx as nx
import numpy as np
from random_walks import *

class LearnEmb:
    def __init__(self, g, dim):

        self.g = g
        self.N = g.number_of_nodes()
        self.dim = dim
        self.emb = self.get_signatures()

    def _get_nblist(self):

        self.nb_list = [[] for _ in range(self.N)]

        for node in range(self.N):
            self.nb_list[node].append(str(node))
            for nb in nx.neighbors(self.g, str(node)):
                self.nb_list[node].append(str(nb))
                for nb_nb in nx.neighbors(self.g, str(nb)):
                    if nb_nb not in self.nb_list[node]:
                        self.nb_list[node].append(str(nb_nb))

    def _get_nblist_random_walks(self):

        self.nb_list = [[] for _ in range(self.N)]

        rw = RandomWalks(g=self.g, method='deepwalk', N=80, L=10)
        for walk in rw.get_walks():
            self.nb_list[int(walk[0])].extend(walk[1:])

    def get_signatures(self):

        #self._get_nblist()
        self._get_nblist_random_walks()

        emb = np.zeros(shape=(self.N, self.dim), dtype=bool)
        masks = [1 << d for d in range(self.dim)]
        for node in range(self.N):
            x = SimHash(self.nb_list[node], self.dim).input
            for d in range(self.dim):
                if x & masks[d]:
                    emb[node][self.dim-d-1] = True
                else:
                    emb[node][self.dim-d-1] = False

        return emb

    def save_emb(self, outputname):

        with open(outputname, 'w') as f:
            f.write("{} {}\n".format(self.N, self.dim))
            for node in range(self.N):
                line = "{} {}\n".format(str(node), " ".join('1' if v else '0' for v in self.emb[node, :]))
                f.write(line)









