# Tuple- collection of immutable ordered heterogenous- items

from typing import Tuple
from collections import namedtuple


t1:Tuple = ('a',10,True)
t2:Tuple = 'b',

print(t1,type(t1))
print(t2,type(t2))


def iterable_items(t:Tuple):
    for ele in t:
        print(ele,end="\t")
    print()

iterable_items(t1)


print(f"1st element::{t1[0]}")

# unpack
u1,*_ = t1
print(f"unpack element 1st::{u1}")
print(f"unpack rest all ele:{_}")

t1 = t1 + (1,3,5)
print(t1)


class Pnt2D:
    def __init__(self,x:int,y:int) -> None:
        self.x = x
        self.y = y
    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(x={self.x},y={self.y})"
    
    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(x={self.x},y={self.y})"
    

a:Tuple = Pnt2D(0,0), Pnt2D(10,10), Pnt2D(20,20)
# we can represent as 
# a:Tuple  = (0,0), (10,10), (20,20)
# >> but we don't know what it represent

try:
    a[0] = 10
except Exception as e:
    print(e.__class__)


a[0].x=-10  # now it's element changeable/modifiable
print(a)
        


# Named Tuples
# inherits from tuple

Point3D = namedtuple('Point3D',('a','b','c'))
# best practise to keep both name as same.

pt1 = Point3D(0,0,0)
pt2 = Point3D(10,10,10)

print(Point3D,type(Point3D))  #type(Point3D)=type ??
print(pt1,type(pt1))
print(isinstance(pt1,tuple))

# it's possible in named_tuple
print(pt1==(0,0,0))


# Using Tuple
u = (1,2,3)
v = (10,20,30)
print(list(zip(u,v)))
print([e[0]+e[1] for e in zip(u,v)] )
print(sum([e[0]+e[1] for e in zip(u,v)] ))

# Using Named Tuple
print(list(zip(pt1,pt2)))
print([e[0]+e[1] for e in zip(pt1,pt2)] )
print(sum([e[0]+e[1] for e in zip(pt1,pt2)] ))


# Usage:
print(f"{pt1.a}")  # accessible by name



print(Point3D._fields)
print(pt1._field_defaults)
print(pt1._asdict())

try:
    # same property as tuple
    pt1.a = -10
except Exception as e:
    print(e.__class__)

# way to do it
pt1= pt1._replace(a=-10)
print(pt1)
print("doc string:: ",Point3D.__doc__)


# getattr
print(getattr(pt1,'a','Nothing here'))
print(getattr(pt1,'x','Nothing here'))