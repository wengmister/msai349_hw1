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


def find_best_attribute_to_split_on_random_forest(data, number_of_classes = 2):
    smallest_H = 1
    chosen_att = ""

    #Assume the all of the examples has all of the attributes (even if unkown)
    attribue_list = list(data[0].keys())
    attribue_list.remove("Class")

    # Randomly select a subset of attributes to consider
    subset_size = max(1, int((len(attribue_list) * RANDOM_SAMPLE_ATTRIBUTES_RATIO)))
    attribue_list = random.sample(attribue_list, subset_size)

    if (len(attribue_list) == 1): return attribue_list[0], 0

    current_entropy = calculate_entropy(data, number_of_classes)

    for att in attribue_list:
        
        seg_data = split_data_by_attribute(data,att)

        this_H = 0.0
        for att_type in seg_data.keys():
            this_H += 1.0*calculate_entropy(seg_data[att_type], number_of_classes) * len(seg_data[att_type])/len(data)

        if(this_H < smallest_H):
            smallest_H = this_H
            chosen_att = att
    
    info_gain = current_entropy - smallest_H
    # print(f"Chosen attribute: {chosen_att}, Info Gain: {info_gain}")

    return chosen_att, info_gain


def ID3_random_forest(examples: list, default = 0):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node) 
    trained on the examples.  Each example is a dictionary of attribute:value pairs,
    and the target class variable is a special attribute with the name "Class".
    Any missing attributes are denoted with a value of "?"

    default - Default class
    '''
    # get a list of all the class labels
    classes = []
    for row in examples:
        classes.append(row['Class'])
    unique_class = len(set(classes))

    #Check homogeneity
    if classes.count(classes[0]) == len(classes):
        return Node(label=classes[0], node_info_gain= 0, value = classes[0] ,is_leaf=True)
    
    #Get a list of attributes
    attributes = list(examples[0].keys())

    # Remove the last attribute (class label)
    attributes.remove('Class')

    # If no attributes are left, return a leaf node with the majority class
    if len(attributes) == 0:
        majority_class = max(set(classes), key=classes.count)
        return Node(label=majority_class, node_info_gain=0, is_leaf=True)

    # Find the best attribute to split on (we'll use information gain)
    best_attribute, info_gain = find_best_attribute_to_split_on_random_forest(examples, unique_class)
    #If there is none, return the default one
    if (best_attribute == ""):
        return Node(label=default, node_info_gain = info_gain, is_leaf=True)
    root = Node(attribute=best_attribute, node_info_gain=info_gain)
    # root.print_tree()
    
    # create a set of all possible values for the best attribute to split on
    attribute_values = set()
    for row in examples:
        attribute_values.add(row[best_attribute])

    for value in attribute_values:
        # find matching examples with best attribute = value
        subset = []
        for row in examples:
            if row[best_attribute] == value:
                subset.append(row)

        # Remove the used attribute and recursively build child nodes
        new_data = remove_best_att_from_data(subset, best_attribute)
        child = ID3_random_forest(new_data, default=default)
        child.value = value
        # Add the child node to the root
        root.add_child(child)

    return root


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
            tree = ID3_random_forest(training_data_after_bagging, default="0")
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
            tree = ID3_random_forest(training_data_after_bagging, default="0")
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