from .config import Config
from .error import Error

class Model:
    def __init__(self):
        self.config = Config()
        self.error = Error()