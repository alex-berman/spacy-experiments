import scipy.spatial.distance
import math

def similarity(v1, v2):
    cosine_distance = scipy.spatial.distance.cosine(v1, v2)
    if math.isnan(cosine_distance):
        return 0
    else:
        return 1 - cosine_distance

# def most_similar(vector, vocab, min_prob=-15, num_results=10):
#     unrare_words = [w for w in vocab if w.prob >= min_prob]
#     by_similarity = sorted(
#         unrare_words, key=lambda word: similarity(word.vector, vector), reverse=True)
#     return [(word.orth_, similarity(word.vector, vector), word.prob)
#             for word in by_similarity[:num_results]]



def most_similar(vector, vocab, num_results=10):
    by_similarity = sorted(
        vocab, key=lambda word: vector.similarity(word), reverse=True)
    return [(word.orth_, vector.similarity(word), word.prob)
            for word in by_similarity[:num_results]]


def word_vector(string, nlp):
    return nlp(string)[0].vector

def most_analogous(a, b, c, nlp, num_results=10):
    d = word_vector(b, nlp) - word_vector(a, nlp) + word_vector(c, nlp)
    c_orth = nlp(c)[0].orth
    words_to_consider = [word for word in nlp.vocab if word.orth != c_orth]
    by_similarity = sorted(
        words_to_consider, key=lambda word: similarity(word.vector, d), reverse=True)
    return [(word.orth_, similarity(word.vector, d), word.prob)
            for word in by_similarity[:num_results]]
