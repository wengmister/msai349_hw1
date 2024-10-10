from node import Node
import math
import parse
from seperate import *

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"

  default - Default class
  '''
  classes = [row['Class'] for row in examples]
  if classes.count(classes[0]) == len(classes):
      return Node(label=classes[0], is_leaf=True)

  # Step 2: If no attributes are left to split, return a leaf node with the majority class
  if len(attributes) == 0:
      majority_class = max(set(classes), key=classes.count)
      return Node(label=majority_class, is_leaf=True)

  # Step 3: Find the best attribute to split on (we'll use information gain)
  best_attribute = choose_best_attribute(data, attributes)
  root = Node(attribute=best_attribute)

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


def information_gain(h0, h1):
  return h0 - h1


def main():
  tennis_data = parse.parse("tennis.data")
  print(tennis_data)
  print(len(tennis_data))


if __name__ == "__main__":
  main()