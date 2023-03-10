# gotta catch them all! gotta catch them all!
# By: Brian Truong

from window import Window

initalization = Window()
while initalization.startup:
    initalization.current_menu.display_menu()
    initalization.game_loop()

