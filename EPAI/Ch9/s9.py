from typing import List,Any 

# - Sequence Types

print("hello")

t = (1,2,3)
print(t[0])

# t[0]=10 # not support item assignment IMMUTABLE

t = ([0,1],2,3)
t[0][1]  = 1000
print(t)


t = {1,4j,'Hi'}
for _ in t:
    print(_) 


word:str = "planet"
print(min(word), max(word))  # finding ascii value and returns

words:List[Any] =  ['planets',1,43,54]
try:
    print(min(words), max(words))   # fails here
except TypeError as e:
    print("not comparable for heterogenous list")

# Index is Supports negative value.
print(f"negative index:: {words[::-1]}")




# is items are SEQUENCE
r = range(11)
print(r)  # lazy # object
print(list(r))   # compute happends

# hashable for only immutable sequence.
print(f"hashable: {hash(r)}")


r = (1,0,'python') # r = frozenset([1,2,3,4])
print(f"hashable for immutable objects: {hash(r)}")

r = ([1,2,4],1,0)  #  r = {1,2,3}
try:
    print(hash(r))
except Exception as e:
    print(f"mutable objects are not hashable")



# - Mututable Sequence
l = [1,2,3,4]
print(f"id={id(l)}, l={l}")
l = l + [5]
print(f"id={id(l)}, l={l}")

l.reverse()
print(f"id={id(l)}, l={l}")

l[-1] = [10,11,12,13,14]
print(f"id={id(l)}, l={l}")

l.clear()
print(f"id={id(l)}, l={l}")


# - List Vs Tuples
## Constant Folding
# recoginzing and eval constant experssion at compile Time rather than computing at runtime

from dis import dis 
import sys 

dis(compile(f'(1,2,3,"a")',filename='string',mode='eval'))
dis(compile(f'[1,2,3,"a",5+7j]',filename='string',mode='eval'))

prev = 0 
for i in range(10):
    c = tuple(range(i+1))
    size_c = sys.getsizeof(c)
    delta, prev = size_c - prev, size_c
    print(f"{i+1} items in tuple:: {size_c}, delta={delta}")


prev = 0 
for i in range(10):
    c = list(range(i+1))
    size_c = sys.getsizeof(c)
    delta, prev = size_c - prev, size_c
    print(f"{i+1} items in list:: {size_c}, delta={delta}")


from timeit import timeit
t  = tuple(range(10000000))
l = list(range(10000000))
print(f"time for reterival number in tuple:: {timeit('t[999999]',globals=globals(),number=10000000)}")
print(f"time for reterival number in list:: {timeit('l[999999]',globals=globals(),number=10000000)}")


# shallow vs deep copy 
l1 = [1,2,3,5]
l2 = l1        # l1.copy()
print(f"id l1={id(l1)}, id l2={id(l2)}, l1 is l2: {l2 is l1}")

import copy 
l1 = [1,2,3,5]
l2 = copy.copy(l1)
print(f"id l1={id(l1)}, id l2={id(l2)}, l1 is l2: {l2 is l1}")




# `note`: copy won't work on nested object

l1  = [[1,2,3],[4,5,6]]
l2  = l1.copy()
l3  = copy.deepcopy(l1)
print(f"id l1={id(l1)}, id l2={id(l2)}, l1 is l2: {l2 is l1}")
print(f"id l1={id(l1)}, id l2={id(l3)}, l1 is l2: {l3 is l1}")



l = [0,1,2,3,4,5]
print(f"l[3:0:-1]:: {l[3:0:-1]}")
print(f"l[3::-1]:: {l[3::-1]}")

print(f"l[3:-100:-1]:: {l[3:-100:-1]}")
print(f"l[3:-1:-1]:: {l[3:-1:-1]}")       # weirdo


compiled_code  = compile("[i**2 for i in range(15)]",filename='',mode='eval')
print(compiled_code)
dis(compiled_code)



# list comprehension
dot_generator = (i*j for i,j in zip(range(10,20),range(100,110)))  # generator
print(f"generator of dot object:: {dot_generator}")
print(f"exec dot object:: {sum(dot_generator)}")


print(globals().keys())