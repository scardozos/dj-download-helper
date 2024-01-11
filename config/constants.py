from .enums import MusicGenres as mg
from .enums import MusicCategory as mc

DOWNLOADS_PATH = 'C:\\Users\\Santi\\Downloads'
SPEK_PATH = "C:\\Program Files\\Spek\\spek.exe"

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