import cPickle
import model_analysis
import spacy
from prettytable import PrettyTable

def save_to_file(filename, data):
    with open(filename, "w") as f:
        cPickle.dump(data, f)

print "Loading model..."
nlp = spacy.load("en_core_web_md", disable=["parser"])
analyzer = model_analysis.SpacyModelAnalyzer(nlp)

num_words = 100

word_ids_by_frequency = sorted(
    [lexeme.orth_ for lexeme in nlp.vocab if lexeme.has_vector],
    key=lambda word_id: nlp.vocab[word_id].prob,
    reverse=True)
common_word_ids = word_ids_by_frequency[:num_words]

all_results = []
for i, word_id1 in enumerate(common_word_ids):
    lexeme1 = nlp.vocab[word_id1]
    print "i=%d lexeme1.orth_=%r" % (i, lexeme1.orth_)
    result = analyzer.compare_distance_metrics(lexeme1.orth_)
    for lexeme2, cosine_rank, cosine_distance, euclidean_rank, euclidean_distance in result:
        word_id2 = lexeme2.orth_
        all_results.append((
            word_id1, word_id2,
            cosine_rank, cosine_distance,
            euclidean_rank, euclidean_distance))

save_to_file("data/distance_metrics_%d_all_results.cPickle" % num_words, all_results)

sorted_by_rank = sorted(
    all_results,
    key=lambda result: min(result[2], result[4]))

save_to_file("data/distance_metrics_%d_by_rank.cPickle" % num_words, sorted_by_rank)

table = PrettyTable(["Word 1", "Word 2", "Cosine rank", "Cosine dist", "Euclidean rank", "Euclidean dist"])
for word_id1, word_id2,cosine_rank, cosine_distance, euclidean_rank, euclidean_distance in sorted_by_rank:
    table.add_row([
        nlp.vocab[word_id1].orth_, nlp.vocab[word_id2].orth_,
        cosine_rank, "%.3f" % cosine_distance,
        euclidean_rank, "%.3f" % euclidean_distance])

print table
