import scipy.spatial.distance
import math

def similarity(v1, v2):
    cosine_distance = scipy.spatial.distance.cosine(v1, v2)
    if math.isnan(cosine_distance):
        return 0
    else:
        return 1 - cosine_distance

class SpacyModelAnalyzer:
    def __init__(self, nlp):
        self._nlp = nlp

    @property
    def nlp(self):
        return self._nlp

    def find_by_analogy(self, token_string_a, token_string_b, token_string_c, num_results=10):
        d_vector = self._word_vector(token_string_b) - self._word_vector(token_string_a) + \
                   self._word_vector(token_string_c)
        c_orth = self.nlp(token_string_c)[0].orth
        words_to_consider = [
            word for word in self.nlp.vocab
            if word.orth != c_orth and word.orth_.islower()]
        by_similarity = sorted(
            words_to_consider, key=lambda word: similarity(word.vector, d_vector), reverse=True)
        return [(word.orth_, similarity(word.vector, d_vector), word.prob)
                for word in by_similarity[:num_results]]

    def _word_vector(self, string):
        return self.nlp(string)[0].vector

    def find_by_similarity(self, token_string, num_results=10):
        vector = self._word_vector(token_string)
        words_to_consider = [
            word for word in self.nlp.vocab
            if word.orth_.islower()]
        by_similarity = sorted(
            words_to_consider, key=lambda word: similarity(word.vector, vector), reverse=True)
        return [(word.orth_, similarity(word.vector, vector), word.prob)
                for word in by_similarity[:num_results]]
