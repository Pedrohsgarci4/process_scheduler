def first_come_first_served(process_manager : object):
    """
    First Core, First Served (FCFS) scheduling algorithm.
    """
    

    while process_manager.cpu_idle > 0 and process_manager.ready != []:
        process = process_manager.ready.pop(0)  
        process_manager.running.append(process) 
        
        allocated = min(process.cpu_demand, process_manager.cpu_idle) 
        
        process.allocate_cpu_time(allocated)
        process_manager.cpu_idle -= allocated
        
        
def first_create_first_served(process_manager : object):
    """
    First Created, First Served (FCFS) scheduling algorithm.
    Prioritizes processes with the smallest start time.
    """
    
    process_manager.ready.sort(key=lambda process: process.start)
    
    
    while process_manager.cpu_idle > 0 and process_manager.ready != []:
        process = process_manager.ready.pop(0)  
        process_manager.running.append(process) 
        
        allocated = min(process.cpu_demand, process_manager.cpu_idle) 
        
        process.allocate_cpu_time(allocated)
        process_manager.cpu_idle -= allocated
        
            
        
        
        