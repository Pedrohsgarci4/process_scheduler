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
         event_generator : list = [], 
         priority : int = 1
        ) -> None:
        
        self.status = "created"
        
        self.cpu_demand_initial = cpu_demand
        
        self.start = start
        self.allocated = 0
        self.cpu_demand = cpu_demand
        self.memory_demand = memory_demand
        self.priority = priority
        self.continuous_cpu_time = 0
        self.event = False
        self.end = 0
        
        
        self.history = []
        
        
        
        if event_generator == []:
            self.event_generator = cycle([False,False])
        else:
            self.event_generator = cycle(event_generator)
        
        self.history = []
        
        self.pid = self.__class__._object_count + 1
        self.__class__._object_count += 1
        
        self.__class__._instances.append(self)
        
        
    def step(self):
        if self.allocated > 0:
            
            if self.status != "running":
                self.status = "running"

            self.continuous_cpu_time += self.allocated
            self.cpu_demand = max(0, self.cpu_demand - self.allocated)
            

            # Checa se o processo gera um evento (por exemplo, se ele precisa ser bloqueado)
            event = next(self.event_generator)
            if event:
                self.status = "blocked"
                self.event = event
        
        elif self.status == "blocked":
            # Tenta desbloquear o processo se não houver eventos de bloqueio
            event = next(self.event_generator)
            if not event:
                self.status = "ready"   
        
        # Verifica se o processo terminou a execução
        if self.cpu_demand <= 0:
            self.status = "finished" 
            
            
        self.history.append(self.status)
        
        
        
    def allocate_cpu_time(self, cpu_time : int = 0):
        self.allocated = max(0, cpu_time)
        
        if self.allocated > 0:
            self.status = 'running'
        else:
            self.status = 'ready' if not self.event else 'blocked'
        
    def metrics(self) -> dict:
        metrics = {
            "PID"  : self.pid,
            "CPU demand" : self.cpu_demand,
            "CPU allocated" : self.allocated,
            "Memory demand"  : self.memory_demand,
            "Priority" : self.priority,
            "Status" : self.status,
            "Continuous time in CPU" : self.continuous_cpu_time,
            "Created" : self.start,
            "End" : self.end
        }
        
        return metrics
        
    @classmethod
    def collect(cls) -> list:
             
        return [
            process.metrics() for process in cls.all()
        ]
        
    @classmethod
    def all(cls):
        return cls._instances.copy()
        
        
        
        