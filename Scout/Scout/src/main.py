from vex import *

brain = Brain()
controller = Controller(PRIMARY)

tankControl = False

wait(30, MSEC)

def setupMotor(port, reversed):
    motor = Motor(port, GearSetting.RATIO_18_1, reversed)
    motor.set_position(0, DEGREES)
    motor.set_velocity(0, PERCENT)
    motor.set_stopping(BRAKE)
    return motor

rightDriveMotor = setupMotor(Ports.PORT10, True)
leftDriveMotor = setupMotor(Ports.PORT20, False)

rightDriveMotor.spin(FORWARD)
leftDriveMotor.spin(FORWARD)

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

controller.buttonR2.pressed(brake)
controller.buttonL2.pressed(tankControlToggle)

controller.axis2.changed(changeSpeedBasedOnAxis, (controller.axis2, rightDriveMotor))
controller.axis3.changed(changeSpeedBasedOnAxis, (controller.axis3, leftDriveMotor))

controller.screen.clear_screen()
while True:
    controller.screen.set_cursor(1, 1)
    controller.screen.print("Tank Control: ", tankControl, " ")

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