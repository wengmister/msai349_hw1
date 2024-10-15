import math
from ID3 import *
import parse

train = parse.parse("cars_train.data")
test_ = parse.parse("cars_test.data")
result = ID3(train, "unacc")
result.print_tree()

acc = test(node = result, examples=test_)

print(f"acc : {100.0*acc:.2f}%")

#my_line = {'Outlook': '0', 'Temperature': '1', 'Humidity': '0', 'Wind': '0'}

#print(evaluate(result,my_line))