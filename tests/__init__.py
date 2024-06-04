import os
import sys

cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, "CHARGER"))
sys.path.insert(0, os.path.join(cwd, "VEHICLE"))

print(os.getcwd())
print(sys.path)
