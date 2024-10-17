import math
from ID3 import *
import parse
import tree

train = parse.parse("house_votes_84.data")[:-50]
test_ = parse.parse("house_votes_84.data")[-51:]
valid = test_

# train = parse.parse("cars_train.data")
# test_ = parse.parse("cars_test.data")
# valid = parse.parse("cars_valid.data")

print(len(train),len(test_))
result = ID3(train, "democrat")
result.print_tree()

mushroom_data = parse.parse("mushroom.data")
mush = ID3(mushroom_data, default= "eatable")

acc = test(node = result, examples=valid)

print(f"acc : {100.0*acc:.2f}%")

result.print_tree()
prune(result,valid)

acc = test(node = result, examples=valid)

print(f"acc : {100.0*acc:.2f}%")

result.print_tree()

#my_line = {'Outlook': '0', 'Temperature': '1', 'Humidity': '0', 'Wind': '0'}

#print(evaluate(result,my_line))