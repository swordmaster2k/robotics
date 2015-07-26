from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from framework.app.widget.navigatorwidget import NavigatorWidget
from framework.app.widget.toolbarwidget import ToolbarWidget
from framework.app.widget.panelwidget import PanelWidget


class RobotApp(App):
    """

    """

    def build(self):
        """

        :return:
        """

        horizontal_layout = BoxLayout(orientation="horizontal")
        horizontal_layout.add_widget(NavigatorWidget())
        horizontal_layout.add_widget(PanelWidget())

        vertical_layout = BoxLayout(orientation="vertical")
        vertical_layout.add_widget(ToolbarWidget(orientation="horizontal"))
        vertical_layout.add_widget(horizontal_layout)

        return vertical_layout
