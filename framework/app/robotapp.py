from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from framework.navigation.pathplanning.gridnav import GridNav

from framework.app.state import State
from framework.app.widget.mapwidget import MapWidget
from framework.app.widget.toolbarwidget import ToolbarWidget
from framework.app.widget.panelwidget import PanelWidget
from framework.app.widget.popupmapwidget import PopupMapWidget
from framework.app.widget.filewidget import FileWidget

from framework.model.map import Map
from framework.model.simulated_robot import Robot
from framework.event.events import OdometryReport
from framework.io.proxy import Proxy
from framework.io.bluetooth_connection import BluetoothConnection
from framework.navigation.planner import Planner


class RobotApp(App):
    """

    """

    def __init__(self):
        """

        :return:
        """
        App.__init__(self)

        # Connection
        self.connection = BluetoothConnection("00:00:12:06:56:83", 0x1001)
        self.proxy = Proxy(self.connection)
        self.proxy.start()

        # Model
        self.robot = Robot(self.proxy)
        self.robot.cell_size = 0.3
        self.robot.x = 0.3
        self.robot.y = 0.3

        self.map_model = Map(self.robot, 3.0, 0.3)
        self.state = State.default
        self.brush = "start"

        self.planning_algorithm = GridNav(self.map_model)
        self.planner = Planner(self.robot, self.map_model, self.planning_algorithm, self.proxy)

        # View
        self.map_widget = None
        self.panel_widget = None
        self.toolbar_widget = None
        self.horizontal_layout = None
        self.vertical_layout = None
        self.popup = None

        self.plan()

    def build(self):
        """

        :return:
        """
        self.map_widget = MapWidget(self)
        self.map_widget.set_map(self.map_model)

        self.panel_widget = PanelWidget()
        self.toolbar_widget = ToolbarWidget(self, orientation="horizontal")

        self.horizontal_layout = BoxLayout(orientation="horizontal")
        self.horizontal_layout.add_widget(self.map_widget)
        self.horizontal_layout.add_widget(self.panel_widget)

        self.vertical_layout = BoxLayout(orientation="vertical")
        self.vertical_layout.add_widget(self.toolbar_widget)
        self.vertical_layout.add_widget(self.horizontal_layout)

        # Add model listeners.
        self.setup_listeners()

        return self.vertical_layout

    def on_start(self):
        return

    def on_stop(self):
        return

    def setup_listeners(self):
        """

        :return:
        """
        self.proxy.listeners.append(self.robot)

        self.robot.listeners.append(self.map_widget)
        self.map_model.listeners.append(self.map_widget)
        self.map_model.path.listeners.append(self.map_widget)

    def create_new_map(self):
        """

        :return:
        """

        new_map_widget = PopupMapWidget()
        new_map_widget.ok_button.bind(on_press=self.on_popup_ok_button)
        new_map_widget.cancel_button.bind(on_press=self.on_popup_cancel_button)

        self.popup = Popup(title='New Map', content=new_map_widget, size_hint=(None, None), size=(300, 200),
                           auto_dismiss=True)
        self.popup.open()

    def open_map(self, instance):
        """

        :param instance:
        :return:
        """
        map_model = Map(self.robot, None, None, str(self.popup.file_input.text))
        self.map_widget.set_map(map_model)

        self.horizontal_layout.remove_widget(self.popup)
        self.horizontal_layout.add_widget(self.map_widget, index=1)

        self.reset_state()

    def save_map(self, instance):
        """

        :param instance:
        :return:
        """
        self.map_widget.map_model.file = self.popup.file_input.text
        self.map_widget.map_model.save()

        self.horizontal_layout.remove_widget(self.popup)
        self.horizontal_layout.add_widget(self.map_widget, index=1)

        self.reset_state()

    def show_open_dialog(self):
        """

        :return:
        """
        if self.state == State.default:
            self.horizontal_layout.remove_widget(self.map_widget)

            self.popup = FileWidget(self.open_map, self.cancel_dialog, "Open")
            self.horizontal_layout.add_widget(self.popup, index=1)

            self.state = State.opening

    def show_save_dialog(self):
        """

        :return:
        """
        if self.state == State.default:
            self.horizontal_layout.remove_widget(self.map_widget)

            self.popup = FileWidget(self.save_map, self.cancel_dialog, "Save")
            self.horizontal_layout.add_widget(self.popup, index=1)

            self.state = State.saving

    def on_popup_ok_button(self, instance):
        """

        :param instance:
        :return:
        """
        content = self.popup.content

        self.popup.dismiss()

        self.map_model = Map(self.robot, float(content.size_text_input.text), float(content.cell_text_input.text))
        self.map_widget.set_map(self.map_model)

    def on_popup_cancel_button(self, instance):
        """

        :param instance:
        :return:
        """
        self.popup.dismiss()

    def cancel_dialog(self, instance):
        """

        :param instance:
        :return:
        """
        self.horizontal_layout.remove_widget(self.popup)
        self.horizontal_layout.add_widget(self.map_widget, index=1)

        self.reset_state()

    def reset_state(self):
        """

        :return:
        """
        self.state = State.default

    def run_plan(self):
        """

        :return:
        """
        self.plan()

        if self.planner.finished:
            self.planner.start()

    def stop_plan(self):
        """

        :return:
        """
        if not self.planner.finished:
            self.planner.finished = True

    def plan(self):
        """

        :return:
        """
        self.planning_algorithm = GridNav(self.map_model)
        self.planning_algorithm.plan()

        self.map_model.path.update_points(self.planning_algorithm.path)

    '''
    Move this out of here.
    '''
    def handle_touch_down(self, x, y):
        """

        :param x:
        :param y:
        :return:
        """
        if self.brush == "start":
            x = x * self.map_model.cell_size
            y = y * self.map_model.cell_size
            self.robot.update_odometry(OdometryReport(x, y, self.robot.heading))
        elif self.brush == "goal":
            self.map_model.set_goal_position(x, y)
        else:
            self.map_model.set_cell_state(x, y)

        self.plan()

