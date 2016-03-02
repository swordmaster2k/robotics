from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import NumericProperty, ListProperty, StringProperty

from framework.util.listener import Listener


class MapWidget(Widget, Listener):
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

    def __init__(self, app):
        """

        :param app:
        :return:
        """
        Widget.__init__(self)

        self.METER_TO_PIXEL_SCALE = 100

        self.app = app
        self.map_model = None

    def handle_event(self, event):
        self.draw()

    def set_map(self, map_model):
        """

        :param map_model:
        :return:
        """
        self.map_model = map_model

        self.draw()

    def on_touch_down(self, touch):
        """

        :param touch:
        :return:
        """
        x = int(touch.pos[0] / (self.map_model.cell_size * self.METER_TO_PIXEL_SCALE))
        y = int(touch.pos[1] / (self.map_model.cell_size * self.METER_TO_PIXEL_SCALE))

        if 0 < x < self.map_model.cells_square - 1 and 0 < y < self.map_model.cells_square - 1:
            self.app.handle_touch_down(x, y)

    def on_size(self, instance, value):
        """

        :param instance:
        :param value:
        :return:
        """
        self.draw()

    def draw(self):
        """

        :return:
        """
        self.canvas.before.clear()
        self.canvas.after.clear()

        canvas = self.canvas.before

        self.draw_cells(canvas)

        if len(self.map_model.path.points) > 0:
            self.draw_path(canvas)

        self.draw_grid(canvas)

    def draw_cells(self, canvas):
        """

        :param canvas:
        :return:
        """
        with canvas:
            for x in range(self.map_model.cells_square):
                for y in range(self.map_model.cells_square):
                    if x == self.map_model.goal.x and y == self.map_model.goal.y:
                        Color(rgba=self.cell_goal_color)
                    elif x == self.map_model.robot.get_cell_x() and y == self.map_model.robot.get_cell_y():
                        Color(rgba=self.cell_robot_color)
                    elif self.map_model.grid[x][y].state == 0:
                        Color(rgba=self.cell_empty_color)
                    else:
                        Color(rgba=self.cell_full_color)

                    cell_size = self.map_model.cell_size * self.METER_TO_PIXEL_SCALE
                    Rectangle(pos=(x * cell_size, y * cell_size), size=(cell_size, cell_size))

    def draw_path(self, canvas):
        """

        :param canvas:
        :return:
        """
        cell_size = self.map_model.cell_size * self.METER_TO_PIXEL_SCALE
        half_cell_size = cell_size / 2

        for i in range(len(self.map_model.path.points) - 1):
            with canvas:
                Color(rgba=self.path_line_color)
                Line(width=self.path_line_width,
                     points=(self.map_model.path.points[i][0] * cell_size,
                             self.map_model.path.points[i][1] * cell_size,
                             self.map_model.path.points[i + 1][0] * cell_size,
                             self.map_model.path.points[i + 1][1] * cell_size))

                # Way point.
                Color(rgba=self.path_point_color)
                Rectangle(pos=(self.map_model.path.points[i][0] * cell_size - 2.5,
                               self.map_model.path.points[i][1] * cell_size - 2.5),
                          size=(5, 5))

        # Last point in the path.
        with canvas:
            Rectangle(pos=(self.map_model.path.points[len(self.map_model.path.points) - 1][0] * cell_size - 2.5,
                           self.map_model.path.points[len(self.map_model.path.points) - 1][1] * cell_size - 2.5),
                      size=(5, 5))

    def draw_grid(self, canvas):
        """

        :param canvas:
        :return:
        """
        if self.grid_location == 'behind':
            width = (self.map_model.cell_size * self.map_model.cells_square) * self.METER_TO_PIXEL_SCALE
            height = width

            iterations = 0
            temp_width = width + (self.map_model.cell_size * self.METER_TO_PIXEL_SCALE)
            temp_height = height + (self.map_model.cell_size * self.METER_TO_PIXEL_SCALE)
            grid_spacing = self.map_model.cell_size * self.METER_TO_PIXEL_SCALE

            # Draw grid interior.
            with canvas:
                Color(rgba=self.grid_line_color)

                while temp_width > grid_spacing:
                    Line(width=self.grid_line_width,
                         points=(self.pos[0] + iterations * grid_spacing,
                                 0,
                                 self.pos[0] + iterations * grid_spacing,
                                 width))
                    temp_width -= grid_spacing
                    iterations += 1
                iterations = 0

                while temp_height > grid_spacing:
                    Line(width=self.grid_line_width,
                         points=(0,
                                 self.pos[1] + iterations * grid_spacing,
                                 height,
                                 self.pos[1] + iterations * grid_spacing))
                    temp_height -= grid_spacing
                    iterations += 1

            # Draw grid outline.
            with self.canvas.after:
                Color(self.grid_outline_color)
                Line(width=self.grid_outline_width, rectangle=(0, 0, width, height))

    def draw_coordinates(self):
        """

        :return:
        """
        return
