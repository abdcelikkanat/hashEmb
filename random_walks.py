import networkx as nx
import numpy as np


class RandomWalks:

    _method_names = ['deepwalk', 'node2vec']
    walks = []

    def __init__(self, g, method, N, L, opts=dict()):

        if method not in self._method_names:
            raise Exception("Invalid method name: {}".format(method))

        self.N = N
        self.L = L

        self.g = g
        self._nodelist = list(g.nodes())

        getattr(self, "_" + method)()

    def _deepwalk(self):

        self._walks = []
        for n in range(self.N):
            np.random.shuffle(self._nodelist)

            for node in self._nodelist:
                walk = [node]

                while len(walk) < self.L:

                    nb_list = list(nx.neighbors(self.g, walk[-1]))
                    nb = np.random.choice(a=nb_list, size=1)[0]

                    walk.append(nb)

                self._walks.append(walk)


    def _node2vec(self):

        raise ValueError("Not implemented!")

    def get_walks(self):

        return self._walks

    def save_walks(self, file_name):

        with open(file_name, 'w') as f:

            for walk in self._walks:
                f.write("{}\n".format(" ".join(w for w in walk)))

