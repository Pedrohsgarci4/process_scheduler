

class ProcessManager:
    """
    Class responsible for representing the Process Manager.
    It is based on a 7-state model.
    """
    def __init__(self, process_generator: object, scheduling_algorithm: callable, memory: int, cpu: int) -> None:
        """
        Args:
            process_generator : object -> Object responsible for generating specifications for new processes
            memory : int -> Memory capacity
            cpu : int -> CPU capacity
        """
        self.steps = 0
        self.memory = memory
        self.cpu = cpu
        
        self.scheduling_algorithm = scheduling_algorithm
        self.process_generator = process_generator
        
        self.new = []
        self.ready = []
        self.ready_suspend = []
        self.running = []
        self.blocked = []
        self.blocked_suspend = []
        self.exit = []
        
        self.agent_metrics = {
            'memory_usage': [self.memory] * 20,
            'cpu_idle': [self.cpu] * 20
        }
        
        
    def monitor(self):
        """
        Monitor the system's memory and CPU usage, updating the metrics for the last 20 steps.
        """
        
        current_memory = max(0, self.memory)  
        current_cpu = max(0, self.cpu )  
        
        # Shift the memory and CPU data to the left and append new values
        self.agent_metrics['memory_usage'] = self.agent_metrics['memory_usage'][1:] + [current_memory]
        self.agent_metrics['cpu_idle'] = self.agent_metrics['cpu_idle'][1:] + [current_cpu]
        
        
    def run_model(
         self,
         stop_condition : callable,
        ) -> None:
        
        self.monitor()
        while(not stop_condition()):
            self.step()
            self.monitor()
            
    
    def step(self):
        """
        Simulate one time step in the process management model.
        Handles state transitions based on the current state of processes.
        """
        
        self.steps += 1 
        
        
        new_processes = self.process_generator.step()
        
        self.new.extend(new_processes)   
                    
        self.scheduling_algorithm(self)
    
    
        
            
    

