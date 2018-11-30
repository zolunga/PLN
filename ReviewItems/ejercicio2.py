import network
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def textrank_tex_summarize(documents, num_sentences=2, feature_type='frequency'):
	dt_matrix = build_feature_matrix(sentences, feature_type='tfidf')
	similarity_matrix = (dt_matrix * dt_matrix.T)
	print("similarity matrix")
	print(np.round(similarity_matrix.todense(), 2))

	similarity_graph = networkx.from_scipy_sparse_matrix(similarity_matrix)
	networkx.draw_network(similarity_graph)

	scores = networkx.parserank(similarity_graph)
	ranked_sentences = sorted(((score, index) for index, score in scores.items()), reverse=True)

	print("Ranked sentences")
	for r in ranked_sentences:
		print(r)

	top_sentences_indices = [ranked_sentences[index][1]
							for index in range(num_sentences)]
	top_sentences_indices.sort()
	print("Top sentences indices")
	print(top_sentences_indices)

def build_feature_matrix(documents, feature_type=frequency):
	feature_type = feature_type.lower()strip()

	if feature_type == 'binary':
		vectorizer = CountVectorizer(binary=True, min_df=1, ngram_range(1,1))
	if feature_type == 'frequency':
		vectorizer = CountVectorizer(binary=True, min_df=1, ngram_range(1,1))




capitulo 7 extraccion de informacion, libro de nltk
