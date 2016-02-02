"""

"""


class OdometryReport:
    """

    """

    def __init__(self, x, y, heading):
        """

        :param x:
        :param y:
        :param heading:
        :return:
        """
        self.x = x
        self.y = y
        self.heading = heading

    def __str__(self):
        """

        :return:
        """
        return ("x: " + str(self.x) + ", y: " + str(self.y)
                + ", heading: " + str(self.heading))


class ScanResult:
    """

    """

    def __init__(self, readings):
        """

        :param readings:
        :return:
        """
        self.readings = readings

    def __str__(self):
        """

        :return:
        """
        string = "scan: "

        for reading in self.readings:
            string += str(reading) + ", "

        return string


class StateEvent:
    """

    """

    def __init__(self, state):
        """

        :param state:
        :return:
        """
        self.state = state

    def __str__(self):
        """

        :return:
        """
        return "state: " + str(self.state)
