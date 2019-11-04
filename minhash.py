import hashlib
import numbers
import collections
from zlib import crc32
import numpy as np
from inspect import isfunction

_prime_number = 4294967311


#def _md5_function(x):
#    if isinstance(x, str):
#        return int(hashlib.md5(x.encode()).hexdigest(), 16)
#    else:
#        return int(hashlib.md5(x).hexdigest(), 16)
#
#
#def _crc32_function(x):
#    return crc32(x) & 0xffffffff


class MinHash:

    max_number = 2 ** 32 - 1

    a = None
    b = None
    prime_number = _prime_number

    hash_function = None

    def __init__(self, hash_function=None):
        '''

        '''

        if isfunction(hash_function):
            self.hash_function = hash_function
        else:
            raise Exception("Invalid function type: {}".format(type(hash_function)))

        self.a = []
        self.b = []

        self.renew_hash_function()

    def renew_hash_function(self):

        def _generate_coefficients(s):

            coefficients = []
            while len(coefficients) < s:

                num = np.random.randint(0, self.max_number)
                if num not in coefficients:
                    coefficients.append(num)

            return coefficients

        coefficients = _generate_coefficients(s=2)
        self.a.append(coefficients[0])
        self.b.append(coefficients[1])

    def get_last_coefficient(self):

        return self.a[-1], self.b[-1]

    def get_all_coefficients(self):

        return self.a, self.b

    def encode(self, values):

        if not isinstance(values, list):
            raise Exception("Invalid input type! {}".format(type(values)))

        a, b = self.get_last_coefficient()

        output = []
        for value in values:

            v = self.hash_function(value)
            hashCode = (a * v + b) % self.prime_number / 2.0 ** 32

            output.append(hashCode)

        return output

    def getMinHashCodeOf(self, values):

        if not isinstance(values, list):
            raise Exception("Invalid input type! {}".format(type(values)))

        a, b = self.get_last_coefficient()
        minHashCode = self.prime_number

        for value in values:

            v = self.hash_function(value)
            hashCode = (a * v + b) % self.prime_number

            if minHashCode > hashCode:
                minHashCode = hashCode

        return minHashCode / 2.0 ** 32

'''
doc1 = ['a', 'c', 'b']
doc2 = ['a', 'c', 'd']

m = MinHash(hash_function=_crc32_function)
b = []
for _ in range(100):
    m.renew_hash_function()
    print(m.encode(['a', 'b', 'c', 'd']))
    doc1_min = m.getMinHashCodeOf(doc1)
    doc2_min = m.getMinHashCodeOf(doc2)
    b.append(doc1_min == doc2_min)

print(np.sum(b)/ float(len(b)), float(len(set(doc1).intersection(doc2)))/len(set(doc1).union(doc2)),   b)
'''
