import hashlib
import numbers
import collections
from zlib import crc32


def _hash_function(x):
    if isinstance(x, str):
        return int(hashlib.md5(x.encode()).hexdigest(), 16)
    else:
        return int(hashlib.md5(x).hexdigest(), 16)


class SimHash():

    def __init__(self, input, dim=128, hash_function=None):
        '''

        '''

        self.dim = dim

        self._masks = [1 << d for d in range(self.dim)]

        self.v = [0 for _ in range(self.dim)]

        if hash_function is None:
            self.hash_function = _hash_function
        else:
            self.hash_function = hash_function

        if isinstance(input, numbers.Integral):
            self.input = input
            raise ValueError("STOP!")
        elif isinstance(input, collections.Iterable):
            self.input = self.build_by_features(input)
        elif isinstance(input, SimHash):
            self.input = input.input
        else:
            raise Exception("Invalid parameter type {}".format(type(input)))

    def build_by_features(self, features):
        """
        `features` might be a list of unweighted tokens (a weight of 1
                   will be assumed), a list of (token, weight) tuples or
                   a token -> weight dict.
        """

        if isinstance(features, dict):
            features = features.items()
        for f in features:
            if isinstance(f, basestring):
                h = self.hash_function(f.encode('utf-8'))
                w = 1
            else:
                raise Exception("Invalid type type {}".format(type(input)))
            for d in range(self.dim):
                self.v[d] += w if h & self._masks[d] else -w

        sum = 0
        for d in range(self.dim):
            if self.v[d] > 0:
                sum |= self._masks[d]

        return sum

    def hamming_distance(self, another):

        assert self.dim == another.dim
        x = (self.input ^ another.input) & ((1 << self.dim) - 1)
        sum = 0
        while x:
            sum += 1
            x &= x - 1
        return sum

    def update_signature_insert(self, value):

        if isinstance(value, basestring):
            h = self.hash_function(value.encode('utf-8'))
            w = 1
        else:
            raise Exception("Invalid type type {}".format(type(input)))
        for d in range(self.dim):
            self.v[d] += w if h & self._masks[d] else -w

        sum = 0
        for d in range(self.dim):
            if self.v[d] > 0:
                sum |= self._masks[d]

        self.input = sum

    def update_signature_delete(self, value):

        if isinstance(value, basestring):
            h = self.hash_function(value.encode('utf-8'))
            w = 1
        else:
            raise Exception("Invalid type type {}".format(type(input)))
        for d in range(self.dim):
            self.v[d] += -w if h & self._masks[d] else w

        sum = 0
        for d in range(self.dim):
            if self.v[d] > 0:
                sum |= self._masks[d]

        self.input = sum

    def get_binary(self):

        binary_repr = []
        for d in range(self.dim):
            if self.input & self._masks[self.dim - d - 1]:
                binary_repr.append(1)
            else:
                binary_repr.append(0)

        return binary_repr