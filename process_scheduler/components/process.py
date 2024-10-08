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
        
        self.start = start
        self.allocated = 0
        self.cpu_demand = cpu_demand
        self.memory_demand = memory_demand
        self.priority = priority
        
        
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
            self.status = "running"
            
            print(self.cpu_demand)
            # Executar o processo e reduzir a demanda de CPU
            self.cpu_demand = max(0, self.cpu_demand - self.allocated)  # Garante que não seja menor que 0
            
            print(self.cpu_demand)

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
        
        
    def allocated_cpu_time(self, cpu_time : int = 0):
        self.allocated = cpu_time
        
    def metrics(self):
        metrics = {
            "status" : self.status,
            "PID" : self.pid,
            "CPU Demand" : self.cpu_demand,
            "Memory Demand" : self.memory_demand
        }
        
        return metrics
    
    @classmethod
    def all(cls):
        return deepcopy(cls._instances)
        
        
        
        