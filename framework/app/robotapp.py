from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.screenmanager import ScreenManager

from kivy.uix.button import Button

from framework.app.widget.mapwidget import MapWidget
from framework.app.widget.toolbarwidget import ToolbarWidget
from framework.app.widget.panelwidget import PanelWidget


class RobotApp(App):
    """

    """

    def build(self):
        """

        :return:
        """

        map_widget = MapWidget(None, None, None)

        horizontal_layout = BoxLayout(orientation="horizontal")
        horizontal_layout.add_widget(map_widget)
        horizontal_layout.add_widget(PanelWidget())

        vertical_layout = BoxLayout(orientation="vertical")
        vertical_layout.add_widget(ToolbarWidget(orientation="horizontal"))
        vertical_layout.add_widget(horizontal_layout)

        return vertical_layout
