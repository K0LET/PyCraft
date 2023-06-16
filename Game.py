#
#  THIS IS THE FILE THAT NEEDS TO RUN WITH THE SERVER!
#  THE SERVER RUNS FIRST!
#  crated by: Yoav Kolet
#

from ursina import *
import World
import Menus


class McGame:
    def __init__(self):
        self.menu = Menus.Menu()
        self.start_menu = Menus.StartMenu()
        self.client = self.start_menu.client
        self.game_world = self.client.world
        self.game_world.disable()
        self.player = self.game_world.player
        self.app = World.gui
        self.play = False

    def game_update(self):
        if held_keys['left mouse'] or held_keys['right mouse']:
            self.player.hand.active()
        else:
            self.player.hand.passive()

        if self.player.fpc.y < -50 or self.player.fpc.y > 50:
            self.game_reset()

    def game_reset(self):
        self.player.fpc.position = (0, 0, 0)

    def game_input(self, key):
        add_remove, block = self.game_world.block.input(key)
        if add_remove == "added":
            self.client.client_update(block)
        elif add_remove == "destroyed":
            self.client.client_update(block)
        if key == "escape":
            disable_client = self.menu.set_menu()
            if disable_client:
                self.player.enable()
            else:
                self.player.disable()

    def run_start(self):
        self.start_menu.enable()
        self.player.disable()
        self.game_world.disable()
        self.app.run()

    def run_game(self):
        self.play = True
        self.start_menu.disable()
        self.player.enable()
        self.client.start_client()
        self.game_world.enable()
        self.game_world.build_world()
        self.start_menu.play.disable()
        self.start_menu.display_players.disable()


def update():
    if game.play:
        game.client.client_update()
        game.game_update()


def input(key):
    if game.play:
        game.game_input(key)


def main():
    global game
    game = McGame()
    game.start_menu.play.on_click = game.run_game
    game.run_start()


if __name__ == "__main__":
    main()
