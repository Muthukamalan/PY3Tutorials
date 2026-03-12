import math
import os 
from  typing import List,AnyStr,Callable
from collections import namedtuple
# Iterable & Iterator II


## class with In memory variable
## class with lazy calc variable (on-request)
class Circle:
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
    

class Factorials:
    def __init__(self, length):
        self.length = length
    
    # Iterable
    def __iter__(self):
        return self.FactIter(self.length)
    
    # Iterator
    class FactIter:
        def __init__(self, length):
            self.length = length
            self.i = 0
            
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                result = math.factorial(self.i)
                self.i += 1
                return result  

###
#### range 
#### with(open(),mode='a') as f
#### enumerate


## Iterator with __getitem__
class Squares:
    def __init__(self,n:int) -> None:
        self._n = n
    def __getitem__(self,i):
        if i>=self._n:
            raise IndexError
        else:
            return i**2

## is __iter__ enough to make iterable
class SimpleIter:
    def __init__(self) -> None:
        pass
    def __iter__(self):
        return None
    
def is_iterable_fn(obj:object)->bool:
    try:
        iter(obj)
        return True
    except Exception as e:
        return False

## iter on  callable 
help(iter)
# sentinal
## design of for-loop


## reversed iterable  
## reversed on custom sequence types
_SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
_RANKS = tuple(range(2, 11) ) + tuple('JQKA')

Card = namedtuple('Card', 'rank suit')

class CardDeck:
    def __init__(self):
        self.length = len(_SUITS) * len(_RANKS)

    def __len__(self):
        return self.length
    
    def __reversed__(self):
        return self.CardDeckIterator(self.length) #,reversed=True
    
    def __iter__(self):
        return self.CardDeckIterator(self.length)
        
    class CardDeckIterator:
        def __init__(self, length,rev=False):
            self.length = length
            self.reversed=rev
            self.i = 0
            
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                if self.reversed:
                    index = self.length -1 - self.i
                else:
                    index = self.i
                suit = _SUITS[index // len(_RANKS)]
                rank = _RANKS[index % len(_RANKS)]
                self.i += 1
                return Card(rank, suit)
            



# iterable /iterator

if __name__=='__main__':
    c = Circle(1)
    print(c.area)   #<< calc now
    print(c.area)   #<< not calc

    c.radius =4
    print(c.area)   #<< since it changes calc again


    print(type(range))  # itarator
    print([num for num in range(10)] )

    origins:set = set()
    with open(os.path.join(os.path.dirname(__file__),'assets','cars.csv'),mode='r') as f:
        print(type(f))  # Lazy Iterator 
        print(f"'__iter__' in dir(f):: {'__iter__' in dir(f)}")
        print(f"'__next__' in dir(f):: {'__next__' in dir(f)}")
        print(f.__next__())
        print(next(f))
        print(f.readline())

        for row in f:
            origin = row.strip('\n').split(';')[-1]
            origins.add(origin)

        print(origins)


    print(f"enumerate iter:: {iter(enumerate('python'))}")



    # Iterable
    d = {'a':1,'b':2}
    keys = d.keys()
    print(f"'__iter__' in dir(keys):: {'__iter__' in dir(keys)}")
    print(f"'__next__' in dir(keys):: {'__next__' in dir(keys)}")

    sq = Squares(10)
    for i in sq:
        print(i)

    try:
        reversed(sq)
    except Exception as e:
        print(f"{e.__class__}, len fn needed for reversed")


    s = SimpleIter()
    print(f"{'__iter__' in dir(s)}")  # will it sufficient
    # next(s)   << Fails
    print(f"is Iterable class:: {is_iterable_fn(s)}")

    deck = CardDeck()
    for card in deck:
        print(card)

    # dup_deck = list(deck)
    # print(dup_deck)
    # print(dup_deck[:-8:-1])

    print(list(reversed(deck)))