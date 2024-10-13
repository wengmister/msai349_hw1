from node import Node
import math
import parse
from separate import *

def ID3(examples: list, default = 0):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"

  default - Default class
  '''
  classes = [row['Class'] for row in examples]

  #Check homogeneity
  if classes.count(classes[0]) == len(classes):
      return Node(label=classes[0],value = classes[0] ,is_leaf=True)
  
  #Get a list of attributes
  attributes = list(examples[0].keys())[:-1] #exclude the last one, which is the class

  # If no attributes are left, return a leaf node with the majority class
  if len(attributes) == 0:
      majority_class = max(set(classes), key=classes.count)
      return Node(label=majority_class, is_leaf=True)

  # Find the best attribute to split on (we'll use information gain)
  best_attribute = find_best_attribute_to_split_on(examples)
  #If there is none, return the default one
  if (best_attribute == ""):
     return Node(value=default,is_leaf=True)
  root = Node(attribute=best_attribute)

  # For each value of the best attribute, create a subtree
  attribute_values = set(row[best_attribute] for row in examples)

  for value in attribute_values:
      subset = [row for row in examples if row[best_attribute] == value]
      
      # Remove the used attribute and recursively build child nodes
      new_data = remove_best_att_from_data(subset, best_attribute)
      child = ID3(new_data)
      child.value = value
      # Add the child node to the root
      root.add_child(child)

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

  if (node.is_leaf):
     return node.label
  
  attribute_value = example[node.attribute]

  # Find the child node that corresponds to this attribute value
  for child in node.children:
      if (child.value == attribute_value):
          return evaluate(child, example) 
  


def main():
  tennis_data = parse.parse("mushroom.data")
  print(tennis_data)
  print(len(tennis_data))
  result = ID3(tennis_data, 0)
  print(result)

if __name__ == "__main__":
  main()