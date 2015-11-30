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
        self.process_groups = {}
        self.single_processes = {}
        self._time_of_last_run = None


    def add_group(self, name, default_process = None):

            process_data = Process_Data(default_process, name, True) if default_process else None

            self.process_groups = {
                default_process : process_data,
                current_process : None
            }

            # call the process
            self._call_process(process_data)
    
    
    def start(self, process, group = None):
        '''
            Starts a process.
            
            @param process: A callable that the Process Data as its only parameter.  
            The Process Data holds information like the process state and when it
            was last run. A process is called periodically if it is running. A
            process also called when it enters other states like STARTED or FINISHED.
            @param group: A string representing the group the process belongs to. Only
            one process can be running in a group at any point in time. The currently
            running process will be either INTERRUPTED if it is the group default or
            FINISHED if it isn't when this process starts.
        '''

        process_data = Process_Data(process, group, group_default)
        
        if group is None:
            self.single_processes[process] = process_data
            self._call_process(process_data)

        elif group in self.process_groups:

            process_group = self.process_groups[group]

            if process_group['current_process']:
                process_group['current_process'].state = Process_Manager.FINISHED
                self._call_process(process_group['current_process'])

            process_group['current_process'] = process_data

            if process_group['default_process'] and process_group['default_process'].state is not Process_Manager.INTERRUPTED:
                process_group['default_process'].state = Process_Manager.INTERRUPTED
                self._call_process(process_group['default_process'])

        else:
            return False

        self._call_process(process_data)
        return True

    def start_sequence(self, processes, group = None):
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
        if self.start(first_process, group):

            process_data = None

            if group in self.process_groups:
                process_data = self.process_groups[group]['current_process']
            else:
                process_data = self.single_processes[first_process]

            process_data.children = processes
        

        
    def finish(self, process = None, group = None):
        '''
            Ends the currently running process 
            
            @param process:
            @param group:
        '''
        
        if process in self.single_processes:
            process_data = self.single_processes[process]
            process_data.state = Process_Manager.FINISHED
            self._call_process(process_data)
            del self.single_processes[process_data]
            self.start_sequence(process_data.children, None)

        elif group in self.process_groups:
            process_group = self.process_groups[group]
            process_data = process_group['current_process']
            if process_data:
                if process_data.children and len(process_data.children) > 0:
                    self.start_sequence(process_data.children, group)
                else:
                    process_data.state = Process_Manager.FINISHED
                    self._call_process(process_data)
                    process_group['current_process'] = None
                    default_process_data = process_group['default_process']
                    if default_process_data:
                        default_process_data.state = Process_Manager.RESUMED
                        self._call_process(default_process_data)
        
        
    
    def _get_group_default(self, group):
        
        if group in self.group_processes:
            return self.group_processes[group]['default_process']
                
        return None
        
    
    
    def _call_process(self, process_data):
        if process_data:
            process_data.process(process_data)
                       
    def get_current_time(self):
        return (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()  
                
    def time_since_last_run(self, process_data):

        if process_data is None or process_data.last_run_time is None:
            return None
        
        return self.get_current_time() - process_data.last_run_time
    
    def time_since_start(self, process_data):
        
        if process_data is None:
            return None
        
        return self.get_current_time() - process_data.start_time
        
    def run(self):
        '''
            Executes each running process
        '''

        # Run group processes
        for group in self.group_processes.values():
            if group.current_process and group.current_process.state is Process_Manager.RUNNING:
                group.current_process.process(group.current_process)
            elif group.default_process and group.default_process.state is Process_Manager.RUNNING:
                group.default_process.process(group.default_process)

        # Run single processes
        running_processes = {}
        
        for process, process_data in self.single_processes.items():
            if process_data.state is Process_Manager.RUNNING:
                running_processes[process] = process_data
        
        for process, process_data in running_processes():
            self._call_process(self, process)
        
    def in_queue(self, process):
        return process in self.processes
    
    def _get_process_data(self, process):
        return None if process not in self.processes else self.processes[process]
    
    def get_state(self, process):
        return None if not self.in_queue(process) else self.processes[process].state