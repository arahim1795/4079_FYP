from colorama import init, Fore
import json
from nltk.corpus import stopwords
import spacy
from spacy.tokenizer import Tokenizer
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from typing import Dict, List


class Annotator:
    def __init__(self, db):
        self.db = db

        self.nlp = spacy.load("en_core_web_lg")

        self.stop_words = stopwords.words("english")
        wanted_stopwords = [
            "up",
            "down",
            "not",
            "off",
            "haven't",
            "aren't",
            "against",
            "under",
            "no",
            "only",
            "don't",
            "didn't",
            "doesn't",
            "hadn't",
            "haven't",
            "isn't",
            "mightn't",
            "wasn't",
            "wouldn't",
            "hasn't",
            "until",
            "won't",
            "only",
            "too",
            "below",
            "above",
            "but",
            "before",
            "after",
            "most",
            "more",
            "less"
        ]
        self.stop_words = [e for e in self.stop_words if e not in wanted_stopwords]
        unwanted_stopwords = ["we'll", "i'm"]
        self.stop_words = self.stop_words + unwanted_stopwords

        self.tokenise = Tokenizer(self.nlp.vocab)

    def _sentencise(self, raw_text: str):
        paragraphed = list(filter(None, raw_text.split("\n")))

        sentencised = []
        for paragraph in paragraphed:
            sentencised += [
                sentence.text.strip() for sentence in self.nlp(paragraph).sents
            ]

        return sentencised

    def _sanitise(self, sentence: str):
        unfiltered = [token.text for token in self.tokenise(sentence)]

        # remove stop words
        filtered = [word for word in unfiltered if word.lower() not in self.stop_words]

        return " ".join(word for word in filtered).replace(" - - ","--").replace(" - ","-")

    def _lemmatise(self, sentences: List[str]):
        lemmatised_sentences = []

        for doc in self.nlp.pipe(sentences):
            lemmatised_sentences.append([token.lemma_ for token in doc])

        for i in range(len(lemmatised_sentences)):
            lemmatised_sentences[i] = " ".join(
                lemma for lemma in lemmatised_sentences[i]
            )

        return lemmatised_sentences

    def _load_file(self, filename: str):
        return json.load(open("./data/" + filename + ".json", "r"))

    def _save_file(self, filename: str, data: List[Dict[str, str]]):
        with open("./data/" + filename + ".json", "w") as file:
            json.dump(data, file, indent=2)

    def manual_annotation(self, raw_text: str, filename: str):

        exisiting_list = self._load_file(filename)
        save = False

        sentences = [
            self._sanitise(sentence) for sentence in self._sentencise(raw_text)
        ]

        sentences = self._lemmatise(sentences)

        sentences = [self._sanitise(sentence) for sentence in sentences]

        init()

        print("Classifying Statements")
        print("1: pos, 2: neu, 3: neg, 4: not relevant")

        annotated_list = []

        while True:
            for sentence in sentences:
                print(">>> " + sentence + " <<<")
                d = {}
                while True:
                    try:
                        x = int(input("> "))

                        if x == 1:
                            d["text"] = sentence
                            d["label"] = "pos"
                            break
                        elif x == 2:
                            d["text"] = sentence
                            d["label"] = "neu"
                            break
                        elif x == 3:
                            d["text"] = sentence
                            d["label"] = "neg"
                            break
                        elif x == 4:
                            print("Not Relevant")
                            break
                        else:
                            print("Invalid Input")
                    except ValueError:
                        print("Invalid Input")
                if x == 1 or x == 2 or x == 3:
                    annotated_list.append(d)

            if annotated_list:
                print("============")
                for i in range(len(annotated_list)):
                    label = str(annotated_list[i].get("label"))
                    text = str(annotated_list[i].get("text"))
                    if label == "pos":
                        print(
                            str(i)
                            + ": "
                            + Fore.GREEN
                            + label
                            + Fore.RESET
                            + " > "
                            + text
                        )
                    elif label == "neu":
                        print(
                            str(i)
                            + ": "
                            + Fore.BLUE
                            + label
                            + Fore.RESET
                            + " > "
                            + text
                        )
                    else:
                        print(
                            str(i) + ": " + Fore.RED + label + Fore.RESET + " > " + text
                        )

                print("============")
                print("Confirm (Y/y) or Quit(Q/q)?")
                print("============")
                try:
                    y = str(input()).lower()
                    if y == "y":
                        save = True
                        break
                    elif y == "q":
                        break
                except ValueError:
                    print("Invalid Input. (Reannotation Required)")
            else:
                break

        if save:
            self._save_file(filename, exisiting_list + annotated_list)

    def automatic_annotation(self, raw_text: str, data_file: str, out_file: str):
        exisiting_list = self._load_file(data_file)

        sentences = [
            self._sanitise(sentence) for sentence in self._sentencise(raw_text)
        ]

        sentences = self._lemmatise(sentences)

        sentences = [self._sanitise(sentence) for sentence in sentences]

        with open("./data/" + data_file + ".json", "r") as file:
            classifier = NaiveBayesClassifier(file, format="json")

        print("Classifying Statements (Auto)")

        auto_classified = []

        for i in range(len(sentences)):

            if not sentences[i] or sentences[i] == "happen" or sentences[i] == "\"":
                continue

            d = {}
            classified = classifier.prob_classify(sentences[i])
            d["text"] = sentences[i]
            d["label"] = classified.max()
            auto_classified.append(d)

        exisiting_list = exisiting_list + auto_classified

        self._save_file(out_file, exisiting_list)
