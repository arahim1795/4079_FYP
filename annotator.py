from colorama import init, Fore
import csv
from nltk.corpus import stopwords
import re
import spacy

# from textblob import TextBlob
# from textblob.classifiers import NaiveBayesClassifier
from typing import List, Tuple, Union


class Annotator:
    def __init__(self, db):
        self.db = db
        self.nlp = spacy.load("en_core_web_lg")

        init()

    def _sentencise(self, raw_text: str):
        paragraphed = list(filter(None, raw_text.split("\n")))

        sentencised = []
        for paragraph in paragraphed:
            sentencised += [
                sentence.text.strip() for sentence in self.nlp(paragraph).sents
            ]

        return sentencised

    def _load(self, save_file: str) -> Tuple[bool, Union[List[List[str]], None]]:
        try:
            data = []
            with open("./data/" + save_file + ".csv", "r") as csvfile:
                data = list(csv.reader(csvfile))

            return True, data
        except Exception as e:
            print(e)
            return False, None

    def _save(self, save_file: str, data: List[List[str]]) -> bool:
        try:
            with open("./data/" + save_file + ".csv", "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(data)
            return True
        except Exception as e:
            print(e)
            return False

    def _paragrapher(self, article: str) -> List[str]:
        # core
        paragprahs = list(filter(None, article.split("\n")))
        paragraphs = [paragpraph.strip() for paragpraph in paragprahs]

        return paragraphs

    def _pre_cleanse_text(self, text: str) -> str:
        # # core
        # # TODO: More Stocker Tickers
        # tickers = ["OTC", "NASDAQ", "NYSE"]
        # ticker_patterns = ["\\(" + ticker + ":.+?\\)" for ticker in tickers]

        # for pattern in ticker_patterns:
        #     text = re.sub(pattern, "", text)

        generic_patterns = [
            ["\\(.+?:.+?\\)", ""],
            ["\\.\\.\\.", ""],
            ["\\([\\w+, !\\?]+\\)", ""],
            ["  ", " "],
            [" \\.", "."],
            [" ,", ","],
            ["^\\d\\. ", ""],
            ["U\\.S\\.", "United States"],
            ["\\.+\\?", ""],
            ['"', ""],
            ["\\b\\w+n't\\b", "not"],
        ]
        for pattern in generic_patterns:
            text = re.sub(pattern[0], pattern[1], text)

        wanted_stopwords = [
            "above",
            "after",
            "against",
            "before",
            "below",
            "but",
            "down",
            "less",
            "more",
            "most",
            "no",
            "nor",
            "not",
            "off",
            "only",
            "under",
            "until",
            "too",
            "up",
        ]
        stop_words = [
            e for e in stopwords.words("english") if e not in wanted_stopwords
        ]

        text = [word for word in text.split() if word.lower() not in stop_words]
        text[0] = text[0].capitalize()
        text = " ".join(word for word in text)

        stopword_pattern = ["[Hh]ere", "[TtWw]hat", "[Tt]here"]
        stopword_pattern = ["\\b" + pattern + "'s\\b" for pattern in stopword_pattern]
        stopword_pattern += ["\\b\\w+'ll\\b", "\\b[Ii](t|'((ve)|m))\\b", "\\b(([Yy]ou)|([Tt]hey))'re\\b"]
        for pattern in stopword_pattern:
            text = re.sub(pattern, "", text)

        text = text.replace("  ", " ")

        return text.strip()

    def _sentence_segmentor(self, text: str) -> list:
        # init
        segmented = []

        # core
        segmented += [sentence.text.strip() for sentence in self.nlp(text).sents]

        return segmented

    def _post_cleanse_text(self, text: str) -> str:
        # core
        generic_patterns = [[".+\\?", ""], [".+vs\\..+", ""], [".*[Ll]et's.*", ""]]
        for pattern in generic_patterns:
            text = re.sub(pattern[0], pattern[1], text)

        return text

    def _lemmatise_sentence(self, text: str) -> str:
        # core
        text = text.replace(",", "").replace(".", "")

        text = self.nlp(text)
        text = " ".join([token.lemma_ for token in text])

        return text.strip().replace(" - - ", "--").replace(" - ", "-").replace(" 's", "'s")

    def manual_annotation(self, articles: List[str], save_file: str):
        # init: load saved annotated data
        load_success, annotated_data = self._load(save_file)
        if load_success:
            print("Load Successful")

        # core
        # 1: Basic Paragraphing
        # 2: Pre Cleanse Text
        # 3: Segment into Sentences via NLP
        # 4: Post Cleanse Text
        # 5: Lemmatise Text
        # 6: Annotate Text

        # 1
        paragraphed_text = []
        for article in articles:
            paragraphed_text += self._paragrapher(article)

        # 2
        paragraphed_text = [
            self._pre_cleanse_text(paragraph) for paragraph in paragraphed_text
        ]

        # 3
        segmented_text = []
        for paragraph in paragraphed_text:
            segmented_text += self._sentence_segmentor(paragraph)

        # 4
        segmented_text = [
            self._post_cleanse_text(sentence) for sentence in segmented_text
        ]
        segmented_text = list(filter(None, segmented_text))

        # 5
        segmented_text = [
            self._lemmatise_sentence(sentence) for sentence in segmented_text
        ]

        # 6
        print("Annotate Text")

        green, blue, red, reset = (
            Fore.GREEN,
            Fore.BLUE,
            Fore.RED,
            Fore.RESET,
        )  # text colours

        print(
            green
            + "0: pos"
            + reset
            + ", "
            + blue
            + "1: neu"
            + reset
            + ", "
            + red
            + "2: neg"
            + reset
        )

        newly_annotated = []
        save_data = False
        while True:
            for sentence in segmented_text:
                print(">> " + sentence)
                while True:
                    try:
                        x = int(input("> "))
                        if x < 0 or x > 2:
                            print("Invalid Range")
                        else:
                            break
                    except ValueError:
                        print("Invalid Input")
                newly_annotated.append([sentence, str(x)])

            if newly_annotated:
                print("============")

                for annotation in newly_annotated:
                    if annotation[1] == "0":
                        print(green + "pos" + reset + " > " + annotation[0])
                    elif annotation[1] == "1":
                        print(blue + "neu" + reset + " > " + annotation[0])
                    else:
                        print(red + "neg" + reset + " > " + annotation[0])

                print("============")
                print("Save (Y/y) or Quit (Q/q)?")
                print(blue + "press any other button to restart annotation" + reset)

                i = str(input("> ")).lower()
                if i == "y" or i == "q":
                    if i == "y":
                        save_data = True
                    break
                else:
                    print("Reset Annotations")

        # final
        if save_data:
            annotated_data += newly_annotated
        save_success = self._save(save_file, annotated_data)
        if save_data:
            print("Save Successful")
        elif save_success:
            print("Annotation Terminated")

    def _unannotated_csv_export(self, articles: List[str], save_file: str):
        # init: load saved annotated data
        load_success, annotated_data = self._load(save_file)
        if load_success:
            print("Import Successful")

        # core
        # 1: Basic Paragraphing
        # 2: Pre Cleanse Text
        # 3: Segment into Sentences via NLP
        # 4: Post Cleanse Text
        # 5: Lemmatise
        # 6: Append Unannotated Data

        # 1
        paragraphed_text = []
        for article in articles:
            paragraphed_text += self._paragrapher(article)

        # 2
        paragraphed_text = [
            self._pre_cleanse_text(paragraph) for paragraph in paragraphed_text
        ]

        # 3
        segmented_text = []
        for paragraph in paragraphed_text:
            segmented_text += self._sentence_segmentor(paragraph)

        # 4
        segmented_text = [
            self._post_cleanse_text(sentence) for sentence in segmented_text
        ]
        segmented_text = list(filter(None, segmented_text))

        # 5
        segmented_text = [
            self._lemmatise_sentence(sentence) for sentence in segmented_text
        ]

        # 6
        newly_annotated = []
        for sentence in segmented_text:
            newly_annotated.append([sentence, None])

        annotated_data += newly_annotated

        # final
        save_success = self._save(save_file, annotated_data)
        if save_success:
            print("Export Successful")

    # def automatic_annotation(self, raw_text: str, data_file: str, out_file: str):
    #     exisiting_list = self._load_file(data_file)

    #     sentences = [
    #         self._sanitise(sentence) for sentence in self._sentencise(raw_text)
    #     ]

    #     sentences = self._lemmatise(sentences)

    #     sentences = [self._sanitise(sentence) for sentence in sentences]

    #     with open("./data/" + data_file + ".json", "r") as file:
    #         classifier = NaiveBayesClassifier(file, format="json")

    #     print("Classifying Statements (Auto)")

    #     auto_classified = []

    #     for i in range(len(sentences)):

    #         if not sentences[i] or sentences[i] == "happen" or sentences[i] == '"':
    #             continue

    #         d = {}
    #         classified = classifier.prob_classify(sentences[i])
    #         d["text"] = sentences[i]
    #         d["label"] = classified.max()
    #         auto_classified.append(d)

    #     exisiting_list = exisiting_list + auto_classified

    #     self._save_file(out_file, exisiting_list)
