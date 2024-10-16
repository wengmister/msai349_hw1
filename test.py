import math
from ID3 import *
import parse

train = parse.parse("house_votes_84.data")[:-200]
test_ = parse.parse("house_votes_84.data")[-201:]
print(len(train),len(test_))
result = ID3(train, "democrat")
result.print_tree()

acc = test(node = result, examples=test_)

print(f"acc : {100.0*acc:.2f}%")

#my_line = {'Outlook': '0', 'Temperature': '1', 'Humidity': '0', 'Wind': '0'}

#print(evaluate(result,my_line))