import abc


class Listener:

    @abc.abstractmethod
    def handle_event(self, event):
        raise NotImplementedError

