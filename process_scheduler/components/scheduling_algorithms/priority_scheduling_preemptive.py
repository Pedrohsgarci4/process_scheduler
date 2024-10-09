def priority_scheduling_preemptive(process_manager: object):
    
    process_manager.ready.sort(key=lambda process: process.priority, reverse=True)
    
    
    process_manager.running.sort(key=lambda process: process.priority)
    
   
    while process_manager.cpu_idle > 0 and process_manager.ready:
        current_process = process_manager.ready[0]
        
        for process in process_manager.running:
            if process.priority < current_process.priority:
                process_manager.running.remove(process)
                
                process_manager.cpu_idle += process.allocated
                
                process_manager.ready.append(process)
            else:
                break
        
        process_manager.ready.remove(current_process)
        
        allocated = min(current_process.cpu_demand, process_manager.cpu_idle)
        current_process.allocate_cpu_time(allocated)
        
        process_manager.cpu_idle -= allocated
        
        process_manager.running.append(current_process)
        
        process_manager.running.sort(key=lambda process: process.priority)
        
        
        
def priority_scheduling_non_preemptive(process_manager: object):
    process_manager.ready.sort(key=lambda process: process.priority, reverse=True)
    
    while process_manager.cpu_idle > 0 and process_manager.ready:
        current_process = process_manager.ready[0]
        
        process_manager.ready.remove(current_process)
        
        allocated = min(current_process.cpu_demand, process_manager.cpu_idle)
        current_process.allocate_cpu_time(allocated)
        
        process_manager.cpu_idle -= allocated
        
        process_manager.running.append(current_process)
        
        if current_process.cpu_demand == 0:
            process_manager.running.remove(current_process)
