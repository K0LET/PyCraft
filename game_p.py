import socket


class GameProtocol:
    def __init__(self, sock=socket.socket()):
        self.socket = sock

    def attempt_to_connect(self, addr: (str, int)) -> bool:
        try:
            self.connect(addr)
            return True
        except (socket.gaierror, ConnectionRefusedError):
            return False

    def connect(self, addr: (str, int)):
        return self.socket.connect(addr)

    def bind(self, addr: (str, int)):
        return self.socket.bind(addr)

    def listen(self):
        return self.socket.listen()

    def close(self):
        self.socket.close()

    def accept(self):
        sock, addr = self.socket.accept()
        sock = GameProtocol(sock)
        return sock, addr

    def getsockname(self):
        return self.socket.getsockname()

    def send_data(self, data: bytes) -> bool:
        try:
            self.socket.sendall(f"{len(data)}".ljust(30).encode())
            self.socket.sendall(data)
        except (ConnectionError, OSError):
            return False
        return True

    def recvall(self, buffsize: int) -> bytes:
        data = b""
        while len(data) < buffsize:
            res = self.socket.recv(buffsize - len(data))
            data += res
            if res == b"":  # connection closed
                return res
        return data

    def recv_data(self):
        data_length = self.recvall(30).decode()
        if data_length != '':
            return self.recvall(buffsize=int(data_length.strip()))

