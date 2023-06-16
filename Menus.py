import socket
from ursina import *
import World
import client


class StartMenu:
    def __init__(self):
        self.gui = World.gui
        self.client = client.Client()
        self.client.player.disable()
        self.menu = Menu()
        self.menu.enable()
        self.ip_bar = InputField(position=(-.55, .375))
        self.name_bar = InputField(position=(-.55, .275))
        self.name_text = Text(text="Enter Name:", color=color.black, position=(-.8, .325))
        self.display_players = Text(text="players:", color=color.black, position=(.4, .4))
        self.enter_ip = Text(text="please enter an ip", color=color.red, position=(-.3, .385))
        self.addr_text = Text(text="Enter Server IP:", color=color.black, position=(-.8, .425))
        self.ip_not_valid = Text(text="IP is not valid", color=color.red, position=(-.3, .385))
        self.name_not_valid = Text(text="name is taken", color=color.red, position=(-.3, .285))
        self.enter_name = Text(text="please enter a name", color=color.red, position=(-.3, .285))
        self.check_ip_text = Text(text="please check the ip", color=color.red, position=(-.3, .385))
        self.play = Button(model="quad", scale=(.11, .05), color=color.black, text="Play", position=(-.745, .2))
        self.Connect = Button(model="quad", scale=(.11, .05), color=color.black, text="Connect", position=(-.745, .2))
        self.background = Entity(model="quad", position=(0, 2.165, 7), scale=(14.6, 8.2), texture='start_menu_background.png')
        self.Connect.on_click = self.connect_on_click
        self.display_players.disable()
        self.name_not_valid.disable()
        self.check_ip_text.disable()
        self.ip_not_valid.disable()
        self.enter_name.disable()
        self.enter_ip.disable()
        self.play.disable()

    def connect_on_click(self):
        self.enter_ip.disable()
        self.enter_name.disable()
        self.name_not_valid.disable()
        self.ip_not_valid.disable()
        self.check_ip_text.disable()
        check_name = self.check_name(self.name_bar.text)
        check_ip = self.check_ip(self.ip_bar.text)
        if not check_ip[0]:
            if check_ip[1] == "empty":
                if not check_name[0]:
                    if check_name[1] == "empty":
                        self.enter_ip.enable()
                        self.enter_name.enable()
                    elif check_name[1] == "name is taken":
                        self.enter_ip.enable()
                        self.name_not_valid.enable()
                else:
                    self.enter_ip.enable()
            else:
                if not check_name[0]:
                    if check_name[1] == "empty":
                        self.ip_not_valid.enable()
                        self.enter_name.enable()
                    elif check_name[1] == "name is taken":
                        self.ip_not_valid.enable()
                        self.name_not_valid.enable()
                else:
                    self.ip_not_valid.enable()
        elif not check_name[0]:
            if not check_name[0]:
                if check_name[1] == "empty":
                    self.enter_name.enable()
                if check_name[1] == "name is taken":
                    self.name_not_valid.enable()

        else:
            connected = self.client.connect_to_server(self.ip_bar.text)
            if connected:
                self.ip_not_valid.disable()
                self.enter_ip.disable()
                self.enter_name.disable()
                self.name_not_valid.disable()
                self.display_players.enable()
                self.client.players_name.append(self.name_bar.text)
                self.Connect.disable()
                self.play.enable()
            else:
                self.check_ip_text.enable()

    def check_name(self, name) -> (bool, str):
        if name in self.client.players_name:
            return False, "name is taken"
        elif name == "":
            return False, "empty"
        else:
            return True, "valid"

    @staticmethod
    def check_ip(ip_str: str) -> (bool, str):
        if ip_str != "":
            valid = True, "valid"
            try:
                socket.inet_aton(ip_str)
            except socket.error:
                valid = False, "not valid"
            return valid
        else:
            return False, "empty"

    @staticmethod
    def display_players(players: ["str"]):
        Text(text="players connected:", color=color.black, position=(.4, .4))
        j = 0.05
        for i in players:
            Text(text=i, color=color.black, position=(.45, .4 - j))
            j += 0.05

    def print_data(self):
        print(self.ip_bar.text, self.name_bar.text)

    def disable(self):
        self.menu.disable()
        self.ip_bar.disable()
        self.Connect.disable()
        self.name_bar.disable()
        self.addr_text.disable()
        self.name_text.disable()
        self.background.disable()

    def enable(self):
        self.menu.enable()
        self.ip_bar.enable()
        self.Connect.enable()
        self.name_bar.enable()
        self.addr_text.enable()
        self.name_text.enable()
        self.background.enable()


class Menu:
    def __init__(self):
        self.gui = World.gui
        self.gui.borderless = True
        self.sc = Button(icon='assets/full-screen.png', scale=(.0452, .0235), position=(.815, .4875))
        self.eb = Button(icon='assets/exit_button.png', scale=(.0455, .0235), position=(.865, .4875))
        window.exit_button.visible = False
        self.sc.on_click = self.screen
        self.eb.on_click = self.exit
        self.active = False
        self.disable()

    def disable(self):
        self.gui.borderless = False
        self.sc.disable()
        self.eb.disable()
        window.fps_counter.visible = False

    def enable(self):
        self.gui.borderless = True
        self.sc.enable()
        self.eb.enable()
        window.fps_counter.visible = True

    @staticmethod
    def exit():
        quit()

    @staticmethod
    def screen():
        if window.fullscreen:
            window.fullscreen = False
        else:
            window.fullscreen = True

    def set_menu(self):
        if not self.active:
            self.active = True
            self.enable()
            return False
        elif self.active:
            self.disable()
            self.active = False
            return True


def main():
    app = StartMenu()
    app.background.position = (0, 0, 0)
    app.gui.run()
    app.enable()


if __name__ == '__main__':
    main()
