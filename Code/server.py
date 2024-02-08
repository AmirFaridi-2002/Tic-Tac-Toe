import socket, threading, json
from board import Board

from colorit import *
init_colorit()

HOST = "127.0.0.1"
PORT = 5555

import re
def validate_input(inp : str) -> bool:
    """ Validates the input """
    return bool(re.match(r"\d \d", inp))

def outp(text : str, c : str) -> None:
    """ Outputs a colored text """
    try: print(color(text, getattr(Colors, c)))
    except: print(f'Invalid color: {c}\n Valid colors: {", ".join([i for i in dir(Colors) if not i.startswith("__")])}')

class Server:
    def __init__(self, host = HOST, port = PORT) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting_list = {3 : [], 4 : [], 5 : []}
        self.waiting_list_lock = threading.Lock()

    def listen(self) -> None:
        """ Listens for connections """
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen()
            outp(f"Listening on {self.host}:{self.port}...", "green")
            while True:
                conn, addr = self.sock.accept()
                outp(f"Connected by {addr}", "green")
                threading.Thread(target = self.handle_client, args = (conn, addr)).start()
        except Exception as e:
            outp(f"Error: {e}", "red")
            self.sock.close()

    def handle_client(self, conn : socket.socket, addr : tuple) -> None:
        """ Handles a client """
        try:    

            conn.send(str.encode(json.dumps({"inp_size" : "Welcome to Tic Tac Toe. Enter the size of the board (3, 4, 5): "})))
            while 1:
                size = conn.recv(1024).decode()
                if size in ["3", "4", "5"]: size = int(size); break
                conn.send(str.encode(json.dumps({"err_inp_size" : "Invalid size! Try again: "})))

            print(color(f"Player {addr} wants to play on a {size}x{size} board.", Colors.blue))

            self.waiting_list_lock.acquire()
            self.waiting_list[size].append(conn)
            if len(self.waiting_list[size]) >= 2:
                self.play(size)
            else: self.waiting_list_lock.release()
        except Exception as e:
            with self.waiting_list_lock:
                del self.waiting_list[size][self.waiting_list[size].index(conn)]
            outp(f"Error: {e}", "red")
            conn.close()


    def play(self, size : int) -> None:
        """ Starts a game """
        p1, p2 = self.waiting_list[size][:2]
        del self.waiting_list[size][:2]
        self.waiting_list_lock.release()

        outp(f"Starting a game on a {size}x{size} board with players {p1} and {p2}.", "blue")

        board = Board(size)

        try:
            p1.send(str.encode(json.dumps({"smpl_msg" : "You are X."})))
            p2.send(str.encode(json.dumps({"smpl_msg" : "You are O."})))
        except Exception as e:
            outp(f"{e}\t\tClosing connection...", "red")
            p1.close(); p2.close()
            return

        msg = {"game_msg" : True, "board" : board._get_state(), "turn" : board.turn, "winner" : board.get_winner(), "tie" : board.check_tie(), 
                    "game_over" : board.check_game_over(), "inp" : False, "msg" : "enter coordinates: ", 
                        "invalid" : False, "err" : "invalid move! try again: ", "state" : board.get_state()}
        
        while p1.fileno() != -1 and p2.fileno() != -1:
            try:
                msg["state"] = board.get_state()
                player = p1 if board.turn == 'X' else p2
                opponent = p2 if board.turn == 'X' else p1

                opponent.send(str.encode(json.dumps(msg)))

                msg["inp"] = True
                player.send(str.encode(json.dumps(msg)))

                while 1:
                    move = player.recv(1024).decode()
                    if validate_input(move):
                        x_coor, y_coor = map(int, move.split())
                        if board.action(x_coor, y_coor): break
                    msg["invalid"] = True
                    player.send(str.encode(json.dumps(msg)))

                msg["invalid"] = False
                msg["inp"] = False

                if board.check_game_over():
                    msg["board"] = board._get_state()
                    msg["winner"] = board.get_winner()
                    msg["tie"] = board.check_tie()
                    msg["game_over"] = board.check_game_over()
                    player.send(str.encode(json.dumps(msg)))
                    opponent.send(str.encode(json.dumps(msg)))
                    break

                msg["board"] = board._get_state()
                msg["turn"] = board.turn
                msg["winner"] = board.get_winner()
                msg["tie"] = board.check_tie()
                msg["game_over"] = board.check_game_over()
            except Exception as e:
                outp(f"{e}\t\tClosing connection...", "red")
                p1.close(); p2.close()
                return
        
        if not msg["game_over"]:
            outp("The opponent has quit the game.", "orange")
            return
        p1.close(); p2.close()
        outp(f"Game over.", "orange")
        return



if __name__ == "__main__":
    Server().listen()