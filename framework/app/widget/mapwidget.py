from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import NumericProperty, ListProperty, StringProperty


class MapWidget(Widget):
    """

    """
    cell_goal_color = ListProperty([0, 1, 0, 1])
    cell_robot_color = ListProperty([1, 1, 0, 1])
    cell_empty_color = ListProperty([0, 0, 1, 1])
    cell_full_color = ListProperty([1, 0, 0, 1])

    path_line_width = NumericProperty(2)
    path_point_color = ListProperty([0, 1, 1, 1])
    path_line_color = ListProperty([1, 0, 1, 1])

    grid_line_width = NumericProperty(1)  # Width of grid lines.
    grid_line_color = ListProperty([1, 1, 1, 1])  # Color of grid lines in RGBA.
    grid_outline_color = ListProperty([1, 1, 1, 1])  # Color of line around grid.
    grid_outline_width = NumericProperty(1)  # Width of grid outline.
    grid_location = StringProperty('behind')  # Location of grid lines, takes 'behind' or 'on_top'.

    def __init__(self, app, map_model, robot, path):
        """

        :param map_model:
        :return:
        """
        Widget.__init__(self)

        self.app = app

        self.map_model = map_model
        self.robot = robot
        self.path = path

        self.cell_size = 30.0
        self.cells_square = 10
        self.squared_size = self.cell_size * self.cells_square

        self.goal_x = 7
        self.goal_y = 7
        self.robot_x = 1
        self.robot_y = 1
        self.path = [[2.5, 2.5], [3.5, 3.5], [3.5, 4.5], [3.5, 5.5], [4.5, 6.5], [5.5, 7.5], [6.5, 7.5], [7.5, 7.5]]
        self.grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def set_map(self, config):
        self.grid = []
        self.cell_size = config[2]
        self.cells_square = int(config[0])
        self.squared_size = self.cell_size * self.cells_square

        self.goal_x = self.cells_square - 2
        self.goal_y = self.cells_square - 2
        self.robot_x = 1
        self.robot_y = 1

        self.grid.append([1] * self.cells_square)
        self.add_grid_row(self.cells_square - 2)
        self.grid.append([1] * self.cells_square)

        self.draw()

    def add_grid_row(self, rows):
        row = [0] * self.cells_square
        row[0] =  1
        row[self.cells_square - 1] = 1
        self.grid.append(row)

        rows -= 1

        if rows == 0:
            return
        else:
            self.add_grid_row(rows)

    def on_touch_down(self, touch):
        x = int(touch.pos[0] / self.cell_size)
        y = int(touch.pos[1] / self.cell_size)

        if 0 < x < self.cells_square - 1 and 0 < y < self.cells_square - 1:
            if self.app.brush == "start":
                self.robot_x = x
                self.robot_y = y
            elif self.app.brush == "goal":
                self.goal_x = x
                self.goal_y = y
            else:
                self.grid[x][y] ^= 1

            self.draw()

    def on_size(self, instance, value):
        self.draw()

    def draw(self):
        self.canvas.before.clear()
        self.canvas.after.clear()

        canvas = self.canvas.before

        self.draw_cells(canvas)
        self.draw_path(canvas)
        self.draw_grid(canvas)

    def draw_cells(self, canvas):
        with canvas:
            for x in range(self.cells_square):
                for y in range(self.cells_square):
                    if x == self.goal_x and y == self.goal_y:
                        Color(rgba=self.cell_goal_color)
                    elif x == self.robot_x and y == self.robot_y:
                        Color(rgba=self.cell_robot_color)
                    elif self.grid[x][y] == 0:
                        Color(rgba=self.cell_empty_color)
                    else:
                        Color(rgba=self.cell_full_color)

                    Rectangle(pos=(x * self.cell_size, y * self.cell_size), size=(self.cell_size, self.cell_size))

    def draw_path(self, canvas):
        for i in range(len(self.path) - 1):
            with canvas:
                Color(rgba=self.path_line_color)
                Line(width=self.path_line_width,
                     points=(self.path[i][0] * self.cell_size,
                             self.path[i][1] * self.cell_size,
                             self.path[i + 1][0] * self.cell_size,
                             self.path[i + 1][1] * self.cell_size))

                Color(rgba=self.path_point_color)
                Rectangle(pos=(self.path[i][0] * self.cell_size - 2.5, self.path[i][1] * self.cell_size - 2.5),
                          size=(5, 5))

        with canvas:
            Rectangle(pos=(self.path[len(self.path) - 1][0] * self.cell_size - 2.5,
                           self.path[len(self.path) - 1][1] * self.cell_size - 2.5),
                      size=(5, 5))

    def draw_grid(self, canvas):
        if self.grid_location == 'behind':
            width = self.cell_size * self.cells_square + self.cell_size
            height = width
            iterations = 0
            grid_spacing = self.cell_size

            # Draw grid interior.
            with canvas:
                Color(rgba=self.grid_line_color)

                while width > grid_spacing:
                    Line(width=self.grid_line_width,
                         points=(self.pos[0] + iterations * grid_spacing,
                                 0,
                                 self.pos[0] + iterations * grid_spacing,
                                 self.squared_size))
                    width -= grid_spacing
                    iterations += 1
                iterations = 0

                while height > grid_spacing:
                    Line(width=self.grid_line_width,
                         points=(0,
                                 self.pos[1] + iterations * grid_spacing,
                                 self.squared_size,
                                 self.pos[1] + iterations * grid_spacing))
                    height -= grid_spacing
                    iterations += 1

            # Draw grid outline.
            with self.canvas.after:
                Color(self.grid_outline_color)
                Line(width=self.grid_outline_width, rectangle=(0, 0, self.squared_size, self.squared_size))

    def draw_coordinates(self):
        return
