class Event:
    job=1
    def __init__(self, eventType, obj, time):
        self.eventType = eventType
        self.obj = obj
        self.time = time