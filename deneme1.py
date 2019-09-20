from simhash import *
import numpy as np
dim = 32

def hamming_distance(v1, v2, dim):
    x = (v1 ^ v2) & ((1 << dim) - 1)
    sum = 0
    while x:
        sum += 1
        x &= x - 1
    return sum


v1 = SimHash(['a', 'b', 'd', 'c','f'], dim)
v2 = SimHash(['d', 'c', 'b', 'a', 'g'], dim)

b1 = np.asarray(v1.get_binary())*1.0
b2 = np.asarray(v2.get_binary())*1.0

s = np.vstack((b1/np.sum(b1), b2/np.sum(b2)))
print(np.sum(np.min(s, 0)) / np.sum(np.max(s, 0)))


#print(v1, v21)
print(v1.hamming_distance(v2))