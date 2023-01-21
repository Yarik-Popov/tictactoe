import tkinter as tk
import typing
from tkinter import ttk
from tkinter.messagebox import showinfo


class Slot:
    def __init__(self, master, row: int, col: int, change_player: typing.Callable, check_win: typing.Callable):
        """
        Initializes the Slot object at the row and col specified
        :param master: Root tk object
        :param row: The row index
        :param col: The column index
        :param change_player: The function to be performed when the user clicks on the button aside from removing the
        button and displaying the label
        """
        #  Values
        self.row = row
        self.col = col
        self.change_player = change_player
        self.check_win = check_win
        self.player = None
        self.text_variable = tk.StringVar()

        # Widgets
        self.button = tk.Button(master, text='Click', command=self.command)
        self.label = tk.Label(master, textvariable=self.text_variable)
        self.init_ui()

    def init_ui(self):
        """Initialize ui"""
        self.button.grid(row=self.row, column=self.col)

    def command(self):
        """Command that is executed when clicked on the button"""
        self.button.grid_forget()
        self.label.grid(row=self.row, column=self.col)
        self.player = self.change_player()
        self.text_variable.set(f'{self.player}')
        self.check_win()

    def close(self):
        """Closes the slot, it is unplayable now"""
        self.button.grid_forget()
        if self.player is None:
            self.text_variable.set('#')
            self.label.grid(row=self.row, column=self.col)

    def __str__(self):
        return f'Slot at {self.row = }, {self.col} with {self.player = }'


class Window(ttk.Frame):
    def __init__(self, master, *, pad_x=10, pad_y=10):
        """
        Game Window
        :param master: Root tk object
        :param pad_x: Padding on the x or rows. Default is 0
        :param pad_y: Padding on the y or columns. Default is 0
        """
        # Initialize window
        super().__init__(master)
        self.master.title('Tic Tac Toe')
        ttk.Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')
        self.__configure_rows_columns(rows_num=5, columns_num=3, pad_x=pad_x, pad_y=pad_y)

        # Initialize widgets
        self.text_variable = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.text_variable)
        self.button_destroy = tk.Button(self, text='New Game', command=self.new_game)

        # Initialize necessary variables
        self.slots = []
        self.is_x = True
        self.players = ['O', 'X']
        self.root = master

        # Creates the buttons
        for i in range(3):
            slot_row = []
            for j in range(3):
                slot_row.append(Slot(self, i, j, self.change_player, self.check_win))
            self.slots.append(slot_row)

        self.init_ui()

    def init_ui(self):
        """This method initialization the ui"""
        self.label.grid(columnspan=3, row=3)
        self.button_destroy.grid(columnspan=3, row=4)
        self.text_variable.set(f'Current player: {self.give_player()}')
        self.pack()

    def __configure_rows_columns(self, rows_num=0, columns_num=0, pad_x=0, pad_y=0):
        """
        Creates rows_num number of rows with padding pad_x and columns_num number of columns with padding pad_y. Called
        on initialization of the object.
        :param rows_num: Number of rows
        :param columns_num: Number of columns
        :param pad_x: Padding in the x
        :param pad_y: Padding in the y
        """
        for i in range(rows_num):
            self.rowconfigure(i, pad=pad_x)

        for i in range(columns_num):
            self.columnconfigure(i, pad=pad_y)

    def change_player(self):
        """
        Changes the player, sets the current player to the screen and returns the past player
        :return: 'X' if not self.x else 'O'
        """
        self.is_x = not self.is_x
        self.text_variable.set(f'Current player: {self.give_player()}')
        return self.give_player(True)

    def give_player(self, opposite=False):
        """
        Gives the player based on if it opposite or not
        :param opposite: Switch player
        :return: 'X' if not self.x and opposite else 'O'
        """
        return self.players[int(not self.is_x if opposite else self.is_x)]

    def new_game(self):
        """Creates a new game"""
        Window(self.root)
        self.destroy()

    def check_win(self):
        """Checks if a given player has won or not"""
        current_player = self.give_player(True)

        # Horizontal
        for i in self.slots:
            count = 0
            for j in i:
                if j.player == current_player:
                    count += 1
                self.end_game(current_player, count)

        # Vertical
        for i in range(3):
            count = 0
            for j in range(3):
                if self.slots[j][i].player == current_player:
                    count += 1
                self.end_game(current_player, count)

        # Diagonal from top left
        count = 0
        for i in range(3):
            if self.slots[i][i].player == current_player:
                count += 1
            self.end_game(current_player, count)

        # Diagonal from top right
        count = 0
        for i in range(3):
            if self.slots[i][2-i].player == current_player:
                count += 1
            self.end_game(current_player, count)

    def end_game(self, current_player: str, count: int):
        """Ends the game based on current player and if the count is 3"""
        if count == 3:
            showinfo('Victory', f'{current_player} has won')
            for i in self.slots:
                for j in i:
                    j.close()


def main():
    """Initialize window and launch it"""
    root = tk.Tk()
    root.state('zoomed')
    Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
