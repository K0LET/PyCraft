from ursina import *
import threading
import pickle
import World
from game_p import GameProtocol


class Client:
    def __init__(self):
        self.players_name = []
        self.other_clients = {}  # client addr, position
        self.IP = "127.0.0.1"
        print(self.IP)
        self.SERVER_PORT = 8080
        self.SERVER_ADDR = (self.IP, self.SERVER_PORT)
        self.client_socket = GameProtocol()
        self.world = World.world()
        self.world.disable()
        self.p = self.world.p
        self.player = self.world.player

    def connect_to_server(self, addr="127.0.0.1") -> bool:
        return self.client_socket.attempt_to_connect((addr, self.SERVER_PORT))

    def send_name(self, name):
        self.client_socket.send_data(b"name: " + bytes(name))

    def receive_data(self):
        while True:
            try:
                received_data = self.client_socket.recv_data()
                r_data = pickle.loads(received_data)
                #
                if r_data is not None or r_data != "":
                    for addr, data in r_data[0].items():
                        if "disconnected" in data:  # disconnecting
                            self.other_clients[addr].disable()
                            print(f"{addr} disconnected")
                        if "Vec3" in str(data):  # update locations
                            data[1] += 1.25
                            if addr != self.client_socket.getsockname():
                                if addr not in self.other_clients:  # create new player as an Entity
                                    self.other_clients[addr] = self.p.Client(position=data, color=color.random_color())
                                else:
                                    self.other_clients[addr].position = data
                    #

            except Exception as e:  # closing connection
                print(e)
                self.client_socket.close()
                print('Connection closed')
                break

    def start_client(self):
        threading.Thread(target=self.receive_data).start()

    def client_update(self, block=None):
        player_position = self.player.fpc.position
        data = pickle.dumps((player_position, block))
        self.client_socket.send_data(data)
        # |need to send|:1. player position V 2.block position and type 3. player name


def main():
    global clnt
    clnt = Client()
    clnt.start_client()


if __name__ == '__main__':
    main()