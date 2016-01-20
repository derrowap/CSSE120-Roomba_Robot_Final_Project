"""
The Python Capstone Project.

CSSE 120 - Introduction to Software Development.
Team members: Joe Faia and Austin Derrow-Pinion (all of them).

The primary author of this module is: Austin Derrow-Pinion.
"""
# TODO: Put the names of ALL team members in the above where indicated.
#       Put YOUR NAME in the above where indicated.

import m0

import tkinter
from tkinter import ttk, Listbox
import new_create
import math
from random import randrange

class Point():
    """ A class that represents a point in two dimensions."""

    def __init__(self, x=0, y=0):
        """
        Takes two optional parameters, x and y,
        and sets this Point's coordinates to the given
        coordinates.  The defaults for x and y are 0.
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """
        Returns a string that represents the Point
        as in this example:  'Point(100, 32.7)'
        """
        return 'Point({},{})'.format(self.x, self.y)

    def distance_from(self, point):
        """
        Takes a Point and returns the distance
        that this Point is from the given Point.
        """
        dx = point.x - self.x
        dy = point.y - self.y
        return math.sqrt((dx * dx) + (dy * dy))


def main():
    """
    Tests functions in this module.
    Intended to be used internally by the primary author of this module.
    """
    print('-------------------------------')
    print('Testing functions in module m1:')
    print('-------------------------------')

    dc = m0.DataContainer()
    root = tkinter.Tk()
    root2 = tkinter.Toplevel()

    connector_frame(root, dc)
    robot_move_autonomously_frame(root, dc)
    waypoints_frame(root, dc)
    play_n_random_notes_frame(root, dc)
    piano_robot_frame(root2, dc)

    root.mainloop()


#-----------------------------------------------------------------------#
#----------------------------Connector Frame----------------------------#
#-----------------------------------------------------------------------#
def connector_frame(root, dc):
    """
    Feature 1. The user can connect and disconnect to the robot, after 
    specifying whether or not to use the simulator and if not, what port 
    to use for connecting.

    The program should behave reasonably if the user errs (e.g. by choosing 
    a wrong port, or connecting to an already-connected robot).

    Preconditions:
      :type root: tkinter.Tk
      :type dc: m0.DataContainer
    """

    connection_frame = ttk.Frame(root, padding=(3, 3), relief='raised')

    # Constructing widgets for the connection_frame
    simulator_button = ttk.Button(connection_frame, text='Connect using simulator')
    port_button = ttk.Button(connection_frame, text='Connect using port')
    disconnect_button = ttk.Button(connection_frame, text='Disconnect')
    port_entry = ttk.Entry(connection_frame, width=10)
    port_label = ttk.Label(connection_frame, text='')

    # Setting commands for widgets
    simulator_button['command'] = lambda: connect_robot(dc, 'sim', port_label)
    port_button['command'] = lambda: connect_robot(dc, port_entry, port_label)
    disconnect_button['command'] = lambda: disconnect_robot(dc)

    # grid() the widgets
    connection_frame.grid(column=0)
    simulator_button.grid(row=0, columnspan=2)
    port_button.grid(row=1, column=0)
    port_entry.grid(row=1, column=1)
    disconnect_button.grid(row=2, columnspan=2)
    port_label.grid()

    return connection_frame

def connect_robot(dc, port_entry, port_label):
    """ 
    Constructs a robot through m0.DataContainer, allowing the 
    connector buttons in connection_frame to connect to a robot 
    """
    if port_entry == 'sim':
        dc.robot = new_create.Create(port_entry)
        print("You have connected to the simulator")

    if port_entry != 'sim':
        if port_entry.get():
            dc.robot = new_create.Create(int(port_entry.get()))
            print("You have connected to your robot")
        else:
            port_label['text'] = 'Enter a port number'

def disconnect_robot(dc):
    """Used by conection_frame to shutdown the robot, hence disconnect"""
    dc.robot.stop()
    dc.robot.shutdown()
    print("You have disconnected from your robot")

#-----------------------------------------------------------------------#
#----------------------------robot move autonomously frame--------------#
#-----------------------------------------------------------------------#
def robot_move_autonomously_frame(root, dc):
    """
    Feature 5. Move autonomously, by going a specified distance in a specified 
    direction at a specified speed.  That is, the user can set the direction 
    (forward, backward, spin left or spin right) and the distance and speed 
    (each in some reasonable units).  Then, the user can make the robot go 
    (e.g. by pressing a Go button) and the robot should move the specified direction 
    for the specified distance at the specified speed, with some reasonable accuracy.

    An important by-product of this feature is to provide a good set of functions 
    that teammates will use for most of the movements that they ask of the robot.

    Advanced options include:

    -There are multiple implementations (any of which can be chosen by the user), 
        with demonstrated understanding of when and why one is better/worse than another.  
        For example, one implementation is the "time" approach, another is the "distance 
        sensor" approach (which itself is really a collection of approaches parameterized 
        by the time to wait between sensor readings), and a third is the "send a script" 
        approach.
    -There is high accuracy for the best implementations.
    +Can move linearly and angularly (hence along a curve) at the same time, with 
        some reasonable understanding of "distance" and "speed" in that case.
    -The motion can be interrupted by the user.
    """
    robot_moving_direction_frame = ttk.Frame(root, padding=(3, 3), relief='raised')

    # Constructing widgets
    direction_box_values = ('Forward', 'Backward', 'Spin Left', 'Spin Right', 'Curved')
    direction_box = ttk.Combobox(robot_moving_direction_frame, state='readonly', values=direction_box_values)
    distance_label = ttk.Label(robot_moving_direction_frame, text='Distance/Degrees:')
    distance_entry = ttk.Entry(robot_moving_direction_frame, width=10)
    radius_label = ttk.Label(robot_moving_direction_frame, text='Turning Radius:')
    radius_entry = ttk.Entry(robot_moving_direction_frame, width=10)
    speed_label = ttk.Label(robot_moving_direction_frame, text='Enter speed between 1 to 50:')
    speed_entry = ttk.Entry(robot_moving_direction_frame, width=10)
    go_button = ttk.Button(robot_moving_direction_frame, text='GO')
    stop_button = ttk.Button(robot_moving_direction_frame, text='STOP')

    # Setting commands for widgets
    go_button['command'] = lambda: move_robot(direction_box.get(), distance_entry.get(), radius_entry.get(), speed_entry.get(), speed_label, dc)
    stop_button['command'] = lambda: stop_robot(dc)

    # grid() the widgets
    robot_moving_direction_frame.grid(column=0)
    direction_box.grid(row=0, columnspan=2)
    distance_label.grid(row=1, column=0)
    radius_label.grid(row=1, column=1)
    distance_entry.grid(row=2, column=0)
    radius_entry.grid(row=2, column=1)
    speed_label.grid(row=3, columnspan=2)
    speed_entry.grid(row=4, columnspan=2)
    stop_button.grid(row=5, column=0)
    go_button.grid(row=5, column=1)

def move_robot(direction, distance, radius, speed, speed_label, dc):
    """
    Function used for robot_distance_move_frame to move the robot after it
    has been connected. It will print how far the robot travels or the 
    degrees it has turned after each call.
    """
    if int(speed) < 1 or int(speed) > 50:
        speed_label['text'] = 'The speed has to be between 1 and 50'
        return None

    if direction == 'Forward':
        dc.robot.go(int(speed), 0)
        dc.robot.waitDistance(int(distance))
    elif direction == 'Backward':
        dc.robot.go(-int(speed), 0)
        dc.robot.waitDistance(-int(distance))
    elif direction == 'Spin Left':
        dc.robot.driveDirect(-int(speed), int(speed))
        dc.robot.waitAngle(int(distance))
    elif direction == 'Spin Right':
        dc.robot.driveDirect(int(speed), -int(speed))
        dc.robot.waitAngle(-int(distance))
    elif direction == 'Curved':
        dc.robot.drive(int(speed), int(radius) * 100)
        dc.robot.waitDistance(int(distance) * 100)
    dc.robot.stop()

    print('Entered:', distance, 'centimeters', direction)
    print('Time estimate:', int(distance) / int(speed), 'seconds.')

def stop_robot(dc):
    dc.robot.stop()
    print('qwv')

#-----------------------------------------------------------------------#
#--------------------------------waypoints frame------------------------#
#-----------------------------------------------------------------------#
def waypoints_frame(root, dc):
    """
    Feature 8. Move through a sequence of user-specified waypoints.

    That is, the user can enter a sequence of (x, y) coordinates and tells the 
    robot to go. Then, the robot moves to each, one after the other. (The origin of 
    the coordinate system is where the robot began the sequence of moves.)

    Advanced options include:

    +There is a nice way to enter coordinates (e.g. by clicking on a map displayed in 
        a window).
    -The path of the robot is shown on a window as the robot moves.
    -The movement can be interrupted by the user.
    -Coordinates can come from a file.
    -The robot can move around obstacles as it moves from waypoint to waypoint.
    +User can control speeds as well (perhaps via pre-specification, perhaps via 
        tele-operation, perhaps both).
    -The robot remembers paths on which it is tele-operated and then can reproduce the 
        paths autonomously.
    -The robot keeps track of its position through ALL its movements (even those 
        produced by teammate's code) and can reproduce them from any point the user 
        specifies.
    """
    dc.point_list = [Point(0, 0)]
    waypoint_frame = ttk.Frame(root, padding=(3, 3), relief='raised')

    # Constructing widgets for frame
    coordinate_label = ttk.Label(waypoint_frame, text='Enter coordinates below to set waypoints:')
    x_label = ttk.Label(waypoint_frame, text='x')
    y_label = ttk.Label(waypoint_frame, text='y')
    x_entry = ttk.Entry(waypoint_frame, width=5)
    y_entry = ttk.Entry(waypoint_frame, width=5)
    waypoint_list = ttk.Label(waypoint_frame, text='Current waypoints:')
    points_list_box = ttk.Combobox(waypoint_frame)
    points_list_box.set('Current Points')
    add_button = ttk.Button(waypoint_frame, text='ADD', width=5)
    go_button = ttk.Button(waypoint_frame, text='GO', width=5)
    reset_button = ttk.Button(waypoint_frame, text='RESET', width=5)
    speed_entry = ttk.Entry(waypoint_frame, width=10)
    speed_label = ttk.Label(waypoint_frame, text='Speed from 1 to 50:')


    # Setting commands for widgets
    add_button['command'] = lambda: current_waypoints(x_entry.get(), y_entry.get(), points_list_box, dc)
    go_button['command'] = lambda: move_to_coordinate(dc, speed_entry.get())
    reset_button['command'] = lambda: empty_points_list(points_list_box, dc)

    # grid the widgets
    waypoint_frame.grid(column=0)
    coordinate_label.grid(row=0, columnspan=3)
    speed_label.grid(row=1, columnspan=2)
    speed_entry.grid(row=1, column=2, sticky="W")
    x_label.grid(row=2, column=0)
    y_label.grid(row=2, column=1)
    x_entry.grid(row=3, column=0)
    y_entry.grid(row=3, column=1)
    add_button.grid(row=4, column=0)
    go_button.grid(row=4, column=1)
    waypoint_list.grid(row=2, column=2)
    points_list_box.grid(row=3, column=2)
    reset_button.grid(row=4, column=2, sticky="W")

def current_waypoints(x, y, points_list_box, dc):
    """ Adds the points from waypoints frame to the combobox and stores them """
    dc.point_list = dc.point_list + [Point(int(x), int(y))]
    points_list_box['values'] = [dc.point_list]

def empty_points_list(points_list_box, dc):
    points_list_box['values'] = []
    dc.point_list = [Point(0, 0)]

def move_to_coordinate(dc, speed):
    """ 
    Moves the robot to the given points one by one. It stores
    the angles that it will need to travel, then stores the distances
    it will need to travel. It will then turn the necessary angle and
    move the necessary distance depending on how long the points list is.   
    """
    angles = []
    distances = []
    robot_spins = []

    # Finds the angles relataive to the x-axis and the distances to travel
    for k in range(len(dc.point_list) - 1):
        angles = angles + [math.atan2(dc.point_list[k + 1].y - dc.point_list[k].y, dc.point_list[k + 1].x - dc.point_list[k].x) * 180 / math.pi]
        distances = distances + [float(dc.point_list[k].distance_from(dc.point_list[k + 1]))]

    # Changes the angles with relativity to 360 degree circle
    for p in range(len(angles)):
        if angles[p] < 0:
            angles[p] = 360 + angles[p]
    print(angles)
    print(distances)

    # Collects the angle that the robot will need to sping each step
    for k in range(len(angles)):
        change_in_angle = 0
        for j in range(len(robot_spins)):
            change_in_angle = change_in_angle + robot_spins[j]
        robot_spins_temp = angles[k] - change_in_angle
        if abs(robot_spins_temp) > 180:
            robot_spins_temp = 360 - abs(robot_spins_temp)
        robot_spins = robot_spins + [robot_spins_temp]
    print(robot_spins)

    # Moves the robot using the robot_spins angles and the distances
    for k in range(len(robot_spins)):
        if robot_spins[k] < 0:
            dc.robot.driveDirect(float(speed), -float(speed))
            dc.robot.waitAngle(robot_spins[k])
        elif robot_spins[k] > 0:
            dc.robot.driveDirect(-float(speed), float(speed))
            dc.robot.waitAngle(robot_spins[k])
        dc.robot.driveDirect(float(speed), float(speed))
        dc.robot.waitDistance(distances[k])
    dc.robot.stop()

#----------------------------------------------------------------------#
#-------------------------------Play N random Notes--------------------#
#----------------------------------------------------------------------#
def play_n_random_notes_frame(root, dc):
    """
    Feature 3.  Play N random notes, where the user specifies N.  The 
    notes must not be 'clipped'.

    Additionally, the use can specify the length of time each note should 
    be played -- either a fixed length of time, or a range from which the 
    time should be chosen at random.
    """
    music_frame = ttk.Frame(root, padding=(3, 3), relief='raised')

    # Constructing widgets
    random_music_button = ttk.Button(music_frame, text='Random Notes')
    N_entry = ttk.Entry(music_frame, width=5)
    duration_entry = ttk.Entry(music_frame, width=5)
    N_label = ttk.Label(music_frame, text='# of notes to play:')
    duration_label = ttk.Label(music_frame, text='Note duration:')

    # Setting Commands for widgets
    random_music_button['command'] = lambda: play_random_music(dc, N_entry.get(), duration_entry.get())

    # grid the widgets
    music_frame.grid(column=0)
    N_label.grid(row=0, column=0)
    N_entry.grid(row=0, column=1)
    duration_label.grid(row=1, column=0)
    duration_entry.grid(row=1, column=1)
    random_music_button.grid(row=2, columnspan=2)

def play_random_music(dc, N, duration):
    # Plays random notes N amount of times
    k = []
    for _ in range(int(N)):
        k = k + [(randrange(31, 127), int(duration))]
    dc.robot.playSong(k)

#----------------------------------------------------------------------#
#----------------------------Piano-------------------------------------#
#----------------------------------------------------------------------#
def piano_robot_frame(root, dc):
    song_list = []
    name_list = []

    piano_frame = ttk.Frame(root, padding=(3, 3), relief='raised')
    # Images
#     record_image = tkinter.PhotoImage(master=root, file='record_image.gif')
#     stop_image = tkinter.PhotoImage(file='black.square.gif')
#     play_image = tkinter.PhotoImage(file='play.gif')

    # Widgets for frame
    intro_label1 = ttk.Label(piano_frame, text='Welcome to the roomba piano!')
    intro_label2 = ttk.Label(piano_frame, text='Enter the duration for the notes')
    intro_label3 = ttk.Label(piano_frame, text='to be played (max 255):')
    duration_entry = ttk.Entry(piano_frame, width=5)
    recording_label1 = ttk.Label(piano_frame, text='Press the record button, then play a song.')
    recording_label2 = ttk.Label(piano_frame, text='Press stop when it is finished, give it a name,')
    recording_label3 = ttk.Label(piano_frame, text='and then press save to add it to your list. You')
    recording_label4 = ttk.Label(piano_frame, text='can play that song at any time by selecting')
    recording_label5 = ttk.Label(piano_frame, text='it in the box and then pressing play.')
    record_button = ttk.Button(piano_frame, text='Record', width=6)
    stop_button = ttk.Button(piano_frame, text='Stop', width=5)
    play_button = ttk.Button(piano_frame, text='Play Song')
    saved_songs_listbox = Listbox(piano_frame, height=6, width=30, selectmode='SINGLE')
    save_label = ttk.Label(piano_frame, text='Give your song a title:')
    save_entry = ttk.Entry(piano_frame, width=15)
    save_button = ttk.Button(piano_frame, text='Save Song')
#     delete_button = ttk.Button(piano_frame, text='Delete Song')


    # White keys constructed
    white_note_values = [31, 33, 35, 36, 38, 40, 41, 43, 45, 47, 48, 50,
                         52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71,
                         72, 74, 76, 77, 79, 81, 83, 84, 86, 88, 89, 91,
                         93, 95, 96, 98, 100, 101, 103, 105, 107, 108, 110,
                         112, 113, 115, 117, 119, 120, 122, 124, 125, 127]
    letter_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    white_keys = []
    for k in range(len(white_note_values)):
        white_keys = white_keys + [ttk.Button(piano_frame, width=2)]


    # Sets text for white keys
    white_keys[0]['text'] = 'G'
    index = 0
    for k in range(1, len(white_keys)):
        white_keys[k]['text'] = letter_notes[index]
        index = index + 1
        if index > 6:
            index = 0

    # White keys' commands
    for k in range(len(white_keys)):
        set_index(white_keys, k, dc, white_note_values, duration_entry)

    # Widget commands
    record_button['command'] = lambda: record_song(dc, 'start')
    stop_button['command'] = lambda: record_song(dc, None)
    save_button['command'] = lambda: add_song_to_list(dc, save_entry.get(), saved_songs_listbox, song_list, name_list)
    play_button['command'] = lambda: play_song(dc, saved_songs_listbox.get('active'), song_list, name_list)
#     delete_button['command'] = lambda: delete_song(name_list, song_list, saved_songs_listbox)

    # Grid the keys
    piano_frame.grid()
    intro_label1.grid(row=0, columnspan=10, sticky='W')
    intro_label2.grid(row=1, columnspan=10, sticky='W')
    intro_label3.grid(row=2, columnspan=10, sticky='W')
    duration_entry.grid(row=2, column=6, columnspan=2, sticky='E')
    recording_label1.grid(row=0, column=12, columnspan=12, sticky='W')
    recording_label2.grid(row=1, column=12, columnspan=12, sticky='W')
    recording_label3.grid(row=2, column=12, columnspan=12, sticky='W')
    recording_label4.grid(row=3, column=12, columnspan=12, sticky='W')
    recording_label5.grid(row=4, column=12, columnspan=12, sticky='W')
    record_button.grid(row=1, column=28, columnspan=2, sticky='W')
    stop_button.grid(row=1, column=30, columnspan=2, sticky='W')
    play_button.grid(row=1, column=32, columnspan=5, sticky='W')
    saved_songs_listbox.grid(row=0, rowspan=5, column=38, columnspan=10)
    save_label.grid(row=0, column=26, columnspan=12, sticky='W')
    save_entry.grid(row=0, column=32, columnspan=12, sticky='W')
    save_button.grid(row=2, column=28, columnspan=4)
#     delete_button.grid(row=2, column=32, columnspan=5, sticky='W')
    for k in range(len(white_keys)):
        white_keys[k].grid(row=10, column=k, pady=3)

def set_index(keys, k, dc, note_values, duration):
    # Sets the commands for the list of buttons
    index = note_values[k]
    keys[k]['command'] = lambda: play_note(dc, index, int(duration.get()))

def play_note(dc, note, duration):
    # The robot plays a note with the given duration
    print(dc.record)
    if dc.record == 'start':
        if dc.song == ():
            dc.song.append(int(note), int(duration))
        else:
            dc.song.append((int(note), int(duration)))
    dc.robot.playNote(note, int(duration))
    print('Note played:', note, '   Duration:', duration)

def record_song(dc, value):
    # Switches the value of record to either start or stop depending on
    # the button being pressed
    dc.record = value
    print(dc.record)

def add_song_to_list(dc, name, saved_songs_listbox, song_list, name_list):
    # Adds the name of the recorded song to the listbox
    # Adds the name to a list of all the names
    # Adds the list of notes as a song to the song list
    name_list.append(name)
    saved_songs_listbox.insert('end', name)
    song_list.append((dc.song))
    dc.song = []

# def delete_song(name_list, song_list, saved_songs_listbox):
#     # Deletes a song from the selected value on the listbox
#     print(name_list)
#     saved_song = saved_songs_listbox.get('active')
#     for k in range(len(name_list)):
#         if saved_song == name_list[k]:
#             name_list.pop(k)
#             song_list.pop(k)
#             index = k
#     saved_songs_listbox.delete(index, 'end')

def play_song(dc, saved_songs_listbox, song_list, name_list):
    # Plays a song that is highlighted from the listbox by finding the position
    # of the name in the list, and then playing the song that matches that in
    # the song list
    for k in range(len(name_list)):
        if saved_songs_listbox == name_list[k]:
            index = k
    dc.robot.playSong(song_list[index])



# ----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
