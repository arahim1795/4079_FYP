import csv
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer
from tqdm import trange
from typing import List


class Evaluator:
    def __init__(self):
        pass

    def evaluate_0(self, file_to_evaluate: str, classifier):
        data = None
        try:
            with open(
                "./backend/data/self_annotated/" + file_to_evaluate + ".csv", "r"
            ) as csvfile:
                data = list(csv.reader(csvfile))
        except Exception as e:
            print(e)

        custom_values, ground_values, movie_values = [], [], []
        for i in trange(len(data)):
            # sentence
            datum = data[i]

            # values
            # - custom
            ground_values.append(int(datum[1]))

            # - annotate
            custom_values.append(int(classifier.classify(str(datum[0]))))

            blob = TextBlob(datum[0], analyzer=NaiveBayesAnalyzer())
            blob_values = []
            blob_values.append(blob.sentiment.p_pos)
            blob_values.append(blob.sentiment.p_neg)

            if blob_values[0] >= 0.5 and blob_values[1] < 0.5:
                movie_values.append(1)
            elif blob_values[1] >= 0.5 and blob_values[0] < 0.5:
                movie_values.append(3)
            else:
                movie_values.append(2)

        accuracy_custom, precision_custom, recall_custom = self.multi_precision_recall(ground_values, custom_values)
        accuracy_movie, precision_movie, recall_movie = self.multi_precision_recall(ground_values, movie_values)

        with open(
            "./backend/data/self_annotated/evaluation_" + file_to_evaluate + ".csv", "w"
        ) as file:
            file.write("acc_custom, acc_movie\n")
            file.write(f"{accuracy_custom}, {accuracy_movie}\n")
            file.write("pre_custom_1, pre_custom_2, pre_custom_3, pre_movie_1, pre_movie_2, pre_movie_3\n")
            file.write(f"{precision_custom[0]}, {precision_custom[1]}, {precision_custom[2]}, {precision_movie[0]}, {precision_movie[1]}, {precision_movie[2]}\n")
            file.write("rec_custom_1, rec_custom_2, rec_custom_3, rec_movie_1, rec_movie_2, rec_movie_3\n")
            file.write(f"{recall_custom[0]}, {recall_custom[1]}, {recall_custom[2]}, {recall_movie[0]}, {recall_movie[1]}, {recall_movie[2]}")

    def multi_precision_recall(self, ground_values: List[int], predict_values: List[int]):
        # multiclass precision and recall
        entries = len(ground_values)
        predict_positive = [0, 0, 0]
        predict_neutral = [0, 0, 0]
        predict_negative = [0, 0, 0]

        for i in range(entries):
            predict = predict_values[i]
            ground = ground_values[i]

            if predict == ground:
                if predict == 1:
                    predict_positive[0] += 1
                elif predict == 2:
                    predict_neutral[1] += 1
                else:
                    predict_negative[2] += 1
            else:
                if predict == 1:
                    if ground == 2:
                        predict_positive[1] += 1
                    else:
                        predict_positive[2] += 1
                elif predict == 2:
                    if ground == 1:
                        predict_neutral[0] += 1
                    else:
                        predict_neutral[2] += 1
                else:
                    if ground == 1:
                        predict_negative[0] += 1
                    else:
                        predict_negative[1] += 1

        print(predict_positive)
        print(predict_neutral)
        print(predict_negative)

        total_predict = [
            sum(predict_positive),
            sum(predict_neutral),
            sum(predict_negative),
        ]

        total_ground = [
            predict_positive[0] + predict_neutral[0] + predict_negative[0],
            predict_positive[1] + predict_neutral[1] + predict_negative[1],
            predict_positive[2] + predict_neutral[2] + predict_negative[2],
        ]

        print(total_predict)
        print(total_ground)

        accuracy = round((predict_positive[0] + predict_neutral[1] + predict_negative[2]) / entries, 2)
        precision = [-1, -1, -1]
        recall = [-1, -1, -1]

        if total_predict[0] > 0:
            precision[0] = round(predict_positive[0] / total_predict[0], 2)
        if total_predict[1] > 0:
            precision[1] = round(predict_neutral[1] / total_predict[1], 2)
        if total_predict[2] > 0:
            precision[2] = round(predict_negative[2] / total_predict[2], 2)

        if total_ground[0] > 0:
            recall[0] = round(predict_positive[0] / total_ground[0], 2)
        if total_ground[1] > 0:
            recall[1] = round(predict_neutral[1] / total_ground[1], 2)
        if total_ground[2] > 0:
            recall[2] = round(predict_negative[2] / total_ground[2], 2)

        return [accuracy, precision, recall]