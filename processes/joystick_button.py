from manager import *

class Joystick_Button(Process):
    
    def __init__(self, joystick, button):
        super().__init__()
        self.joystick = joystick
        self.button = button
        self.current_state = False
        self.event_listeners = {
            'when_pressed' : [],
            'when_released' : [],
            'while_pressed' : [],
            'while_released' : []                
        }
        
        Process_Manager.add(self)
        self.start()
        
    def get_button(self):
        return self.joystick.getRawButton(self.button)
        
    def on_start(self):
        self.current_state = self.get_button()
        
    def run(self, elapsed_time):
        
        prev_state = self.current_state
        self.current_state = self.get_button()
        
        if self.current_state:
            self.notify_listeners('while_pressed')
        else:
            self.notify_listeners('while_released')
            
        if prev_state is not self.current_state:
            if self.current_state:
                self.notify_listeners('when_pressed')
            else:
                self.notify_listeners('when_released')
            
        
    def notify_listeners(self, type):
        for listener in self.event_listeners[type]:
            listener()
            
    def add_listener(self, type, listener):
        self.event_listeners[type].append(listener)
            
    def when_pressed(self, listener):
        self.add_listener('when_pressed', listener)
        
    def when_released(self, listener):
        self.add_listener('when_released', listener)
        
    def while_pressed(self, listener):
        self.add_listener('while_pressed', listener)
        
    def while_released(self, listener):
        self.add_listener('while_released', listener)
        