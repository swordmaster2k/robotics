import os
import math
import copy
import shutil

from pathlib import Path

from .cell import Cell
from .goal import Goal

'''
A Map containing a 2D grid of cells of a specified size. The size of the
grid is in meters, the number of cells in the grid is calculated using
the grids size and the size of individual cells.

The Map also contains the robot operatin on it and the location of the
goal. Path planners can use the data in each cell of the grid for 
planning the motion of the robot.
'''


class Map:
    def __init__(self, robot, grid_size, cell_size, file=None):
        """

        :param robot:
        :param grid_size:
        :param cell_size:
        :return:
        """
        self.robot = robot                                                  # The robot traversing this map.
        self.grid_size = grid_size                                          # Size in meters down either side.
        self.cell_size = cell_size                                          # Cell size in meters.
        self.grid = []                                                      # Contains a list of columns, treated like a 2D array.
        self.path = []                                                      # Calculated path to follow.
        self.file = file
        self.cells_square = 0

        if self.file is not None:
            self.open()
        else:
            self.cells_square = int(round(self.grid_size / self.cell_size, 0))  # Number of cells down either side of the grid.
            self.goal = Goal(self.cells_square - 2 ,self.cells_square - 2)      # Goal position.
            self.populate_grid()

    def open(self):
        """

        :return:
        """
        print("opening map: " + str(self.file))

        infile = Path(self.file).open()

        # Do not bother with any validation for now.
        self.grid_size = float(infile.readline())
        self.cell_size = float(infile.readline())
        self.robot.cell_size = self.cell_size

        self.cells_square = int(round(self.grid_size / self.cell_size, 0))  # Number of cells down either side of the grid.
        self.populate_grid()

        y = self.cells_square - 1

        while y >= 0:
            line = infile.readline()

            for x in range(self.cells_square):
                if line[x] == "#":
                    self.grid[x][y].state = 1
                elif line[x] == "R":
                    self.robot.change_odometry(round(x * self.cell_size, 2), round(y * self.cell_size, 2), 1.57)
                    self.robot.x = 1
                    self.robot.y = 1
                    '''
                    print("Waiting for odometry change...")

                    # Wait for odometry change to take affect.
                    while self.robot.x != round(x * self.cell_size, 2) and self.robot.y != round(y * self.cell_size, 2):
                        continue

                    print("Odometry change successful!")
                    '''
                elif line[x] == "G":
                    self.goal = Goal(x, y)
                elif line[x] == " ":
                    self.grid[x][y].state = 0

            y -= 1

        infile.close()

    def save(self):
        """

        :return:
        """
        print("saving map: " + str(self.file))

        shutil.copy(self.file, self.file + ".tmp")

        try:
            os.remove(self.file)

            outfile = Path(self.file)
            outfile.touch()
            outfile = outfile.open("w+")

            # Do not bother with any validation for now.
            outfile.write(str(self.grid_size) + "\n")
            outfile.write(str(self.cell_size) + "\n")

            y = self.cells_square - 1

            while y >= 0:
                for x in range(self.cells_square):
                    if x == self.robot.x and y == self.robot.y:
                        outfile.write("R")
                    elif x == self.goal.x and y == self.goal.y:
                        outfile.write("G")
                    else:
                        if self.grid[x][y].state == 0:
                            outfile.write(" ")
                        else:
                            outfile.write("#")
                outfile.write(str("\n"))
                y -= 1

            outfile.close()
            os.remove(self.file + ".tmp")
        except IOError as err:
            print(str(err))
            os.rename(self.file + "tmp", self.file)

    def populate_grid(self):
        """
        Populates the grid with unknown cells.
        :return:
        """
        for x in range(self.cells_square):
            column = []

            for y in range(self.cells_square):
                if x == 0 or y == 0 or x == self.cells_square - 1 or y == self.cells_square - 1:
                    column.append(Cell(x, y, "", 1))  # Add a free cell.
                else:
                    column.append(Cell(x, y, "", 0))  # Add a free cell.

            self.grid.append(column)

    def ping_to_cells(self, distance):
        """
        Returns the most significant cells involved in a ping, it is not
        100% accurate in cases where the ping cuts the corner of a cell but
        it does return the most important cells.

        Returns a copy of the cells in the pings area.

        Returns -1 if no cells are affected.

        Distance is specified in cells.

        TODO: Take into account that different range finders will have
        different fields of view!
        :param distance:
        :return:
        """
        cells = []
        did_occupy = False

        last_x = -1
        last_y = -1

        while distance > 0:
            cell_x = math.floor(self.robot.x + (distance *
                                                math.cos(self.robot.heading)))

            cell_y = math.floor(self.robot.y + (distance *
                                                math.sin(self.robot.heading)))

            if cell_x >= self.cells_square or cell_y >= self.cells_square:
                distance -= self.cell_size
                continue

            cell = copy.deepcopy(self.grid[cell_x][cell_y])

            if cell != -1:
                if (cell.x == math.floor(self.robot.x) and
                            cell.y == math.floor(self.robot.y)):
                    break

                if cell.x != last_x or cell.y != last_y:
                    if not did_occupy:  # Occupy the first cell to be inbounds.
                        cell.state = 2  # Occupied.
                        did_occupy = True
                    else:
                        cell.state = 1  # Free.

                    cells.append(cell)
                    last_x = cell.x
                    last_y = cell.y

            distance -= self.cell_size

        return cells

    def point_to_cell(self, x, y):
        """
        Returns the cell at the x, y coordinate in meters.

        Returns -1 if out of bounds.
        :param x:
        :param y:
        :return:
        """
        cell_x = int(round(max(0, min(x / self.cell_size,
                                      self.cells_square - 1)), 0))

        cell_y = int(round(max(0, min(y / self.cell_size,
                                      self.cells_square - 1)), 0))

        if cell_x > self.cells_square or cell_y > self.cells_square:
            return -1  # Cell out of bounds.

        return self.grid[cell_x][cell_y]

    def update_map(self, cells):
        """
        Updates the map based on the new cell data provided.

        Returns the affected cells if any.
        :param cells:
        :return:
        """
        updated_cells = []

        if len(cells) > 0:
            for i in range(len(cells)):
                cell = cells[i]

                if self.grid[cell.x][cell.y].state != cell.state:
                    self.grid[cell.x][cell.y].state = cell.state
                    updated_cells.append(self.grid[cell.x][cell.y])

        return updated_cells

    def print_map(self):
        """
        Prints a textual representation of the map.

        O(n^2) algorithm to run over the grid. Consider using
        recursion instead.

        Same as running over a 2D array in C using two for loops.
        """
        y = 0
        header = ""
        rows = ""
        symbol = ""
        found_robot = False
        robot_position = self.point_to_cell(self.robot.x, self.robot.y)

        if robot_position == -1:
            found_robot = True

        for y in range(self.cells_square):
            x = 0
            header += "    " + str(y)
            rows += str(y) + " "

            for x in range(self.cells_square):
                if not found_robot and robot_position.x == x and robot_position.y == y:
                    rows += "[ R ]"
                    found_robot = True
                else:
                    if self.grid[x][y].state == 0:
                        symbol = "#"
                    elif self.grid[x][y].state == 1:
                        symbol = " "
                    else:
                        symbol = "0"
                    rows += "[ " + symbol + " ]"

            if y < self.cells_square:
                rows += "\n\n"

        print(header)
        print(rows)
