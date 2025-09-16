from collections import deque
from Process import Process

class RoundRobin:
    def __init__(self, list):
        self.list = list
        self.queue = deque()
        self.quantum = 200
        self.current_time=0
        
    def reorderProcess(self, process: Process):
        process.burstTime -= self.quantum
        if process.burstTime >0:
            self.queue.append(process)
        else:
            process.completionTime = self.current_time
            process.turnaroundTime = self.current_time - process.arrivalTime
            process.waitingTime = process.turnaroundTime - process.originalBurstTime
    
    def runRoundRobin(self):
        processIndex =0
        
        while len(self.queue)> 0 or processIndex < len(self.list) :
            
            if processIndex < len(self.list) :
                for i in range(processIndex, len(self.list)):
                    if self.list[i].arrivalTime <= self.current_time :
                        if self.list[i] not in self.queue :
                            self.queue.append(self.list[i])
                        processIndex = i + 1
                    else :
                        break
                    
            if len(self.queue) > 0:
                currentProcess = self.queue.popleft()
                
                executionTime = min(self.quantum, currentProcess.burstTime)
                self.current_time += executionTime
                
                self.verify_process(processIndex)
                self.reorderProcess(currentProcess)
            else :
                self.current_time += 100
            
            
        self.print_final_table()

    
    
    
    def verify_process(self, process_index):
        if process_index < len(self.list):
            for i in range(process_index, len(self.list)):
                if self.list[i].arrivalTime <= self.current_time:
                    if self.list[i] not in self.queue:
                        self.queue.append(self.list[i])

    
    
        
    def print_final_table(self):
        print("\n" + "=" * 80)
        print("TABLA FINAL DE RESULTADOS")
        print("=" * 80)

        # Encabezados
        print(f"{'Proceso':<10} {'AT':<4} {'BT':<4} {'q':<4} {'CT':<4} {'TAT':<6} {'NTAT':<6} {'WT':<4}")
        print("-" * 80)

        for process in self.list:
            ntat = process.turnaroundTime / process.originalBurstTime

            print(f"{process.name:<10} "
                f"{process.arrivalTime:<4} "
                f"{process.originalBurstTime:<4} "
                f"{self.quantum:<4} "
                f"{process.completionTime:<4} "
                f"{process.turnaroundTime:<6} "
                f"{ntat:<6.2f} "
                f"{process.waitingTime:<4}")
            
            
if __name__ == "__main__":
    processes = [
        Process("P1", 100, 200, 200, 0, 0, 0, 0),
        Process("P2", 300, 500, 500, 0, 0, 0, 0),
        Process("P3", 600, 200, 200, 0, 0, 0, 0),
        Process("P4", 800, 600, 600, 0, 0, 0, 0),
        Process("P5", 1000, 700, 700, 0, 0, 0, 0),
        Process("P6", 1100, 300, 300, 0, 0, 0, 0),
    ]
    
    rr = RoundRobin(processes)
    rr.runRoundRobin()