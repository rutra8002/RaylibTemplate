import pyray as rl
from app.displays.base import BaseDisplay
from app.displays.keybinds import KeybindsDisplay
from app.displays.audio import AudioDisplay
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
        gap = 20
        labels = ["Keybinds", "Audio", "Back"]
        total_h = len(labels) * bh + (len(labels) - 1) * gap
        top = (self.game.height - total_h) // 2
        buttons = []
        for i, label in enumerate(labels):
            y = top + i * (bh + gap)
            btn = button.Button(
                self.game,
                cx,
                y,
                bw,
                bh,
                label,
                24,
                rl.WHITE,
                rl.DARKGRAY,
                rl.GRAY,
                rl.GREEN,
            )
            buttons.append(btn)
        return buttons

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

        keybinds_btn, audio_btn, back_btn = self.buttons
        if keybinds_btn.is_clicked:
            self.game.change_display(KeybindsDisplay(self.game, self))
        if audio_btn.is_clicked:
            self.game.change_display(AudioDisplay(self.game, self))
        if back_btn.is_clicked:
            self.game.change_display(self.previous_display)
