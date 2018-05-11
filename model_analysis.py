from scipy.spatial import distance
import math

COSINE = "cosine"
EUCLIDEAN = "euclidean"

def similarity(v1, v2, metric=COSINE):
    if metric == COSINE:
        return cosine_distance(v1, v2)
    elif metric == EUCLIDEAN:
        return -euclidean_distance(v1, v2)
    else:
        raise Exception("Unsupported metric %r" % metric)

def cosine_distance(v1, v2):
    d = distance.cosine(v1, v2)
    if math.isnan(d):
        return 0
    else:
        return 1 - d

def euclidean_distance(v1, v2):
    return distance.euclidean(v1, v2)

class SpacyModelAnalyzer:
    def __init__(self, nlp):
        self._nlp = nlp

    @property
    def nlp(self):
        return self._nlp

    def find_by_analogy(self, token_string_a, token_string_b, token_string_c, num_results=10):
        d_vector = self.word_vector(token_string_b) - self.word_vector(token_string_a) + \
                   self.word_vector(token_string_c)
        c_orth = self.nlp(token_string_c)[0].orth
        words_to_consider = [
            word for word in self.nlp.vocab
            if word.orth != c_orth and word.orth_.islower()]
        by_similarity = sorted(
            words_to_consider, key=lambda word: similarity(word.vector, d_vector), reverse=True)
        return [(word.orth_, similarity(word.vector, d_vector), word.prob)
                for word in by_similarity[:num_results]]

    def word_vector(self, string):
        return self.token(string).vector

    def token(self, string):
        return self.nlp(string)[0]

    def find_by_similarity(self, token_string, metric=COSINE, num_results=10):
        vector = self.word_vector(token_string)
        words_to_consider = [
            word for word in self.nlp.vocab
            if word.orth_.islower()]
        by_similarity = sorted(
            words_to_consider,
            key=lambda word: similarity(word.vector, vector, metric),
            reverse=True)
        return [(word.orth_, similarity(word.vector, vector, metric), word.prob)
                for word in by_similarity[:num_results]]

    def interpolate_linear(self, token_string_a, token_string_b, num_steps=3):
        vector_a = self._word_vector(token_string_a)
        vector_b = self._word_vector(token_string_b)
        a_orth = self.nlp(token_string_a)[0].orth
        b_orth = self.nlp(token_string_b)[0].orth
        words_to_consider = [
            word for word in self.nlp.vocab
            if word.orth_.islower() and word.orth not in [a_orth, b_orth]]
        results = []
        for n in range(num_steps):
            r = float(n+1) / (num_steps+1)
            vector = vector_a + r * (vector_b - vector_a)
            by_similarity = sorted(
                words_to_consider,
                key=lambda word: similarity(word.vector, vector), reverse=True)
            if len(by_similarity) > 0:
                word = by_similarity[0]
                results.append((word.orth_, similarity(word.vector, vector), word.prob))
        return results

    def interpolate_nearest_neighbour(self, token_string_a, token_string_b, num_neighbours=10):
        vector_a = self.word_vector(token_string_a)
        vector_b = self.word_vector(token_string_b)
        a_orth = self.token(token_string_a).orth
        b_orth = self.token(token_string_b).orth
        results = []
        current_orth = a_orth
        current_vector = vector_a
        previous_orths = set()
        while current_orth != b_orth:
            previous_orths.add(current_orth)
            words_to_consider = [
                word for word in self.nlp.vocab
                if word.orth not in previous_orths and \
                word.orth_.islower()]
            by_similarity_to_current = sorted(
                words_to_consider,
                key=lambda word: similarity(word.vector, current_vector), reverse=True)
            nearest_neighbours = by_similarity_to_current[:num_neighbours]
            print [w.orth_ for w in nearest_neighbours]
            word = max(
                nearest_neighbours,
                key=lambda word: similarity(word.vector, vector_b))
            print word.orth_ # TEMP
            print "similarity to b:", similarity(word.vector, vector_b) # TEMP
            results.append((word.orth_, word.prob))
            current_orth = word.orth
            current_vector = word.vector
        return results

    def compare_distance_metrics(self, w1, rank_threshold=100):
        token1 = self.token(w1)
        v1 = token1.vector
        orth1 = token1.orth
        lexemes_to_consider = [
            lexeme for lexeme in self.nlp.vocab
            if lexeme.has_vector and lexeme.orth != orth1]

        by_cosine = sorted(
            lexemes_to_consider, key=lambda lexeme: distance.cosine(v1, lexeme.vector))
        cosine_ranks = {}
        for index, lexeme in enumerate(by_cosine):
            cosine_ranks[lexeme.orth] = index
    
        by_euclidean = sorted(
            lexemes_to_consider, key=lambda lexeme: distance.euclidean(v1, lexeme.vector))
        euclidean_ranks = {}
        for index, lexeme in enumerate(by_euclidean):
            euclidean_ranks[lexeme.orth] = index

        def rank_difference(lexeme):
            return abs(cosine_ranks[lexeme.orth] - euclidean_ranks[lexeme.orth])

        by_disagreement = sorted(lexemes_to_consider, key=rank_difference, reverse=True)
        for lexeme in by_disagreement:
            cosine_rank = cosine_ranks[lexeme.orth]
            euclidean_rank = euclidean_ranks[lexeme.orth]
            if cosine_rank < rank_threshold and euclidean_rank >= rank_threshold or \
               euclidean_rank < rank_threshold and cosine_rank >= rank_threshold:
                yield lexeme, cosine_rank, distance.cosine(v1, lexeme.vector), \
                    euclidean_rank, distance.euclidean(v1, lexeme.vector)
