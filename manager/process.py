from enum import Enum
import datetime

class Process:
    
    States = Enum('States', 'NOT_STARTED RUNNING FINISHED FAILED')
    
    def __init__(self):
        self.state = Process.States.NOT_STARTED
        self.start_time = None
        self.has_run = False
        
    def get_state(self):
        return self.state
    
    def start(self):
        self.state = Process.States.RUNNING
        self.on_start()
        self.start_time = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
    
    def time_since_start(self):
        if self.start_time is None:
            return 0
        
        now = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
        return now - self.start_time
    
    def fail(self):
        self.state = Process.States.FAILED
        self.on_fail()
    
    def finish(self):
        self.state = Process.States.FINISHED
        self.on_finish()
        
    def on_start(self):
        pass
    
    def on_finish(self):
        pass
    
    def on_fail(self):
        pass
    
    def run(self, time_since_last_run):
        pass
    
    def is_finished(self):
        return False
    
    
    
    