from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from framework.app.widget.mapwidget import MapWidget
from framework.app.widget.toolbarwidget import ToolbarWidget
from framework.app.widget.panelwidget import PanelWidget
from framework.app.widget.popupmapwidget import PopupMapWidget
from framework.app.widget.filewidget import FileWidget

from framework.model.map import Map
from framework.model.simulated_robot import SimulatedRobot


class RobotApp(App):
    """

    """

    def __init__(self):
        App.__init__(self)

        self.robot = SimulatedRobot(None)

        self.brush = "start"

        self.map_widget = None
        self.panel_widget = None
        self.toolbar_widget = None
        self.horizontal_layout = None
        self.vertical_layout = None

        self.popup = None

    def build(self):
        """

        :return:
        """
        self.map_widget = MapWidget(self)
        self.panel_widget = PanelWidget()
        self.toolbar_widget = ToolbarWidget(self, orientation="horizontal")

        self.horizontal_layout = BoxLayout(orientation="horizontal")
        self.horizontal_layout.add_widget(self.map_widget)
        self.horizontal_layout.add_widget(self.panel_widget)

        self.vertical_layout = BoxLayout(orientation="vertical")
        self.vertical_layout.add_widget(self.toolbar_widget)
        self.vertical_layout.add_widget(self.horizontal_layout)

        return self.vertical_layout

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
        map_model = Map(self.robot, None, None, str(self.popup.file_input.text))
        self.map_widget.set_map(map_model)

        self.horizontal_layout.remove_widget(self.popup)
        self.horizontal_layout.add_widget(self.map_widget, index=1)

    def save_map(self, instance):
        self.map_widget.map_model.file = self.popup.file_input.text
        self.map_widget.map_model.save()

        self.horizontal_layout.remove_widget(self.popup)
        self.horizontal_layout.add_widget(self.map_widget, index=1)

    def show_open_dialog(self):
        self.horizontal_layout.remove_widget(self.map_widget)

        self.popup = FileWidget(self.open_map, self.cancel_dialog, "Open")
        self.horizontal_layout.add_widget(self.popup, index=1)

    def show_save_dialog(self):
        self.horizontal_layout.remove_widget(self.map_widget)

        self.popup = FileWidget(self.save_map, self.cancel_dialog, "Save")
        self.horizontal_layout.add_widget(self.popup, index=1)

    def on_popup_ok_button(self, instance):
        content = self.popup.content

        self.popup.dismiss()
        self.map_widget.create_new_map(float(content.size_text_input.text), float(content.cell_text_input.text))

    def on_popup_cancel_button(self, instance):
        self.popup.dismiss()

    def cancel_dialog(self, instance):
        self.horizontal_layout.remove_widget(self.popup)
        self.horizontal_layout.add_widget(self.map_widget, index=1)