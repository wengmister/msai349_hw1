from node import Node
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
  best_attribute, info_gain = find_best_attribute_to_split_on(examples, unique_class)
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
      child = ID3(new_data, default=default)
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
  num_success_prediction = 0
  num_prediction = 0
  for example in examples:
    gt = example['Class']
    predict = evaluate(node, example)
    if(gt == predict):
      num_success_prediction += 1
    num_prediction += 1
  accuracy = num_success_prediction / num_prediction
  return accuracy


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
  training_data = parse.parse("cars_train.data")
  print(calculate_entropy(training_data, 2))

  print("Training...")
  result = ID3(training_data, default="0")
  print("Trained a decision tree:")
  result.print_tree()
  print("")

  print("Testing...")
  testing_data = parse.parse("cars_train.data")
  accuracy = test(result, testing_data)
  print("Accuracy: "+str(accuracy))

if __name__ == "__main__":
  main()