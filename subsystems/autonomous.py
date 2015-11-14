import wpilib
from manager import *
from enum import Enum
from common import height_levels as hl


class Autonomous:
    
    Modes = Enum('Modes', 'DO_NOTHING MOVE_FORWARD ONE_OBJECT')
    
    def auto_move_forward(self, process):
        
        if process.state is Process_Manager.START:
            self.robot.drive.tank(1, 1)
        
        elif data.state is Process_Manager.RUNNING:
            if process.time_since_start > 3:
                self.robot.drive.tank(0, 0)
                return Process_Manager.FINISHED

    def auto_one_object(self, process):
        
        if state is Process_Manager.START:
            self.robot.grabber_lift.clamp()
            process.step = 1
            
        elif state is Process_Manager.RUNNING:
            if process.step is 1 and process.time_since_start > 1:
                self.robot.grabber_lift.prepare_to_move_to_position(hl.START_HEIGHT + hl.TOTE_HEIGHT)
                self.robot.grabber_lift.move_to_position()
                process.step = 2
                
            if process.step is 2:
                return Process_Manager.FINISHED
    
    def __init__(self, robot):
        self.mode = Autonomous.Modes.DO_NOTHING
        
        # Change the autonomous mode that is run if the user selects one on the dashboard
        Event_Manager.add_listener('dashboard.updated', self.auto_mode_changed)
        
        # Run the autonomous mode that is selected
        Event_Manager.add_listener('auto.init', self.start_auto)
        
    def auto_mode_changed(self, event):
        if event['key'] is 'Autonomous Mode':
            self.mode = event['value']
            
    def start_auto(self, event):
        
        autonomous = None
        
        if self.mode is Autonomous.Modes.DO_NOTHING: 
            pass
        elif self.mode is Autonomous.Modes.MOVE_FORWARD: 
            autonomous = Auto_Move_Forward() 
        elif self.mode is Autonomous.Modes.ONE_OBJECT: 
            autonomous = Auto_One_Object()
        
        if autonomous:   
            Process_Manager.start(autonomous)