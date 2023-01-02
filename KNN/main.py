import numpy as np
from numpy.linalg import norm


def euclidean_distance(a, b):
    a, b = np.array(a), np.array(b)  # można założyć poprawny typ na wejściu
    return np.sqrt(sum((a - b)**2))


def manhattan_distance(a, b):
    return sum(abs(value1-value2) for value1, value2 in zip(a,b))  # nie dałoby się uniknąć tej pętli?


def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))  # 1-


def max_distance(a,b):
    return max(abs(value1-value2) for value1, value2 in zip(a,b))


def train(train_set, test_instance, k, distance_function):  # a jak wywołać to wielokrotnie  # czym jest test_instance?
    distances = []
    for train_instance in train_set:
        distances.append((train_instance, distance_function(test_instance, train_instance)))
    distances.sort(key=lambda x: x[1])
    knn = []
    for i in range(k):
        knn.append(distances[i][0])
    return knn


def predict(train_set, test_set, k, distance_function):
    prediction = []
    for test_instance in test_set:
        knn = train(train_set, test_instance, k, distance_function)
        result = [row[-1] for row in knn]
        prediction.append(max(set(result), key=result.count))
    return prediction


if __name__ == '__main__':
    train_set = [[2.7, 2.5, 0],
               [1.4, 2.2, 0],
               [3.3, 4.4, 0],
               [1.3, 1.8, 0],
               [3.06, 3, 0],
               [7, 2.7, 1],
               [5.3, 2.0, 1],
               [6.8, 1.3, 1],
               [8.6, -1, 1],
               [7, 3.5, 1],
                [3.9, 2.5, 0],
                [1.8, 2.5, 0],
                [1.7, 3.5, 0]]

    test_set = [[3, 2, 0],
               [1.9, 4, 0],
               [8.3, 7.4, 1],
               [5.3, 5.8, 1]]

    predictions = predict(train_set, test_set, 3, manhattan_distance)
    predictions2 = predict(train_set, test_set, 5, manhattan_distance)
    predictions3 = predict(train_set, test_set, 10, manhattan_distance)
    for i in range(len(test_set)):
        print('Number of neighbours: %d, expected value: %d, result: %d.' % (3, test_set[i][-1], predictions[i]))
        print('Number of neighbours: %d, expected value: %d, result: %d.' % (5, test_set[i][-1], predictions2[i]))
        print('Number of neighbours: %d, expected value: %d, result: %d.' % (10, test_set[i][-1], predictions3[i]))


