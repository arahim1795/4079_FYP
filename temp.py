# def split_dataset():

#     data = json.load(open("./data/annotated.json", "r"))
#     cutoff_index = int(0.7 * len(data))
#     print(cutoff_index)
#     numpy.random.shuffle(data)

#     print(data)

#     with open("./data/train.json", "w") as file:
#         json.dump(data[:cutoff_index], file, indent=2)

#     with open("./data/test.json", "w") as file:
#         json.dump(data[cutoff_index:], file, indent=2)

# split_dataset()

# for i in range(66, 67):
#     annotator.automatic_annotation(articles[i], "auto_annotated", "auto")


# c1 = NaiveBayesClassifier(train)
# dist = c1.prob_classify("GM closest high bang")

# print("pos:")
# print(round(dist.prob("pos"), 2))
# print("\n")
# print("neutral:")
# print(round(dist.prob("neu"), 2))


# # print(sentences)

# # list_of_sentence = list(doc.sents)

# # print(len(list_of_sentence))
# # print(list_of_sentence)

# # for sen in list_of_sentence:
# #     sentiment = TextBlob(str(sen))
# #     print(sentiment.sentiment)


# # # check for type
# # ls = [type(item) for item in tokens_str]
# # print(ls)