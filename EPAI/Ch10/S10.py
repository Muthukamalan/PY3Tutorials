from typing import List,Set,Optional,Dict,Iterator
import os 
import math
import itertools
import pandas as pd 
from collections import namedtuple


squares:List = []
for i in range(1,11):
    squares.append(i**2)
print(squares)

squares:List = [i**2 for i in range(1,11)]
print(squares)


old_squares:List = [i**2 for i in range(1,11) if i%2!=0]

even_squares:List = [
                        i**2 
                        for i in range(1,11) 
                        if i%2==0
                    ]


# Iterables
## implements __iter__ and __next__

s:Set = {'a','b','c','d','e','f'} 
print(f"'__getitem__' in dir(set):: {'__getitem__' in dir(set)}")
print(f"'__iter__' in dir(set):: {'__iter__' in dir(set)}")

print([item for item in s]) ## iter but not ordered

try:
    print(s[0])
except Exception as e:
    print(f'trying to access index based element on set:: {e.__class__}')



class Squares:
    def __init__(self,length:int) -> None:
        self.length = length
        self.i=0
    def __next__(self):
        print('calling __next__')
        if self.i >=self.length:
            raise StopIteration
        else:
            res = self.i**2
            self.i+=1
            return res 
    def __len__(self):
        return self.length
    

sq = Squares(10)
for i in range(11):
    try:
        print(next(sq),end="\t")
    except Exception as e:
        print(f"exhauste and {e.__class__}")


sq = Squares(10)
try:
    for i in sq: 
        print(i)
except Exception as e:
    print(f"not iterable with :: {e.__class__}")



class Squares:
    def __init__(self,length:int) -> None:
        self.length = length
        self.i=0
    
    ########### code change ###
    def __iter__(self):
        print('calling __iter__')
        return self
    ############################

    def __next__(self):
        print('calling __next__')
        if self.i >=self.length:
            raise StopIteration
        else:
            res = self.i**2
            self.i+=1
            return res 
    def __len__(self):
        return self.length
    
sq = Squares(10)
try:
    for i in sq: 
        print(i,end=",")
    print()
except Exception as e:
    print(f"not iterable with :: {e.__class__}")

try:
    print(next(iter(sq)))
except Exception as e:
    print("after for loop please re-init, this is exhaust!! {}".format(e.__class__))



# Sepeating DATA and ITERATOR
print("#"*70)
class IterCities:
    def __init__(self,obj) -> None:
        print('calling Itercities __init__')
        self.__obj = obj
        self.idx   = 0
    def __iter__(self)->'IterCities':
        print("calling Itercities instance __iter__")
        return self
    def __next__(self):
        print('calling Itercities instance __next__')
        if self.idx >= len(self.__obj):
            raise StopIteration
        else:
            item = self.__obj._places[self.idx]
            self.idx+=1
            return item
    
class Cities:
    def __init__(self) -> None:
        self._places = ['Kovilpatti','Chennai',"Bangalore"]
    def __len__(self)->int:
        return len(self._places)
    def __iter__(self)-> 'IterCities':
        print("calling cities instance __iter__")
        return IterCities(self)
    

my_city  = Cities()
for c in my_city:
    print(c,end="\t")

try:
    my_city[0]
except Exception as e:
    print(f"try to access index of city:: {e.__class__}")
print("#"*70)







class Cities:
    '''
            __iter__  -> address -> iterator_address -> __next__
    '''
    def __init__(self) -> None:
        self._places = ['Kovilpatti','Chennai',"Bangalore"]
    def __len__(self)->int:
        return len(self._places)
    def __getitem__(self,idx)->str:
        return self._places[idx]
    def __iter__(self)-> 'IterCities':
        print("calling cities instance __iter__")
        return self.IterCities(self)
    
    class IterCities:
        def __init__(self,obj) -> None:
            print('calling Itercities __init__')
            self.__obj = obj
            self.idx   = 0
        def __iter__(self)->'IterCities':
            print("calling Itercities instance __iter__")
            return self
        def __next__(self):
            print('calling Itercities instance __next__')
            if self.idx >= len(self.__obj):
                raise StopIteration
            else:
                item = self.__obj._places[self.idx]
                self.idx+=1
                return item

my_city  = Cities()
iter1  = iter(my_city)
iter2  = iter(my_city)
print(f"city:: {next(iter1)}")
print(f"city:: {my_city[0]}")
print(f"id: iter1::{id(iter1)}", f"id: iter2::{id(iter2)}")

print("#"*70)


# APPROACH: ONE
with open(os.path.join('assets','cars.csv'),mode='r') as f:
    csv:List = []
    for line in f.readlines():
        row:List = []
        for cell in line.split(";"):
            row.append(cell.strip())
        csv.append(row)
df = pd.DataFrame(csv)
print(df)


# APPROACH: TWO
def cast_fn(data_type,val)->Optional[int|str|float]:
    if data_type=='DOUBLE':
        return float(val)
    elif data_type=='INT':
        return int(val)
    else:
        return str(val)
    
def cast_row_fn(data_type,data_row)->List:
    return [ cast_fn(data_type,data_row) for data_type, data_row in zip(data_type,data_row) ]


with open(os.path.join('assets','cars.csv'),mode='r') as f:
    cars:List = []
    row_index:int = 0
    for line in f:
        if row_index==0:
            headers = line.strip('\n').split(';')
            Car = namedtuple('Car',headers)
        elif row_index==1:
            data_types = line.strip('\n').split(';')
        else:
            data = line.strip('\n').split(';')
            data = cast_row_fn(data_types,data)
            car = Car(*data)
            cars.append(car)
        row_index+=1

print(cars[10])
print(next(iter(cars)))


# APPROACH: THREE
with open(os.path.join('assets','cars.csv'),mode='r') as f:
    iter_file:Iterator  = iter(f)
    headers:List    = next(iter_file).strip('\n').split(';')
    Car = namedtuple('Car',headers)

    data_types:List = next(iter_file).strip('\n').split(';')
    cars_data:List  = [cast_row_fn(data_types, line.strip('\n').split(';')) for line in iter_file]
    cars = [Car(*item) for item in cars_data]

print(cars[100])


# Cyclic Iterators
'''
1,2,3,4,5,6,7,8,9,10
N,S,W,E 
1N,2S,3W,4E,5N,6S,7W,8E,9N,10S
'''
class CyclicIterator:
    def __init__(self,lst:List) -> None:
        self.lst:List  = lst 
        self.i:int     = 0
    def __iter__(self):
        return self
    def __next__(self):
        result = self.lst[self.i % len(self.lst)]
        self.i += 1
        return result
    
iter_cycl:Iterator = CyclicIterator("NSWE")
print([f"{idx}::{next(iter_cycl)}" for idx,i in enumerate(range(10),start=1)])
print( list( zip( range(1,11), 'NSWE'*(10//4 + 1)  ) ) )


iter_cycl:Iterator = itertools.cycle("NSWE")
print([f"{idx}::{next(iter_cycl)}" for idx,i in enumerate(range(10),start=1)])




#TODO: Next Class
# Yield and Generator
# lazy iterable
# inbuild
# sorting
# iterable with self + next + next-after (pre-created)


# lazy class calaculating area after we requested
class Circle:
    def __init__(self, r):
        self.radius = r
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, r):
        self._radius = r
    @property
    def area(self):
        print("calculating")
        return math.pi * self.radius ** 2
    

class LazyCircle:
    def __init__(self, r):
        self.radius = r
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, r):
        self._radius = r
        self._area = None
    @property
    def area(self):
        if self._area is None:
            print('Calculating area...')
            self._area = math.pi * self.radius ** 2
        return self._area


