#!/usr/bin/env python3

from data_generator import generate_usernames
import utilities as util
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from word_score import generate_username_scores
import sys

""" NiceName
A python package for detecting offensive usernames.

Note: Usernames are assumed to be 25 charaters max and consist of alphanumeric characters and symbols on a keyboard (no spaces).

Authors: Harrison Whitner, Jeremy Howe
Creation Date: 11/28/20
"""


""" CONSTANTS """

TRAINING_SET_FILENAME = 'data/generated/training_set.txt'
TESTING_SET_FILENAME = 'data/generated/testing_set.txt'


""" FUNCTIONS """


def generate_data_set(n_samples: int, file_name, percent_offensive=0.5, percent_obfuscated=0.5, debug=False):
    """Create data which the KNN used to predict usernames is fit upon."""

    generate_usernames("./data/generated/training_usernames.txt", n_samples, percent_offensive, percent_obfuscated)
    username_array = util.file_to_array("./data/generated/training_usernames.txt")

    with open(file_name, 'w') as output_file:

        for entry in username_array:

                label, username = entry.split('\t')

                jaro, lev, comparison = generate_username_scores(username)

                output_file.write(username + ' ' + str(jaro) + ' ' + str(lev) + ' ' + str(comparison) + " " + str(label) + '\n')


def predict_username_is_offensive(username: str, model, debug=False) -> bool:
    """Given a username, predict whether it is offensive or inoffensive using a KNN fitted on generated usernames."""
    
    test_features = [generate_username_scores(username)]
    test_target = model.predict(test_features)

    #0 -> inoffensive, 1 -> offensive
    print('The username', username, 'is predicted to be', 'offensive' if test_target[0] else 'inoffensive')
    result = test_target[0]

    return bool(result)

def train_model(model):
    training_data = util.file_to_array(TRAINING_SET_FILENAME)
    features = []
    targets = []

    for row in training_data:
        curName, jaro, lev, comparison, label = row.split()
        features.append([float(jaro), float(lev), float(comparison)])
        targets.append(int(label))

    model.fit(features, targets)
    
def calculate_accuracy(model):

    training_data = util.file_to_array(TESTING_SET_FILENAME)
    features = []
    true_targets = []

    for row in training_data:
        name, jaro, lev, comparison, label = row.split()
        features.append([float(jaro), float(lev), float(comparison)])
        true_targets.append(int(label))

    pred_targets = model.predict(features)
    print(classification_report(true_targets, pred_targets, target_names=['inoffensive', 'offensive']))
    cm = confusion_matrix(true_targets, pred_targets)
    print('confusion matrix:')
    print(f'TN: {cm[0][0]:3} FN: {cm[1][0]:3}')
    print(f'FP: {cm[0][1]:3} TP: {cm[1][1]:3}')

def main():
    generate_data_set(1000, TRAINING_SET_FILENAME, 0.5, 0.5)
    generate_data_set(100, TESTING_SET_FILENAME, 0.5, 0.5)
    knn_model = KNeighborsClassifier(10, weights='distance')
    train_model(knn_model)
    if '-a' in sys.argv or '--accuracy' in sys.argv:
        calculate_accuracy(knn_model)
    else:
        while True:
            predict_username_is_offensive(input('enter a username to score: '), knn_model)

if __name__ == "__main__":
    main()
