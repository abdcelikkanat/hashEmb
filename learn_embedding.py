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

    def _get_ego(self, e=1):

        self.nb_list = [[] for _ in range(self.N)]

        for node in range(self.N):
            if e >= 1:
                self.nb_list[node].append(str(node))
                for nb in nx.neighbors(self.g, str(node)):
                    self.nb_list[node].append(str(nb))
                    if e >= 2:
                        for nb_nb in nx.neighbors(self.g, str(nb)):
                            if nb_nb not in self.nb_list[node]:
                                self.nb_list[node].append(str(nb_nb))

    def _get_nblist_random_walks(self):

        self.nb_list = [[] for _ in range(self.N)]

        rw = RandomWalks(g=self.g, method='deepwalk', N=80, L=10)
        for walk in rw.get_walks():
            self.nb_list[int(walk[0])].extend(walk[1:])

    def _get_context_set(self):

        self.nb_list = [[] for _ in range(self.N)]

        window_size = 10
        rw = RandomWalks(g=self.g, method='deepwalk', N=80, L=10)
        for walk in rw.get_walks():
            walk_len = len(walk)
            for current_pos_inx in range(walk_len):

                min_pos_inx = max(0, current_pos_inx-window_size)
                max_pos_inx = min(walk_len, current_pos_inx+window_size)

                for context_pos_inx in range(min_pos_inx, max_pos_inx):
                    if context_pos_inx != current_pos_inx:
                        self.nb_list[int(walk[current_pos_inx])].append(walk[context_pos_inx])

    def get_signatures(self):

        #self._get_ego(e=2)
        #self._get_ego(e=1)
        #self._get_nblist_random_walks()
        self._get_context_set()


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









