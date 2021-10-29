from task import Task

def tasksetInfo(processorsNumber, tasks):
    totalUtilization = 0.0
    print("=========================================")
    print("Numero de processadores: ", processorsNumber)
    for task in tasks:
        taskUtilization = task.executionTime/task.deadline
        print("{} c: {} d: {} U: {}".format(
            task.name,
            task.executionTime,
            task.deadline,
            round(taskUtilization, 2)
        ))
        totalUtilization = totalUtilization + taskUtilization
    print("=========================================\n")
    print("Utilizacao total do sistema: ", round(totalUtilization / processorsNumber, 2))


def loadDataFromFile(filename):
    Task.number = 1
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
    tasksetInfo(processorsNumber, tasks)
    return processorsNumber, tasks