from enum import Enum

class ListMode(Enum):
    FULL_LIST_MODE = "full_list_mode"
    ONLY_NEW_MUSIC = "only_new_music"

class MoveMode(Enum):
    MOVE = "Move"
    COPY = "Copy"

class MusicGenres(Enum):
    MINIMAL = "Minimal"
    HOUSE = "House"
    DEEP_HOUSE = "Deep House"
    TECH_HOUSE = "Tech House"
    TECHNO = "Techno"
    HARD_TECHNO = "Hard Techno"
    PSYTRANCE = "Psytrance"

class MusicCategory(Enum):
    CHILL = "Chill"
    MID = "Mid"
    UP = "Up"