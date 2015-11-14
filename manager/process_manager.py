import datetime

class Process_Manager:
    
    def __init__(self):
        self.processes = {}
        self._time_of_last_run = None
    
    
    def add(self, process):
        
        if not self.in_queue(process):
            self.processes.append(process)
    
    def add_sequence(self, processes):
        
        
        
        # don't add processes if any of them are in the queue
        for process in processes:
            if self.in_queue(process):
                return False
        
        # add the processes
        for i in range(0, len(processes) - 1):
            processes[i].add_child(processes[i + 1])
            
            
        self.add[processes[0]]
        return True
    
    def remove(self, pid):
        
        if not self.in_queue(pid):
            return False
        
        del self.processes[pid]
        
        return True
    
    def run(self):
        
        # get elapsed time since last run
        time_since_last_run = 0
        
        now = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
        if self._time_of_last_run is not None:
            time_since_last_run = now - self._time_of_last_run
            
        self._time_of_last_run = now
        
        # add all child processes that are done
        children_to_add = []
        for process in self.processes:
            if process.get_state() == Process.State.FINISHED:
                children_to_add.extend(process.get_children())
                
        # remove all processes that are done or have failed
        self.processes = filter(lambda process: process.get_state() is not Process.States.FINISHED and 
                                    process.get_state() is not Process.States.FAILED, self.proceses)
                
        # add the children to the list
        self.processes.extend(children_to_add)
             
        # get all proccesses that are currently running and run them
        processes_to_run = filter(lambda process: process.running(), self.processes)
        
        for process in processes_to_run:
            if process.is_finished():
                process.finish()
            else:
                if process.has_run:
                    process.run(time_since_last_run)
                else:
                   process.run(0) 
                   process.has_run = True
    
    def in_queue(self, pid):
        return pid in self.processes
