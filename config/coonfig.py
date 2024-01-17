import json 
from typing import List
from pydantic import BaseModel, ValidationError
from .enums import MoveMode, ListMode
from .enums import MusicCategory, MusicGenres 
from .constants import MUSIC_PATH, DOWNLOADS_PATH
from .constants import SPEK_PATH, MUSIC_CATEGORIES, MUSIC_GENRES
from enum import Enum

class BaseConfig(BaseModel):
    music_path: str
    downloads_path: str
    spek_path: str
    
    displayed_music_categories: List[MusicCategory]
    displayed_music_genres: List[MusicGenres]

class DefaultConfig(BaseModel):
    music_genre: MusicGenres
    music_category: MusicCategory
    move_mode: MoveMode
    list_mode: ListMode
    
class Config(BaseConfig):
    default: DefaultConfig

def load_and_gen_if_not_exists() -> Config:
    try:
        with open('config.json') as f:
            config_json = json.load(f)
            print("Config file found! Deserializing")
            config = Config(**config_json)

            return config

    except FileNotFoundError as e:
        print("Config file not found! Generating...")

        config = Config(
            music_path=MUSIC_PATH,
            downloads_path=DOWNLOADS_PATH,
            spek_path=SPEK_PATH,
            displayed_music_categories=MUSIC_CATEGORIES,
            displayed_music_genres=MUSIC_GENRES,
            default=DefaultConfig(
                music_genre=MusicGenres.MINIMAL,
                music_category=MusicCategory.UP,
                move_mode=MoveMode.COPY,
                list_mode=ListMode.FULL_LIST_MODE
            )
        )
        
        config_json = config.model_dump_json(indent=4)

        with open('config.json', "w") as f:
            f.write(config_json)

        return config

    except ValidationError as e:
        print("FATAL! CONFIG FILE INVALID")
        return None