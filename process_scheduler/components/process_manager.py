from process_scheduler.components.process import*
from process_scheduler.components.scheduling_algorithms import *
from process_scheduler.components.process_generator import *

import json
import os

class ProcessManager:
    """
    Class responsible for representing the Process Manager.
    It is based on a 7-state model.
    """
    def __init__(self,
                 process_generator: object,
                 memory: int,
                 cpu_capacity: int,
                 scheduling_algorithm: callable = first_create_first_served,
                 priority_algorithm : callable = lambda process: process.start
                 ) -> None:
        """
        Args:
            process_generator : object -> Object responsible for generating specifications for new processes
            memory : int -> Memory capacity
            cpu : int -> CPU capacity
        """
        self.steps = 0
        self.memory = memory
        self.memory_idle = memory
        
        self.cpu = cpu_capacity
        self.cpu_idle = 0
        
        
        
        self.scheduling_algorithm = scheduling_algorithm
        self.priority_algorithm = priority_algorithm
        self.process_generator = process_generator
        
        self.new = []
        self.ready = []
        self.ready_suspend = []
        self.running = []
        self.blocked = []
        self.blocked_suspend = []
        self.exit = []
        
        self.agent_metrics = {
            'memory_usage': [self.memory_idle] * 3,
            'cpu_idle': [self.cpu_idle] * 3,
            'new' : [[]] * 3,
            'ready' : [[]]*3,
            'ready_suspend' : [[]]*3,
            'blocked' : [[]]*3,
            'blocked_suspend' : [[]]*3,
            'running' : [[]]*3,
            'exit' : [[]]*3
        }
        
        
    def monitor(self):
        """
        Monitor the system's memory, CPU usage, and process queues (including PID and allocated CPU),
        updating the metrics for the last 3 steps.
        """
        current_memory = max(0, self.memory_idle)  
        current_cpu = max(0, self.cpu_idle)  
        
        # Shift the memory and CPU data to the left and append new values
        self.agent_metrics['memory_usage'] = self.agent_metrics['memory_usage'][1:] + [current_memory]
        self.agent_metrics['cpu_idle'] = self.agent_metrics['cpu_idle'][1:] + [current_cpu]
        
        # Helper function to extract (pid, allocated_cpu) pairs from each process in the queue
        def extract_process_info(queue):
            return [(process.pid, process.allocated, process.cpu_demand, process.memory_demand) for process in queue]
        
        # Shift the process queues data to the left and append the current states of the queues
        self.agent_metrics['new'].append(extract_process_info(self.new))
        self.agent_metrics['ready'].append(extract_process_info(self.ready))
        self.agent_metrics['ready_suspend'].append(extract_process_info(self.ready_suspend))
        self.agent_metrics['running'].append(extract_process_info(self.running))
        self.agent_metrics['blocked'].append(extract_process_info(self.blocked))
        self.agent_metrics['blocked_suspend'].append(extract_process_info(self.blocked_suspend))
        self.agent_metrics['exit'].append(extract_process_info(self.exit))
        
    def run_model(self, stop_condition: callable) -> None:
        self.monitor()
        while not stop_condition():
            self.step()
            self.monitor()
            self.print()
            # input()
            os.system("clear")
        
        # Salvar as métricas ao final da execução
        self.save_metrics_to_json()
    
                
            
    
    def step(self):
        """
        Simulate one time step in the process management model.
        Handles state transitions based on the current state of processes.
        """
        
        self.steps += 1 
        
        
        self.process_generator.step() 
        
        # Verificando se há processos na lista de suspensos:
        for process in sorted(self.ready_suspend, key=self.priority_algorithm):
            
            self.ready_suspend.sort(key=self.priority_algorithm)
            self.ready.sort(key=self.priority_algorithm)

            if self.memory_idle < process.memory_demand:
                
                # Se houverem processos menos prioritarios bloqueados ocupando memória o suficiente para o processo ser levado para a memória principal 
                if sum([ p.memory_demand for p in self.blocked + self.ready if self.priority_algorithm(p) <= self.priority_algorithm(process)]) >= process.memory_demand:
                    
                    # Remove o primeiro item(menos prioritario) até ter espaço para carregar o processo
                    while self.memory_idle < process.memory_demand:
                        p = self.blocked.pop()
                        
                        self.blocked_suspend.append(p)
                        
                        self.memory_idle += p.memory_demand
                        
                        if self.blocked == []:
                            break
                
                    if self.memory_idle >= process.memory_demand:
                        # Carregando o processo para a memória principal
                        self.memory_idle -= process.memory_demand
                        self.ready.append(process)
                        self.ready_suspend.remove(process)
                    
                    else:
                        # Remove o primeiro item(menos prioritario) até ter espaço para carregar o processo
                        while self.memory_idle < process.memory_demand:
                            p = self.ready.pop()

                            self.ready_suspend.append(p)

                            self.memory_idle += p.memory_demand

                        # Carregando o processo para a memória principal
                        self.memory_idle -= process.memory_demand
                        self.ready.append(process)
                        self.ready_suspend.remove(process)
            else:
                self.memory_idle -= process.memory_demand
                self.ready.append(process)
                self.ready_suspend.remove(process)
                    
                    
        for process in self.running:
            if process.status == "blocked":
                self.running.remove(process) 
                process.allocate_cpu_time()    
                self.blocked.append(process) 
                
            if process.status == 'finished':
                self.running.remove(process)
                self.memory_idle += process.memory_demand 
                self.exit.append(process)     
                
                
                
        for process in self.blocked:
            if process.status != "blocked":
                if self.memory_idle <= process.memory_demand and self.ready_suspend == []:
                    self.blocked.remove(process)     
                    self.ready.append(process) 
                else:
                    self.blocked.remove(process)     
                    self.ready_suspend.append(process) 

        for process in self.blocked_suspend:
            if process.status != "blocked":
                self.blocked_suspend.remove(process)     
                self.ready_suspend.append(process) 
                
              
                    
        self.scheduling_algorithm(self)
        
        self.cpu_idle = self.cpu - sum([ process.allocated for process in self.running])
        
        for process in self.blocked + self.blocked_suspend + self.running:
            process.step()
        
        
        self.ready_suspend.extend(self.new)    
        self.new.clear()
        
    
    def print(self):
        """
        Print the current system metrics including memory, CPU, and process queues over the last 3 steps.
        """
        print("\n===== Monitoramento dos Últimos 3 Steps =====\n")

        # Mostrar uso de memória e CPU ociosa nos últimos 3 steps
        print("Uso de Memória (últimos 3 steps):")
        print(self.agent_metrics['memory_usage'])
        print("\nCPU Ociosa (últimos 3 steps):")
        print(self.agent_metrics['cpu_idle'])

        # Função auxiliar para formatar e exibir os dados de cada fila
        def print_queue_info(queue_name, queue_data):
            print(f"\nFila {queue_name} (últimos 3 steps):")
            for step, processes in enumerate(queue_data, 1):
                print(f"Step {step}: ", end="")
                if processes:
                    process_info = ", ".join([f"(PID: {pid}, CPU: {cpu}, CPU demand: {cpu_demand}, Memory demand: {mem_demand})" for pid, cpu, cpu_demand, mem_demand in processes])
                    print(process_info)
                else:
                    print("Nenhum processo")

        # Exibir informações das filas
        print_queue_info("New", self.agent_metrics['new'][-3:])
        print_queue_info("Ready", self.agent_metrics['ready'][-3:])
        print_queue_info("Ready Suspend", self.agent_metrics['ready_suspend'][-3:])
        print_queue_info("Running", self.agent_metrics['running'][-3:])
        print_queue_info("Blocked", self.agent_metrics['blocked'][-3:])
        print_queue_info("Blocked Suspend", self.agent_metrics['blocked_suspend'][-3:])
        print_queue_info("Exit", self.agent_metrics['exit'][-3:])

        print("\n=============================================\n") 



    def save_metrics_to_json(self) -> None:
        """
        Collects metrics from the process manager and processes, then saves them to a JSON file.

        Args:
            process_manager : object -> The instance of ProcessManager to collect metrics from.
            filename : str -> The name of the output JSON file (default is 'metrics.json').
        """
        # Coletar métricas de uso de memória e CPU ociosa
        metrics = {
            "steps": self.steps,
            "memory_usage": self.agent_metrics['memory_usage'],
            "cpu_idle": self.agent_metrics['cpu_idle'],
            "queues": {
                "new": self.agent_metrics['new'],
                "ready": self.agent_metrics['ready'],
                "ready_suspend": self.agent_metrics['ready_suspend'],
                "running": self.agent_metrics['running'],
                "blocked": self.agent_metrics['blocked'],
                "blocked_suspend": self.agent_metrics['blocked_suspend'],
                "exit": self.agent_metrics['exit']
            }
        }

        # Coletar métricas de todos os processos
        process_metrics = [process.metrics() for process in Process.all()]

        # Adicionar as métricas dos processos ao dicionário de métricas
        metrics["processes"] = process_metrics

        # Salvar as métricas em um arquivo JSON
        with open(f"metrics_{self.scheduling_algorithm.__name__}-{self.priority_algorithm.__name__}.json", "w") as json_file:
            json.dump(metrics, json_file, indent=4)
