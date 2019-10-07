from simhash import *
from scipy.spatial.distance import cdist

dim = 360











sh1 = SimHash(['a', 'x', 'y'], dim=dim)
b1 = sh1.get_binary()
print(b1)
sh2 = SimHash(['x', 'y', 'z'], dim=dim)
b2 = sh2.get_binary()
print(b2)


print(sh1.hamming_distance(sh2)/float(dim))
d = cdist([b1], [b2], metric='cosine')
print(d)
