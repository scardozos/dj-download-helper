from .config import Config
from .error import Error
from .player import Player

class Model:
    def __init__(self):
        self.config = Config()
        self.error = Error()
        self.player = Player()
