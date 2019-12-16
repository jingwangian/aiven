import os
import sys
from os.path import dirname

print(dirname(dirname(__file__)))
sys.path.insert(0, dirname(dirname(__file__)))

# print("final path:", sys.path)
