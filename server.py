import threading
import pickle
import traceback

from game_p import GameProtocol


class GameServer:
    def __init__(self):
        self.SERVER_HOST = '0.0.0.0'
        self.SERVER_PORT = 8080
        self.SERVER_ADDR = (self.SERVER_HOST, self.SERVER_PORT)

        self.server_socket = GameProtocol()
        self.server_socket.bind(self.SERVER_ADDR)
        self.server_socket.listen()
        print("server is up and running")

        self.clients = []
        self.positions = {}

    def handle_client(self, client_socket: GameProtocol, client_address):
        print(f'New client connected: {client_address}')

        while True:
            try:
                if len(self.clients) > 1:
                    data = client_socket.recv_data()
                    if data is not None:
                        pickle_data = pickle.loads(data)
                        self.positions[client_address] = pickle_data[0]
                        # sends players position and blocks position
                        for c in self.clients:
                            if c != client_socket:
                                client_socket.send_data(data=pickle.dumps((self.positions, None)))
                        #

            except Exception as e:
                print(f'Client {client_address} disconnected')
                self.clients.remove(client_socket)
                for c in self.clients:
                    if c != client_socket:
                        c.send_data(pickle.dumps(({client_address: "disconnected"}, None)))
                client_socket.close()
                break

    def run_server(self):
        for i in range(9):
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f'Accepted new connection from {client_address}')
            threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()


def main():
    srvr = GameServer()
    srvr.run_server()


if __name__ == '__main__':
    main()