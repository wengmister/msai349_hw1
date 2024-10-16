import ID3
from random import sample
import numpy as np
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
        if (prune):
            this_tree = ID3.prune(this_tree,this_examples)
        acc_values.append(ID3.test(node= this_tree,examples=test_data))
    
    return np.array(acc_values)

def plot_learning_curve(example_sizes, acc_values):

    plt.plot(example_sizes,acc_values*100, label = 'Training data')
    plt.xlabel("Number of examples")
    plt.ylabel("Training accuracy [%]")
    
    plt.grid()
    plt.show()
    