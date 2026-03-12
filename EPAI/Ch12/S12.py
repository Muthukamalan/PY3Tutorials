from numbers import Number
import os 
import math 
# aggregator:: range, any, all, sum, min, max
# any
# all

def squares(n):
    for i in range(n):    # range:: aggregator
        yield i**2        # after send result it'll pause and if we call again starts from where it's pauses

def factorials_fn(n:int):
    for i in range(n):
        yield math.factorial(i)


# Iterator
class FactIter:
    def __init__(self,n:int) -> None:
        self.n = n 
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.i>=self.n: raise StopIteration
        else:
            res = math.factorial(self.i)
            self.i +=1
            return res
        

# Previous Class
class Fib:
    def __init__(self,n) -> None:
        self.n = n 
    def __iter__(self):
        return self.FibIter(self.n)
    
    class FibIter:
        def __init__(self,n ) -> None:
            self.n = n 
            self.i = 0 
        def __iter__(self): return self 
        def __next__(self):

            def fib(n):
                fib_0 = 1
                fib_1 = 1 
                for i in range(n-1):
                    fib_0,fib_1 = fib_1, fib_0+fib_1
                return fib_1
            
            if self.i >=self.n: raise StopIteration
            else:
                res = fib(self.i)
                self.i +=1 
                return res

def yield_me():
    # Ist CALL
    print("line1,....")
    yield "Planet"
    # 2nd CALL
    print('line2,....')
    yield "Earth"
    # 3rd CALL
    # StopIteration


def fib(n):
    fib_0 = 1
    fib_1 = 1 
    yield(fib_0)
    yield(fib_1)
    for i in range(n-2):
        fib_0,fib_1 = fib_1, fib_0+fib_1
        yield fib_1



# yield from 
def matrix(n:int):
    gen = ( (i*j for j in range(1,n+1)) for i in range(1,n+1) )
    return gen


def matrix_iterator(n):
    def matrix_fn(n:int):
        gen = ( (i*j for j in range(1,n+1)) for i in range(1,n+1) )
        return gen

    for row in matrix_fn(n):
        yield from row


# from functool import reduce, starmap, zip, zip_longest

if __name__=='__main__':
    sq = squares(5)
    print(f"use sq once:: {list(sq)}")
    print(f"use sq twice:: {list(sq)}")

    print(f"any([0,'',None,'hello']):: {any([0,'',None,'hello'])}")
    print(f"all([0,'',None,'hello']):: {all([0,'',None,'hello'])}")

    print(f"isinstance(10,Number):: {isinstance(10,Number)}")
    print(f"isinstance(10.5,Number):: {isinstance(10.5,Number)}")
    print(f"isinstance(10.5+5j,Number):: {isinstance(10.5+5j,Number)}")



    nums = [1,2,3,4,5,6,'hello']
    # print(list(map(str,nums)))
    print(f"check all nums or not <{nums}> :: {all(list(map(lambda x:isinstance(x,Number), nums)))}")
    print(f"check all nums or not <{nums}> ::{all((isinstance(x,Number) for x in nums))}")


    with open(os.path.join(os.path.dirname(__file__),'assets','car-brands-1.txt'),mode='r',encoding='latin-1') as f:
        for row in f:
            print(row,end='')
    print()

    with open(os.path.join(os.path.dirname(__file__),'assets','car-brands-2.txt'),mode='r',encoding='latin-1') as f:
        print(f"checking row size>=13:: {any(len(row)>=13 for row in f)}")



    # Iterator
    fiter = FactIter(10)
    for seq in fiter:
        print(seq,end=" ")
    print()

    # Yielding and Generators
    # print(yield_me())
    yielded_me = yield_me()
    print(f"yielded me:: {yielded_me}")
    print(next(yielded_me))
    print(next(yielded_me))
    try:
        print(next(yielded_me))
    except Exception as e:
        print(e.__class__)

    # print(list(yield_me()))

    for num in factorials_fn(10):
        print(num)


    fib_iterable = Fib(7)
    print(fib_iterable) # Iterable
    for i in fib_iterable:
        print(i)
    print(list(fib_iterable))


    print([i for i in fib(8)])
    

    # Yield from 
    print(list(matrix(5))) # returns list of generators
    # print matrix
    for i in matrix(5):
        print(list(i))


# ----------------------------------------------------
from typing import List,Sequence,NamedTuple,Dict
import os 
from datetime import datetime
from collections import namedtuple
import pickle 
from rich import print


cars:List[NamedTuple] = []
# lazy read
with open(os.path.join(os.getcwd(),"assets",'nyc_parking_tickets.csv'),mode='r') as f:
    # call once and pick headers
    header = [_.strip().replace(' ','_') for _ in next(f).split(',')]        
    # Tuple
    Cars = namedtuple(typename='Cars',field_names=header)

    # Read line by line
    for row in f.readlines():
        # print(row)

        if len(row.split(','))==9:
            c  = Cars(*[i for i in row.split(',')])
            c  = c._replace(
                        Issue_Date = datetime.strptime(c.Issue_Date, '%m/%d/%Y'),
                        Summons_Number=int(c.Summons_Number),
                        Violation_Code=int(c.Violation_Code),
                        Violation_Description=c.Violation_Description.strip()
                )
            cars.append(c)
        else:
            ...



with open(os.path.join(os.path.dirname(__file__),'assets','cars.pkl'),mode='wb') as f:
    pickle.dump(cars,f)



# cars
with open(os.path.join(os.path.dirname(__file__),'assets','cars.pkl'),mode='rb') as f:
    cars = pickle.load(f)


# .value_counts
car_make:Dict = {}
for c in cars:
    if c.Vehicle_Make in car_make:
        car_make[c.Vehicle_Make] += 1
    else:
        car_make[c.Vehicle_Make]=0
    
print(car_make)