from copy import deepcopy
from itertools import cycle

class Process:
    _object_count = 0
    _instances = []
    
    def __init__(
         self,
         start : int,
         cpu_demand : int = 1,
         memory_demand : int = 1,
         duration : int = 1,
         event_generator : list = [] 
        ) -> None:
        
        self.status = "created"
        
        self.cpu = cpu_demand
        self.memory = memory_demand
        self.duration = duration
        
        
        if event_generator == []:
            self.event_generator = cycle([False,False])
        else:
            self.event_generator = cycle(event_generator)
        
        self.history = []
        
        self.pid = self.__class__._object_count + 1
        self.__class__._object_count += 1
        
        self.__class__._instances.append(self)
        
        
    def step(self):
        
        if self.status == "running":
            self.duration -= 1
            
            event = next(self.event_generator)
            
            if event:
                self.event = event

        elif self.status == "blocked":
            event = next(self.event_generator)
            
            if not event:
                self.status = "ready"   
           
        if self.duration <= 0:
            self.status = "finished"
            
        self.history.append(self.status)
        
    def metrics(self):
        metrics = {
            "status" : self.status,
            "PID" : self.pid
        }
        
        return metrics
    
    @classmethod
    def all(cls):
        return deepcopy(cls._instances)
        
        
        
        