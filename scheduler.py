from event import Event
from job import Job
from eventTypes import EventTypes
from jobStates import JobStates
from processor import Processor

MAX_TIME = 31
class Scheduler:
    def __init__(
            self,
            processorsNumber,
            processorsNumberPrime,
            tasks,
            a,
            h,
            S,
            assignedTasks,
        ):
        self.processors = []
        for i in range(processorsNumber + processorsNumberPrime):
            self.processors.append(Processor()) 
        self.t = 0
        self.tasks = tasks
        self.readyJobs = [[] for i in range(len(self.processors))]
        self.processorsNumber = processorsNumber
        self.processorsNumberPrime = processorsNumberPrime
        self.a = a
        self.h = h
        self.S = S
        self.assignedTasks = assignedTasks
        self.nextJobArrival = 0
        self.agenda = []
        self.initializeAgenda()
        self.schedule(S, processorsNumber, processorsNumberPrime)

    def simulate(self, job, procIndex):
        cpu = self.processors[procIndex]
        if (job != None):
            currentJob = cpu.running
            job.executionTime = job.executionTime - 1
            print("{} => {} in time {}".format(cpu.name, job.task.name, self.t + 1))
            if (job.executionTime == 0):
                job.state = JobStates.FINISHED
                print("FINISHED {} execution".format(job.task.name))
                for readyJob in self.readyJobs[procIndex]:
                    if (readyJob == job):
                        self.readyJobs[procIndex].remove(job)
                        break
            else:
                job.state = JobStates.RUNNING
                cpu.running = job
            if (currentJob and (currentJob != job) and (currentJob.state != JobStates.FINISHED)):
                print("preempt")
        else:
            cpu.running = None

    def initializeAgenda(self):
        for task in self.tasks:
            event = Event(EventTypes.DEADLINE, task, self.t)
            self.agenda.append(event)

    def processEvent(self):
        if (self.agenda[0].time == self.t):
            while (len(self.agenda) > 0):
                if (self.agenda[0].time != self.t):
                    break
                event = self.agenda[0]
                if (event.eventType == EventTypes.DEADLINE):
                    self.createJob(event.obj)
                    arrivalEvent = Event(EventTypes.DEADLINE, event.obj, event.obj.deadline + self.t)
                    self.agenda.append(arrivalEvent)
                self.agenda.pop(0)


    def createJob(self, task):
        taskIndex = -1
        for taskI in range(len(self.tasks)):
            if self.tasks[taskI] == task:
                taskIndex = taskI
                break
        cpuIndex = self.assignedTasks[taskIndex]
        self.readyJobs[cpuIndex].append(
            Job(
                task,
                task.executionTime,
                task.deadline + self.t
            )
        )


    
    def EDF(self, processor):
        readyJobs = self.readyJobs[processor]
        if readyJobs:
            job = min(readyJobs, key=lambda x: x.deadline)    
            self.simulate(job, processor)


    def schedule(self, S, processorsNumber, processorsNumberPrime):
        while self.t <= MAX_TIME:
            self.processEvent()
            self.agenda.sort(key=lambda x: x.time)
            print("\n\n")
            print("In time {}".format(self.t + 1))
            for processor in range(processorsNumber):
                if (processorsNumberPrime > 0):
                    if (((self.t - self.offsets[processor] + S) % S) >= S- self.procsExec[processor]):
                        self.EDF(processor)
                    else:
                        stayIdle = True
                        for np in range(processorsNumber, processorsNumber + processorsNumberPrime):
                            npIndex = np - processorsNumber
                            for r in range(len(self.a[np])-2):
                                if ((self.a[npIndex][r] <= self.t) and (self.t < self.a[npIndex][r+1])):
                                    break
                            if (self.h[npIndex][r] == processor):
                                stayIdle = False
                                break
                        if (stayIdle == False):
                            self.EDF(np)
                else:
                    self.EDF(processor)
            print("\n\n")
            self.t = self.t + 1