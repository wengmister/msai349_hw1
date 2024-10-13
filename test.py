import math
from ID3 import *
import parse

tennis_data = parse.parse("mushroom.data")
result = ID3(tennis_data, 0)
result.print_tree()
#evaluate(result,tennis_data[0])