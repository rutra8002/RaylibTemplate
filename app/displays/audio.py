import pyray as rl
from app.displays.base import BaseDisplay
from app.ui import button, menu, slider


class AudioDisplay(BaseDisplay):
    def __init__(self, game, previous_display):
        super().__init__(game)
        self.previous_display = previous_display
        rl.enable_cursor()

        slider_width = 360
        slider_height = 16
        slider_x = (self.game.width - slider_width) // 2
        base_y = self.game.height // 2 - 40
        gap = 60
        self.master_slider = slider.Slider(
            self.game,
            slider_x,
            base_y,
            slider_width,
            slider_height,
            min_value=0.0,
            max_value=1.0,
            value=self.game.audio.master_volume,
            step=0.05,
        )
        self.music_slider = slider.Slider(
            self.game,
            slider_x,
            base_y + gap,
            slider_width,
            slider_height,
            min_value=0.0,
            max_value=1.0,
            value=self.game.audio.music_volume,
            step=0.05,
        )
        self.sfx_slider = slider.Slider(
            self.game,
            slider_x,
            base_y + gap * 2,
            slider_width,
            slider_height,
            min_value=0.0,
            max_value=1.0,
            value=self.game.audio.sfx_volume,
            step=0.05,
        )

        bw, bh = 200, 50
        back_x = (self.game.width - bw) // 2
        back_y = self.game.height - 90
        self.back_button = button.Button(
            self.game,
            back_x,
            back_y,
            bw,
            bh,
            "Back",
            22,
            rl.WHITE,
            rl.DARKGRAY,
            rl.GRAY,
            rl.GREEN,
        )

        self.focus_items = [self.master_slider, self.music_slider, self.sfx_slider, self.back_button]
        self.menu = menu.MenuController(self.game, self.focus_items)

    def render(self):
        super().render()
        title = "Audio"
        title_size = 36
        title_w = rl.measure_text(title, title_size)
        rl.draw_text(title, (self.game.width - title_w) // 2, 60, title_size, rl.WHITE)

        label_size = 20
        labels = [
            ("Master Volume", self.master_slider.value, self.master_slider.rect.y - 26),
            ("Music Volume", self.music_slider.value, self.music_slider.rect.y - 26),
            ("SFX Volume", self.sfx_slider.value, self.sfx_slider.rect.y - 26),
        ]
        for text, value, y in labels:
            label = f"{text}: {int(value * 100)}%"
            label_w = rl.measure_text(label, label_size)
            rl.draw_text(label, (self.game.width - label_w) // 2, int(y), label_size, rl.WHITE)

        self.master_slider.draw()
        self.music_slider.draw()
        self.sfx_slider.draw()
        self.back_button.draw()

    def update(self):
        self.menu.update()
        self.game.audio.set_master_volume(self.master_slider.value)
        self.game.audio.set_music_volume(self.music_slider.value)
        self.game.audio.set_sfx_volume(self.sfx_slider.value)

        if self.back_button.is_clicked:
            self.game.change_display(self.previous_display)
