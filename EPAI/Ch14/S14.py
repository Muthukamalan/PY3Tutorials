import math 
import types 
from typing import Any
import os
import sys 
from rich import print
from collections import namedtuple
from importlib.util import find_spec
# 
_globals:dict[str,Any] = globals()
print(f"{type(_globals)=},\n"f"{_globals.get('math')=},\n",f"{id(math)=}")

print(math)
print(f"{find_spec('math')=}")
print(sys.modules.get('math'))


print(math.__dict__)

print(f"{math.sqrt is math.__dict__.get('sqrt')=}")

print(f"{isinstance(math,types.ModuleType)=}")

# print(help(types.ModuleType))


# -----------------------------------------------------------
mod = types.ModuleType('mymodule',"My First Module")
# print(help(mod))


mod.Point = namedtuple('Point','x y')
mod.distance = lambda pt1,pt2: math.sqrt((pt1.x - pt2.x)**2 + (pt1.y - pt2.y) ** 2)

print(mod.__dict__)

p1  = mod.Point(0,0)
p2 = mod.Point(1,1)
print(f"{mod.distance(pt1=p1,pt2=p2)=}")

print(f"{sys.path=}")



# --------------------------------------------------------------------
with open('module1.py', 'w') as code_file:
    code_file.write('print("*"*100);print("Hello from module1");print("*"*100);\n')
    code_file.write('a = 100\n')
    code_file.close()
print(f"{find_spec('module1')=}")


external_module_path  = os.environ.get("HOME")
external_module_fpath =  os.path.join(os.path.curdir,'module1.py')

import module1
print(f"{module1.a=}")
print(f"{'module1' in sys.modules=}")



for key in sorted(sys.modules.keys()):
    print(key)


# --------------------------------------------------------
print(f"{'cmath' in sys.modules=}")
from cmath import exp
print(f"{'cmath' in sys.modules=}")
print(f"{'cmath' in globals()=}")
print(f"{'exp' in globals()=}")

