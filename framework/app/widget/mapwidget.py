from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, ListProperty, StringProperty


class MapWidget(Widget):
    """

    """

    grid_spacing = NumericProperty(30.)  # Number of pixels between each grid line.
    grid_line_width = NumericProperty(1)  # Width of grid lines.
    grid_line_color = ListProperty([1, 1, 1, 1])  # Color of grid lines in RGBA.
    grid_outline_color = ListProperty([1, 1, 1, 1])  # Color of line around grid.
    grid_outline_width = NumericProperty(1)  # Width of grid outline.
    grid_location = StringProperty('behind')  # Location of grid lines, takes 'behind' or 'on_top'.

    def __init__(self, map_model, robot, path):
        """

        :param map_model:
        :return:
        """
        Widget.__init__(self)

        self.map_model = map_model
        self.robot = robot
        self.path = path

        self.draw_grid()

    def on_size(self, instance, value):
        self.canvas.before.clear()
        self.canvas.after.clear()
        self.draw_grid()

    def draw_background(self):
        return

    def draw_obstacles(self):
        return

    def draw_path(self):
        return

    def draw_robot(self):
        return

    def draw_grid(self):
        if self.grid_location == 'behind':
            canvas = self.canvas.before
            width = self.size[0]
            height = self.size[1]
            iterations = 0
            grid_spacing = self.grid_spacing

            # Draw grid interior.
            with canvas:
                Color(rgba=self.grid_line_color)

                while width > grid_spacing:
                    Line(width=self.grid_line_width,
                         points=(self.pos[0] + iterations * grid_spacing,
                                 self.pos[1],
                                 self.pos[0] + iterations * grid_spacing,
                                 self.pos[1] + self.size[1]))
                    width -= grid_spacing
                    iterations += 1
                iterations = 0

                while height > grid_spacing:
                    Line(width=self.grid_line_width,
                         points=(self.pos[0],
                                 self.pos[1] + iterations * grid_spacing,
                                 self.pos[0] + self.size[0],
                                 self.pos[1] + iterations * grid_spacing))
                    height -= grid_spacing
                    iterations += 1

            # Draw grid outline.
            with self.canvas.after:
                Color(self.grid_outline_color)
                Line(width=self.grid_outline_width, rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1]))

    def draw_coordinates(self):
        return
