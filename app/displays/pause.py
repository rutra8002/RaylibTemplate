import pyray as rl
from app.displays.base import BaseDisplay
from app.displays.settings import SettingsDisplay
from app.ui import button
from app.ui import menu
from app.managers import KeyboardAction


class PauseDisplay(BaseDisplay):
    def __init__(self, game, previous_display):
        super().__init__(game)
        self.previous_display = previous_display
        rl.enable_cursor()

        self.buttons = self._create_buttons()
        self.menu = menu.MenuController(self.game, self.buttons)

    def _create_buttons(self):
        bw, bh = 220, 60
        gap = 20
        total_h = bh * 3 + gap * 2
        start_y = (self.game.height - total_h) // 2
        cx = (self.game.width - bw) // 2
        back_btn = button.Button(
            self.game,
            cx,
            start_y,
            bw,
            bh,
            "Back",
            24,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )
        settings_btn = button.Button(
            self.game,
            cx,
            start_y + bh + gap,
            bw,
            bh,
            "Settings",
            24,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )
        menu_btn = button.Button(
            self.game,
            cx,
            start_y + (bh + gap) * 2,
            bw,
            bh,
            "Main Menu",
            24,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )
        return [back_btn, settings_btn, menu_btn]

    def _resume_previous(self):
        if hasattr(self.previous_display, "hidden_cursor"):
            self.previous_display.hidden_cursor = False
        self.game.change_display(self.previous_display)

    def render(self):
        super().render()
        title = "Paused"
        title_size = 36
        title_w = rl.measure_text(title, title_size)
        rl.draw_text(title, (self.game.width - title_w) // 2, self.game.height // 2 - 100, title_size, rl.WHITE)
        for b in self.buttons:
            b.draw()

    def update(self):
        if self.game.keyboard.is_pressed(KeyboardAction.PAUSE):
            self._resume_previous()
            return

        self.menu.update()

        back_btn, settings_btn, menu_btn = self.buttons
        if back_btn.is_clicked:
            self._resume_previous()
        if settings_btn.is_clicked:
            self.game.change_display(SettingsDisplay(self.game, self))
        if menu_btn.is_clicked:
            self.game.change_display(self.game.base_display)
