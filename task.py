class Task:
    number=1
    def __init__(self, executionTime, deadline):
        self.name = "T" + str(Task.number)
        Task.number = Task.number + 1
        self.executionTime = executionTime
        self.deadline = deadline