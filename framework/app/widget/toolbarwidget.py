from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.label import Label


class ToolbarWidget(BoxLayout):
    """

    """

    def __init__(self, app, **kwargs):
        BoxLayout.__init__(self, **kwargs)

        self.app = app

        self.spacing = 10
        self.padding = [10, 10, 325, 10]

        self.new_button = Button(text="new")
        self.new_button.bind(on_press=self.new_button_on_press)

        self.open_button = Button(text="open")
        self.open_button.bind(on_press=self.open_button_on_press)

        self.save_button = Button(text="save")
        self.save_button.bind(on_press=self.save_button_on_press)

        self.start_toggle_button = ToggleButton(text="start", group="brush", state="down")
        self.start_toggle_button.bind(on_press=self.start_button_on_press)

        self.goal_toggle_button = ToggleButton(text="goal", group="brush")
        self.goal_toggle_button.bind(on_press=self.goal_button_on_press)

        self.obstacle_toggle_button = ToggleButton(text="obstacle", group="brush")
        self.obstacle_toggle_button.bind(on_press=self.obstacle_button_on_press)

        self.run_pause_button = Button(text="run/pause")
        self.run_pause_button.bind(on_press=self.run_button_on_press)

        self.stop_button = Button(text="stop")
        self.stop_button.bind(on_press=self.stop_button_on_press)

        self.speed_label = Label(text="Execution Speed: ")
        self.speed_slider = Slider(min=-3, max=3, value=0)

        self.add_widget(self.new_button)
        self.add_widget(self.open_button)
        self.add_widget(self.save_button)
        self.add_widget(self.start_toggle_button)
        self.add_widget(self.goal_toggle_button)
        self.add_widget(self.obstacle_toggle_button)
        self.add_widget(self.run_pause_button)
        self.add_widget(self.stop_button)
        self.add_widget(self.speed_label)
        self.add_widget(self.speed_slider)

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
        print("run/pause")

    def stop_button_on_press(self, instance):
        print("stop")
