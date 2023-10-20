from vex import *

brain=Brain()

wait(30, MSEC)

no_limit = False
limit = 50

controller = Controller(PRIMARY)

def setupMotor(port, reversed):
    motor = Motor(port, GearSetting.RATIO_6_1, reversed)
    motor.set_position(0, DEGREES)
    motor.set_velocity(0, PERCENT)
    motor.set_stopping(BRAKE)
    return motor

right_front_motor = setupMotor(Ports.PORT1, True)
right_back_motor = setupMotor(Ports.PORT10, True)
right_motor_group = MotorGroup(right_front_motor, right_back_motor)

left_front_motor = setupMotor(Ports.PORT11, False)
left_back_motor = setupMotor(Ports.PORT20, False)
left_motor_group = MotorGroup(left_front_motor, left_back_motor)

def toggleNoLimit():
    global no_limit
    no_limit = not no_limit

def increaseLimit():
    global limit
    limit = min(100, limit + 1)

def decreaseLimit():
    global limit
    limit = max(1, limit - 1)

def changeSpeedBasedOnAxis(axis: Controller.Axis, motor_group: MotorGroup):
    velocity = 0
    global limit
    if (no_limit):
        velocity = axis.position()
    else: 
        if (axis.position() >= 0):
            velocity = min(limit, axis.position())
        elif (axis.position()):
            velocity = max(-limit, axis.position())
    motor_group.set_velocity(velocity, PERCENT)

controller.buttonA.pressed(toggleNoLimit)
controller.buttonUp.pressed(increaseLimit)
controller.buttonDown.pressed(decreaseLimit)
controller.axis2.changed(changeSpeedBasedOnAxis, (controller.axis2, right_motor_group))
controller.axis3.changed(changeSpeedBasedOnAxis, (controller.axis3, left_motor_group))

wait(15, MSEC)

controller.screen.clear_screen()

right_motor_group.spin(FORWARD)
left_motor_group.spin(FORWARD)

while True:
    controller.screen.set_cursor(1, 1)
    no_limit_value = ""
    if (no_limit):
        no_limit_value = "true "
    else:
        no_limit_value = "false"
    controller.screen.print("No Limit: ", no_limit_value)
    controller.screen.set_cursor(2, 1)
    controller.screen.print("Motor Limit: ", limit, "    ")