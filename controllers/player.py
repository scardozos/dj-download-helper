import os
import tkinter as tk
from models.player import Player

TICK_MS = 250
SEEK_STEP_SECONDS = 10

class PlayerController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["mainpage"]
        self.bar = self.frame.player_bar
        self.listbox: tk.Listbox = self.frame.listbox
        self.player: Player = self.model.player

        self.dragging_slider = False
        self.tick_id = None

        self.bar.play_pause_btn.config(command=self.handle_play_pause)
        self.bar.prev_btn.config(command=self.handle_previous)
        self.bar.next_btn.config(command=self.handle_next)

        self.bar.seek_scale.bind("<ButtonPress-1>", self.handle_slider_press)
        self.bar.seek_scale.bind("<ButtonRelease-1>", self.handle_slider_release)

        # Shortcuts, bound on the listbox so they don't clash with
        # typing in entries or with space activating a focused button
        self.listbox.bind("<Double-Button-1>", self.handle_double_click)
        self.listbox.bind("<space>", self.handle_play_pause)
        self.listbox.bind("<Left>", lambda e: self.seek_relative(-SEEK_STEP_SECONDS))
        self.listbox.bind("<Right>", lambda e: self.seek_relative(SEEK_STEP_SECONDS))

        self.player.add_event_listener("player_changed", self.player_changed_listener)
        self.player.add_event_listener("player_error", self.player_error_listener)

        self.bar.bind("<Destroy>", self.shutdown)

        self.tick()

    # -- Playlist --

    def get_path(self, idx: int) -> str:
        return os.path.join(
            self.model.config.config.downloads_path,
            self.listbox.get(idx)
        )

    def get_selected_idx(self):
        selected = self.listbox.curselection()
        return selected[0] if selected else None

    def get_current_idx(self):
        """Index of the playing track in the list, else the selected one"""
        current_name = os.path.basename(self.player.current_path)
        items = self.listbox.get(0, tk.END)
        if current_name in items:
            return items.index(current_name)
        return self.get_selected_idx()

    def select_idx(self, idx: int):
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)
        self.listbox.see(idx)
        # Keeps the main page's selected file & destination path in sync
        self.listbox.event_generate("<<ListboxSelect>>")

    def play_idx(self, idx: int):
        self.select_idx(idx)
        self.player.load_and_play(self.get_path(idx))

    # -- Handlers --

    def handle_play_pause(self, event=None):
        if self.listbox.size() == 0:
            return "break"

        selected_idx = self.get_selected_idx()

        if selected_idx is None:
            if self.player.current_path:
                self.player.toggle_pause()
            else:
                self.play_idx(0)
        elif self.get_path(selected_idx) == self.player.current_path:
            self.player.toggle_pause()
        else:
            self.play_idx(selected_idx)

        return "break"

    def handle_double_click(self, event):
        idx = self.listbox.nearest(event.y)
        if idx >= 0:
            self.play_idx(idx)
        return "break"

    def handle_previous(self):
        self.skip(-1)

    def handle_next(self):
        self.skip(1)

    def skip(self, step: int) -> bool:
        current_idx = self.get_current_idx()
        if current_idx is None:
            return False

        new_idx = current_idx + step
        if not 0 <= new_idx < self.listbox.size():
            return False

        self.play_idx(new_idx)
        return True

    def seek_relative(self, seconds: float):
        self.player.seek(self.player.position() + seconds)
        return "break"

    def handle_slider_press(self, event):
        self.dragging_slider = True

    def handle_slider_release(self, event):
        self.dragging_slider = False
        self.player.seek(self.bar.seek_scale.get())

    # -- Listeners & UI updates --

    def player_changed_listener(self, player: Player):
        self.bar.play_pause_btn_txt.set(
            "⏸" if player.current_path and not player.is_paused else "▶"
        )
        self.bar.track_name_var.set(
            os.path.basename(player.current_path) or "Nothing playing"
        )
        self.bar.seek_scale.config(to=player.length)
        self.bar.time_total_var.set(self.format_time(player.length))

    def player_error_listener(self, player: Player):
        self.frame.move_res_label_var.set(player.last_error)

    def tick(self):
        if self.player.is_finished():
            # Autoplay the next track, stop at the end of the list
            if not self.skip(1):
                self.player.stop()

        position = (
            self.bar.seek_scale.get()
            if self.dragging_slider
            else self.player.position()
        )

        if not self.dragging_slider:
            self.bar.seek_scale.set(position)

        self.bar.time_elapsed_var.set(self.format_time(position))

        self.tick_id = self.bar.after(TICK_MS, self.tick)

    def shutdown(self, event):
        if self.tick_id:
            self.bar.after_cancel(self.tick_id)
            self.tick_id = None
        self.player.quit()

    @staticmethod
    def format_time(seconds: float) -> str:
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes}:{seconds:02d}"
