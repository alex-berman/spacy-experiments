import model_analysis
import spacy
import pprint
from prettytable import PrettyTable

print "Loading model..."
nlp = spacy.load("en_core_web_md", disable=["parser"])
analyzer = model_analysis.SpacyModelAnalyzer(nlp)

print "Analyzing similarity..."
result = analyzer.find_by_similarity(u"happy")
pprint.pprint(result)

print "Analyzing analogy..."
result = analyzer.find_by_analogy(u"man", u"king", u"woman")
pprint.pprint(result)

print "Interpolating..."
result = analyzer.interpolate_linear(u"happy", u"sad", num_steps=3)
pprint.pprint(result)

print "Comparing distance metrics..."
result = analyzer.compare_distance_metrics(u"happy")
table = PrettyTable(["Word", "Cosine rank", "Cosine dist", "Euclidean rank", "Euclidean dist"])
for lexeme, cosine_rank, cosine_distance, euclidean_rank, euclidean_distance in result:
    table.add_row([lexeme.orth_,
                   cosine_rank, "%.3f" % cosine_distance,
                   euclidean_rank, "%.3f" % euclidean_distance])

print table
