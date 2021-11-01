from offlineProcedure import OfflineProcedure
from fileReader import loadDataFromFile
from colors import bcolors
import os
from scheduler import Scheduler

directory = 'tasksets'

for filename in os.scandir(directory):
    if filename.is_file():
        print(filename.path)
        processorsNumber, tasks = loadDataFromFile(filename.path)
        try:
            processorsNumberPrime, tasksOff, a, h, S, assignedTasks = OfflineProcedure(tasks, processorsNumber).taskAssigment()
            Scheduler(
                processorsNumber,
                processorsNumberPrime,
                tasksOff,
                a,h,
                S,
                assignedTasks
            )
        except ValueError as err:
            message = err.args[0]
            print(bcolors.FAIL + message + bcolors.ENDC)
        print("\n\n")
    break
