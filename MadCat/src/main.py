from vex import *

brain = Brain()
controller = Controller(PRIMARY)

tankControl = False
driveSpeedFactor = 0.5
bandMotorSpeed = 100;
forkMotorSpeed = 20;

wait(30, MSEC)

def setupMotor(port, ratio, reversed):
    motor = Motor(port, ratio, reversed)
    motor.set_position(0, TURNS)
    motor.set_velocity(0, PERCENT)
    motor.set_stopping(BRAKE)
    motor.spin(FORWARD)
    return motor

rightDriveMotor = setupMotor(Ports.PORT10, GearSetting.RATIO_18_1,True)
leftDriveMotor = setupMotor(Ports.PORT20, GearSetting.RATIO_18_1, False)
band_motor = setupMotor(Ports.PORT1, GearSetting.RATIO_18_1, True)
fork_motor = setupMotor(Ports.PORT2, GearSetting.RATIO_36_1, True)
#arm_motor = setupMotor(Ports.Port3, GearSetting.RATIO_36_1, True)

def changeSpeedBasedOnAxis(axis: Controller.Axis, motor: Motor):
    if (tankControl): 
        motor.set_velocity((axis.position() / 2), PERCENT)

def brake():
    leftDriveMotor.set_velocity(0, PERCENT)
    rightDriveMotor.set_velocity(0, PERCENT)

def tankControlToggle():
    tankControl = not tankControl

def bandMotorForward():
    band_motor.set_velocity(bandMotorSpeed, VelocityUnits.PERCENT)

def bandMotorReverse():
    band_motor.set_velocity(-bandMotorSpeed, VelocityUnits.PERCENT)

def bandMotorStop():
    band_motor.set_velocity(0, VelocityUnits.PERCENT)

def forkMotorForward():
    fork_motor.set_velocity(forkMotorSpeed, VelocityUnits.PERCENT)

def forkMotorReverse():
    fork_motor.set_velocity(-forkMotorSpeed, VelocityUnits.PERCENT)

def forkMotorStop():
    fork_motor.set_velocity(0, VelocityUnits.PERCENT)

controller.buttonB.pressed(brake)
controller.buttonA.pressed(tankControlToggle)

controller.buttonL1.pressed(bandMotorReverse)
controller.buttonL1.released(bandMotorStop)

controller.buttonR1.pressed(bandMotorForward)
controller.buttonR1.released(bandMotorStop)

controller.buttonL2.pressed(forkMotorReverse)
controller.buttonL2.released(forkMotorStop)

controller.buttonR2.pressed(forkMotorForward)
controller.buttonR2.released(forkMotorStop)

controller.axis2.changed(changeSpeedBasedOnAxis, (controller.axis2, rightDriveMotor))
controller.axis3.changed(changeSpeedBasedOnAxis, (controller.axis3, leftDriveMotor))

brain.screen.clear_screen()
controller.screen.clear_screen()
while True:
    controller.screen.set_cursor(1, 1)
    tcValue = "";
    if (tankControl):
        tcValue = "true "
    else:
        tcValue = "false";
    controller.screen.print("Tank Control: ", tcValue)
    controller.screen.set_cursor(2, 1)
    controller.screen.print("Speed Factor: ", int(driveSpeedFactor * 100), "%")

    if (tankControl):
        continue
    velocity = controller.axis3.position()
    if (velocity == 0):
        leftDriveMotor.set_velocity(0, PERCENT)
        rightDriveMotor.set_velocity(0, PERCENT)
        continue
    else:
        leftDriveMotor.set_velocity((velocity + controller.axis1.position()) * driveSpeedFactor, PERCENT)
        rightDriveMotor.set_velocity((velocity - controller.axis1.position()) * driveSpeedFactor, PERCENT)