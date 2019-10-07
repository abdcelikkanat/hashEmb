from simhash import *
import numpy as np
from scipy.spatial.distance import cdist
dim = 1024


def hamming_distance(v1, v2, dim):
    x = (v1 ^ v2) & ((1 << dim) - 1)
    sum = 0
    while x:
        sum += 1
        x &= x - 1
    return sum


def cosine_similarity(v1, v2):

    return 1.0 - cdist(np.asarray([v1.get_binary()]), np.asarray([v2.get_binary()]), metric='cosine')[0][0]



v1 = SimHash(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p'], dim)
v2 = SimHash(['a', 'b', 'c'], dim)
v3 = SimHash(['a', 'b', 'd'], dim)

b1 = np.asarray(v1.get_binary())*1.0
b2 = np.asarray(v2.get_binary())*1.0
b3 = np.asarray(v3.get_binary())*1.0

print(b1)
print(b2)
print(b3)
print(cosine_similarity(v1, v2))
print(cosine_similarity(v1, v3))
print(cosine_similarity(v2, v3))