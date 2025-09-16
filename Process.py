class Process:
    def __init__(self, name, arrivalTime, burstTime, originalBurstTime, completionTime, turnaroundTime, waitingTime, countChangeContext):
        self.name = name
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.originalBurstTime = originalBurstTime
        self.completionTime = completionTime
        self.turnaroundTime = turnaroundTime
        self.waitingTime = waitingTime
        self.countChangeContext = countChangeContext
