import model_analysis
import spacy
from prettytable import PrettyTable

print "Loading model..."
nlp = spacy.load("en_core_web_md", disable=["parser"])
analyzer = model_analysis.SpacyModelAnalyzer(nlp)

num_words = 100

lexemes_by_frequency = sorted(
    [lexeme for lexeme in nlp.vocab if lexeme.has_vector],
    key=lambda lexeme: lexeme.prob,
    reverse=True)
common_lexemes = lexemes_by_frequency[:num_words]

all_results = []
for lexeme1 in common_lexemes:
    print lexeme1.orth_
    result = analyzer.compare_distance_metrics(lexeme1.orth_)
    for lexeme2, cosine_rank, cosine_distance, euclidean_rank, euclidean_distance in result:
        all_results.append((
            lexeme1, lexeme2, cosine_rank, cosine_distance, euclidean_rank, euclidean_distance))

sorted_by_rank = sorted(
    all_results,
    key=lambda result: min(result[2], result[4]))

table = PrettyTable(["Word 1", "Word 2", "Cosine rank", "Cosine dist", "Euclidean rank", "Euclidean dist"])
for lexeme1, lexeme2, cosine_rank, cosine_distance, euclidean_rank, euclidean_distance in sorted_by_rank:
    table.add_row([
        lexeme1.orth_, lexeme2.orth_,
        cosine_rank, "%.3f" % cosine_distance,
        euclidean_rank, "%.3f" % euclidean_distance])

print table
