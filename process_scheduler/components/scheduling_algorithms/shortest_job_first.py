def shortest_job_first(process_manager):
    """
    Shortest Job First scheduling algorithm (non-preemptive).
    """
    # Ordenar a fila Ready com base no tempo de execução estimado dos processos
    process_manager.ready.sort(key=lambda process: process.cpu_demand)

    while process_manager.cpu_idle > 0 and process_manager.ready != []:
        # Selecionar o processo com o menor tempo de execução
        process = process_manager.ready.pop(0)  
        process_manager.running.append(process)  
        
        allocated = min(process.cpu_demand, process_manager.cpu_idle) 
        
        process.allocated_cpu_time(allocated)
        process_manager.cpu_idle -= allocated