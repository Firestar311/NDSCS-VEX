from vex import *

brain = Brain()
controller = Controller(PRIMARY)

tankControl = False
driveSpeedFactor = 0.5
chain = False

wait(30, MSEC)

def setupMotor(port, ratio, reversed):
    motor = Motor(port, ratio, reversed)
    motor.set_position(0, TURNS)
    motor.set_velocity(0, PERCENT)
    motor.set_stopping(BRAKE)
    motor.spin(FORWARD)
    return motor

right_drive_motor = setupMotor(Ports.PORT3, GearSetting.RATIO_18_1,True)
left_drive_motor = setupMotor(Ports.PORT8, GearSetting.RATIO_18_1, False)
left_chain_motor = setupMotor(Ports.PORT6, GearSetting.RATIO_6_1, False)
right_chain_motor = setupMotor(Ports.PORT7, GearSetting.RATIO_6_1, True)


def changeSpeedBasedOnAxis(axis: Controller.Axis, motor: Motor):
    if (tankControl): 
        motor.set_velocity((axis.position() / 2), PERCENT)

def brake():
    left_drive_motor.set_velocity(0, PERCENT)
    right_drive_motor.set_velocity(0, PERCENT)

def tankControlToggle():
    global tankControl
    tankControl = not tankControl

def toggleChainMotors():
    global chain
    if (chain):
        left_chain_motor.set_velocity(0, VelocityUnits.PERCENT)
        right_chain_motor.set_velocity(0, VelocityUnits.PERCENT)
    else:
        left_chain_motor.set_velocity(100, VelocityUnits.PERCENT)
        right_chain_motor.set_velocity(100, VelocityUnits.PERCENT)
    chain = not chain

controller.buttonB.pressed(brake)
controller.buttonA.pressed(tankControlToggle)
controller.buttonX.pressed(toggleChainMotors)

controller.axis2.changed(changeSpeedBasedOnAxis, (controller.axis2, right_drive_motor))
controller.axis3.changed(changeSpeedBasedOnAxis, (controller.axis3, left_drive_motor))

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
    chainValue = "";
    if (chain):
        chainValue = "on "
    else:
        chainValue = "off";
    controller.screen.print("Chain: ", chainValue)
    controller.screen.set_cursor(3, 1)
    controller.screen.print("Speed Factor: ", int(driveSpeedFactor * 100), "%")

    if (tankControl):
        continue
    velocity = controller.axis3.position()
    if (velocity == 0):
        left_drive_motor.set_velocity(0, PERCENT)
        right_drive_motor.set_velocity(0, PERCENT)
        continue
    else:
        left_drive_motor.set_velocity((velocity + controller.axis1.position()) * driveSpeedFactor, PERCENT)
        right_drive_motor.set_velocity((velocity - controller.axis1.position()) * driveSpeedFactor, PERCENT)