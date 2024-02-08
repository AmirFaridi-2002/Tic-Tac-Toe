class Board:
    def __init__(self, size : int) -> None:
        self.size = size
        self.grid = [['-' for _ in range(size)] for _ in range(size)]
        self.turn = 'X'
    
    def _Rules(self) -> dict:
        """ Rules for different sizes """
        return {3: 3, 4: 4, 5: 4}

    def __str__(self) -> str:
        """ A string representation of the board """
        display = str()
        for row in self.grid: display += " | ".join(row) + "\n" + "-"*(4 * len(row) - 1) + "\n"
        return display
    
    def __repr__(self) -> str:
        """ A string representation of the board """
        return self.__str__()
    
    def __getitem__(self, index : int) -> list:
        """ Returns the row at index """
        return self.grid[index]
    
    def __setitem__(self, index : int, value : list) -> None:
        """ Sets the row at index to value """
        self.grid[index] = value

    def __len__(self) -> int:
        """ Returns the size of the board """
        return self.size
    
    def __contains__(self, item : str) -> bool:
        """ Returns True if item is in the board, False otherwise """
        if any(item in row for row in self.grid): return True
    
    def is_full(self) -> bool:
        """ Returns True if the board is full, False otherwise """
        return True if '-' not in self else False
    
    def is_valid(self, x_coor : int, y_coor : int) -> bool:
        """ Returns True if the position is valid, False otherwise """
        return (0 <= x_coor and x_coor < self.size
                and 0 <= y_coor and y_coor < self.size and self[x_coor][y_coor] == '-')
    
    def _get_state(self) -> str:
        """ Returns the state of the board """
        return self.__str__() + "\n"
    
    def get_state(self) -> list:
        """ Returns the state of the board """
        return self.grid
    
    def reset_board(self, size : int) -> None:
        """ Resets the board to a new size """
        self.__init__(size)

    def action(self, x_coor : int, y_coor : int) -> bool:
        """ Performs an action on the board """
        if self.is_valid(x_coor, y_coor):
            self[x_coor][y_coor] = self.turn
            self.turn = 'X' if self.turn == 'O' else 'O'
            return True
        return False
    
    def check_winner(self, symbol : str) -> bool:
        """ Returns True if player has won according to the rules, False otherwise """
        rules = self._Rules()
        for row in self.grid:
            for i in range(len(row) - rules[self.size] + 1):
                if all(row[i + j] == symbol for j in range(rules[self.size])): return True

        for col in range(len(self)):
            for i in range(len(self) - rules[self.size] + 1):
                if all(self[i + j][col] == symbol for j in range(rules[self.size])): return True

        for i in range(len(self) - rules[self.size] + 1):
            for j in range(len(self) - rules[self.size] + 1):
                if all(self[i + k][j + k] == symbol for k in range(rules[self.size])): return True

        for i in range(len(self) - rules[self.size] + 1):
            for j in range(rules[self.size] - 1, len(self)):
                if all(self[i + k][j - k] == symbol for k in range(rules[self.size])): return True
        return False    
    
    def check_tie(self) -> bool:
        """ Returns True if the game is a tie, False otherwise """
        return True if self.is_full() and not self.check_winner('X') and not self.check_winner('O') else False

    def check_game_over(self) -> bool:
        """ Returns True if the game is over, False otherwise """
        return True if self.check_winner('X') or self.check_winner('O') or self.check_tie() else False
    
    def get_winner(self) -> str:
        """ Returns the winner of the game """
        if self.check_winner('X'): return 'X'
        elif self.check_winner('O'): return 'O'
        return None

  

if __name__ == "__main__":
    print("This is a module. Import it instead.")
    exit()