import datetime

class Process_Data:
    
    '''
        Contains data about a process like its current state, its group and
        when it was started
    '''
    
    def __init__(self, process, group = None, group_default = False):
        '''
            Initializes the process data. The process data should only be modified by
            the Process Manager.
        
            @param process: A function that takes the process data as a single parameter.
            @param group: The name of the group the process belongs to.
            @param group_default: If True then this is the process that the group will default
            to if the group's currently running process finishes or is interrupted.
        '''
        self.process = process
        self.children = []
        self.state = Process_Manager.STARTED
        self.group = group
        self.group_default = group_default
        self.start_time = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
        self.last_run_time = None       

class Process_Manager:
    
    # Only one process in a group can be running at a given point of time.
    # When a process in a group is started or resumed the process in the group
    # currently running is interrupted.
    INTERRUPTED = 1
    # When a process that has been interrupted it must be resumed before it can
    # be run again.
    RESUMED = 2
    # This is the first state a process must have when added to the process manager.
    STARTED = 3
    # When a process enters this state it is removed from the process manager.
    FINISHED = 4
    # A process in this state is executed periodically.
    RUNNING = 5
    
    def __init__(self):
        self.processes = {}
        self._time_of_last_run = None
    
    
    def start(self, process, group = None, group_default = False):
        '''
            Starts a process.
            
            @param process: A function that the Process Data as its only parameter.  
            The Process Data holds information like the process state and when it
            was last run. A process is called periodically if it is running. A
            process also called when it enters other states like STARTED or FINISHED.
            @param group: A string representing the group the process belongs to. Only
            one process can be running in a group at any point in time. The currently
            running process will be either INTERRUPTED if it is the group default or
            FINISHED if it isn't when this process starts.
            @param group_default: When the currently running process is finished then
            the INTERRUPTED group default process will be RESUMED.
            
        '''
        
        # Only add the process if it hasn't been added
        if process in self.processes:
            return False
        
        self.processes[process] = Process_Data(process, group, group_default)       
        
        # If this process is the default remove the current default
        if group is not None and group_default is True:
            for proc in self.processes.values():
                if proc.group is group and proc.group_default is True:
                    self.finish(proc)
                    break
        
        # Gives group control to this process
        self._set_group_process(process)
        
        # call the process
        self._call_process(process)

        
    def finish(self, process, call = True):
        '''
            Ends a process. The process is removed and control is given back to its
            group's default.
            
            @param process: The process that is finished.
            @param call: Calls the process with the FINISHED state if True
        '''
        
        # The process is now FINISHED. Get process data and remove the process
        process_data = self._get_process_data(process)
        del self.processes[process]
        
        # Alert the process that it has stopped
        if call: self._call_process(process)
        
        # Add the children of the process as a sequence
        self.start_sequence(process_data.children, process_data.group, process_data.group_default)
        
        # Give control back to the group default
        if process_data.group_default is False or len(process_data.children) is 0:
            group_default = self._get_group_default(process_data.group)
            if group_default:
                self._set_group_process(group_default)
        
        return True
        
    
    def start_sequence(self, processes, group = None, group_default = False):
        ''' 
            Creates a sequence of processes. If a group is given then each process
            in belongs to that group.
            
            @param processes: A list of processes that will be run in sequence.
            @param group: A string representing a group of processes. No two processes
            in a group can be running at the same time.
        '''
        
        if len(processes) is 0:
            return
        
        first_process = processes.pop(0)
        
        # Don't add the children if the process wasn't added
        if self.start(first_process, group, group_default):
            self.processes[first_process].children = processes
        
    
    def _get_group_default(self, group):
        
        if group:
            for proc, proc_data in self.processes.items():
                if proc_data.group is group and proc_data.group_default is True:
                    return proc
                
        return None
        
                
        
    def _set_group_process(self, process):
        ''' 
            Start or resume a process and interrupt all other processes in the group.
        '''
        
        process_data = self._get_process_data(process)

        if process_data.state is Process_Manager.INTERRUPTED:
            process_data.state = Process_Manager.RESUMED
            
         # Interrupt all the other processes in the group
        if process_data.group is not None:
            for proc, data in self.processes.items():
                if proc is process or proc.group is not process[group]:
                    continue
                
                proc.state = Process_Manager.INTERRUPTED
            
    
    def _call_process(self, process):
        
        process_data = self._get_process_data(process)    
        process(process_data)
                       
    def get_current_time(self):
        return (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()  
                
    def time_since_last_run(self, process):
        
        process_data = self._get_process_data(process)
        if process_data is None:
            return None
        
        return None if last_run is None else self.get_current_time() - process_data.last_run_time
    
    def time_since_start(self, process):
        
        process_data = self._get_process_data(process)
        if process_data is None:
            return None
        
        return self.get_current_time() - process_data.start_time
        
    def run(self):
        '''
            Executes each running process
        '''
        
        running_processes = {}
        
        for process, process_data in self.processes.items():
            if process_data.state is Process_Manager.RUNNING:
                running_processes[process] = process_data
        
        for process, process_data in running_processes():
            state = self._call_process(self, process)
            if state is Process_Manager.FINISHED:
                self.finish(process, False)
        
    def in_queue(self, process):
        return process in self.processes
    
    def _get_process_data(self, process):
        return None if process not in self.processes else self.processes[process]
    
    def get_state(self, process):
        return None if not self.in_queue(process) else self.processes[process].state