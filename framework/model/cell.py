"""
A Cell class for use on a Map grid. The cell contains (x, y) coordinates,
data for planners to manipulate, and a state for graphical representation.
"""

class Cell:
    """
    Initialises a new cell.
    """

    def __init__(self, x, y, data, state):
        self.x = x
        self.y = y
        self.data = data
        self.state = state  # 0 = Empty, 1 = Occupied

    def __str__(self):
        """
        Prints the contents of the cell to the standard output.
        :return:
        """
        print("x: " + str(self.x) + ", y: " + str(self.y) + ", data: "
              + str(self.data) + ", state: " + str(self.state))
