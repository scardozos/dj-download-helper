from .enums import MusicGenres as mg
from .enums import MusicCategory as mc
from .enums import MoveMode as mm
from .enums import ListMode as lm

MUSIC_PATH = 'D:\\Music\\Organized'
DOWNLOADS_PATH = 'C:\\Users\\Santi\\Downloads'
SPEK_PATH = "C:\\Program Files\\Spek\\spek.exe"

DEFAULT_MUSIC_GENRE = mg.MINIMAL
DEFAULT_MUSIC_CATEGORY = mc.UP
DEFAULT_MOVE_MODE = mm.COPY
DEFAULT_LIST_MODE = lm.FULL_LIST_MODE

SUPPORTED_AUDIO_EXTENSIONS = [
    ".mp3",
    ".aiff",
    ".flac",
    ".wav"
]

MUSIC_GENRES = [
    mg.MINIMAL,
    mg.HOUSE,
    mg.DEEP_HOUSE,
    mg.TECH_HOUSE,
    mg.TECHNO,
    mg.HARD_TECHNO,
    mg.PSYTRANCE,
]

MUSIC_CATEGORIES = [
    mc.CHILL,
    mc.MID,
    mc.UP
]

SHOW_NEW_DOWNLOADS_TXT = "Only show new downloads"
SHOW_ALL_DOWNLOADS_TXT = "Show all downloads"
ENABLE_REFRESH_TXT = "Enable Auto-Refresh"
DISABLE_REFRESH_TXT = "Disable Auto-Refresh"