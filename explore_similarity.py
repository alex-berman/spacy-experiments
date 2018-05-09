import spacy
from scipy.spatial.distance import cosine, euclidean

print "Loading model..."
nlp = spacy.load("en_core_web_md")

v1 = nlp(u"hello")[0].vector

by_cosine = sorted(nlp.vocab, key=lambda lexeme: cosine(v1, lexeme.vector))
cosine_ranks = {}
for index, lexeme in enumerate(by_cosine):
    cosine_ranks[lexeme.orth] = index
    
by_euclidean = sorted(nlp.vocab, key=lambda lexeme: euclidean(v1, lexeme.vector))
euclidean_ranks = {}
for index, lexeme in enumerate(by_euclidean):
    euclidean_ranks[lexeme.orth] = index

rank_threshold = 10
by_disagreement = sorted(nlp.vocab, key=lambda lexeme: abs(cosine_ranks[lexeme.orth] - euclidean_ranks[lexeme.orth]), reverse=True)
for lexeme in by_disagreement:
    cosine_rank = cosine_ranks[lexeme.orth]
    euclidean_rank = euclidean_ranks[lexeme.orth]
    if cosine_rank < rank_threshold and euclidean_rank >= rank_threshold or \
       euclidean_rank < rank_threshold and cosine_rank >= rank_threshold:
        print lexeme.orth_, cosine_rank, euclidean_rank
