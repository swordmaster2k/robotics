from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from .numberictextinput import NumericTextInput


class PopupMapWidget(GridLayout):
    """

    """

    def __init__(self):
        GridLayout.__init__(self, cols=2, rows=4, spacing=[5, 5])

        self.result = (None, None, None)

        self.width_text_input = NumericTextInput((10, 50), text="10")
        self.height_text_input = NumericTextInput((10, 50), text="10")
        self.cell_text_input = NumericTextInput((0.1, 1.0), True, text="0.3")

        self.ok_button = Button(text="OK")
        self.cancel_button = Button(text="Cancel")

        self.add_widget(Label(text="Width: "))
        self.add_widget(self.width_text_input)

        self.add_widget(Label(text="Height: "))
        self.add_widget(self.height_text_input)

        self.add_widget(Label(text="Cell Size: "))
        self.add_widget(self.cell_text_input)

        self.add_widget(self.ok_button)
        self.add_widget(self.cancel_button)