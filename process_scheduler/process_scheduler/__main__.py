from process_scheduler.components import *


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_and_update_graphs(process_manager: ProcessManager):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
    
    # First graph: Memory and CPU idle over the last 20 steps
    def update_resource_usage(i):
        ax1.clear()
        ax1.plot(process_manager.agent_metrics['memory_usage'], label='Memory Usage')
        ax1.plot(process_manager.agent_metrics['cpu_idle'], label='CPU Idle')
        ax1.set_ylim(0, process_manager.memory)  # Ensure the y-axis scales to memory capacity
        ax1.set_title(f'Memory and CPU Idle over Last 20 Steps (Step {process_manager.steps})')
        ax1.legend(loc='upper right')
    
    # Second graph: Queue visualization
    def update_queue_status(i):
        ax2.clear()
        queues = [process_manager.new, process_manager.ready, process_manager.ready_suspend, 
                  process_manager.running, process_manager.blocked, process_manager.blocked_suspend, 
                  process_manager.exit]
        queue_names = ['New', 'Ready', 'Ready Suspend', 'Running', 'Blocked', 'Blocked Suspend', 'Exit']
        
        # Visualize each queue as a horizontal bar
        for idx, queue in enumerate(queues):
            ax2.text(0, idx, f'{queue_names[idx]}: {queue}', va='center', ha='left')
        
        ax2.set_yticks(range(len(queue_names)))
        ax2.set_yticklabels(queue_names)
        ax2.set_xlim(-0.5, 10)  # Adjust based on expected queue sizes
        ax2.set_title(f'Process Queues (Step {process_manager.steps})')

    # Combine both update functions into one animation
    ani = FuncAnimation(fig, lambda i: (update_resource_usage(i), update_queue_status(i)), interval=1000)
    
    plt.tight_layout()
    plt.show()
    
def main():
    pass
    
if __name__ == "__main__":
    main()