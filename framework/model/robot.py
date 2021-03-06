import math

from framework.event.events import OdometryReport, StateEvent
from framework.util.listener import Listener
from framework.util.notifier import Notifier


class Robot(Listener, Notifier):
    """
    A generic Robot class which (may) represent(s) a hardware robot that
    implements the communications interface defined by the robonav tool.
    It is possible to use this class for simulations where no hardware
    robot exists.

    It can communicate with a hardware robot using Bluetooth, WiFi,
    Ethernet, Serial, InfraRed, etc. using the abstracted connection
    approach.

    This class keeps track of the robots position, orientation, the path it
    has traversed, physical dimensions, state, and the cell resolution
    it is operating in.

    It does not matter if the robot is a wheeled, tracked, bipod, etc. as
    long as the hardware conforms to the generic interface required by
    the robonav tool.
    """

    def __init__(self, connection=None):
        Notifier.__init__(self)

        # Data connection to robot.
        self.connection = connection

        self.x = 0  # In meters.
        self.y = 0
        self.heading = 1.57

        # List of visited points.
        self.trail = []

        # Physical dimensions in meters.
        self.width = 0.18
        self.length = 0.23

        # State string.
        self.state = ""

        # Size of the cells we are operating in.
        self.cell_size = 0.15

    def handle_event(self, event):
        """

        :param event:
        :return:
        """
        if isinstance(event, OdometryReport):
            self.update_odometry(event)
        elif isinstance(event, StateEvent):
            self.state = event.state

    '''
    Gets the robots x position in cells.
    '''

    def get_cell_x(self):
        return int(self.x / self.cell_size)

    '''
    Gets the robots y position in cells.
    '''

    def get_cell_y(self):
        return int(self.y / self.cell_size)

    '''
    Instructs the robot to go forward.
    '''

    def go_forward(self):
        self.connection.send("w\n")

    '''
    Instructs the robot to go backward.
    '''

    def go_backward(self):
        self.connection.send("s\n")

    '''
    Instructs the robot to rotate left.
    '''

    def rotate_left(self):
        self.connection.send("a\n")

    '''
    Instructs the robot to rotate right.
    '''

    def rotate_right(self):
        self.connection.send("d\n")

    '''
    Instructs the robot to halt.
    '''

    def halt(self):
        self.connection.send("q\n")

    '''
    Instructs the robot to begin a scan.
    '''

    def scan(self):
        self.connection.send("e\n")

    '''
    Instructs the robot to ping.
    '''

    def ping(self):
        self.connection.send("p\n")

    '''
    Instructs the robot to reset itself.
    '''

    def reset(self):
        self.connection.send("z\n")

    '''
    Instructs the robot to update its odometry with the new parameters.
    '''

    def change_odometry(self, x, y, heading):
        self.connection.send("c," + str(x) + "," + str(y) + "," +
                             str(heading) + "\n")

    '''
    Instructs the robot to rotate to face the specified heading.
    '''

    def rotate_to(self, heading):
        if heading == 6.28: # Catch the rounding issue from face.
            heading = 0

        if not (0.0 <= heading < 6.28):
            print("heading not within bounds: " + str(heading))
            return self.heading
        elif self.heading == heading:
            print("already at heading: " + str(heading))
            return self.heading

        print("rotate_to: " + str(heading))

        self.connection.send("r" + str(round(heading, 2)) + "\n")

        return heading

    '''
    Instructs the robot to travel a straight line distance.
    '''

    def travel_distance(self, distance):
        print("travel_distance: " + str(round(distance * self.cell_size, 2)))

        # Distance is cell based so send as meters.
        self.connection.send("t" + str(round(distance * self.cell_size, 2)) + "\n")

    '''
    Instructs the robot to face a point.
    '''

    def face(self, x, y):
        dx = x - self.get_cell_x()
        dy = y - self.get_cell_y()

        alpha = math.atan2(dy, dx)
        beta = alpha - self.heading

        if beta < 0:
            beta += 6.28
        elif beta >= 6.28:
            beta -= 6.28

        heading = self.heading + beta

        if heading < 0:
            heading += 6.28
        elif heading >= 6.28:
            heading -= 6.28

        heading = self.rotate_to(round(heading, 2))

        return heading

    '''
    Instructs the robot to go a point.
    '''

    def go_to(self, x, y):
        heading = self.face(x, y)

        if heading != self.heading:
            while self.state != "Halted":
                continue

        distance = math.sqrt((x - self.get_cell_x()) ** 2 + (y - self.get_cell_y()) ** 2)

        self.travel_distance(round(distance, 2))

    '''
    Returns a boolean value to the caller indicating if there has
    been a change.

    The update stores the x and y coordinates in meters so they must
    be converted.
    '''

    def update_odometry(self, update):
        changed = False

        if self.x != update.x:
            self.x = update.x
            changed = True

        if self.y != update.y:
            self.y = update.y
            changed = True

        if self.heading != update.heading:
            self.heading = update.heading
            changed = True

        if self.heading < 0:
            self.heading += 6.28
        elif self.heading >= 6.28:
            self.heading -= 6.28

        if changed:
            self.trail.append([self.get_cell_x(), self.get_cell_y()])
            self.notify_listeners(update)

        return changed
