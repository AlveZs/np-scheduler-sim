class Job:
    number=1
    def __init__(self, task, executionTime, deadline):
        self.task = task
        Job.number = Job.number + 1
        self.executionTime = executionTime
        self.deadline = deadline
        self.state = 'ready'