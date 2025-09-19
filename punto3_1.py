from collections import deque
from Process import Process
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class RoundRobin:
    def __init__(self, list):
        self.list = list
        self.queue = deque()
        self.quantum = 200
        self.current_time=0
        self.gantt_chart = []
        self.execution_history = []
        
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
                
                start_time = self.current_time
                executionTime = min(self.quantum, currentProcess.burstTime)
                self.current_time += executionTime
                
                self.gantt_chart.append({
                    'process': currentProcess.name,
                    'start': start_time,
                    'end': self.current_time,
                    'duration': executionTime
                })
                
                self.execution_history.append({
                    'time': f"{start_time}-{self.current_time}",
                    'process': currentProcess.name,
                    'remaining_burst': currentProcess.burstTime - executionTime,
                    'quantum_used': executionTime
                })
                
                self.verify_process(processIndex)
                self.reorderProcess(currentProcess)
            else :
                start_time = self.current_time
                self.current_time += 100
                self.gantt_chart.append({
                    'process': 'IDLE',
                    'start': start_time,
                    'end': self.current_time,
                    'duration': 100
                })
            
        self.draw_gantt_chart()
        results = self.print_final_table()
        return results

    
    
    
    def verify_process(self, process_index):
        if process_index < len(self.list):
            for i in range(process_index, len(self.list)):
                if self.list[i].arrivalTime <= self.current_time:
                    if self.list[i] not in self.queue:
                        self.queue.append(self.list[i])

    def draw_gantt_chart(self):
        """Dibuja el diagrama de Gantt usando caracteres ASCII"""
        print("\n" + "=" * 100)
        print("DIAGRAMA DE GANTT - ROUND ROBIN")
        print("=" * 100)
        
        print("\nHistorial de Ejecución:")
        print(f"{'Tiempo':<12} {'Proceso':<10} {'Quantum':<8} {'Burst Restante':<15}")
        print("-" * 50)
        for entry in self.execution_history:
            print(f"{entry['time']:<12} {entry['process']:<10} {entry['quantum_used']:<8} {entry['remaining_burst']:<15}")
        
        print(f"\nDiagrama de Gantt:")
        print("Tiempo: ", end="")
        
        for i, interval in enumerate(self.gantt_chart):
            if i == 0:
                print(f"{interval['start']:<8}", end="")
            print(f"{interval['end']:<8}", end="")
        print()
        
        print("        ", end="")
        for interval in self.gantt_chart:
            duration_chars = max(6, len(str(interval['end'] - interval['start'])))
            bar = "█" * duration_chars
            print(f"|{bar:<6}|", end="")
        print()
        
        print("Proceso:", end="")
        for interval in self.gantt_chart:
            process_name = interval['process']
            print(f"  {process_name:<6}", end="")
        print()
        
    def draw_gantt_chart_matplotlib(self):
        """Dibuja el diagrama de Gantt usando matplotlib"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            import numpy as np
            
            fig, ax = plt.subplots(figsize=(15, 8))
            colors = {'P1': 'lightblue', 'P2': 'lightgreen', 'P3': 'lightcoral', 
                     'P4': 'lightyellow', 'P5': 'lightpink', 'P6': 'lightgray', 'IDLE': 'white'}
            
            y_pos = 0
            height = 0.8
            
            for interval in self.gantt_chart:
                start = interval['start']
                duration = interval['duration']
                process = interval['process']
                
                color = colors.get(process, 'lightsteelblue')
                
                rect = patches.Rectangle((start, y_pos), duration, height, 
                                       linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)
                
                ax.text(start + duration/2, y_pos + height/2, process, 
                       ha='center', va='center', fontweight='bold')
                
                ax.text(start, y_pos - 0.1, str(start), ha='center', va='top', fontsize=8)
                ax.text(start + duration, y_pos - 0.1, str(start + duration), ha='center', va='top', fontsize=8)
            
            ax.set_xlim(0, self.current_time + 100)
            ax.set_ylim(-0.5, 1.5)
            ax.set_xlabel('Tiempo', fontsize=12)
            ax.set_title(f'Diagrama de Gantt - Round Robin (Quantum = {self.quantum})', fontsize=14, fontweight='bold')
            ax.set_yticks([])
            
            ax.grid(True, axis='x', alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("Matplotlib no está instalado. Mostrando solo el diagrama ASCII.")
            return False
        return True

    
    
        
    def print_final_table(self):
        print("\n" + "=" * 100)
        print("TABLA FINAL DE RESULTADOS - ROUND ROBIN")
        print("=" * 100)
        
        print(f"Quantum: {self.quantum}")
        print(f"Tiempo total de simulación: {self.current_time}")
        print()

        print(f"{'Proceso':<10} {'AT':<6} {'BT':<6} {'CT':<6} {'TAT':<6} {'WT':<6} {'NTAT':<8}")
        print("-" * 100)
        print(f"{'(Name)':<10} {'(ms)':<6} {'(ms)':<6} {'(ms)':<6} {'(ms)':<6} {'(ms)':<6} {'(ratio)':<8}")
        print("-" * 100)

        total_tat = 0
        total_wt = 0
        total_ntat = 0

        for process in self.list:
            ntat = process.turnaroundTime / process.originalBurstTime if process.originalBurstTime > 0 else 0
            
            total_tat += process.turnaroundTime
            total_wt += process.waitingTime
            total_ntat += ntat

            print(f"{process.name:<10} "
                f"{process.arrivalTime:<6} "
                f"{process.originalBurstTime:<6} "
                f"{process.completionTime:<6} "
                f"{process.turnaroundTime:<6} "
                f"{process.waitingTime:<6} "
                f"{ntat:<8.2f}")
        
        print("-" * 100)
        
        num_processes = len(self.list)
        avg_tat = total_tat / num_processes
        avg_wt = total_wt / num_processes
        avg_ntat = total_ntat / num_processes
        
        print(f"{'PROMEDIOS:':<10} {'':>6} {'':>6} {'':>6} {avg_tat:<6.1f} {avg_wt:<6.1f} {avg_ntat:<8.2f}")
        print()
        
        print("Leyenda:")
        print("AT  = Arrival Time (Tiempo de llegada)")
        print("BT  = Burst Time (Tiempo de ráfaga)")
        print("CT  = Completion Time (Tiempo de finalización)")
        print("TAT = Turnaround Time (Tiempo de retorno) = CT - AT")
        print("WT  = Waiting Time (Tiempo de espera) = TAT - BT")
        print("NTAT= Normalized TAT (TAT normalizado) = TAT / BT")
        
        print("\n" + "=" * 50)
        print("Intentando mostrar diagrama de Gantt con matplotlib...")
        if not self.draw_gantt_chart_matplotlib():
            print("Mostrando diagrama ASCII como alternativa.")
            
        return {
            'avg_turnaround_time': avg_tat,
            'avg_waiting_time': avg_wt,
            'avg_normalized_tat': avg_ntat,
            'total_time': self.current_time
        }
            
            
if __name__ == "__main__":
    processes = [
        Process("P1", 100, 200, 200, 0, 0, 0, 0),
        Process("P2", 300, 500, 500, 0, 0, 0, 0),
        Process("P3", 600, 200, 200, 0, 0, 0, 0),
        Process("P4", 800, 600, 600, 0, 0, 0, 0),
        Process("P5", 1000, 700, 700, 0, 0, 0, 0),
        Process("P6", 1100, 300, 300, 0, 0, 0, 0),
    ]
    
    print("SIMULACIÓN DE ROUND ROBIN")
    print("=" * 80)
    print("Procesos a simular:")
    print(f"{'Proceso':<10} {'Arrival Time':<15} {'Burst Time':<15}")
    print("-" * 40)
    for p in processes:
        print(f"{p.name:<10} {p.arrivalTime:<15} {p.originalBurstTime:<15}")
    
    rr = RoundRobin(processes)
    print(f"\nQuantum: {rr.quantum} ms")
    print("\nIniciando simulación...\n")
    results = rr.runRoundRobin()
    
    print(f"\n{'='*80}")
    print("RESUMEN DE LA SIMULACIÓN")
    print(f"{'='*80}")
    print(f"Tiempo total de ejecución: {results['total_time']} ms")
    print(f"Tiempo promedio de retorno: {results['avg_turnaround_time']:.1f} ms")
    print(f"Tiempo promedio de espera: {results['avg_waiting_time']:.1f} ms")
    print(f"TAT normalizado promedio: {results['avg_normalized_tat']:.2f}")
    print(f"{'='*80}")