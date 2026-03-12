import os
import csv
# context manager


class MyContxt:
    def __init__(self) -> None:
        print(f"instance of Object created!!")

    def __enter__(self):
        print('entering context here: opening DB')
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print('existing context here: Closing DB connection')



class Resource:
    def __init__(self,name) -> None:
        self.name = name 
        self.state = None 
class ResrcManager:
    def __init__(self,name) -> None:
        self.name = name 
        self.resrc = None
    def __enter__(self):
        print('entering contxt')
        self.resrc:Resource = Resource(self.name)
        self.resrc.state = 'created'
        return self.resrc
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print("exiting contxt")
        self.resrc.state = 'destroyed'
        if exception_type:
            print('err occured!!')



def lazy_read_data():
    with open(os.path.join(os.path.dirname(__file__),'assets','cars.csv'),'r') as f:
        return csv.reader(f,delimiter=',',quotechar='"')

def read_data():
    with open(os.path.join(os.path.dirname(__file__),'assets','cars.csv'),'r') as f:
        return list(csv.reader(f,delimiter=',',quotechar='"'))
    
def yield_data():
    with open(os.path.join(os.path.dirname(__file__),'assets','cars.csv'),'r') as f:
        yield from csv.reader(f,delimiter=',',quotechar='"')


class DataIterator:
    def __init__(self,name) -> None:
        self.name = name 
        self._f   = None 

    def __iter__(self): return self 
    
    def __next__(self):
        row = next(self._f)
        return row.strip("\n").split(';')
    
    def __enter__(self): 
        self._f = open(self.name)
        return self 
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if not self._f.closed:
            self._f.close()
        return False
    




class CSVDATAReader:
    def __init__(self,name) -> None:
        self.name = name 
        self._f   = None 

    def __iter__(self): return self 
    
    def __next__(self):
        row = next(self._f)
        return row
    
    def __enter__(self): 
        self._f = csv.reader(open(self.name))
        return self 
    def __exit__(self, exception_type, exception_value, exception_traceback):
        return False
    

if __name__=='__main__':


    # Error Handling
    try:
        # 10/2
        10/0
    except ZeroDivisionError as e:
        print(f"exception block:: {e.__class__}")
    finally:
        print('finally ran!!')


    # 
    try:
        f = open('imaginary_file.txt','w')
        print(f"is file closed:: {f.closed}")    
    except Exception as e:
        print(f"exception block:: {e.__class__}")
    finally:
        f.close()
        print('closing file!!')

    # context manager
    with open('imaginary_file.txt','w') as f:
        print(f"is file closed:: {f.closed}")        
        f.write('hello planet!\n')
    print(f"is file closed:: {f.closed}")    
    os.remove('imaginary_file.txt')


    # own context manger
    with MyContxt() as context:
        pass

    # Custom context Manager
    with ResrcManager('spam') as resrc:
        print(f"{resrc.name} == {resrc.state}")
    print(f"{resrc.name} == {resrc.state}")


    try:
        print('*'*20,"Lazy Read",'*'*20)
        for row in lazy_read_data():
            print(row)
    except ValueError as e:
        print("I/O Operation on closed File")


    try:
        print('*'*20,"In Memory Read",'*'*20)
        for row in read_data():
            print(row)
    except ValueError as e:
        print("I/O Operation on closed File")


    try:
        print('*'*20,"Yield From Read",'*'*20)
        for row in yield_data():
            print(row)
    except ValueError as e:
        print("I/O Operation on closed File")


    # DataIterator
    with DataIterator(os.path.join(os.path.dirname(__file__),'assets','cars.csv')) as data:
        print('*'*20,"DataIterator",'*'*20)
        for row in data:
            print(row)


    with DataIterator(os.path.join(os.path.dirname(__file__),'assets','nyc_parking_tickets_extract.csv')) as data:
        print('*'*20,"DataIterator",'*'*20)
        for row in data:
            print(row)

    
    with DataIterator(os.path.join(os.path.dirname(__file__),'assets','personal_info.csv')) as data:
        print('*'*20,"DataIterator",'*'*20)
        for row in data:
            print(row)


    ###########################################################################
    # 
    #                    Assignment
    # 
    ###########################################################################

    

    fname:str = 'personal_info.csv'
    Filename  = os.path.join(os.path.dirname(__file__),'assets',fname)
    with CSVDATAReader(Filename) as data:
        print('*'*20,f"{fname}::DataIterator",'*'*20)
        for row in data:
            print(row)

    fname:str = 'nyc_parking_tickets_extract.csv'
    Filename  = os.path.join(os.path.dirname(__file__),'assets',fname)
    with CSVDATAReader(Filename) as data:
        print('*'*20,f"{fname}::DataIterator",'*'*20)
        for row in data:
            print(row)

    fname:str = 'cars.csv'
    Filename  = os.path.join(os.path.dirname(__file__),'assets',fname)
    with CSVDATAReader(Filename) as data:
        print('*'*20,f"{fname}:: DataIterator",'*'*20)
        for row in data:
            print(row)