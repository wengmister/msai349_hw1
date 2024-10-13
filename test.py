import math
from ID3 import *
import parse

train = parse.parse("cars_train.data")
test_ = parse.parse("cars_test.data")
result = ID3(train, "unacc")
result.print_tree()

tes = 0

for line in test_:
   if (not evaluate(result,line) == line["Class"]):
      evaluate(result,line) == line["Class"]
   tes += 1 if evaluate(result, line) == line["Class"] else 0

print(f"acc : {100.0*tes/len(test_)}")

#my_line = {'Outlook': '0', 'Temperature': '1', 'Humidity': '0', 'Wind': '0'}

#print(evaluate(result,my_line))