import pyray as rl
from app.displays.base import BaseDisplay
from app.displays.keybinds import KeybindsDisplay
from app.ui import button
from app.ui import menu


class SettingsDisplay(BaseDisplay):
    def __init__(self, game, previous_display):
        super().__init__(game)
        self.previous_display = previous_display
        rl.enable_cursor()

        self.buttons = self._create_buttons()
        self.menu = menu.MenuController(self.game, self.buttons)

    def _create_buttons(self):
        bw, bh = 260, 60
        cx = (self.game.width - bw) // 2
        cy = (self.game.height - bh) // 2
        gap = 20
        keybinds_btn = button.Button(
            self.game,
            cx,
            cy,
            bw,
            bh,
            "Keybinds",
            24,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )
        back_btn = button.Button(
            self.game,
            cx,
            cy + bh + gap,
            bw,
            bh,
            "Back",
            24,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )
        return [keybinds_btn, back_btn]

    def render(self):
        super().render()
        title = "Settings"
        title_size = 36
        title_w = rl.measure_text(title, title_size)
        rl.draw_text(title, (self.game.width - title_w) // 2, self.game.height // 2 - 100, title_size, rl.WHITE)
        for b in self.buttons:
            b.draw()

    def update(self):
        self.menu.update()

        keybinds_btn, back_btn = self.buttons
        if keybinds_btn.is_clicked:
            self.game.change_display(KeybindsDisplay(self.game, self))
        if back_btn.is_clicked:
            self.game.change_display(self.previous_display)
