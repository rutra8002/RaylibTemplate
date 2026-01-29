import pyray as rl
from app.displays.base import BaseDisplay
from app.ui import button


class PauseDisplay(BaseDisplay):
    def __init__(self, game, previous_display):
        super().__init__(game)
        self.previous_display = previous_display
        rl.enable_cursor()

        self.buttons = self._create_buttons()
        self.focus_index = 0

    def _create_buttons(self):
        bw, bh = 220, 60
        cx = (self.game.width - bw) // 2
        cy = (self.game.height - bh) // 2
        gap = 20
        back_btn = button.Button(
            self.game,
            cx,
            cy,
            bw,
            bh,
            "Back",
            24,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )
        menu_btn = button.Button(
            self.game,
            cx,
            cy + bh + gap,
            bw,
            bh,
            "Main Menu",
            24,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )
        return [back_btn, menu_btn]

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
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
            self._resume_previous()
            return

        if self.game.gamepad_enabled:
            y = getattr(self.game, "left_joystick_y", 0.0)
            if y < -self.game.gamepad_deadzone:
                self.focus_index = max(0, self.focus_index - 1)
            elif y > self.game.gamepad_deadzone:
                self.focus_index = min(len(self.buttons) - 1, self.focus_index + 1)
        else:
            self.focus_index = -1

        for i, b in enumerate(self.buttons):
            b.update(focused=(i == self.focus_index))

        back_btn, menu_btn = self.buttons
        if back_btn.is_clicked:
            self._resume_previous()
        if menu_btn.is_clicked:
            self.game.change_display(self.game.base_display)
