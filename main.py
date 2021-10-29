from offlineProcedure import OfflineProcedure
from fileReader import loadDataFromFile
import os

directory = 'tasksets'

for filename in os.scandir(directory):
    if filename.is_file():
        print(filename.path)
        processorsNumber, tasks = loadDataFromFile(filename.path)
        try:
            OfflineProcedure(tasks, processorsNumber)
            print("\n\n")
        except ValueError as err:
            message, assigments = err.args
            print(message)
            print(assigments)