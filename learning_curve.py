import ID3
from random import sample
import numpy as np

def get_learning_curve_data(examples_sizes,test_data,prune = False,default = 0):
    '''
    examples_sizes (np.array) - a range of the example sizes
    test_data (dictionary) - The test data to test on.
    '''

    #initialize an accuray value list
    acc_values = []
    for size in examples_sizes:
        #Get a random sample of ${size} examples
        this_examples = sample(test_data,size)
        #Train the tree
        this_tree = ID3.ID3(this_examples,default=default)
        acc_values.append(ID3.test(node= this_examples,examples=test_data))
    
    return np.array(acc_values)
