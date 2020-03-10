from colorama import init, Fore
import csv
import multiprocessing as mp
from nltk.corpus import stopwords
import re
from sklearn.utils import gen_even_slices
import spacy
from textblob.classifiers import NaiveBayesClassifier
from tqdm import trange
from typing import List, Optional, Tuple, Union


class Annotator:
    def __init__(self):
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

    def _pre_cleanse_text(self, text: str) -> Union[str, None]:
        # # core
        try:
            # # TODO: More Stocker Tickers
            # tickers = ["OTC", "NASDAQ", "NYSE"]
            # ticker_patterns = ["\\(" + ticker + ":.+?\\)" for ticker in tickers]

            # for pattern in ticker_patterns:
            #     text = re.sub(pattern, "", text)

            generic_patterns = [
                ["\\(?[A-Z]+?:[A-Z\\.]+?\\)", ""],
                ["\\.\\.\\.", ""],
                ["\\([\\w+, !\\?]+\\)", ""],
                ["\\.+\\?", ""],
                ['"', ""],
                ["\\b\\w+n't\\b", "not"],
                [" ?-- ?", " "],
                [" \\.", "."],
                [" ,", ","],
                ["  ", " "],
                ["^\\d\\. ", ""],
                ["[A-Z]+\\$", "$"],
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
            stopword_pattern = [
                "\\b" + pattern + "'s\\b" for pattern in stopword_pattern
            ]
            stopword_pattern += [
                "\\b\\w+'ll\\b",
                "\\b(([Yy]ou)|([Tt]hey)|([Ww]e))('(r|v)e)?\\b",
                "\\b[Uu]s\\b",
                "\\b[Tt]hem((self)|(selves))?\\b",
                "\\b[Ii](t((self)|(selves))?|'((ve)|m))\\b",
                "\\bme\\b",
                " (\\[\\])|(\\(\\))",
            ]
            for pattern in stopword_pattern:
                text = re.sub(pattern, "", text)

            text = text.replace("  ", " ")

            specific_patterns = [
                ["A\\.[Oo]\\.", "AO"],
                ["P/E", "price-to-earning"],
                ["U\\.S\\.", "United States"],
                ["[Nn]o\\.", "number"],
            ]
            for pattern in specific_patterns:
                text = re.sub(pattern[0], pattern[1], text)

            return text.strip()
        except Exception as e:
            print(e)
            return None

    def _sentence_segmentor(self, text: str) -> list:
        # init
        segmented = []

        # core
        segmented += [sentence.text.strip() for sentence in self.nlp(text).sents]

        return segmented

    def _post_cleanse_text(self, text: str) -> str:
        # core
        generic_patterns = [
            ["^: ", ""],
            [".+\\?", ""],
            [".+vs\\..+", ""],
            [".*[Ll]et's.*", ""],
        ]
        for pattern in generic_patterns:
            text = re.sub(pattern[0], pattern[1], text)

        return text

    def _lemmatise_sentence(self, text: str) -> str:
        # core
        generic_patterns = [["\\.$", ""], [",", ""]]
        for pattern in generic_patterns:
            text = re.sub(pattern[0], pattern[1], text)

        text = self.nlp(text)
        text = " ".join([token.lemma_ for token in text])

        generic_patterns = [
            [" \\.", "."],
            [" 's", "'s"],
            [" '", ""],
            ["' ", " "],
            ["\\$ ", "$"],
            [" %", "%"],
            [" ;", ";"],
            [" :", ":"],
            [":$", ""],
            ["\\( ", "("],
            [" \\)", ")"],
            [" - ", "-"],
            ["  ", " "],
        ]

        for pattern in generic_patterns:
            text = re.sub(pattern[0], pattern[1], text)

        return text.strip()

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
        paragraphed_text = list(filter(None, paragraphed_text))

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

        # core: process unannotated data
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
        paragraphed_text = list(filter(None, paragraphed_text))

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
            newly_annotated.append([sentence, ""])

        annotated_data += newly_annotated

        # final
        save_success = self._save(save_file, newly_annotated)
        if save_success:
            print("Export Successful")

    def _multi_annotate(self, sentences: List[str], classifier) -> List[Tuple[str]]:
        # 1: pos, 2: neu, 3: neg
        annotated = []
        for i in trange(len(sentences)):
            annotated.append(
                tuple((sentences[i], int(classifier.classify(sentences[i]))))
            )
        return annotated

    def automatic_annotation(self, articles: List[str], save_file: str):
        # init: load saved annotated data
        load_success, annotated_data = self._load(save_file)
        if load_success:
            print("Import Successful")

        annotated_data = [tuple((datum[0], datum[1])) for datum in annotated_data]

        # core: process unannotated data
        # 1: Basic Paragraphing
        # 2: Pre Cleanse Text
        # 3: Segment into Sentences via NLP
        # 4: Post Cleanse Text
        # 5: Lemmatise Text
        # 6: Multi-Process Annotate Text

        # 1
        paragraphed_text = []
        for article in articles:
            paragraphed_text += self._paragrapher(article)

        # 2
        paragraphed_text = [
            self._pre_cleanse_text(paragraph) for paragraph in paragraphed_text
        ]
        paragraphed_text = list(filter(None, paragraphed_text))

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
        num_threads = mp.cpu_count() - 2
        p = mp.Pool(processes=num_threads)

        classifier = NaiveBayesClassifier(annotated_data)

        zipped_model = []
        zipped_data = []
        slices = list(gen_even_slices(len(segmented_text), num_threads))

        for s in slices:
            zipped_data.append(segmented_text[s])
            zipped_model.append(classifier)

        data = p.starmap(self._multi_annotate, zip(zipped_data, zipped_model))

        annotated = []
        for dataset in data:
            annotated += dataset

        if data:
            annotated_data += annotated

        save_success = self._save(save_file, annotated_data)
        if save_success:
            print("Export Successful")
