
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


from process_scheduler import *


    
    

def generate_dataset(n_processes=10):
    process_numbers = [random.randint(1, 5) for _ in range(n_processes)]
    interval_creation = [random.randint(1, 10) for _ in range(n_processes)]
    memory_demand = [random.randint(1, 10) for _ in range(n_processes)]
    cpu_demand = [ random.randint(1,5) for _ in range(n_processes)]
    event_generators = [[random.choice([True, False]) for _ in range(10)] for _ in range(n_processes)]
    
    return process_numbers, interval_creation, memory_demand, cpu_demand, event_generators


def main():
    
    process_numbers, interval_creation, memory_demand, cpu_demand, event_generators = generate_dataset()
    
    process_generator = ProcessGenerator(
        process_numbers=process_numbers,
        interval_creation=interval_creation,
        memory_demand=memory_demand,
        cpu_demand=cpu_demand,
        event_generators=event_generators
    )
    
    process_manager = ProcessManager(process_generator, memory=500, cpu=1, scheduling_algorithm=fcfs)
    
    process_generator.connect_to_manager(process_manager)
    
    
    stop_condition = lambda: process_manager.steps >= 50 
    
    
    process_manager.run_model(stop_condition)
        
if __name__ == "__main__":
    main()