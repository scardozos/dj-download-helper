from pages.main import View
from common import config
from .main_page import MainPageController
from .config_page import ConfigPageController
from .error_page import ErrorPageController

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.main_page_controller = MainPageController(self.model, self.view)
        self.config_page_controller = ConfigPageController(self.model, self.view)
        self.error_page_controller = ErrorPageController(self.model, self.view)

        self.model.error.add_event_listener(
            "error_happened", self.error_state_listener
        )

        self.model.config.add_event_listener(
            "config_saved", self.config_saved_listener
        )

    def start(self):
        if self.model.config.cst_config_loaded:
            
            self.view.switch("configpage")

            # Disabled while working on configpage, uncomment l8r 
            # & rm switch to configpage
            #self.view.switch("mainpage")

        if not self.model.config.cst_config_loaded:
            self.view.switch("configpage")

        if (not self.model.config.cst_config_loaded and
            self.model.config.config == None):
            self.model.error.trigger("Config invalid")

        self.view.start_mainloop()

    def config_saved_listener(self, new_config):
        config.save_config_to_json_file(new_config.config, "config.json")
        self.main_page_controller.fill_view(new_config.config)

    def error_state_listener(self, data):
        if data.err_happened:
            self.error_page_controller.update(data)
            self.view.switch("errorpage")