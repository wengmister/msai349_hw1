from node import Node
import math
import parse

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  pass

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  pass

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  pass

def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  pass


def calculate_entropy(labels):
    """
    Calculate the entropy of a set of labels without using Counter.
    """
    # Total number of labels
    total_count = len(labels)
    
    # Get the unique labels
    unique_labels = set(labels)
    
    # Calculate the entropy
    entropy = 0.0
    for label in unique_labels:
        count = labels.count(label)
        p_i = count / total_count
        entropy -= p_i * math.log2(p_i)
    
    return entropy


def main():
  tennis_data = parse.parse("tennis.data")
  print(tennis_data)
  print(len(tennis_data))


if __name__ == "__main__":
  main()