from task import Task
import sys
import math

class OfflineProcedure:
    def __init__(self, tasks, processorsNumber):
        self.S = 0
        self.processorsNumber = processorsNumber
        self.processorsCaps = []
        self.processorsUtilization = []
        self.unassignedTasksExist = True;
        self.tasks = tasks
        self.tasksNumber = len(self.tasks)
        self.taskAssigned = [-1] * self.tasksNumber
        self.firstTaskUnassigned = 0
        self.notionalCap = 0
        self.offsets = [0] * self.processorsNumber
        self.procsExec = [0.0] * self.processorsNumber
        self.taskAssigment(self.processorsNumber, self.tasksNumber, self.tasks)

    def inflate(self, U):
        return (2*U) / (1+U)

    def deflate(self, U):
        return U / (2-U)
    
    def enlargeArraysUandAandCAPby(self, size):
        for i in range(self.processorsNumber, size):
            self.processorsUtilization.append(0.0)
    
    def reindexTasksInHFOrder(self):
        return self.tasks.sort(key=lambda task: (task.executionTime / task.deadline), reverse = True)   

    def taskAssigment(self, processorsNumber, tasksNumber, tasks):
        # stage 1
        self.reindexTasksInHFOrder()
        for p in range(processorsNumber):
            self.processorsCaps.append(1)
            self.processorsUtilization.append(0)

        # first-fit
        for i in range(tasksNumber):
            currentProcessor = 0
            while (currentProcessor < processorsNumber):
                taskUtilization = tasks[i].executionTime / tasks[i].deadline
                if (self.processorsUtilization[currentProcessor] + taskUtilization <= self.processorsCaps[currentProcessor]):
                    self.taskAssigned[i] = currentProcessor;
                    self.processorsUtilization[currentProcessor] = self.processorsUtilization[currentProcessor] + taskUtilization
                    break
                else:
                    currentProcessor = currentProcessor + 1
            if ((i + 1 == tasksNumber) and (self.taskAssigned[i] != -1)):
                self.unassignedTasksExist = False
            if (self.taskAssigned[i] == -1):
                self.firstTaskUnassigned = i
        
        if (self.unassignedTasksExist):
            # stage 2
            S = tasks[0].deadline
            for i in range(tasksNumber):
                if (tasks[i].deadline < S):
                    S = tasks[i].deadline

            for p in range(processorsNumber):
                self.procsExec[p] = self.inflate(self.processorsUtilization[p]) * S
                self.notionalCap = self.notionalCap + (1 - (self.procsExec[p] / S))
            for p in range(processorsNumber-1):
                self.offsets[p+1] = round(self.offsets[p] + S - self.procsExec[p], 2)
            
            processorsNumberPrime = math.floor(round(self.notionalCap, 2))
            self.enlargeArraysUandAandCAPby(processorsNumber + processorsNumberPrime + 1)
            for p in range (processorsNumber, processorsNumber + processorsNumberPrime):
                self.processorsCaps.append(1); #full-capacity notional CPU
            self.processorsCaps.append(self.deflate(round(self.notionalCap, 2)) - processorsNumberPrime)

            a = [[None for i in range(processorsNumber + 1)] for j in range(processorsNumber, processorsNumber + processorsNumberPrime+1)]
            h  = [[None for i in range(processorsNumber)] for j in range(processorsNumber, processorsNumber + processorsNumberPrime+1)]
            
            currentProcessor = 0

            # now create notional CPUs
            for p in range(processorsNumber, (processorsNumber - 1) + processorsNumberPrime + 1):
                pIndex = p - processorsNumber
                stop = False
                a[pIndex][0] = 0
                r = 1
                while (stop == False):
                    end = round(S * self.inflate(self.processorsCaps[p]), 2)
                    a[pIndex][r] = min(round(a[pIndex][r-1] + S - self.procsExec[currentProcessor], 2), end)
                    h[pIndex][r-1] = currentProcessor
                    if (a[pIndex][r] == end):
                        stop = True
                    else:
                        r = r+1
                        currentProcessor = currentProcessor+1

            for i in range(self.firstTaskUnassigned, tasksNumber):
                currentProcessor = processorsNumber
                while (currentProcessor <= processorsNumber + processorsNumberPrime + 1):
                    taskUtilization = tasks[i].executionTime / tasks[i].deadline
                    if (self.processorsUtilization[currentProcessor] + taskUtilization <= self.processorsCaps[currentProcessor]):
                        self.taskAssigned[i] = currentProcessor;
                        self.processorsUtilization[currentProcessor] = self.processorsUtilization[currentProcessor] + taskUtilization
                        break
                    else:
                        currentProcessor = currentProcessor + 1
                if (self.taskAssigned[i] == -1):
                    sys.exit("Nao foi possivel alocar todas as tarefas")
                    return 0

        print("Tarefas alocadas com sucesso")
        return 1