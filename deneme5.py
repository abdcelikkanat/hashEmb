from simhashsrp import *
import numpy as np
from scipy.spatial.distance import cdist
dim = 1024


def _crc32_function(x):
    return crc32(x) & 0xffffffff

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


s1 = ['0', '1', '2', '5', '7', '8']
s2 = ['1', '2', '3', '5', '8']
s3 = ['2', '3', '5', '7']


srp = SimHashSRP(dim=dim, vocab_size=16, hash_function=_crc32_function)


b1 = srp.encode(s1)
b2 = srp.encode(s2)
b3 = srp.encode(s3)

print(b1)
print(b2)
print(b3)


print(equality_prob(b1, b2))

print("-------------------------------------------")

c = cosine_similarity_sets(s1=s1, s2=s2)
t = 1.0 - (np.arccos(c) / np.pi)

print(c)

print("->", t)
