def first_come_first_served_modificated(self):
    # Manipulando as transferencias entre a fila 'ready_suspend', 'new' e 'ready'
    for process in self.ready_suspend:
        if self.memory - process.memory < 0:
            less_priority_processes_blocked = sorted([ p for p in self.ready if p.start > process.start], key=lambda p: p.start, reverse=True)
            less_priority_processes_ready = sorted([ p for p in self.ready if p.start > process.start], key=lambda p: p.start, reverse=True)
            
            memory_demand_less_priority_processes = sum(map(lambda p: p.memory, less_priority_processes_ready))
            memory_demand_less_priority_processes += sum(map(lambda p: p.memory, less_priority_processes_blocked))
            
            if memory_demand_less_priority_processes >= process.memory:
                pass
            if sum(map(lambda p: p.memory, less_priority_processes_ready)) >= process.memory:
                for p in less_priority_processes_ready:
                    if self.memory - process.memory <= 0:
                        self.ready.remove(p)
                        self.ready_suspend.append(p)
                        self.memory += p.memory
                        
                    else:
                        break