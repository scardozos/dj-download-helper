
class ErrorPageController():
    def __init__(self, model, view):
        self.model = model 
        self.view = view
        self.frame = self.view.frames["errorpage"]

        self.update(self.model.error)

    def update(self, err_model):
        self.model.error = err_model
        self.frame.err_msg_var.set(err_model.err_msg)