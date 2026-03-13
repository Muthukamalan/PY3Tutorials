# Setup
- [X] conda
- [X] UV

# Pre-Requisites
- [Python3 by Boot.dev](https://youtu.be/4M87qBgpafk?si=MH3ZjR2OkevPYiQK)
#  Content 
- [X] *Basics*: Python Type Hierarchy, Multi-line statements and strings, Variable Names, Conditionals, Functions, The While Loop, Break Continue and the Try Statement, The For Loop and Classes
- [X] *Object Mutability and Interning*: Variables and Memory References, Garbage Collection, Dynamic vs static Typing, Variable Re-assignment, Object Mutability, Variable Equality, Everything is an Object and Python Interning
- [X] *Numeric Types I*: Integers, Constructors, Bases, Rational Numbers, Floats, rounding, Coercing to Integers and equality
- [X] *Numeric Types II*: Decimals, Decimal Operations, Decimal Performance, Complex Numbers, Booleans, Boolean Precedence and Comparison Operators
- [X] *Functional Parameters*: Argument vs Parameter, Positional and keyword Arguments, Unpacking Iterables, Extended Unpacking, __*args_, Keyword Arguments, __**kwags_, Args and Kwargs together, Parameter Defaults and Application
- [X] *First Class Functions Part I*: Lambda Expressions, Lambdas and Sorting, Functional Introspection, Callables, Map, Filter, Zip and List Comprehension
- [X] *First Class Functions Part II*: List Comprehension, Reducing functions, Partial Functions, Operator Module, Docstrings and Annotations.
- [X] *Scopes and Closures*: Global and Local Scopes, Nonlocal scopes, Closures, and Closure Applications
- [X] *Decorators*: Decorators and Decorator applications (timers, logger, stacked decorators, memoization, decorator class and dispatching)
- [X] *Tuples and Named Tuples*: Tuples, Tuples as data structures, named Tuples, DocStrings, and Application
- [X] *Modules, Packages and Namespaces*: Module, Python Imports, importlib, import variants, reloading modules,`__main__`, packages, structuring, and namespaces
- [X] *fStrings, Timing Functions and Command Line Arguments*: Dictionary Ordering, kwargs, tuples, fStrings, Timing Functions and Command Line Arguments
- [X] *Sequence Types I*: Sequence Types, Mutable Sequence Types, List vs Tuples, Index Base and Slice Bounds, Copying Sequence and Slicing
- [X] *Sequence Types II and Advanced List Comprehension*: Custom Sequences, In-place Concatenation and Repetition, Sorting Sequences, List Comprehensions + Small Project
- [X] *Iterables and Iterators*: Iterating Collections, Iterators, Iterables, Cyclic Iterators, in-built Iterators, iter() function and iterator applications
- [X] *Generators and Iteration Tools*: Yielding and Generator Functions, Generator Expressions, Yield From, Aggregators, Chaining and Teeing, Zipping and their applications
- [X] *Context Managers*: Context Managers, Lasy Iterators, Generators and Context Managers, Nested Context Managers and their application


# Project Proposal
`Title`: **Custom DataLoader for Multimodal Datasets**

`Description`:
In this project, you will build a flexible DataLoader class that can load, preprocess, and manage different types of datasets commonly used in AI and machine learning projects, including:

- Image datasets: CIFAR-10, CIFAR-100, MNIST
- Text datasets: Small text datasets
- Structured data: CSV files
- Unstructured data: Folders containing multiple files of various formats

`Your DataLoader should`: 
- *Download datasets from online sources* if they are not already present locally.
- *Handle different file formats* and organize data appropriately.
- *Provide data in batches* for efficient processing.
- *Support data augmentation and preprocessing* steps.
- *Be extensible* to accommodate new data types and sources.


**Project Breakdown by Concepts**
1. Basics
- *Classes*: Implement the DataLoader as a class.
- *Functions*: Define methods for downloading, loading, and preprocessing data.
- *Loops and Conditionals*: Iterate over files and data, check for file existence.

2. Object Mutability and Interning
- Manage mutable data structures like lists and dictionaries to store datasets.
- Understand how changes to objects affect data integrity.

3. Numeric Types I & II
- Handle numerical computations during preprocessing (e.g., normalization).
- Use booleans and comparison operators for condition checks.

4. Functional Parameters
- Create flexible methods that accept various parameters for data transformations.
- Use **kwargs to pass optional preprocessing functions.

5. First-Class Functions Part I & II
- Use lambda functions for simple data transformations.
- Employ map and filter to process data iterables.

6. Scopes and Closures
- Maintain state within data loading functions using closures if necessary.

7. Decorators
- Implement decorators to log the time taken for data loading and preprocessing.
- Use decorators for caching data to avoid redundant computations.

8. Tuples and NamedTuples
- Use namedtuples to represent data samples with features and labels.

9. Modules, Packages, and Namespaces
-Organize code into modules for loaders, preprocessors, utils, etc.
- Use packages to separate different components logically.

10. f-Strings, Timing Functions, and Command Line Arguments
- Use f-strings for informative print statements.
- Accept command-line arguments for configuration (e.g., dataset selection).

11. Sequence Types I & II and Advanced List Comprehension
- Manage collections of data samples.
- Use list comprehensions for efficient data processing.

12. Iterables and Iterators
- Implement an iterator protocol in the DataLoader to iterate over data batches.

13. Generators and Iteration Tools
- Use generators to load data on-the-fly without consuming excessive memory.

14. Context Managers
- Use context managers when opening files to ensure they are properly closed.

15. Exception Handling (Try/Except)
- Handle exceptions during file I/O and data processing to prevent crashes.


```sh
project_root/
├── dataloader/
│   ├── __init__.py
│   ├── dataloader.py
│   ├── preprocessors.py
│   └── utils.py
├── datasets/
│   └── (Your datasets will be stored here)
├── tests/
│   └── test_dataloader.py
├── main.py
└── requirements.txt
```