from collections import Counter
import string
import re

def generate_tokens(file):
    with open(file) as opened_file:
        for line in opened_file:
            tokens = line.split()
            for token in tokens:
                yield token


def n_most_popular_words(n, filename):
    word_list = []
    most_popular_words = []
    punctuation = ["?", ",", ";", "!", ".", "-",":"]

    # punctuation is not included
    for token in generate_tokens(filename):
        if token not in punctuation:
            new_token = re.sub(r'[^\w\s]', '', token)
            # token = token.translate(str.maketrans('', '', string.punctuation))
            word_list.append(new_token.lower())

    # each word with number of occurrence in text
    word_count = Counter(word_list)

    # if given n is bigger than number of unique words
    # then n is changed to amount of all unique words
    if n > len(word_count):
        n = len(word_count)

    for i in range(n):
        most_popular_words.append(word_count.most_common()[i])

    #check if n is not too big - index out of range error
    if n < len(word_count):
        i = n - 1
        while True:
            # check if (n + 1)th word is in the text same number of times as nth word
            if word_count.most_common()[i][1] == word_count.most_common()[i + 1][1]:
                most_popular_words.append(word_count.most_common()[i + 1])
                i += 1
                # check if i is not too big - index out of range error
                if i == len(word_count) - 1:
                    break
            else:
                break

    return most_popular_words


if __name__ == "__main__":
    filename = "potop.txt"

    print(n_most_popular_words(198, filename))
    print("Number of words printed: " + str(len(n_most_popular_words(198, filename))))
    print("198th most popular word was in the book same number of times as 199th word, that is way array is longer")
