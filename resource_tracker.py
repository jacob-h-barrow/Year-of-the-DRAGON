from typing import List, Tuple, Optional, NoReturn, TypeAlias, Any, TypedDict
from dataclasses import dataclass

import tracemalloc
import time

@dataclass
class Time_Spent:
    real: float
    cpu: float
    timestamp: float
    
    def states(self):
        return self.real, self.cpu, self.timestamp

class ResourceTrackingDecorator:
    object_tracker = {}
    
    @classmethod
    def display(cls):
        for func_name, values in cls.object_tracker.items():
            print(f"Here is the data for {func_name}")
            for time_spent in values:
                real, spent, timestamp = time_spent.states()
                print(f"At {timestamp}\t", end="")
                print(f"Real time: {real:.2f} seconds\t", end="")
                print(f"CPU time: {spent:.2f} seconds")
            print()
    
    def __init__(self, func):
        if (name := func.__name__) not in self.object_tracker.keys():
            self.object_tracker[name] = []
        
        self.func = func
        
    def __call__(self, *args, **kwargs):
        # Change later
        if kwargs['_print']:
            print('"{}" was called with the following arguments'.format(self.func.__name__))
            print('\t{}\n\t{}\n'.format(args, kwargs))
        start = time.perf_counter(), time.process_time()
        result = self.func(*args, **kwargs)
        end = time.perf_counter(), time.process_time()
        
        self.object_tracker[self.func.__name__].append(Time_Spent(end[0] - start[0], end[1] - start[1], time.time()))
 
@ResourceTrackingDecorator
def first_fxn(*args, **kwargs):
    if kwargs['_print']:
        print("\tHello from the decorated function; received arguments:", args, kwargs)

@ResourceTrackingDecorator
def second_fxn(*args, **kwargs):
    if kwargs['_print']:
        print("\tHello from the decorated function; received arguments:", args, kwargs)      
        
def convert_to_KiB(block_size: int) -> float:
    return block_size / 1024
    
def track_deco(func):
    def inner(*args, **kwargs):
        tracemalloc.start()
        
        result = func(*args, **kwargs)
        
        current_blocks, peak_blocks = tracemalloc.get_traced_memory()
        print('Function Metrics:\n\tBlocks of memory used:\n\t\tCurrent %d (%f KiB)\n\t\tPeak %d (%f KiB)\n' % \
              (current_blocks, convert_to_KiB(current_blocks), peak_blocks, convert_to_KiB(peak_blocks)))
        
        return result
    return inner
    
@track_deco
def test():
    return [i**2 for i in range(10)]
    
def timing_deco(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        
        print(f'{func.__name__} took {(time.time() - start) * 10**6} microseconds to run!')
        
        return result
    return inner
    
def timing_deco_2(func):
    def inner(*args, **kwargs):
        start = time.perf_counter(), time.process_time()
        result = func(*args, **kwargs)
        end = time.perf_counter(), time.process_time()
        
        print(f" Real time: {end[0] - start[0]:.2f} seconds")
        print(f" CPU time: {end[1] - start[1]:.2f} seconds")
        
        return result
    return inner
if __name__ == "__main__":
    args = [chr(97 + i) for i in range(26)]
    kwargs = {'hello': 10, 'goodbye': 100, '_print': False}
    for call in range(5):
        if call == 0:
            first_fxn(*args[:2], _print=True)
            print()
            second_fxn(*args[:3], _print=True)
        else:
            first_fxn(*args[:randint(2,25)], **kwargs)
            second_fxn(*args[:randint(1,25)], **kwargs)
            
    print('\nTracking blocks')

    print(f'Running function: {test()}')
