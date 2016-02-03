class NoPathException(Exception):
    """
    Raised when no path to the goal can be found.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
