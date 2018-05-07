import model_analysis
import spacy
import pprint

print "Loading model..."
nlp = spacy.load("en_core_web_md")
analyzer = model_analysis.SpacyModelAnalyzer(nlp)

print "Analyzing similarity..."
result = analyzer.find_by_similarity(u"happy")
pprint.pprint(result)

# print "Analyzing analogy..."
# result = analyzer.find_by_analogy(u"man", u"king", u"woman")
# pprint.pprint(result)

