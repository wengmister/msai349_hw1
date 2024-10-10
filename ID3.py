from node import Node
import math
import parse
from separate import *

def ID3(examples: dict, default):
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

  attributes = set(examples.keys())

  # If no attributes are left to split, return a leaf node with the majority class
  if len(attributes) == 0:
      majority_class = max(set(classes), key=classes.count)
      return Node(label=majority_class, is_leaf=True)

  # Find the best attribute to split on (we'll use information gain)
  best_attribute = find_best_attribute_to_split_on(examples)
  root = Node(attribute=best_attribute)

  # For each value of the best attribute, create a subtree
  attribute_values = set(row[best_attribute] for row in examples)
  for value in attribute_values:
      subset = [row for row in examples if row[best_attribute] == value]
      
      # Remove the used attribute and recursively build child nodes
      new_attributes = [attr for attr in attributes if attr != best_attribute]
      child = ID3(subset, new_attributes)
      
      # Add the child node to the root
      root.add_child(value, child)

  return root


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


def main():
  tennis_data = parse.parse("tennis.data")
  print(tennis_data)
  print(len(tennis_data))


if __name__ == "__main__":
  main()