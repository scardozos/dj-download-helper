# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pydantic>=2.0",
#     "watchdog",
#     "pygame-ce",
#     "mutagen",
# ]
# ///

from models.main import Model
from pages.main import View
from controllers.main import Controller

if __name__ == "__main__":
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()