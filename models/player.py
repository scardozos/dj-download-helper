import os
import mutagen
from .base import ObservableModel

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame


class Player(ObservableModel):
    def __init__(self):
        super().__init__()

        self.current_path = ""
        self.length = 0.0
        self.is_paused = False
        self.last_error = ""

        # get_pos() restarts from 0 every time play() is called (e.g. when
        # seeking), so keep track of where the last play() started from
        self._offset = 0.0

        try:
            pygame.mixer.init()
            self.available = True
        except pygame.error as e:
            print(f"Audio device not available: {e}")
            self.available = False

    def load_and_play(self, path: str) -> bool:
        if not self.available:
            return self._fail("No audio device available")

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error playing '{path}': {e}")
            self.stop()
            return self._fail(
                f"Can't play '{os.path.basename(path)}' (format not supported)"
            )

        self.current_path = path
        self.length = self._get_length(path)
        self.is_paused = False
        self._offset = 0.0
        self.last_error = ""
        self.trigger_event("player_changed")
        return True

    def toggle_pause(self):
        if not self.current_path:
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        self.is_paused = not self.is_paused
        self.trigger_event("player_changed")

    def stop(self):
        """Stop and release the file, so it can be moved (Windows locks it)"""
        if self.available:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

        self.current_path = ""
        self.length = 0.0
        self.is_paused = False
        self._offset = 0.0
        self.trigger_event("player_changed")

    def seek(self, seconds: float) -> bool:
        if not self.current_path:
            return False

        seconds = max(0.0, seconds)
        if self.length:
            seconds = min(seconds, self.length)

        try:
            pygame.mixer.music.play(start=seconds)
        except pygame.error as e:
            print(f"Error seeking: {e}")
            return self._fail("Seeking is not supported for this file")

        if self.is_paused:
            pygame.mixer.music.pause()

        self._offset = seconds
        return True

    def position(self) -> float:
        if not self.current_path:
            return 0.0

        # get_pos() is -1 once the track has stopped
        played = max(pygame.mixer.music.get_pos(), 0) / 1000
        position = self._offset + played
        return min(position, self.length) if self.length else position

    def is_finished(self) -> bool:
        return (
            bool(self.current_path)
            and not self.is_paused
            and not pygame.mixer.music.get_busy()
        )

    def quit(self):
        if self.available:
            pygame.mixer.quit()
            self.available = False

    def _get_length(self, path: str) -> float:
        try:
            audio = mutagen.File(path)
            # A file without tags is falsy, so compare against None
            return audio.info.length if audio is not None else 0.0
        except mutagen.MutagenError as e:
            print(f"Error reading length of '{path}': {e}")
            return 0.0

    def _fail(self, err_msg: str) -> bool:
        self.last_error = err_msg
        self.trigger_event("player_error")
        return False
