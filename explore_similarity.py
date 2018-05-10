import spacy
from scipy.spatial.distance import cosine, euclidean
from prettytable import PrettyTable

print "Loading model..."
nlp = spacy.load("en_core_web_md")

w1 = u"hello"
token1 = nlp(w1)[0]
v1 = token1.vector
orth1 = token1.orth
lexemes_to_consider = [lexeme for lexeme in nlp.vocab
                       if lexeme.has_vector and lexeme.orth != orth1]

by_cosine = sorted(lexemes_to_consider, key=lambda lexeme: cosine(v1, lexeme.vector))
cosine_ranks = {}
for index, lexeme in enumerate(by_cosine):
    cosine_ranks[lexeme.orth] = index
    
by_euclidean = sorted(lexemes_to_consider, key=lambda lexeme: euclidean(v1, lexeme.vector))
euclidean_ranks = {}
for index, lexeme in enumerate(by_euclidean):
    euclidean_ranks[lexeme.orth] = index

by_disagreement = sorted(lexemes_to_consider, key=lambda lexeme: abs(cosine_ranks[lexeme.orth] - euclidean_ranks[lexeme.orth]), reverse=True)

rank_threshold = 100
table = PrettyTable(["Word", "Cosine rank", "Cosine dist", "Euclidean rank", "Euclidean dist"])
for lexeme in by_disagreement:
    cosine_rank = cosine_ranks[lexeme.orth]
    euclidean_rank = euclidean_ranks[lexeme.orth]
    if cosine_rank < rank_threshold and euclidean_rank >= rank_threshold or \
       euclidean_rank < rank_threshold and cosine_rank >= rank_threshold:
        table.add_row([lexeme.orth_,
                       cosine_rank, "%.3f" % cosine(v1, lexeme.vector),
                       euclidean_rank, "%.3f" % euclidean(v1, lexeme.vector)])
print table
