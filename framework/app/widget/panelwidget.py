from kivy.uix.gridlayout import GridLayout

class PanelWidget(GridLayout):
    """

    """

    def __init__(self, app, **kwargs):
        GridLayout.__init__(self, **kwargs)

        self.app = app

    def enable_checkbox_on_active(self, checkbox):
        self.ids["connect_button"].disabled = not checkbox.active
        self.ids["disconnect_button"].disabled = not checkbox.active
        self.ids["mac_address_textinput"].disabled = not checkbox.active

    def connect_button_on_press(self):
        mac_address = self.ids["mac_address_textinput"].text

        if mac_address:
            self.app.connect_bluetooth(mac_address)

    def disconnect_button_on_press(self):
        self.app.disconnect_bluetooth()
