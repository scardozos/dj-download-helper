from pages.main import View
from common import config
from .main_page import MainPageController

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.main_page_controller = MainPageController(model, view)

    def start(self):
        if self.model.config.cst_config_loaded:
            self.view.switch("mainpage")
        self.view.start_mainloop()