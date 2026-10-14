
class ErrorPageController():
    def __init__(self, model, view):
        self.model = model 
        self.view = view
        self.frame = self.view.frames["errorpage"]

        self.frame.back_btn.config(command=self.go_to_configpage)

        self.update(self.model.error)

    def update(self, err_model):
        self.model.error = err_model
        self.frame.err_msg_var.set(err_model.err_msg)

        # Nothing to go back to if the config file itself couldn't be loaded
        if self.model.config.config is None:
            self.frame.back_btn.grid_remove()
        else:
            self.frame.back_btn.grid()

    def go_to_configpage(self):
        self.model.error.clear()
        self.view.switch("configpage")