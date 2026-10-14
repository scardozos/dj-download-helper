import os
import shutil

SUPPORTED_AUDIO_EXTENSIONS = [
    ".mp3",
    ".aiff",
    ".flac",
    ".wav",
    ".m4a"
]

SHOW_NEW_DOWNLOADS_TXT = "Only show new downloads"
SHOW_ALL_DOWNLOADS_TXT = "Show all downloads"
ENABLE_REFRESH_TXT = "Enable Auto-Refresh"
DISABLE_REFRESH_TXT = "Disable Auto-Refresh"
AVAILABLE_MUSIC_GENRES_TXT = "Available Music Genres"
DISPLAYED_MUSIC_GENRES_TXT = "Displayed Music Genres"
AVAILABLE_MUSIC_CATEGORIES_TXT = "Available Music Categories"
DISPLAYED_MUSIC_CATEGORIES_TXT = "Displayed Music Categories"


CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config.json"
)

# Defaults used to generate the config file on first run
MUSIC_PATH = os.path.join(os.path.expanduser("~"), "Music")
DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
SPEK_PATH = shutil.which("spek") or next(
    (
        path for path in [
            "C:\\Program Files\\Spek\\spek.exe",
            "C:\\Program Files (x86)\\Spek\\spek.exe",
        ]
        if os.path.exists(path)
    ),
    ""
)

DEFAULT_MUSIC_GENRES = [
    "Minimal",
    "House",
    "Deep House",
    "Tech House",
    "Techno",
    "Hard Techno",
    "Psytrance",
]

DEFAULT_MUSIC_CATEGORIES = [
    "Chill",
    "Mid",
    "Up"
]