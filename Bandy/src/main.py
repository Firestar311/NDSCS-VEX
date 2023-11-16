from vex import *

brain = Brain()
controller = Controller(PRIMARY)

tankControl = False

wait(30, MSEC)

def setupMotor(port, ratio, reversed):
    motor = Motor(port, ratio, reversed)
    motor.set_position(0, TURNS)
    motor.set_velocity(0, PERCENT)
    motor.set_stopping(BRAKE)
    return motor

rightDriveMotor = setupMotor(Ports.PORT10, GearSetting.RATIO_18_1,True)
leftDriveMotor = setupMotor(Ports.PORT20, GearSetting.RATIO_18_1, False)
band_motor = setupMotor(Ports.PORT1, GearSetting.RATIO_18_1, True)

rightDriveMotor.spin(FORWARD)
leftDriveMotor.spin(FORWARD)
band_motor.spin(FORWARD)

def changeSpeedBasedOnAxis(axis: Controller.Axis, motor: Motor):
    if (tankControl): 
        motor.set_velocity(axis.position(), PERCENT)

def brake():
    global leftDriveMotor
    global rightDriveMotor
    leftDriveMotor.set_velocity(0, PERCENT)
    rightDriveMotor.set_velocity(0, PERCENT)

def tankControlToggle():
    global tankControl
    tankControl = not tankControl

def toggleBandMotor(): 
    global band_motor
    vel = band_motor.velocity(VelocityUnits.PERCENT)
    if (vel == 0): 
        band_motor.set_velocity(100, VelocityUnits.PERCENT)
    else: 
        band_motor.set_velocity(0, VelocityUnits.PERCENT)

def setForwardBandMotorSpin():
    band_motor.spin(FORWARD)

def setReverseBandMotorSpin(): 
    band_motor.spin(REVERSE)

controller.buttonB.pressed(brake)
controller.buttonA.pressed(tankControlToggle)
controller.buttonX.pressed(toggleBandMotor)

controller.buttonL1.pressed(setReverseBandMotorSpin)
controller.buttonR1.pressed(setForwardBandMotorSpin)

controller.axis2.changed(changeSpeedBasedOnAxis, (controller.axis2, rightDriveMotor))
controller.axis3.changed(changeSpeedBasedOnAxis, (controller.axis3, leftDriveMotor))

controller.screen.clear_screen()
while True:
    controller.screen.set_cursor(1, 1)
    controller.screen.print("Tank Control: ", tankControl, "  ")
    controller.screen.set_cursor(2, 1)
    controller.screen.print("Band Motor: ", band_motor.direction(), "    ")

    if (tankControl):
        continue
    velocity = controller.axis3.position()
    if (velocity == 0):
        leftDriveMotor.set_velocity(0, PERCENT)
        rightDriveMotor.set_velocity(0, PERCENT)
        continue
    else:
        leftDriveMotor.set_velocity(velocity + controller.axis1.position(), PERCENT)
        rightDriveMotor.set_velocity(velocity - controller.axis1.position(), PERCENT)