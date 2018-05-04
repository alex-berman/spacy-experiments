import model_analysis
import spacy
import pprint

nlp = spacy.load("en_core_web_md")
analyzer = model_analysis.SpacyModelAnalyzer(nlp)
result = analyzer.find_by_analogy(u"man", u"king", u"woman")
pprint.pprint(result)
