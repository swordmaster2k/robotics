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

        self.new_button = Button(background_normal="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/new.png",
                                 size_hint_x=None, size_hint_y=None, width=48, height=48)
        self.new_button.bind(on_press=self.new_button_on_press)

        self.open_button = Button(background_normal="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/open.png",
                                  size_hint_x=None, size_hint_y=None, width=48, height=48)
        self.open_button.bind(on_press=self.open_button_on_press)

        self.save_button = Button(background_normal="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/save.png",
                                  size_hint_x=None, size_hint_y=None, width=48, height=48)
        self.save_button.bind(on_press=self.save_button_on_press)

        self.start_toggle_button = ToggleButton(background_normal="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/start.png",
                                                background_down="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/start_down.png",
                                                group="brush", state="down", size_hint_x=None, size_hint_y=None, width=48, height=48)
        self.start_toggle_button.bind(on_press=self.start_button_on_press)

        self.goal_toggle_button = ToggleButton(background_normal="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/goal.png",
                                               background_down="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/goal_down.png",
                                               group="brush", size_hint_x=None, size_hint_y=None, width=48, height=48)
        self.goal_toggle_button.bind(on_press=self.goal_button_on_press)

        self.edit_toggle_button = ToggleButton(background_normal="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/edit.png",
                                               background_down="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/edit_down.png",
                                               group="brush", size_hint_x=None, size_hint_y=None, width=48, height=48)
        self.edit_toggle_button.bind(on_press=self.obstacle_button_on_press)

        self.run_button = Button(background_normal="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/run.png",
                                 size_hint_x=None, size_hint_y=None, width=48, height=48)
        self.run_button.bind(on_press=self.run_button_on_press)

        self.stop_button = Button(background_normal="/home/joshua/Documents/Projects/Robotics/robotics/framework/app/icon/stop.png",
                                  size_hint_x=None, size_hint_y=None, width=48, height=48)
        self.stop_button.bind(on_press=self.stop_button_on_press)

        self.add_widget(self.new_button)
        self.add_widget(self.open_button)
        self.add_widget(self.save_button)
        self.add_widget(self.start_toggle_button)
        self.add_widget(self.goal_toggle_button)
        self.add_widget(self.edit_toggle_button)
        self.add_widget(self.run_button)
        self.add_widget(self.stop_button)

    def new_button_on_press(self, instance):
        self.app.create_new_map()

    def open_button_on_press(self, instance):
        self.app.show_open_dialog()

    def save_button_on_press(self, instance):
        if self.app.map_widget.map_model.file is None:
            self.app.show_save_dialog()
        else:
            self.app.map_widget.map_model.save()

    def start_button_on_press(self, instance):
        self.app.brush = "start"

    def goal_button_on_press(self, instance):
        self.app.brush = "goal"

    def obstacle_button_on_press(self, instance):
        self.app.brush = "obstacle"

    def run_button_on_press(self, instance):
        self.app.run_plan()

    def stop_button_on_press(self, instance):
        self.app.stop_plan()
