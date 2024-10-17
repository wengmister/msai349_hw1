from node import Node
import parse
from separate import *
from ID3 import test, ID3, evaluate
import random
import copy

# Constants
LEARNING_DATA_RATIO = 0.6
NUM_TREES = 200
NUM_COMPARE_TEST = 15
RANDOM_SAMPLE_ATTRIBUTES_RATIO = 0.9


def random_wash_data(data):
    """
    Randomly change the order of data 
    """
    copied_data = copy.deepcopy(data)
    random.shuffle(copied_data)
    return copied_data


def random_subset(data, size):
    """
    Randomly select a subset of the data.
    """
    copied_data = copy.deepcopy(data)
    return random.choices(copied_data, k=size)


def test_forest(trees, examples):
    """
    Evaluates the accuracy of the entire forest by using majority voting among the individual trees.
    """
    num_success_prediction = 0
    for example in examples:
        predicted_class = evaluate_forest(trees, example)
        if predicted_class == example['Class']:
            num_success_prediction += 1
    accuracy = num_success_prediction / len(examples)
    return accuracy


def evaluate_forest(trees, example):
    """
    Predicts the class for an example by majority voting among all trees.
    """
    votes = []
    for tree in trees:
        votes.append(evaluate(tree, example))
    return max(set(votes), key=votes.count)


def main_candy():
    # Load data
    data = parse.parse("candy.data")

    # Record average accuracy for random forest and ID3
    average_random_forest_accuracy = 0
    average_ID3_accuracy = 0

    # Compare the accuracy of random forest and ID3
    for i in range(NUM_COMPARE_TEST):
        washed_data = random_wash_data(data)
        size = len(washed_data)

        # Split data into training and testing sets
        training_data = washed_data[:int(size*LEARNING_DATA_RATIO)]
        testing_data = washed_data[int(size*LEARNING_DATA_RATIO):]

        # Train multiple trees
        trees = []
        for i in range(NUM_TREES):
            # Train a tree
            # Bagging (Randomly select a subset of the data)
            training_data_after_bagging = random_subset(training_data, int(len(training_data)))
            tree = ID3(training_data_after_bagging, default="0", attributes_random_sample_ratio=RANDOM_SAMPLE_ATTRIBUTES_RATIO)
            trees.append(tree)

        # Test the random forest trees
        random_forest_accuracy = test_forest(trees, testing_data)

        # Train a single ID3 tree
        ID3_tree = ID3(training_data, default="0")
        ID3_accuracy = test(ID3_tree, testing_data)

        average_random_forest_accuracy += random_forest_accuracy
        average_ID3_accuracy += ID3_accuracy

    # Print the results
    average_random_forest_accuracy /= NUM_COMPARE_TEST
    average_ID3_accuracy /= NUM_COMPARE_TEST
    print(f"Random Forest Average Accuracy: {round(average_random_forest_accuracy, 2)}, ID3 Average Accuracy: {round(average_ID3_accuracy, 2)} \n")


def main_cars():
    # Load data
    training_data = parse.parse("cars_train.data")
    testing_data = parse.parse("cars_test.data")

    # Record average accuracy for random forest and ID3
    average_random_forest_accuracy = 0
    average_ID3_accuracy = 0

    # Compare the accuracy of random forest and ID3
    for i in range(NUM_COMPARE_TEST):
        # Train multiple trees
        trees = []
        for i in range(NUM_TREES):
            # Train a tree
            # Bagging (Randomly select a subset of the data)
            training_data_after_bagging = random_subset(training_data, int(len(training_data)))
            tree = ID3(training_data_after_bagging, default="0", attributes_random_sample_ratio=RANDOM_SAMPLE_ATTRIBUTES_RATIO)
            trees.append(tree)

        # Test the random forest trees
        random_forest_accuracy = test_forest(trees, testing_data)

        # Train a single ID3 tree
        ID3_tree = ID3(training_data, default="0")
        ID3_accuracy = test(ID3_tree, testing_data)

        average_random_forest_accuracy += random_forest_accuracy
        average_ID3_accuracy += ID3_accuracy

    # Print the results
    average_random_forest_accuracy /= NUM_COMPARE_TEST
    average_ID3_accuracy /= NUM_COMPARE_TEST
    print(f"Random Forest Average Accuracy: {round(average_random_forest_accuracy, 2)}, ID3 Average Accuracy: {round(average_ID3_accuracy, 2)}")


if __name__ == "__main__":
    print(f"Training and Testing Random Forest and ID3 on candy.data.")
    print(f"Spliting ratio for training set and testing set: {LEARNING_DATA_RATIO}")
    print(f"Number of trees in the random forest: {NUM_TREES}")
    print(f"Number of experiments conducted to test the average accuracy: {NUM_COMPARE_TEST}")
    main_candy()

    print(f"Training and Testing Random Forest and ID3 on cars_training.data.")
    print(f"Number of trees in the random forest: {NUM_TREES}")
    print(f"Number of experiments conducted to test the average accuracy: {NUM_COMPARE_TEST}")
    main_cars()