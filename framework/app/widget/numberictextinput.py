from kivy.uix.textinput import TextInput


class NumericTextInput(TextInput):
    """

    """

    def __init__(self, range, is_cell_size=False, **kwargs):
        TextInput.__init__(self, **kwargs)

        self.range = range
        self.is_cell_size = is_cell_size

    def insert_text(self, substring, from_undo=False):
        try:
            string = self.text + substring

            number = float(string)

            if self.is_cell_size:
                if string == "0" or string == "0.":
                    super(NumericTextInput, self).insert_text(substring)
                elif self.range[0] <= number <= self.range[1]:
                    super(NumericTextInput, self).insert_text(substring)
            else:
                if len(string) < 2:
                    super(NumericTextInput, self).insert_text(substring)
                elif self.range[0] <= number <= self.range[1]:
                    super(NumericTextInput, self).insert_text(substring)
        except TypeError:
            return

    def _on_focus(self, instance, value, *largs):
        super(NumericTextInput, self)._on_focus(instance, value, *largs)

        if not value:
            if not self.range[0] <= float(self.text) <= self.range[1]:
                self._set_text(str(self.range[0]))
