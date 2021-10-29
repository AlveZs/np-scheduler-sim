from offlineProcedure import OfflineProcedure
from fileReader import loadDataFromFile

processorsNumber, tasks = loadDataFromFile("tasks.txt")
OfflineProcedure(tasks, processorsNumber)