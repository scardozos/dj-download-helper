from .base import ObservableModel
from common import config
from common.enums import MoveMode, ListMode

class Config(ObservableModel):
    def __init__(self):
        super().__init__()

        settings, self.cst_config_loaded = config.load_and_gen_if_not_exists()
        
        if settings is not None:
            self.config = settings
            self.current_move_mode = settings.default.move_mode
            self.current_list_mode = settings.default.list_mode
        else:
            self.config = None
            


    def change_current_move_mode_to(self, move_mode: MoveMode):
        self.current_move_mode = move_mode
        self.trigger_event("move_mode_changed")

    def change_current_list_mode_to(self, list_mode: ListMode):
        self.current_list_mode = list_mode
        self.trigger_event("list_mode_changed")