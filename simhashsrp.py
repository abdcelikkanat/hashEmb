################################
#
################################


import hashlib
import numbers
import collections
from zlib import crc32
import numpy as np
from scipy.stats import ortho_group


def _md5_function(x):
    if isinstance(x, str):
        return int(hashlib.md5(x.encode()).hexdigest(), 16)
    else:
        return int(hashlib.md5(x).hexdigest(), 16)


def _crc32_function(x):
    return crc32(x) & 0xffffffff


class SimHashSRP:

    max_number = 2 ** 32 - 1

    dim = None

    hash_function = None

    w = None

    def __init__(self, vocab_size, dim, hash_function=None, hash_method="random-normal"):
        '''

        '''

        if type(hash_function) == 'function':
            self.hash_function = hash_function
        else:
            self.hash_function = _crc32_function

        self.vocab_size = vocab_size
        self.dim = dim
        self.renew_hash_function(method=hash_method)

    def renew_hash_function(self, method="random-normal"):

        # def _generate_coefficients(s):
        #
        #     coefficients = []
        #     while len(coefficients) < s:
        #
        #         num = np.random.randint(0, self.max_number)
        #         if num not in coefficients:
        #             coefficients.append(num)
        #
        #     return coefficients
        #
        # coefficients = _generate_coefficients(s=2)
        # self.a.append(coefficients[0])
        # self.b.append(coefficients[1])

        if method == "random-normal":
            self.w = np.random.normal(loc=0.0, scale=1.0, size=(self.dim, self.vocab_size))
        elif method == "orthogonal":
            if self.vocab_size < self.dim:
                raise ValueError("Vocabulary size ({}) is less than the dimension size ({})!".format(self.vocab_size, self.dim))
            self.w = ortho_group.rvs(self.vocab_size)
            self.w = self.w[0:self.dim, :]



    # def get_last_coefficient(self):
    #
    #     return self.a[-1], self.b[-1]
    #
    # def get_all_coefficients(self):
    #
    #     return self.a, self.b

    def encode(self, values):

        if not isinstance(values, list):
            raise Exception("Invalid input type! {}".format(type(values)))

        x = np.zeros(shape=(self.vocab_size, ), dtype=np.float)
        for value in values:

            x[int(value)] = 1.0

        output = np.sign(np.dot(x, self.w.T))

        output[output == -1] += 1

        return output


'''
doc1 = ['0', '1', '2']
doc2 = ['1', '2', '3']

m = SinHashSRP(dim=16, vocab_size=5, hash_function=_crc32_function)
m.renew_hash_function()
enc1 = m.encode(doc1)
enc2 = m.encode(doc2)

print(enc1)
print(enc2)

'''