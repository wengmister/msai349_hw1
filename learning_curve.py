import ID3
from random import sample
import numpy as np
import parse
from matplotlib import pyplot as plt

def get_learning_curve_data(examples_sizes,train_data,test_data,prune = False,default = 0):
    '''
    examples_sizes (np.array) - a range of the example sizes
    test_data (dictionary) - The test data to test on.
    '''

    #initialize an accuray value list
    acc_values = []
    for size in examples_sizes:
        #Get a random sample of ${size} examples
        this_examples = sample(train_data,size)
        #Train the tree
        this_tree = ID3.ID3(this_examples,default=default)
        acc_values.append(ID3.test(node= this_tree,examples=test_data))
    
    return np.array(acc_values)

def plot_learning_curve(example_sizes, acc_values):

    plt.plot(example_sizes,acc_values*100)
    plt.xlabel("Number of examples")
    plt.xlabel("Trainng accuracy [%]")
    plt.grid()
    plt.show()
    

example_size = np.arange(10,32,1)
test_data = parse.parse("cars_test.data")
train_data = parse.parse("cars_train.data")

learn_curve = get_learning_curve_data(examples_sizes=example_size,train_data=train_data,test_data=test_data,default = "unacc")

plot_learning_curve(example_size,learn_curve)