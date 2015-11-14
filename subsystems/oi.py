from networktables import NetworkTable
from wpilib.joystick import Joystick
from processes.joystick_button import Joystick_Button
from common import logitec_controller as lc
from manager import *
from subsystems.autonomous import Autonomous
from wpilib.sendablechooser import SendableChooser
from wpilib.smartdashboard import SmartDashboard

class OI:
    
    def __init__(self, robot):
        self.robot = robot
        
        
        # update OI with logs
        Event_Manager.add_listeners({
            'auto.periodic' : self.log,
            'teleop.periodic' : self.log
        })
        
        # notify listeners when SmartDashboard is updated
        sd = NetworkTable.getTable('SmartDashboard')
        sd.addTableListener(self.dashboard_listener, True)
        
        # add autonomous mode chooser to smartdashboard
        self.auto_choose = SendableChooser()
        self.auto_choose.addObject('Auto Do Nothing', Autonomous.Modes.DO_NOTHING)
        self.auto_choose.addObject('Auto Move Forward', Autonomous.Modes.MOVE_FORWARD)
        self.auto_choose.addObject('Auto One Object', Autonomous.Modes.ONE_OBJECT)
        SmartDashboard.putData('Autonomous Mode', self.auto_choose)
        
        # joystick events
        self.joystick = Joystick(0)
        l_bumper = Joystick_Button(self.joystick, lc.L_BUMPER)
        l_trigger = Joystick_Button(self.joystick, lc.L_TRIGGER)
        r_bumper = Joystick_Button(self.joystick, lc.R_BUMPER)
        r_trigger = Joystick_Button(self.joystick, lc.R_TRIGGER)
        btn_one   = Joystick_Button(self.joystick, 1)
        btn_two   = Joystick_Button(self.joystick, 2)
        
        # update the joysick axis periodically
        Event_Manager.add_listener('teleop.periodic', self.update_axis)
        
        l_bumper.while_pressed(lambda: Event_Manager.trigger('joystick.l_bumper.while_pressed'))
        l_trigger.while_pressed(lambda: Event_Manager.trigger('joystick.l_trigger.while_pressed'))
        l_bumper.when_pressed(lambda: Event_Manager.trigger('joystick.l_bumper.when_pressed'))
        l_trigger.when_pressed(lambda: Event_Manager.trigger('joystick.l_trigger.when_pressed'))
        l_bumper.when_released(lambda: Event_Manager.trigger('joystick.l_bumper.when_released'))
        l_trigger.when_released(lambda: Event_Manager.trigger('joystick.l_trigger.when_released'))
        r_bumper.when_pressed(lambda: Event_Manager.trigger('joystick.r_bumper.when_pressed'))
        btn_two.when_pressed(lambda: Event_Manager.trigger('joystick.btn_two.when_pressed'))
        btn_one.when_pressed(lambda: Event_Manager.trigger('joystick.btn_one.when_pressed'))
        
        
        
    def log(self, data):
        self.robot.drive.log()
        self.robot.grabber_lift.log()
        
    def dashboard_listener(self, source, key, value, is_new):
        Event_Manager.trigger('dashboard.updated', {
            'source' : source,
            'key' : key,
            'value' : value,
            'is_new' : is_new                                     
        })
        
    def update_axis(self, data):
        Event_Manager.trigger('joystick.axis.updated', {
            'x_left' : self._get_axis(self.joystick, lc.L_AXIS_X)(),
            'y_left' : self._get_axis(self.joystick, lc.L_AXIS_Y)(),
            'x_right' : self._get_axis(self.joystick, lc.R_AXIS_X)(),
            'y_right' : self._get_axis(self.joystick, lc.R_AXIS_Y)()       
        })                                                  
                                                  
    def _get_axis(self, joystick, axis):
        def axis_func():
            val = joystick.getAxis(axis)
            if abs(val) >= .1:
                return val
            else:
                return 0
        
        return axis_func