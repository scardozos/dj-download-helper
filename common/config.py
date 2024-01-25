import json 
from typing import List
from pydantic import BaseModel, field_validator, ValidationError, ValidationInfo
from .enums import MoveMode, ListMode
from .constants import MUSIC_PATH, DOWNLOADS_PATH
from .constants import SPEK_PATH, DEFAULT_MUSIC_CATEGORIES, DEFAULT_MUSIC_GENRES

class BaseConfig(BaseModel):
    available_music_categories: List[str]
    available_music_genres: List[str]
    music_path: str
    downloads_path: str
    spek_path: str

    
class DefaultConfig(BaseModel):
    music_genre: str
    music_category: str
    move_mode: MoveMode
    list_mode: ListMode
    
class Config(BaseConfig):
    default: DefaultConfig
    displayed_music_categories: List[str]
    displayed_music_genres: List[str]

    @field_validator("displayed_music_genres")
    @classmethod
    def validate_displayed_music_genres(
        cls, 
        displayed_genres: List[str], 
        info: ValidationInfo
    ) -> List[str]:
        if (
            not all(
                displayed_genre
                in
                info.data["available_music_genres"] 
                for displayed_genre in displayed_genres
            )
        ):
            raise ValueError("displayed_music_genres must only contain genres set in available_music_genres")
        return displayed_genres

    @field_validator("displayed_music_categories")
    @classmethod
    def validate_displayed_music_categories(
        cls, 
        displayed_categories: List[str], 
        info: ValidationInfo
    ) -> List[str]:
        if (
            not all(
                displayed_category
                in
                info.data["available_music_categories"] 
                for displayed_category in displayed_categories
            )
        ):
            raise ValueError("displayed_music_categories must only contain categories set in available_music_categories")
        return displayed_categories


def load_and_gen_if_not_exists() -> (Config, str):
    try:
        with open('config.json') as f:
            config_json = json.load(f)
            print("Config file found! Deserializing")
            config = Config(**config_json)

            return config, True

    except FileNotFoundError as e:
        print("Config file not found! Generating...")

        config = Config(
            available_music_genres=DEFAULT_MUSIC_GENRES,
            available_music_categories=DEFAULT_MUSIC_CATEGORIES,

            music_path=MUSIC_PATH,
            downloads_path=DOWNLOADS_PATH,
            spek_path=SPEK_PATH,

            displayed_music_categories=DEFAULT_MUSIC_CATEGORIES,
            displayed_music_genres=DEFAULT_MUSIC_GENRES,

            default=DefaultConfig(
                music_genre=DEFAULT_MUSIC_GENRES[0], # Minimal
                music_category=DEFAULT_MUSIC_CATEGORIES[-1], # Up
                move_mode=MoveMode.COPY,
                list_mode=ListMode.FULL_LIST_MODE
            )
        )
        
        config_json = config.model_dump_json(indent=4)

        with open('config.json', "w") as f:
            f.write(config_json)

        return config, False

    except ValidationError as e:
        print(f"FATAL! CONFIG FILE INVALID:\n{e}")
        return None, False