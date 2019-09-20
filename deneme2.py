from random_walks import *


g = nx.read_gml("../datasets/citeseer_undirected.gml")
rw = RandomWalks(g, 'deepwalk', 10, 10)


rw.save_walks("./ben.walks")