from functools import reduce,partial
import operator
import inspect
from typing import Callable,Annotated

# Docstring & Annotations

def factorial(n:int,/)->int:
    ''' 
        Factorial Function 
        - n:input int
    '''
    _fact:int = 1
    if n==0: return _fact
    while(n>0):
        _fact *= n 
        n -= 1
    return _fact

print(f"docs :: {factorial.__doc__}")
print(f"annotations: {factorial.__annotations__}")
print(help(factorial))

factorial.__doc__ = 'get fooled!'
print(factorial.__doc__)

# Lambda
func = lambda x,*args,y,**kwargs: (x,*args,y,kwargs)
print(f"func(1,'a','b',y=100,a=1,b=2): {func(1,'a','b',y=100,a=1,b=2)}")
def apply_func(x,fn): return fn(x)

print(f"cubic: {apply_func(3,lambda x:x**3)}")
print(f"square: {apply_func(3,lambda x:x**2)}")

def apply_func(fn,*args,**kwargs): return fn(*args,**kwargs)

print(f"apply_func(lambda x,y:x+y,1,2)    :: {apply_func(lambda x,y:x+y, 1, 2 )}")
print(f"apply_func(lambda x,*,y:x+y,1,y=2):: {apply_func(lambda x,*,y:x+y,   1, y=2)}")
print(f"apply_func(lambda *args:sum(args), 1,2,3,4,5,6,7,8,9,0):: {apply_func(lambda *args:sum(args), 1,2,3,4,5,6,7,8,9,0)}")

lst:list = ['c','D','a','B','A']
print(f"sorted list:: {sorted(lst,key=str.lower)}")
print(f'a:{ord("a")}')
print(f'A:{ord("A")}')

complex_list = [3+1j, 5-823j, 0, -3,51j]
print(sorted(complex_list,key=lambda x: ((x.real)**2 + (x.imag)**2)) )


# Introspection
print(f"getmembers:: {inspect.getmembers(factorial)}")



def func(a,b=2,c=3,*,kw1,kw2=2,**kwargs): pass 
f = func 

print(func.__name__)
print(f.__name__)
print(help(f))
print(func.__defaults__)
print(func.__kwdefaults__)
print(func.__code__)
print(func.__code__.co_varnames)
print(func.__code__.co_argcount)
print(inspect.getsource(func))

print(f"ismethod:: {inspect.ismethod(func)}")


class PyClass:
    def py_instance(self):
        '''method'''
        pass 

    @classmethod
    def py_classmethod(cls):
        ''' accept classname as reference. not bound to instance'''
        pass 

    @staticmethod
    def py_static1():
        '''
            independent of this class or not upto you declare
            here I'm free
        '''
        pass 

    @staticmethod
    def py_static2(self,cls):
        '''
            independent of this class or not upto you declare
            here I'm not
        '''
        pass 


pyc = PyClass()

## IsMethod on Instance
print(f"inspect.ismethod(pyc.py_instance):: {inspect.ismethod(pyc.py_instance)}\ninspect.ismethod(pyc.py_classmethod):: {inspect.ismethod(pyc.py_classmethod)}") 
print(f"inspect.ismethod(pyc.py_static1):: {inspect.ismethod(pyc.py_static1)}\ninspect.ismethod(pyc.py_static2):: {inspect.ismethod(pyc.py_static2)}") 

print('**100')

# IsFunction on Instance
print(f"inspect.isfunction(pyc.py_instance):: {inspect.isfunction(pyc.py_instance)}\ninspect.isfunction(pyc.py_classmethod):: {inspect.isfunction(pyc.py_classmethod)}") 
print(f"inspect.isfunction(pyc.py_static1):: {inspect.isfunction(pyc.py_static1)}\ninspect.isfunction(pyc.py_static2):: {inspect.isfunction(pyc.py_static2)}") 




## IsMethod on CLASS
print(f"inspect.ismethod(PyClass.py_instance):: {inspect.ismethod(PyClass.py_instance)}\ninspect.ismethod(PyClass.py_classmethod):: {inspect.ismethod(PyClass.py_classmethod)}") 
print(f"inspect.ismethod(PyClass.py_static1):: {inspect.ismethod(PyClass.py_static1)}\ninspect.ismethod(PyClass.py_static2):: {inspect.ismethod(PyClass.py_static2)}") 

print('**100')

# IsFunction on CLASS
print(f"inspect.isfunction(PyClass.py_instance):: {inspect.isfunction(PyClass.py_instance)}\ninspect.isfunction(PyClass.py_classmethod):: {inspect.isfunction(PyClass.py_classmethod)}") 
print(f"inspect.isfunction(PyClass.py_static1):: {inspect.isfunction(PyClass.py_static1)}\ninspect.isfunction(PyClass.py_static2):: {inspect.isfunction(PyClass.py_static2)}") 



def print_info(f: Callable) -> None:
    print(f.__name__)
    print('=' * len(f.__name__), end='\n\n')
    
    print('{0}\n{1}\n'.format(inspect.getcomments(f), 
                              inspect.cleandoc(f.__doc__)))
    
    print('{0}\n{1}'.format('Inputs', '-'*len('Inputs')))
    
    sig = inspect.signature(f)
    for param in sig.parameters.values():
        print('Name:', param.name)
        print('Default:', param.default)
        print('Annotation:', param.annotation)
        print('Kind:', param.kind)
        print('--------------------------\n')
        
    print('{0}\n{1}'.format('\n\nOutput', '-'*len('Output')))
    print(sig.return_annotation)



# TODO: Provide implementation
def my_func( a:Annotated[str,'a string'],b: int = 1,*args:Annotated[str,...,'additional positional args'],kw1: Annotated[dict,'first keyword-only arg'],kw2:Annotated[dict, 'second keyword-only arg'] = 10,**kwargs:Annotated[dict,..., 'additional keyword-only args']) -> str:
    '''
    Docstring for my_func
    
    :param a: Description
    :type a: Annotated[str, 'a string']
    :param b: Description
    :type b: int
    :param args: Description
    :type args: Annotated[str, ..., 'additional positional args']
    :param kw1: Description
    :type kw1: Annotated[dict, 'first keyword-only arg']
    :param kw2: Description
    :type kw2: Annotated[dict, 'second keyword-only arg']
    :param kwargs: Description
    :type kwargs: Annotated[dict, ..., 'additional keyword-only args']
    :return: Description
    :rtype: str
    '''
    pass 


def new_func():
    """does something or other"""


print_info(my_func)


# Callable
print(callable(print))
print(callable(list.append))

class MyClass:
    def __init__(self):
        print('initializing...')
        self.counter = 0
    
    def __call__(self, x=1):
        self.counter += x
        print(self.counter)


m = MyClass()
print('is `m` instance callable',callable(m))  #??


# Map, Filter & Zip

print(f"map(factorial,[1,2,3,4]):: {map(factorial,[1,2,3,4])}")        # Designing
print(f"list(map(factorial,[1,2,3,4])):: {list(map(factorial,[1,2,3,4]))}")  # Execute
print(f"list comphrension: [factorial(i) for i in range(1,5)]:{[factorial(i) for i in range(1,5)]}")   # list comphrension

print(f"list(map(lambda x,y:x+y,[1,2,3,4,5],[6,7,8,9,0])): {list(map(lambda x,y:x+y,[1,2,3,4,5],[6,7,8,9,0]))}")
print(f"list(zip([1,2,3,4,5,6],[1,2,3,4,5])): {list(zip([1,2,3,4,5,6],[1,2,3,4,5]))}")
print(f"list(zip([1,2,3,4,5,6],[1,2,3,4,5])): {list(zip([1,2,3,4,5,6],[1,2,3,4,5]))}")
print(f"list(filter(lambda x:x%2==0,range(0,11))): {list(filter(lambda x:x%2==0,range(0,11)))}")


# Reduce

print(f"reduce(lambda x,y:x if x>y else y,range(100)):: {reduce(lambda x,y:x if x>y else y,range(100))}")
print(f"reduce(lambda x,y:x*y, range(1,11)):: {reduce(lambda x,y:x*y, range(1,11))}")


# Partial    
# Functional Programming currying
def my_func(a, b, *args, k1, k2, **kwargs):
    print(a, b, args, k1, k2, kwargs)

f = partial(my_func, 10, k1='a')
print(f"f(1000,1,2,3,4,k2='b',k3='c',k4='d'):: {f(1000,1,2,3,4,k2='b',k3='c',k4='d')}")


# Operator

print(f'range(5,59,7): {list(range(5,59,7))}')
print(f"reduce(operator.mul, [1, 2, 3, 4]):: {reduce(operator.mul, [1, 2, 3, 4])}")

get_two = operator.itemgetter(2)
print(f"operator.itemgetter(2)(iterable):: {get_two(range(5,50,7))}")