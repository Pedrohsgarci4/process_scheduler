from itertools import cycle
from random import randint

from .process import *
class ProcessGenerator:
    def __init__(self,
                 process_numbers : list = [],
                 interval_creation : list = [],
                 memory_demand : list = [],
                 cpu_demand : list = [],
                 event_generators : list = []
                 ) -> None:
        
        self.process_numbers = cycle(process_numbers)
        self.interval_creation = cycle(interval_creation)
        self.memory_demands = cycle(memory_demand)
        self.cpu_demands = cycle(cpu_demand)
        self.event_generators = cycle(event_generators)
        
        self.interval = 0
        
    
    
    def step(self):
        if self.interval <= 0:
            new_processes = []
            
            n_process = next(self.process_numbers)

            for _ in range(n_process):
                
                process = Process(
                    start=self.process_manager.steps,
                    cpu_demand=next(self.cpu_demands),
                    memory_demand=next(self.memory_demands),
                    event_generator=next(self.event_generators),
                    priority=randint(1,3)
                )
                
                new_processes.append(process)
            
            # Atualiza o intervalo:
            self.interval = next(self.interval_creation)
            
            self.process_manager.new.extend(new_processes)
        
        else:
            self.interval -= 1
            return []
            
    
    def connect_to_manager(self, process_manager : object):
        self.process_manager = process_manager
        