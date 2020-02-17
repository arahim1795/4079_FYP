from nltk.corpus import stopwords
from spacy.lang.en import English
from spacy.pipeline import Sentencizer
from spacy.tokenizer import Tokenizer
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer


train = [
    ("Depending look it, there's never better worse time Disney (NYSE:DIS).", "neu",),
    (
        "The media giant closed fiscal 2019 bang, reports financial results fiscal first quarter Tuesday's market close.",
        "pos",
    ),
]

test = [
    ("Apple closes bang", "pos"),
]

# sanitised_data = split_paragraph(test_paragraph)

c1 = NaiveBayesClassifier(train)
dist = c1.prob_classify("GM closest high bang")

print("pos:")
print(round(dist.prob("pos"), 2))
print("\n")
print("neutral:")
print(round(dist.prob("neu"), 2))


# print(sentences)

# list_of_sentence = list(doc.sents)

# print(len(list_of_sentence))
# print(list_of_sentence)

# for sen in list_of_sentence:
#     sentiment = TextBlob(str(sen))
#     print(sentiment.sentiment)


# # check for type
# ls = [type(item) for item in tokens_str]
# print(ls)
