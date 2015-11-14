import manager
from subsystems import *
import wpilib
from common import port_values as pv


class MyRobot(manager.EventRobot):
    
    def robotInit(self):
        '''
            Initialize robot components here
        '''
        
        self.drive = Drive(self)
        self.grabber_lift = Grabber_Lift(self)
        self.oi = OI(self)
        self.autonomous = Autonomous(self)
        self.teleop = Teleop(self)

if __name__ == '__main__':
    wpilib.run(MyRobot)