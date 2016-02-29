from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


class ToolbarWidget(BoxLayout):
    """

    """

    def __init__(self, app, **kwargs):
        BoxLayout.__init__(self, **kwargs)

        self.app = app

        self.spacing = 10
        self.padding = [10, 10, 325, 10]

    def new_button_on_press(self):
        self.app.create_new_map()

    def open_button_on_press(self):
        self.app.show_open_dialog()

    def save_button_on_press(self):
        if self.app.map_widget.map_model.file is None:
            self.app.show_save_dialog()
        else:
            self.app.map_widget.map_model.save()

    def start_button_on_press(self):
        self.app.brush = "start"

    def goal_button_on_press(self):
        self.app.brush = "goal"

    def obstacle_button_on_press(self):
        self.app.brush = "obstacle"

    def run_button_on_press(self):
        self.app.run_plan()

    def stop_button_on_press(self):
        self.app.stop_plan()
