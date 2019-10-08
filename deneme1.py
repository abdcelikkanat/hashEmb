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

def cosine_similarity_sets(s1, s2):

    return float(len(set(s1).intersection(set(s2)))) / np.sqrt(len(s1) * len(s2))


def equality_prob(b1, b2):

    return np.sum(b1 == b2) / float(len(b1))


s1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
s11 = ['aa', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
s2 = ['a', 'b', 'c']
s3 = ['a', 'b', 'd']
s4 = ['a', 'x', 'y', 'z', 'b', 'c', 'd', 'd', 'e', 'k']

v1 = SimHash(s1, dim)
v11 = SimHash(s11, dim)
v2 = SimHash(s2, dim)
v3 = SimHash(s3, dim)
v4 = SimHash(s4, dim)

b1 = np.asarray(v1.get_binary())*1.0
b11 = np.asarray(v11.get_binary())*1.0
b2 = np.asarray(v2.get_binary())*1.0
b3 = np.asarray(v3.get_binary())*1.0
b4 = np.asarray(v4.get_binary())*1.0


print(b1)
print(b2)
print(b3)
print(b4)


print(equality_prob(b3, b1))
print(v1.hamming_distance(v3)/float(dim))

print("-------------------------------------------")

c = cosine_similarity_sets(s1=s1, s2=s3)
t = 1.0 - (np.arccos(c) / np.pi)

print(c)

print("->", t)
