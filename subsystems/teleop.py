from manager import *

class Teleop:
    
    def __init__(self, robot):
        self.robot = robot
        
        # Start teleop when initialized
        Event_Manager.add_listener('teleop.init', self.start_teleop)
        
        
        
    def start_teleop(self, event):
        
        # set the wheel speeds every time the joystick axis are updated
        Event_Manager.add_listener('joystick.axis.updated', self.set_wheel_motors)
        
        # Set break mode on for grabber lift  when lifter starts moving up or down
        Event_Manager.add_listener('joystick.l_bumper.when_pressed', self.set_break_mode)
        Event_Manager.add_listener('joystick.l_trigger.when_pressed', self.set_break_mode)
        
        # Move lifter down when left bumper is held down
        Event_Manager.add_listener('joystick.l_bumper.while_pressed', self.move_lifter_down)
        
        # Move lifter up when left trigger is held down
        Event_Manager.add_listener('joystick.l_trigger.while_pressed.', self.move_lifter_up)
        
        # Stop lifter when left trigger/bumper is released
        Event_Manager.add_listener('joystick.l_bumper.when_released', self.stop_lifter)
        Event_Manager.add_listener('joystick.l_trigger.when_released', self.stop_lifter)
        
        # Toggle claw when right bumper is pressed
        Event_Manager.add_listener('joystick.r_bumper.when_pressed', self.toggle_claw)

        
    def set_wheel_motors(self, axis):
        self.robot.drive.robot_move(axis['x_left'], axis['y_left'], axis['x_right'], 0)
        
    def move_lifter_down(self, data):
        self.robot.grabber_lift.move_lifter(-.7)
        
    def move_lifter_up(self, data):
        self.robot.grabber_lift.move_lifter(.7)
        
    def set_break_mode(self, data):
        self.robot.grabber_lift.change_break_mode(True)
        
    def stop_lifter(self, data):
        self.robot.grabber_lift.change_break_mode(True)
        self.robot.grabber_lift.move_lifter(0)
        position = self.grabber_lift.pot_reading()
        self.robot.grabber_lift.prepare_to_move_to_position(position)
        self.robot.grabber_lift.move_to_position()
        
    def toggle_claw(self, data):
        if self.grabber_lift.is_clamped():
            self.robot.grabber_lift.release()
        else:
            self.robot.grabber_lift.clamp()
    