import numpy as np
import sys

input_path = sys.argv[1]
output_path = sys.argv[2]

input_embeddings={}
output_embeddings={}
with open(input_path, 'r') as fin, open(output_path, 'w') as fout:
    firstline = fin.readline()
    N, dim = (int(value) for value in firstline.strip().split())
    fout.write("{} {}\n".format(N, dim//2))


    for line in fin.readlines():
        tokens = line.strip().split()
        input_embeddings = np.asarray([float(token) for token in tokens[1:]])
        output_embedding = 0.5*(input_embeddings[0:dim//2] + input_embeddings[dim//2:])
        fout.write("{} {}\n".format(tokens[0], ' '.join(str(v) for v in output_embedding)))
