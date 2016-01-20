"""
The Python Capstone Project.

CSSE 120 - Introduction to Software Development.
Team members: Joe Faia & Austin Derrow-Pinion (all of them).

The primary author of this module is: Joe Faia.
"""
# TODO: Put the names of ALL team members in the above where indicated.
#       Put YOUR NAME in the above where indicated.

import m0
import m1
import m3
import m4

import tkinter
from tkinter import ttk
import new_create
from _ast import Break

import time
import math


def main():
    """
    Tests functions in this module.
    Intended to be used internally by the primary author of this module.
    """
    print('-------------------------------')
    print('Testing functions in module m2:')
    print('-------------------------------')

    root = tkinter.Tk()

    dc = m0.DataContainer()
    m1.connector_frame(root, dc)
    tele_operate_frame(root, dc)
    bang_bang_frame(root, dc)
    line_follow_P_frame(root, dc)
    line_follow_PID_frame(root, dc)
    polygon_frame(root, dc)


    root.mainloop()

    root2 = tkinter.Tk()

    sprint_GUI(root2, dc)

    root2.mainloop()
class Sensor_value(object):
    def __init__(self):
        self.black = None
        self.white = None
class Stop(object):
    '''Inturupts proccesses'''
    def __init__(self):
        self.stop_bangbang = False
        self.stop_line_P = False
        self.stop_line_pid = False
        self.stop_move = False

class Remote(object):
    def __init__(self, dc, Left=0, Right=0):
        self.Left = Left
        self.Right = Right
        self.dc = dc

    def go_left(self):
        '''Turns the robot Left'''
        self.Left += 3

        if self.Left > 50:
            self.Left = 50

        if self.Right > 50:
            self.Right = 50

        self.dc.robot.driveDirect(self.Right, self.Left)

    def go_right(self):
        '''Turns the robot Right'''
        self.Right += 3

        if self.Left > 50:
            self.Left = 50

        if self.Right > 50:
            self.Right = 50

        self.dc.robot.driveDirect(self.Right, self.Left)

    def increase(self):
        '''Sets both weels to the same speed and increases the speed to the wheels'''

        if self.Left >= self.Right:
            self.Left += 3
            self.Right = self.Left
        else:
            self.Right += 3
            self.Left = self.Right

        if self.Left > 50:
            self.Left = 50

        if self.Right > 50:
            self.Right = 50

        self.dc.robot.driveDirect(self.Right, self.Left)

    def decrease(self):
        '''Sets both weels to the same speed and decreases the speed to the wheels'''
        if self.Left >= self.Right:
            self.Left -= 3
            self.Right = self.Left
        else:
            self.Right -= 3
            self.left = self.Right

        if self.Left > 50:
            self.Left = 50

        if self.Right > 50:
            self.Right = 50

        self.dc.robot.driveDirect(self.Right, self.Left)

    def stop(self):
        self.Left = 0
        self.Right = 0
        self.dc.robot.stop()

def tele_operate_frame(root, dc):
    """
    Constructs and returns a Frame (on the given root window)
    that contains this module's widgets.
    Also sets up callbacks for this module's widgets.

    Preconditions:
      :type root: tkinter.Tk
      :type dc: dcContainer2
    """
    main_frame = ttk.Frame(root, padding=3, relief='raised')
    main_frame.grid(row=0, column=1)

    remote = Remote(dc)

    speed_entry = ttk.Entry(main_frame, width=20)
    speed_label = ttk.Label(main_frame, text='Enter Speed:')

    enter_button = ttk.Button(main_frame, text='Enter')
    enter_button['command'] = lambda: set_speed(remote, int(speed_entry.get()))

    foward_button = ttk.Button(main_frame, text='Accelerate')
    foward_button['command'] = lambda: increase(remote)

    back_button = ttk.Button(main_frame, text='break')
    back_button['command'] = lambda: decrease(remote)

    left_button = ttk.Button(main_frame, text='Left')
    left_button['command'] = lambda: go_left(remote)

    right_button = ttk.Button(main_frame, text='Right')
    right_button['command'] = lambda: go_right(remote)

    stop_button = ttk.Button(main_frame, text='stop')
    stop_button['command'] = lambda: stop(remote)

    arrows_button = ttk.Button(main_frame, text='Use arrow keys')
    arrows_button['command'] = lambda: arrows(remote)

    space_lable = ttk.Label(main_frame, text='')
    space_lable2 = ttk.Label(main_frame, text='')

    speed_label.grid(row=0, column=0)
    speed_entry.grid(row=0, column=1)
    enter_button.grid(row=0, column=2)

    space_lable2.grid(row=1, column=0)

    foward_button.grid(row=2, column=1)
    right_button.grid(row=3, column=2)
    left_button.grid(row=3, column=0)
    stop_button.grid(row=3, column=1)
    back_button.grid(row=4, column=1)

    space_lable.grid(row=5, column=0)

    arrows_button.grid(row=7, column=1)


    return main_frame
def arrows(remote):

    root = tkinter.Toplevel()

    left_label = ttk.Label(root, text='Left arrow turns left')
    right_label = ttk.Label(root, text='Right arrow turns right')
    accelerate_label = ttk.Label(root, text='Up arrow increases speed')
    break_label = ttk.Label(root, text='Down arrow decreases speed')
    stop_label = ttk.Label(root, text='ESC stops robot')

    left_label.grid()
    right_label.grid()
    accelerate_label.grid()
    break_label.grid()
    stop_label.grid()

    root.bind_all('<Key-Left>', lambda event: go_left_key(remote, event))
    root.bind_all('<Key-Right>', lambda event: go_right_key(remote, event))
    root.bind_all('<Key-Up>', lambda event: increase_key(remote, event))
    root.bind_all('<Key-Down>', lambda event: decrease_key(remote, event))
    root.bind_all('<Key-Escape>', lambda event: stop_key(remote, event))


def stop(remote):

    remote.stop()


def calibrate_black(value, sensor):
    sensor.black = value
    print(value)
def calibrate_white(value, sensor):
    sensor.white = value
    print(value)
def bang_bang_frame(root, dc):
    stopper = Stop()

    bang_frame = ttk.Frame(root, padding=3, relief='raised')
    bang_frame.grid(row=1, column=1)

    light_sensor = new_create.Sensors.cliff_front_left_signal

    sensor = Sensor_value()

    cal_black = ttk.Button(bang_frame, text='Calibrate Black')
    cal_black['command'] = lambda: calibrate_black(dc.robot.getSensor(light_sensor), sensor)
    cal_white = ttk.Button(bang_frame, text='Calibrate White')
    cal_white['command'] = lambda: calibrate_white(dc.robot.getSensor(light_sensor), sensor)

    go_button = ttk.Button(bang_frame, text='bang bang')
    go_button['command'] = lambda: bang_bang(dc, root, sensor.black, sensor.white, stopper)

    stop_button = ttk.Button(bang_frame, text='stop')
    stop_button['command'] = lambda: interupt_bangbang(dc, stopper)

    go_button.grid()
    stop_button.grid()
    cal_black.grid()
    cal_white.grid()

    return bang_frame

def bang_bang(dc, root, black, white, stopper):
    light_sensor = new_create.Sensors.cliff_front_left_signal
    midpoint = abs((black - white) / 2)

    print(midpoint)
    print(dc.robot.getSensor(light_sensor))


    stopper.stop_bangbang = False
    while True:
        if stopper.stop_bangbang:
            break
        value = dc.robot.getSensor(light_sensor)
        if value < midpoint:
            dc.robot.driveDirect(5, 10)
        else:
            dc.robot.driveDirect(10, 5)
        time.sleep(.1)
        root.update()
def line_follow_P_frame(root, dc):

    stopper = Stop()

    p_frame = ttk.Frame(root, padding=3, relief='raised')
    p_frame.grid(row=2, column=1)

    light_sensor = new_create.Sensors.cliff_front_left_signal

    sensor = Sensor_value()

    cal_black = ttk.Button(p_frame, text='Calibrate Black')
    cal_black['command'] = lambda: calibrate_black(dc.robot.getSensor(light_sensor), sensor)
    cal_white = ttk.Button(p_frame, text='Calibrate White')
    cal_white['command'] = lambda: calibrate_white(dc.robot.getSensor(light_sensor), sensor)

    go_button = ttk.Button(p_frame, text='Line Follow P')
    go_button['command'] = lambda: line_follow_P(dc, root, sensor.black, sensor.white, stopper)

    stop_button = ttk.Button(p_frame, text='stop')
    stop_button['command'] = lambda: interupt_line_p(dc, stopper)

    go_button.grid()
    stop_button.grid()
    cal_black.grid()
    cal_white.grid()

def line_follow_PID_frame(root, dc):

    p_frame = ttk.Frame(root, padding=3, relief='raised')
    p_frame.grid(row=3, column=1)

    stopper = Stop()

    light_sensor = new_create.Sensors.cliff_front_left_signal

    sensor = Sensor_value()

    cal_black = ttk.Button(p_frame, text='Calibrate Black')
    cal_black['command'] = lambda: calibrate_black(dc.robot.getSensor(light_sensor), sensor)
    cal_white = ttk.Button(p_frame, text='Calibrate White')
    cal_white['command'] = lambda: calibrate_white(dc.robot.getSensor(light_sensor), sensor)


    kp_label = ttk.Label(p_frame, text='Enter Kp paramer: ')
    kp_entry = ttk.Entry(p_frame)

    ki_label = ttk.Label(p_frame, text='Enter Ki paramer: ')
    ki_entry = ttk.Entry(p_frame)

    kd_label = ttk.Label(p_frame, text='Enter Kd paramer: ')
    kd_entry = ttk.Entry(p_frame)

    go_button = ttk.Button(p_frame, text='Line Follow PID')
    go_button['command'] = lambda: line_follow_PID(dc, root, sensor.black, sensor.white, stopper, int(kp_entry.get()), int(kp_entry.get()), int(kp_entry.get()))

    stop_button = ttk.Button(p_frame, text='stop')
    stop_button['command'] = lambda: interupt_line_pid(dc, stopper)

    kp_label.grid(row=0, column=0)
    ki_label.grid(row=1, column=0)
    kd_label.grid(row=2, column=0)
    kp_entry.grid(row=0, column=1)
    ki_entry.grid(row=1, column=1)
    kd_entry.grid(row=2, column=1)
    go_button.grid(row=3, column=1)
    stop_button.grid(row=4, column=1)


    cal_black.grid()
    cal_white.grid()

def line_follow_P(dc, root, black, white, stopper):

    line_follow_PID(dc, root, black, white, stopper, 100, 0, 0)

def line_follow_PID(dc, root, black, white, stopper, kp, ki, kd):

    light_sensor = new_create.Sensors.cliff_front_left_signal
    midpoint = abs(black - white) / 2

    integral = 0
    derivitive = 0
    lasterror = 0

    stopper.stop_line_pid = False
    while True:
        if stopper.stop_line_pid:
            break
        value = dc.robot.getSensor(light_sensor)
        error = midpoint - value
        integral += error
        derivitive = error - lasterror

        correction = (kp / 100) * error + (ki / 100) * integral + (kd / 100) * derivitive

        if correction > 40:
            correction = 40
        elif correction < -40:
            correction = -40

        if value < midpoint:
            dc.robot.driveDirect(15 - correction, 15 + correction)
        else:
            dc.robot.driveDirect(15 + correction, 15 - correction)

        lasterror = error
        time.sleep(.1)
        root.update()

def polygon_frame(root, dc):

    main_frame = ttk.Frame(root, padding=3, relief='raised')
    main_frame.grid(row=4, column=1)

    n_sides_label = ttk.Label(main_frame, text='Enter Number of Sides: ')
    n_sides = ttk.Entry(main_frame)

    side_length_label = ttk.Label(main_frame, text='Enter Side Length: ')
    side_length = ttk.Entry(main_frame)

    speed_label = ttk.Label(main_frame, text='Enter Speed: ')
    speed = ttk.Entry(main_frame)

    enter = ttk.Button(main_frame, text='Enter')
    enter['command'] = lambda: polygon_drive(dc, int(n_sides.get()), int(side_length.get()), int(speed.get()))

    n_sides_label.grid(row=0, column=0)
    side_length_label.grid(row=1, column=0)
    n_sides.grid(row=0, column=1)
    side_length.grid(row=1, column=1)
    speed_label.grid(row=2, column=0)
    speed.grid(row=2, column=1)
    enter.grid(row=3, column=1)
    ''

def polygon_drive(dc, n, side_length, speed):

    side_length = side_length * 10
    tot_ang = (n - 2) * 180
    ang = tot_ang / n
    sec = side_length / speed

    for _ in range(n):
        dc.robot.driveDirect(speed, speed)
        dc.robot.waitTime(sec * 10)
        dc.robot.stop()
        dc.robot.driveDirect(-5, 5)
        dc.robot.waitAngle(180 - ang)
        dc.robot.stop()

def sprint_GUI(root2, dc):
    time_frame = ttk.Frame(root2, padding=(20, 20), relief='raised')
    time_frame.grid()

    update_button = ttk.Button(time_frame, text='Hours Worked')
    update_button['command'] = lambda: update(time_frame)

    update_button.grid(row=0, column=0)

    return time_frame

def update(time_frame):

    derrow = open('hours-1.txt', 'r')
    faia = open('hours-2.txt', 'r')
    faia_s = faia.read()
    derrow_s = derrow.read()

    lines_faia = faia_s.split('\n')
    lines_derrow = derrow_s.split('\n')

    faia_total_time = 0.0
    for k in range(len(lines_faia)):
        if 'Time: ' in lines_faia[k]:
            x = int(lines_faia[k][len(lines_faia[k]) - 3])
            y = int(lines_faia[k][len(lines_faia[k]) - 1])
            faia_total_time += x + (y / 10)

    print('faia')
    print(faia_total_time)

    derrow_total_time = 0.0
    for k in range(len(lines_derrow)):
        if 'Time: ' in lines_derrow[k]:
            x = int(lines_derrow[k][len(lines_derrow[k]) - 3])
            y = int(lines_derrow[k][len(lines_derrow[k]) - 1])
            derrow_total_time += x + (y / 10)

    print('derrow')
    print(derrow_total_time)

    derrow_label = ttk.Label(time_frame, text='Austin Derrow-Pinion worked {} Total Hours'.format(derrow_total_time))
    faia_label = ttk.Label(time_frame, text='Joseph Faia worked {} Total Hours'.format(faia_total_time))

    derrow_label.grid(row=1, column=0)
    faia_label.grid(row=2, column=0)

def set_speed(remote, speed):
    remote.Left = speed
    remote.Right = speed
def go_left(remote):
    remote.go_left()
def go_right(remote):
    remote.go_right()
def increase(remote):
    remote.increase()
def decrease(remote):
    remote.decrease()
def go_left_key(remote, event=False):
    if event:
        go_left(remote)
def go_right_key(remote, event=False):
    if event:
        go_right(remote)
def increase_key(remote, event=False):
    if event:
        increase(remote)
def decrease_key(remote, event=False):
    if event:
        decrease(remote)
def stop_key(remote, event=False):
    if event:
        stop(remote)
def interupt_move(remote, stopper):
    remote.stop()
    stopper.stop_move = True
def interupt_bangbang(dc, stopper):
    dc.robot.stop()
    stopper.stop_bangbang = True
def interupt_line_p(dc, stopper):
    dc.robot.stop()
    stopper.stop_line_pid = True
def interupt_line_pid(dc, stopper):
    dc.robot.stop()
    stopper.stop_line_pid = True
# ----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
