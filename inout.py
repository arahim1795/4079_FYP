import json
from nltk.corpus import stopwords
from spacy.lang.en import English
from spacy.pipeline import Sentencizer
from spacy.tokenizer import Tokenizer


def sanitise_sentence(sentence):

    # set up
    stop_words = stopwords.words("english")
    stop_words.append("--")
    # print(stop_words)

    nlp = English()
    tokenizer = Tokenizer(nlp.vocab)

    # tokenise
    tokens = tokenizer(sentence)
    tokens_str = [token.text for token in tokens]  # convert from token to string type
    # print(tokens_str)
    tokens_str_filtered = [word for word in tokens_str if word not in stop_words]
    # print(tokens_str_filtered)

    reformed_sentence = " ".join(word for word in tokens_str_filtered)
    # print(reformed_sentence)

    return reformed_sentence


def split_paragraph(paragraph):

    # set up
    nlp = English()
    sentencizer = Sentencizer()
    nlp.add_pipe(sentencizer)

    document = nlp(paragraph)

    sentences = list(document.sents)

    return [sanitise_sentence(sentence.text) for sentence in sentences]


# test_paragraph = "Depending on how you look at it, there's never been a better -- or worse -- time to own Disney (NYSE:DIS). The media giant closed out fiscal 2019 with a bang, and it reports financial results for its fiscal first quarter after Tuesday's market close."

# sanitised_data = split_paragraph(test_paragraph)

data = json.load(open("data/preprocessed.json", "r"))
# print(type(data))
# print(data)

positives = []
neutrals = []
for datum in data:
    # print(datum["label"])
    pre_processed_string = datum["text"]
    datum["text"] = sanitise_sentence(pre_processed_string)
    if datum["label"] == "pos":
        positives.append(datum)
    if datum["label"] == "neu":
        neutrals.append(datum)

combination = positives + neutrals

with open("out/sorted.json", "w") as f:
    json.dump(combination, f, indent=2)
