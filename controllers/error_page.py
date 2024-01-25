
class ErrorPageController():
    def __init__(self, model, view):
       self.model = model 
       self.view = view
       self.frame = self.view.frames["errorpage"]

       self.frame.err_msg_var.set(model.error.err_msg)