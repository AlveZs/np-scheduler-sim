class Processor:
    number=1
    def __init__(self):
        self.name = "P" + str(Processor.number)
        Processor.number = Processor.number + 1
        self.running = None
        self.isRunning = False