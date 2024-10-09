quantum = 3

def round_robin(process_manager : object):
    global quantum
    
    for process in process_manager.running:
        if process.continuos_cpu_time >= quantum:
            process_manager.running.remove(process)
            process_manager.cpu_idle += process.allocated
            process.allocate_cpu_time()
            process_manager.ready.append(process)
            
            
    
    while process_manager.cpu_idle > 0 and process_manager.ready != []:
        process = process_manager.ready.pop(0)  
        process_manager.running.append(process)  
        
        allocated = min(process.cpu_demand, process_manager.cpu_idle) 
        allocated = max(allocated, quantum)
        
        process.allocate_cpu_time(allocated)
        process_manager.cpu_idle -= allocated
            