import pyray as rl
from app.displays.base import BaseDisplay
from app.ui import button, menu


class KeybindsDisplay(BaseDisplay):
    def __init__(self, game, previous_display):
        super().__init__(game)
        self.previous_display = previous_display
        rl.enable_cursor()

        self.pending_action = None
        self.action_buttons = self._create_action_buttons()
        self.back_button = self._create_back_button()
        self.focus_buttons = [btn for _, btn in self.action_buttons] + [self.back_button]
        self.menu = menu.MenuController(self.game, self.focus_buttons)

    def _create_action_buttons(self):
        bw, bh = 360, 50
        cx = (self.game.width - bw) // 2
        top = 140
        gap = 14
        buttons = []
        for i, action in enumerate(self.game.keyboard.action_order):
            y = top + i * (bh + gap)
            btn = button.Button(
                self.game,
                cx,
                y,
                bw,
                bh,
                "",
                20,
                rl.WHITE,
                rl.DARKGRAY,
                rl.GRAY,
                rl.GREEN,
            )
            buttons.append((action, btn))
        return buttons

    def _create_back_button(self):
        bw, bh = 200, 50
        cx = (self.game.width - bw) // 2
        y = self.game.height - 90
        return button.Button(
            self.game,
            cx,
            y,
            bw,
            bh,
            "Back",
            22,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )

    def _update_button_labels(self):
        for action, btn in self.action_buttons:
            label = f"{action.name}: {self.game.keyboard.format_binding(action)}"
            btn.text = label

    def render(self):
        super().render()
        title = "Keybinds"
        title_size = 36
        title_w = rl.measure_text(title, title_size)
        rl.draw_text(title, (self.game.width - title_w) // 2, 60, title_size, rl.WHITE)

        if self.pending_action is not None:
            msg = f"Press a key for {self.pending_action.name}"
            msg_size = 20
            msg_w = rl.measure_text(msg, msg_size)
            rl.draw_text(msg, (self.game.width - msg_w) // 2, 110, msg_size, rl.YELLOW)

        self._update_button_labels()
        for _, btn in self.action_buttons:
            btn.draw()
        self.back_button.draw()

    def update(self):
        if self.pending_action is not None:
            if self.game.keyboard.last_pressed:
                key = self.game.keyboard.last_pressed[-1]
                self.game.keyboard.bind(self.pending_action, key)
                self.pending_action = None
            return

        self.menu.update()

        for action, btn in self.action_buttons:
            if btn.is_clicked:
                self.pending_action = action

        if self.back_button.is_clicked:
            self.game.change_display(self.previous_display)
