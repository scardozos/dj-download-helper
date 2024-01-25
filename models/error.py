from .base import ObservableModel

class Error(ObservableModel):
    def __init__(self):
        super().__init__()
        self.err_msg = ""
        self.err_happened = False

    def trigger(self, err_msg):
        self.err_happened = True
        self.err_msg = err_msg
        self.trigger_event("error_happened")
        