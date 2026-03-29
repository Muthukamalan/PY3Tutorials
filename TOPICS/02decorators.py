"""
Docstring for Decorators

- The underlying mechanics of how decorators work.
- How to use common decorators to implement practical tasks like caching, context management, model wrapping, and configuration injection.
- How to build a decorator from scratch and integrate it into your codebase.
"""

from contextlib import contextmanager
import gc 
import torch
from typing import AsyncGenerator, Literal, Mapping, Optional,Union,Callable, TypeVar
from typing_extensions import ParamSpec
from abc import ABC, abstractmethod
from functools import wraps
from vllm import PromptType, RequestOutput, SamplingParams
import deepspeed


"""
The purpose of `@classmethod` here is to define a context manager within the class's scope that can access class variables.
Its first parameter is `cls` , allowing it to access class attributes, such as cls.optimize_device_cache.

Without @classmethod, this function could only be called as a regular function or an instance method, and it wouldn't be able to access class variables through the class. 
```
cudaclear = PPODecorators()
cudacelar.exmpty_device_cache()
```

Class Variable: defined within a class, shared by all instance and belongs to the class. `ClassName.var` / `self.__class__.var`

"""


class PPODecorators:
    optimize_device_cache = False

    @classmethod
    @contextmanager
    def exmpty_device_cache(cls):
        yield   # This is the insertion point for the code inside the with block
        if cls.optimize_device_cache:
            # The cache clearing code executes after the with statemen
            if torch.cuda.is_available():
                gc.collect()
                torch.cuda.empty_cache()
                gc.collect()
            elif torch.xpu.is_available():
                gc.collect()
                torch.xpu.empty_cache()
                gc.collect()

"""
When decorated with `@contextmanager`
vWhen you decorate a function with @contextmanager, that function becomes a context manager that can be used with the with ... as x: syntax.

- Code before yield is executed upon entering the context (__enter__()).
- Code after yield is executed upon exiting the context (__exit__()).
- The value yielded: the object bound to the as target in the with statement.
"""

with PPODecorators.exmpty_device_cache():
    #  run a PPO optimization steps
    pass 

DistributedDataParallel:object
DeepSpeedEngine: object
Accelerator:object 
remove_hooks:Callable
add_hooks:Callable


@contextmanager
def unwrap_model_for_generation(
    model: Union["DistributedDataParallel", "DeepSpeedEngine"],
    accelerator: "Accelerator",
    gather_deepspeed3_params: bool = True,
):
    """
    Its function is to return an “unwrapped model ready for generation tasks,” 
    based on whether DeepSpeed Stage 3 is used and whether parameters need to be gathered.
    """
    unwrapped_model = accelerator.unwrap_model(model)
    if accelerator.state.deepspeed_plugin is not None and accelerator.state.deepspeed_plugin.zero_stage == 3:
        
        if not gather_deepspeed3_params:
            '''
            If using DeepSpeed ZeRO Stage 3 without gathering parameters, it skips parameter collection. 
            This saves VRAM but may slow down generation. Here, it also directly yields an unwrapped model.
            '''
            yield accelerator.unwrap_model(model)
        else:
            import deepspeed

            with deepspeed.zero.GatheredParameters(model.parameters()):
                '''
                - You can use the same code to support various distributed training wrappers (DDP/DeepSpeed).
                - The unwrapping logic is handled automatically, performing necessary parameter aggregation and hook cleanup based on conditions.
                - Inside the with block, you can call .generate(...) as if it were a regular model.
                - And after the with block finishes, it automatically cleans up the state (e.g., restores hooks).
                '''
                remove_hooks(model)
                yield accelerator.unwrap_model(model)
                add_hooks(model)
    else:
        '''
        It directly returns the unwrapped model; there are no complex operations. 
        This corresponds to regular DDP or DeepSpeed Stage 1/2.
        '''
        yield unwrapped_model

    
with unwrap_model_for_generation(model="",accelerator="") as unwrapped_model:
    # When this code is executed, the code before yield has already run.
    # The object returned by yield is assigned to unwrapped_model
    pass 






########################################################################################################################################################


"""
`@abstractmethod` and `@property`. They are often used together to build strict interface specifications in object-oriented architectures.

from abc import `ABC`. An `ABC` is used to define an interface or a protocol class.  specifies the methods or properties that subclasses must implement.
At runtime, you cannot directly instantiate a class that has unimplemented abstract methods; doing so will raise a TypeError

`@abstractmethod` indicates that a method or property is abstract and must be implemented by subclasses. 
`@property` turns a method into a “property,” allowing it to be accessed like a field.

"""

class EngineClient(ABC):

    @property
    @abstractmethod
    def is_running(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_stopped(self) -> bool:
        ...

    @property
    @abstractmethod
    def errored(self) -> bool:
        ...

    @property
    @abstractmethod
    def dead_error(self) -> BaseException:
        ...

    @abstractmethod
    def generate(
        self,
        prompt: PromptType,
        sampling_params: SamplingParams,
        request_id: str,
        lora_request: Optional[LoRARequest] = None, # type: ignore
        trace_headers: Optional[Mapping[str, str]] = None,
        prompt_adapter_request: Optional[PromptAdapterRequest] = None,  # type: ignore
        priority: int = 0,
    ) -> AsyncGenerator[RequestOutput, None]:
        """Generate outputs for a request."""
        ...

'''
The EngineClient class is an interface definition that standardizes the structure for all “client” classes:

- It requires client classes to implement certain state properties (like is_running).
- It requires the implementation of an asynchronous generate method.
- It uses ABC and @abstractmethod to enforce that all subclasses must implement these interfaces.
- It uses @property to provide a cleaner interface for state attributes.

'''




########################################################################################################################################################


"""
A method decorated with `@staticmethod:`

- Does not receive self or cls as the first argument.
- Cannot access instance attributes (self.x) or class variables (cls.y).
- Is almost identical to a regular function, but it is placed within the clas'ss namespace to logically organize it as part of the class.
- It has no state dependency on the members of the Class
"""


class DPOTrainer:
    @staticmethod
    def tokenize_row(features, processing_class, max_prompt_length, max_completion_length, add_special_tokens):
        ...


fn:Callable = DPOTrainer.tokenize_row # just to logically group keeping inside class


"""
A Quick Recap of Decorator Basics
When you want to modify or enhance the behavior of a function in a uniform, automatic, and reusable way, decorators are the best choice.

Common use cases include:

- Logging: such as printing the function name, input arguments, and return value.
- Profiling: such as automatically recording execution time and memory usage.
- Caching (Memoization): remembering function outputs to avoid redundant computations.
- Access Control / Validation: checking user permissions or the validity of parameters.
- Concurrency Control: for example, adding locks to a function for thread safety.
- Retry Mechanisms: for instance, automatically retrying a function after failure (e.g., an API call).

"""


P = ParamSpec("P")  #  This special type variable is used to pass the exact parameter types of the decorated function to the wrapper function.
R = TypeVar("R")  # This is used to capture and return the exact return type of the original function.


def bulb_decorator(func:Callable[P,R])->Callable[P,R]:
    @wraps(func)
    def wrapper(*args:P.args,**kwargs:P.kwargs):
        print("Turn on Bulb")
        result = func(*args,**kwargs)
        print("Turn off Bulb")
        return result
    return wrapper
        

def marriage_function():
    return "Happy marriage!"

fnc = bulb_decorator(marriage_function)
print(fnc())



"""
## Decorators with Args

@video_decorator_with_camera("SONY")
    def fn():
        ...

You need two levels of function nesting:


"""

def video_decorator_with_camera(camera:str="SONY"):
    def video_decorator(func:Callable[P,R])->Callable[P,R]:
        @wraps(func)
        def wrapper(*args:P.args,**kwargs:P.kwargs):
            print(f"[Shooting camera on {camera}]")
            return func(*args,**kwargs)
        return wrapper
    return video_decorator


birthday_func:Callable = lambda x:f"Happy birthday, {x}"

birthday_func_with_nission = video_decorator_with_camera("NISSON")(birthday_func)

'''
- First, something(…) is executed, which returns a true decorator function.
- Then, the foo function is passed to this returned decorator.

'''



class my_context_decorator:
    def __init__(self, func):
        self.func = func
        # Use functools.wraps to preserve original function metadata
        wraps(func)(self) 

    def __enter__(self):
        print(f"-- Entering context for '{self.func.__name__}' --")
        # Perform setup actions
        return self.func # Return the function to be used in the 'as' part of 'with'

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"-- Exiting context for '{self.func.__name__}' --")
        # Perform cleanup actions
        if exc_type:
            print(f"An exception occurred: {exc_val}")
        return False # Propagate exceptions if any

    def __call__(self, *args, **kwargs):
        # Allow direct calling of the decorated function without 'with'
        with self:
            return self.func(*args, **kwargs)

# Apply the decorator
@my_context_decorator
def say_hello(name):
    print(f"Hello, {name}!")
    return f"Execution complete for {name}"

# Usage with a 'with' statement
with say_hello("Alice") as result: # Note: Calling the function applies the decorator as a context manager
    # The 'result' variable here holds the return value of __enter__
    print(f"Function returned: {result}") 

# The decorated function can also be called directly like a normal function
print(say_hello("Bob"))