from framework.util.notifier import Notifier


class Path(Notifier):
    """

    """

    def __init__(self, points):
        """

        :return:
        """
        Notifier.__init__(self)

        self.points = points

    def update_points(self, points):
        """

        :param points:
        :return:
        """
        self.points = points

        self.notify_listeners(self.points)
