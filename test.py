import math
from ID3 import *
import parse

data = parse.parse("tennis.data")
result = ID3(data, 0)
result.print_tree()

tes = 0

for line in data:
   if (not evaluate(result,line) == line["Class"]):
      evaluate(result,line) == line["Class"]
   tes += 1 if evaluate(result, line) == line["Class"] else 0

print(f"acc : {100.0*tes/len(data)}")

#my_line = {'Outlook': '0', 'Temperature': '1', 'Humidity': '0', 'Wind': '0'}

#print(evaluate(result,my_line))