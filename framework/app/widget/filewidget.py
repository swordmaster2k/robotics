from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserIconView


class FileWidget(BoxLayout):
    """

    """

    def __init__(self, action_callback, cancel_callback, action_text):
        """

        :return:
        """
        BoxLayout.__init__(self, orientation="vertical")

        self.file_chooser = FileChooserIconView(size_hint=(1,0.7), on_submit=self.update_file_input)
        self.file_input = TextInput()
        self.action_button = Button(text=action_text, on_press=action_callback)
        self.cancel_button = Button(text="Cancel", on_press=cancel_callback)

        self.horizontal_layout = GridLayout(cols=3, row_force_default=True, row_default_height=40, size_hint=(1, 0.055))
        self.horizontal_layout.add_widget(self.file_input)
        self.horizontal_layout.add_widget(self.action_button)
        self.horizontal_layout.add_widget(self.cancel_button)

        self.add_widget(self.file_chooser)
        self.add_widget(self.horizontal_layout)

    def update_file_input(self, instance, selection, touch):
        self.file_input.text = selection[0]


