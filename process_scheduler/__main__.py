
import random


from process_scheduler import *


    


def generate_dataset(n_processes=10):
    process_numbers = [random.randint(1, 3) for _ in range(n_processes)]
    interval_creation = [random.randint(1, 5) for _ in range(n_processes)]
    memory_demand = [random.randint(10, 30) for _ in range(n_processes)]
    cpu_demand = [ random.randint(1,5) for _ in range(n_processes)]
    event_generators = [[random.choice([True, False, False]) for _ in range(15)] for _ in range(n_processes)]
    
    return process_numbers, interval_creation, memory_demand, cpu_demand, event_generators





if __name__ == "__main__":
    import argparse
    
    
    parser = argparse.ArgumentParser(description="")
    
    parser.add_argument("scheduling_algorithm", help="Scheduling algorithm name.")

    parser.add_argument("-p", "--priority_algorithm", help="Priority algorithm name.")
    
    parser.add_argument("-t", "--ticks", type=int, help="Number of steps in the simulation.")
    
    parser.add_argument("-c", "--cpu_capacity", type=int, help="CPU capacity value.")
    
    parser.add_argument("-s", "--seed", type=int, help="Seed to generate the process dataset.")
    


    
    args = parser.parse_args()
    
    
    random.seed( int(args.seed) if args.seed else 1)
    
    
    priority_algorithms = {
        "first_come_highest_priority"  : lambda x: 0, # Will not change the order of the queues
        "priority" : lambda p: p.priority,
        "moment_creation" : lambda p: p.start,# Sort by the time it was created
    }
    
    process_numbers, interval_creation, memory_demand, cpu_demand, event_generators = generate_dataset()
    
    process_generator = ProcessGenerator(
        process_numbers=process_numbers,
        interval_creation=interval_creation,
        memory_demand=memory_demand,
        cpu_demand=cpu_demand,
        event_generators=event_generators
    )
    
    scheduling_algorithm = globals() [args.scheduling_algorithm]
    
    if not callable(scheduling_algorithm):
        raise Exception("The expected parameter must be the name of an already defined function")
    
    
    if args.priority_algorithm in priority_algorithms:
        priority_algorithm = priority_algorithms[args.priority_algorithm]
    else:
        raise Exception("The expected parameter must be the name of an already defined function")
    
    
    process_manager = ProcessManager(
        process_generator, 
        memory=500, 
        cpu_capacity= int(abs(args.cpu_capacity)) if args.cpu_capacity else 1,
        scheduling_algorithm=scheduling_algorithm,
        priority_algorithm=priority_algorithm,
        )
    
    process_generator.connect_to_manager(process_manager)
    
    
    stop_condition = (lambda: process_manager.steps >= int(args.ticks) ) if args.ticks else lambda: process_manager.steps >= 50
    
    
    process_manager.run_model(stop_condition)
    
    
    
    
    
    
    