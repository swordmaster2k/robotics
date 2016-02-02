class Notifier:
    def __init__(self):
        self.listeners = []

    def notify_listeners(self, event):
        for listener in self.listeners:
            listener.handle_event(event)