base=".."
dataset="citeseer_undirected"
emb=${base}/NodeSketch/embs_NodeSketch_${dataset}_order\=2_mine.embedding
output=${base}/NodeSketch/embs_NodeSketch_${dataset}_order\=2_mine.result
python run.py classification --graph ${base}/datasets/${dataset}.gml --emb ../NodeSketch/${emb} --output_file ${output} --classification_method svm-hamming --num_of_shuffles 10


base=".."
dataset="cora_undirected"
emb=${base}/NodeSketch/embs_NodeSketch_${dataset}_order\=2_mine.embedding
output=${base}/NodeSketch/embs_NodeSketch_${dataset}_order\=2_mine.result
python run.py classification --graph ${base}/datasets/${dataset}.gml --emb ../NodeSketch/${emb} --output_file ${output} --classification_method svm-hamming --num_of_shuffles 10



base=".."
dataset="dblp_undirected"
emb=${base}/NodeSketch/embs_NodeSketch_${dataset}_order\=2_mine.embedding
output=${base}/NodeSketch/embs_NodeSketch_${dataset}_order\=2_mine.result
python run.py classification --graph ${base}/datasets/${dataset}.gml --emb ../NodeSketch/${emb} --output_file ${output} --classification_method svm-hamming --num_of_shuffles 10



base=".."
dataset="blogcatalog"
emb=${base}/NodeSketch/embs_NodeSketch_${dataset}_order\=2_mine.embedding
output=${base}/NodeSketch/embs_NodeSketch_${dataset}_order\=2_mine.result
python run.py classification --graph ${base}/datasets/${dataset}.gml --emb ../NodeSketch/${emb} --output_file ${output} --classification_method svm-hamming --num_of_shuffles 10
