from .event_manager import Event_Manager as EM
from .process_manager import Process_Manager as PM
from wpilib import IterativeRobot

Event_Manager = EM()
Process_Manager = PM()

class EventRobot(IterativeRobot):
    
    def __init__(self):
        super().__init__()
        Event_Manager.remove_all_listeners()
    
    def autonomousInit(self):
        Event_Manager.trigger('auto.init')      
    
    def autonomousPeriodic(self):
        Event_Manager.trigger('auto.periodic')
    
    def teleopInit(self):
        Event_Manager.trigger('teleop.init')
    
    def teleopPeriodic(self):
        Event_Manager.trigger('teleop.periodic')