"""This module contains the implementation of a Tic Tac Toe game where Player 2 interacts through a GUI interface.

It utilizes the tkinter library for graphical user interface components and communication is established
using sockets. The Player2 class represents the actions and behavior of Player 2 in the game.

Dependencies:
    - tkinter: The standard GUI library in Python.
    - socket: Provides the networking functionality for communication.
    - threading: Allows for concurrent execution of functions.
    - gameboard: A module providing the BoardClass for maintaining game state.

Usage:
    To play the game, create an instance of the Player2 class, passing the tkinter root window and an instance
    of BoardClass as arguments. Then, call the `startServer()` method to initiate the game setup and GUI.
"""
import tkinter as tk
import socket
import threading
from gameboard import BoardClass  # Import your gameboard module

class Player2():

    """Represents Player 2 in a Tic Tac Toe game.

    Attributes:
        root (Tk): The main tkinter root window.
        game_board (BoardClass): The game board instance.
        server_socket (socket.socket): The server socket for communication.
        client_socket (socket.socket): The client socket for communication.
        guiboard (list): The 2D list of GUI buttons representing the game board.
        is_waiting (bool): Flag to indicate if the player is waiting.

    Methods:
        startServer(): Starts the server to wait for Player 1.
        initializeServer(): Initializes the server socket and starts waiting for Player 1.
        create_server_socket(host, port): Creates a server socket for communication.
        waitForPlayer1(): Waits for Player 1 to connect.
        enterUsername(): Allows Player 2 to enter their username.
        sendUsername(): Sends Player 2's username to Player 1 and prepares for the game.
        setGUI(): Sets up the game GUI.
        createGameBoard(): Creates the GUI representation of the game board.
        receiveMove(): Receives and processes the opponent's move.
        clickButton(row, col): Handles the player's move when clicking a button.
        disableButton(): Disables all buttons on the GUI.
        enableButton(): Enables all buttons on the GUI.
        endGame(): Displays final statistics and ends the game.
    """

    def __init__(self, root: tk.Tk, game_board: BoardClass):
        """Initializes the Player2 instance.

        Args:
            root (Tk): The main tkinter root window.
            game_board (BoardClass): The game board instance.
        """
        self.root = root
        self.game_board = game_board
        self.server_socket = None
        self.client_socket = None
        self.guiboard = None
        self.is_waiting = False


    def startServer(self):
        """Starts the server to wait for Player 1."""
        self.root.title("Welcome Player 2!")
        self.root.geometry('400x400')
        host_label = tk.Label(self.root, text="| Create a Server to Start the Game |\n\nEnter your host/IP Address:")
        host_label.pack()
        self.host_entry = tk.Entry(self.root)
        self.host_entry.pack()
        port_label = tk.Label(self.root, text="Enter your port number:")
        port_label.pack()
        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()
        self.start_server_button = tk.Button(self.root, text="Start Server", command=self.initializeServer)
        self.start_server_button.pack()


    def initializeServer(self):
        """Initializes the server socket and starts waiting for Player 1."""
        self.start_server_button.config(state="disabled")
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        self.server_socket = self.create_server_socket(host, port)
        threading.Thread(target=self.waitForPlayer1).start()


    def create_server_socket(self, host: str, port: int) -> socket.socket:
        """Creates a server socket for communication.

        Args:
            host (str): The host/IP address to bind the socket to.
            port (int): The port number to bind the socket to.

        Returns:
            socket.socket: The created server socket.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        return server_socket


    def waitForPlayer1(self):
        """Waits for Player 1 to connect."""
        self.root.title("Waiting for Connection...")
        self.client_socket, _ = self.server_socket.accept()
        self.enterUsername()


    def enterUsername(self):
        """Allows Player 2 to enter their username."""
        self.root.title("Connected to Opponent!")
        for widget in self.root.winfo_children():
            widget.destroy()  
        username_label = tk.Label(self.root, text="Enter your user name as (Player 2):")
        username_label.pack()
        self.userentry = tk.Entry(self.root)
        self.userentry.pack()
        self.submit_user_button = tk.Button(self.root, text="Submit", command=self.sendUsername)
        self.submit_user_button.pack()


    def sendUsername(self):
        """Sends Player 2's username to Player 1 and prepares for the game."""
        self.submit_user_button.config(state="disabled")
        p2user = self.userentry.get()
        self.client_socket.send(p2user.encode())
        self.root.title("Waiting on Opponent's User...")
        p1user = self.client_socket.recv(1024).decode()
        self.game_board.setPlayer1Name(p1user)
        self.game_board.setPlayer2Name(p2user)
        self.game_board.addWinLoss(p1user)
        self.game_board.addWinLoss(p2user)
        self.game_board.setPlayerProfile2()
        self.userentry.destroy()
        self.root.title("Player 2 - Tic Tac Toe")
        self.root.after(0, self.setGUI)


    def setGUI(self):
        """Sets up the game GUI."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.update()
        self.heading = tk.Label(self.root, text="Tic Tac Toe")
        self.heading.grid(row=0, column=1)
        self.subheading = tk.Label(self.root, text="Game Start!")
        self.subheading.grid(row=1, column=1)
        self.game_board.resetDefaultTurn()
        self.turn_label = tk.Label(self.root, text=f"Turn: {self.game_board.userturn}")
        self.turn_label.grid(row=2, column=1)
        self.createGameBoard()


    def createGameBoard(self):
        """Creates the GUI representation of the game board."""
        self.guiboard = []
        for row in range(3):
            row_buttons = []
            for col in range(3):
                button = tk.Button(self.root, text="", width=10, height=3, command=lambda row=row, col=col: self.clickButton(row, col))
                button.grid(row=row+4, column=col)
                row_buttons.append(button)
            self.guiboard.append(row_buttons)
        self.root.update()
        self.disableButton()
        self.receiveMove()


    def receiveMove(self):
        """Receives and processes the opponent's move."""
        waitlabel = tk.Label(self.root, text="Waiting...")
        waitlabel.grid(row=3, column=1)
        self.root.update()
        move_info = self.client_socket.recv(1024).decode()
        waitlabel.destroy()
        self.root.update()
        if move_info == "Fun Times":
            self.game_board.resetDefaultTurn()
            self.endGame()
        elif move_info == "Play Again":
            self.game_board.resetDefaultTurn()
            self.setGUI()
        else:
            try:
                row, col = map(int, move_info.split(','))
            except:
                self.endGame()
        self.game_board.updateGameBoard(row, col, self.guiboard)
        if self.game_board.isWinner():
            self.game_board.updateGamesPlayed()
            self.game_board.resetGameBoard()
            self.subheading.config(text=f"{self.game_board.userturn} is the Winner!")
            self.root.update()
            self.receiveMove()
        elif self.game_board.boardIsFull():
            self.game_board.updateGamesPlayed()
            self.game_board.resetGameBoard()
            self.subheading.config(text="It's a tie!")
            self.root.update()
            self.receiveMove()
        else:
            self.game_board.changePlayerTurn()
            self.turn_label.config(text=f"Turn: {self.game_board.userturn}")
            self.root.update()
            self.enableButton()


    def clickButton(self, row: int, col: int):
        """Handles the player's move when clicking a button.

        Args:
            row (int): Row index of the clicked button.
            col (int): Column index of the clicked button.
        """
        try:
            self.game_board.updateGameBoard(row, col, self.guiboard)
            self.client_socket.send(f"{row},{col}".encode())
            if self.game_board.isWinner():
                self.game_board.updateGamesPlayed()
                self.game_board.resetGameBoard()
                self.subheading.config(text=f"{self.game_board.userturn} is the Winner!")
                self.root.update()
                self.disableButton()
                self.receiveMove()
            elif self.game_board.boardIsFull():
                self.game_board.updateGamesPlayed()
                self.game_board.resetGameBoard()
                self.subheading.config(text="It's a tie!")
                self.root.update()
                self.disableButton()
                self.receiveMove()
            else:
                self.game_board.changePlayerTurn()
                self.turn_label.config(text=f"Turn: {self.game_board.userturn}")
                self.root.update()
                self.disableButton()
                self.receiveMove()
        except ValueError:
            self.turn_label.config(text=f"Invalid move.")

            
    def disableButton(self):
        """Disables all buttons on the GUI."""
        for row in self.guiboard:
            for button in row:
                button.config(state="disabled")


    def enableButton(self):
        """Enables all buttons on the GUI."""
        for row in self.guiboard:
            for button in row:
                button.config(state="normal")


    def endGame(self):
        """Displays final statistics and ends the game."""
        for widget in self.root.winfo_children():
                widget.destroy()
        player1, player2, gamesplayed, numwins, numlosses, numties = self.game_board.computeStats()
        end_label = tk.Label(self.root, text=f"{self.game_board.player1} has ended the game!")
        end_label.pack()
        stats_label = tk.Label(self.root, text="Final Statistics:")
        stats_label.pack()
        stats_text = (
            f"Player 2: {player2}\n"
            f"Games Played: {gamesplayed}\n"
            f"Number of Wins ({player2}): {numwins}\n"
            f"Number of Losses ({player2}): {numlosses}\n"
            f"Number of Ties: {numties}"
        )
        stats_display = tk.Label(self.root, text=stats_text)
        stats_display.pack()

        self.root.update()
        exit()
        
if __name__ == "__main__":
    root = tk.Tk()
    game_board = BoardClass()
    player2 = Player2(root, game_board)
    player2.startServer()
    root.mainloop()
