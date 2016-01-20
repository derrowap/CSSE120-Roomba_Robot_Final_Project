"""
The Python Capstone Project.

This file contains data SHARED by the other modules in this project.

CSSE 120 - Introduction to Software Development.
Team members: Joe Faia and Austin Derrow-Pinion (all of them).
"""
# TODO: Put the names of ALL team members in the above where indicated.

import m1
import m2
import m3
import m4

import tkinter
from tkinter import ttk

# ----------------------------------------------------------------------
# TODO: TEAM-PROGRAM this module so that it runs your entire program,
#       incorporating parts from m1 .. m4.
# ----------------------------------------------------------------------


class DataContainer():
    """ A container for the data shared across the application. """

    def __init__(self):
        """ Initializes instance variables (fields). """
        self.robot = None
        self.point_list = None
        self.record = None
        self.song = []


def main():
    """ Runs the MAIN PROGRAM. """
    print('----------------------------------------------')
    print('Integration Testing of the INTEGRATED PROGRAM:')
    print('----------------------------------------------')
    dc = DataContainer()
    root = tkinter.Tk()
    root.title('Full Remote')

    root2 = tkinter.Tk()
    root2.title('GUI Reader')

    # Austin Derrow-Pinion Frames
    m1.connector_frame(root, dc)
    m1.robot_move_autonomously_frame(root, dc)
    m1.waypoints_frame(root, dc)
    m1.play_n_random_notes_frame(root, dc)
    m1.piano_robot_frame(root2, dc)

    # Joe Faia Frames
    m2.tele_operate_frame(root, dc)
    m2.bang_bang_frame(root, dc)
    m2.line_follow_P_frame(root, dc)
    m2.line_follow_PID_frame(root, dc)
    m2.polygon_frame(root, dc)
    m2.sprint_GUI(root2, dc)

    root.mainloop()

# ----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
