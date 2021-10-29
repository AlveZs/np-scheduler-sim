from task import Task

def loadDataFromFile(filename):
    tasks = []
    f = open(filename, "r")
    processorsNumber = int(f.readline().split()[1])           
    for line in f:
        l=[float(j) for j in line.split()]
        # period = float(l[-2])
        deadline = float(l[-1])
        execution = float(l[1])
        newTask = Task(execution, deadline)
        tasks.append(newTask)
    f.close()
    return processorsNumber, tasks