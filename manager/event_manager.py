
class Event_Manager:

    def __init__(self):
        self.uid = 1
        self.listeners = {}
    
    def add_listener(self, event_name, callback):
        
        uid = self.uid = self.uid + 1
        
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        
        if callback not in self.listeners[event_name]:
            self.listeners[event_name].append(callback)
      
    def add_listeners(self, listener_map):
        for event_name, callback in listener_map.items():
            self.add_listener(event_name, callback)
            
    
    def remove_listener(self, event_name, callback):
        
        if event_name in self.listeners and callback in self.listeners[event_name]:
            self.listeners[event_name].remove(callback)
            
    def remove_all_listeners(self, event_name = None):
        ''' 
            Removes all the listeners for a specific event, or all listeners if
            no event name is given
        '''    
        
        if event_name is None:
            self.listeners = {}
        elif event_name in self.listeners:
            del self.listeners[event_name]
            
    
    def trigger(self, event_name, event_data = None):
        
        if event_name not in self.listeners:
            return
        
        for callback in self.listeners[event_name]:
            callback(event_data)