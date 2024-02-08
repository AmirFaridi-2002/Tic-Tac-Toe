import socket, json, os

from colorit import *
init_colorit()

def clr():
    """ Clears the screen """
    os.system("cls" if os.name == "nt" else "clear")

HOST = "127.0.0.1"
PORT = 5555

class Client:
    def __init__(self, host = HOST, port = PORT) -> None:
        """ Initializes the client """
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """ Connects to the server """
        self.client_socket.connect((self.host, self.port))
        print(color(f"Connected to {self.host}:{self.port}", Colors.green))
        self.handle()

    def handle(self):
        """ Handles the client """
        while True:
            msg = json.loads(self.client_socket.recv(1024).decode())

            if "ERROR" in msg.keys():
                print(color(msg["ERROR"], Colors.red))
                break

            elif "inp_size" in msg.keys(): 
                print(color(msg["inp_size"], Colors.blue), end = "")
                self.client_socket.send(str.encode(input()))
            
            elif "err_inp_size" in msg.keys():
                print(color(msg["err_inp_size"], Colors.red), end = "")
                self.client_socket.send(str.encode(input()))

            elif "smpl_msg" in msg.keys(): print(color(msg["smpl_msg"], Colors.purple))

            elif "game_msg" in msg.keys() and msg["game_msg"] == True:
                clr()
                print(color(msg["board"], Colors.orange))

                if msg["game_over"]:
                    if msg["winner"]: print(color(f"Player {msg['winner']} won!", Colors.yellow))
                    else: print(color("It's a tie!", Colors.yellow))
                    break

                if "inp" in msg.keys() and msg["inp"] == True:
                    print(color(msg["msg"], Colors.blue), end = "")
                    move = input()
                    self.client_socket.send(str.encode(move))

                elif "invalid" in msg.keys() and msg["invalid"] == True:
                    print(color(msg["err"], Colors.red), end = "")
                    move = input()
                    self.client_socket.send(str.encode(move))
            else: print(color("Unknown message!", Colors.red)); print(color(msg, Colors.red))

        print(color("Disconnected.", Colors.red))
        self.client_socket.close()


if __name__ == "__main__":
    client = Client(HOST, PORT)
    client.connect()