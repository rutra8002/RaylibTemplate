from app import game


# text = "Hello, Raylib!"
# font_size = 20
#
# while not rl.window_should_close():
#     text_width = rl.measure_text(text, font_size)
#     x = (screen_w - text_width) // 2
#     y = (screen_h - font_size) // 2
#
#     rl.begin_drawing()
#     rl.clear_background(rl.RAYWHITE)
#     rl.draw_text(text, x, y, font_size, rl.DARKGRAY)
#     rl.end_drawing()
#
# rl.close_window()

if __name__ == '__main__':
    gmae = game.Game()
    gmae.loop()