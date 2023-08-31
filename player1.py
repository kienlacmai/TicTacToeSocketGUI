"""This module contains the implementation of a Tic Tac Toe game where Player 1 interacts through a GUI interface.

It utilizes the tkinter library for graphical user interface components and communication is established
using sockets. The Player1 class represents the actions and behavior of Player 1 in the game.

Dependencies:
    - tkinter: The standard GUI library in Python.
    - socket: Provides the networking functionality for communication.
    - gameboard: A module providing the BoardClass for maintaining game state.

Usage:
    To play the game, create an instance of the Player1 class, passing the tkinter root window and an instance
    of BoardClass as arguments. Then, connect to Player2 via the `connectToP2()` method to initiate the game setup and GUI.
"""
import tkinter as tk
import socket
from gameboard import BoardClass

class Player1():
    """Represents Player 1 in the Tic Tac Toe game.

    Attributes:
        root (tk.Tk): The main tkinter root window.
        game_board (BoardClass): Instance of the game board.
        client_socket (socket.socket): Socket for communicating with Player 2.
        gameheading (tk.Label): GUI label for game heading.
        gamesubheading (tk.Label): GUI label for game subheading.
        turn_label (tk.Label): GUI label for displaying current turn.
        guiboard (list): 2D list of GUI buttons representing the game board.

    Methods:
        connectToP2(): Set up connection to Player 2.
        attemptConnection(connectip, ipentry, connectport, portentry, initialize):
            Attempt connection to Player 2.
        connect_to_server(host, port): Establish connection to the server.
        showRetryPrompt(): Display retry prompt after connection failure.
        determineIfRetry(cannotconnect, cannotentry, retryatt):
            Determine if the user wants to retry the connection.
        retryConnection(): Retry the connection.
        enterUsername(): Prompt for entering username.
        sendAndReceiveUser(enteruser, userentry, submituser):
            Send user's name and receive opponent's name.
        setGUI(): Set up the GUI for the game.
        createGameBoard(): Create the game board GUI.
        receiveMove(): Receive opponent's move.
        clickButton(row, col): Handle button click event.
        disableButton(): Disable all buttons on the game board.
        enableButton(): Enable all buttons on the game board.
        endGame(): Handle end of the game.
        determineIfEnd(): Determine if the player wants to end the game.
        showStats(): Display final game statistics.
    """

    def __init__(self, root: tk.Tk, game_board: BoardClass):
        """Initializes Player1 instance.

        Args:
            root (tk.Tk): The main tkinter root window.
            game_board (BoardClass): The instance of the game board.
        """
        self.root = root
        self.game_board = game_board
        self.client_socket = None
        self.gameheading = tk.Label(self.root, text="Default")
        self.gamesubheading = tk.Label(self.root, text="Default")
        self.turn_label = tk.Label(self.root, text="Default")
        self.guiboard = None

        
    def connectToP2(self):
        """Sets up connection to Player 2."""
        self.root.title("Welcome Player 1!")
        self.root.geometry('400x400')
        connectip = tk.Label(self.root, text="| Connect to Opponent to Start Game |\n\nEnter Player 2's host name/IP address: ")
        connectip.pack()
        ipentry = tk.Entry(self.root)
        ipentry.pack()
        connectport = tk.Label(self.root, text="Enter the port to use: ")
        connectport.pack()
        portentry = tk.Entry(self.root)
        portentry.pack()
        initialize = tk.Button(self.root, text="Connect", command=lambda: self.attemptConnection(connectip, ipentry, connectport, portentry, initialize))
        initialize.pack()

        
    def attemptConnection(self, connectip: tk.Label, ipentry: tk.Entry, connectport: tk.Label, portentry: tk.Entry, initialize: tk.Button):
        """Attempt connection to Player 2.

        Args:
            connectip (tk.Label): Label widget for connection information.
            ipentry (tk.Entry): Entry widget for IP address.
            connectport (tk.Label): Label widget for port information.
            portentry (tk.Entry): Entry widget for port number.
            initialize (tk.Button): Button widget for initializing connection.
        """
        try:
            host = ipentry.get()
            port = int(portentry.get())
            connectip.destroy()
            ipentry.destroy()
            connectport.destroy()
            portentry.destroy()
            initialize.destroy()
            client_socket = self.connect_to_server(host, port)
            self.client_socket = client_socket
            self.enterUsername()
        except (ValueError, ConnectionRefusedError, Exception):
            connectip.destroy()
            ipentry.destroy()
            connectport.destroy()
            portentry.destroy()
            initialize.destroy()
            self.showRetryPrompt()

            
    def connect_to_server(self, host: str, port: int) -> socket.socket:
        """Establish connection to the server.

        Args:
            host (str): Host name or IP address.
            port (int): Port number.

        Returns:
            socket.socket: Client socket object.
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket


    def showRetryPrompt(self):
        """Display retry prompt after connection failure."""
        cannotconnect = tk.Label(self.root, text="An connection error occurred. Would you like to try again? (y/n):")
        cannotconnect.pack()
        cannotentry = tk.Entry(self.root)
        cannotentry.pack()
        retryatt = tk.Button(self.root, text="Submit", command=lambda: self.determineIfRetry(cannotconnect, cannotentry, retryatt))
        retryatt.pack()


    def determineIfRetry(self, cannotconnect: tk.Label, cannotentry: tk.Entry, retryatt: tk.Button):
        """Determine if the user wants to retry the connection.

        Args:
            cannotconnect (tk.Label): Label widget for retry prompt.
            cannotentry (tk.Entry): Entry widget for user's response.
            retryatt (tk.Button): Button widget for retry submission.
        """
        response = cannotentry.get().lower()
        cannotconnect.destroy() 
        cannotentry.destroy() 
        retryatt.destroy() 
        if response == 'y':
            self.retryConnection()
        elif response == 'n':
            self.root.destroy()
            exit()
        else:
            self.root.destroy()
            exit()


    def retryConnection(self):
        """Retry the connection."""
        self.root.after(0, self.connectToP2)


    def enterUsername(self):
        """Prompts username entry."""
        self.root.title("Connected to Opponent!")
        enteruser = tk.Label(self.root, text="Enter your user name as (Player 1):")
        enteruser.pack()
        userentry = tk.Entry(self.root)
        userentry.pack()
        submituser = tk.Button(self.root, text="Submit", command=lambda: self.sendAndReceiveUser(enteruser, userentry, submituser))
        submituser.pack()


    def sendAndReceiveUser(self, enteruser: tk.Label, userentry: tk.Entry, submituser: tk.Button):
        """Send user's name and receive opponent's name.

        Args:
            enteruser (tk.Label): Label widget for entering username.
            userentry (tk.Entry): Entry widget for user's username.
            submituser (tk.Button): Button widget for submitting username.
        """
        userentry.config(state="disabled")
        p1user = userentry.get()
        self.client_socket.send(p1user.encode())
        self.root.title("Waiting on Opponent's User...")
        p2user = self.client_socket.recv(1024).decode()
        self.game_board.setPlayer1Name(p1user)
        self.game_board.setPlayer2Name(p2user)
        self.game_board.addWinLoss(p1user)
        self.game_board.addWinLoss(p2user)
        self.game_board.setPlayerProfile1()
        enteruser.destroy()
        userentry.destroy()
        submituser.destroy()
        self.root.title("Player 1 - Tic Tac Toe")
        self.root.update()
        self.setGUI()


    def setGUI(self):
        """Initializes GUI setup."""
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
        """Creates gameboard GUI."""
        self.guiboard = []
        for row in range(3):
            row_buttons = []
            for col in range(3):
                button = tk.Button(self.root, text="", width=10, height=3, command=lambda row=row, col=col: self.clickButton(row, col))
                button.grid(row=row + 4, column=col)
                row_buttons.append(button)
            self.guiboard.append(row_buttons)
        self.enableButton()


    def receiveMove(self):
        """Receives move from opponent."""
        waitlabel = tk.Label(self.root, text="Waiting...")
        waitlabel.grid(row=3, column=1)
        self.root.update()
        move_info = self.client_socket.recv(1024).decode()
        waitlabel.destroy()
        self.root.update()
        row, col = map(int, move_info.split(','))
        self.game_board.updateGameBoard(row, col, self.guiboard)
        if self.game_board.isWinner():
            self.game_board.updateGamesPlayed()
            self.game_board.resetGameBoard()
            self.subheading.config(text=f"{self.game_board.userturn} is the Winner!")
            self.root.update()
            self.endGame()
        elif self.game_board.boardIsFull():
            self.game_board.updateGamesPlayed()
            self.game_board.resetGameBoard()
            self.subheading.config(text="It's a tie!")
            self.root.update()
            self.endGame()
        else:
            self.game_board.changePlayerTurn()
            self.turn_label.config(text=f"Turn: {self.game_board.userturn}")
            self.root.update()
            self.enableButton()
            
        
    def clickButton(self, row, col):
        """Handles button click event.

        Args:
            row (int): Row index of the clicked button.
            col (int): Column index of the clicked button.
        """
        try:
            self.game_board.updateGameBoard(row, col, self.guiboard)
            self.client_socket.send(f"{row},{col}".encode())
            if self.game_board.isWinner():
                self.disableButton()
                self.game_board.updateGamesPlayed()
                self.game_board.resetGameBoard()
                self.subheading.config(text=f"{self.game_board.userturn} is the Winner!")
                self.root.update()
                self.endGame()
            elif self.game_board.boardIsFull():
                self.disableButton()
                self.game_board.updateGamesPlayed()
                self.game_board.resetGameBoard()
                self.subheading.config(text="It's a tie!")
                self.root.update()
                self.endGame()
            else:
                self.game_board.changePlayerTurn()
                self.turn_label.config(text=f"Turn: {self.game_board.userturn}")
                self.root.update()
                self.disableButton()
                self.receiveMove()
        except ValueError:
            self.turn_label.config(text=f"Invalid move.")

        
    def disableButton(self):
        """Disable all buttons on the game board."""
        for row in self.guiboard:
            for button in row:
                button.config(state="disabled")


    def enableButton(self):
        """Enables all buttons on the game board."""
        for row in self.guiboard:
            for button in row:
                button.config(state="normal")

                
    def endGame(self):
        """Handles end of the game."""
        endinglabel = tk.Label(self.root, text="The game has ended... Play again? (y/n)")
        endinglabel.grid(row=9, column=1)
        self.endingentry = tk.Entry()
        self.endingentry.grid(row=10,column=1)
        endingsubmit = tk.Button(self.root, text="Submit", command=self.determineIfEnd)
        endingsubmit.grid(row=11,column=1)
        self.root.update()
        
    def determineIfEnd(self):
        """Determines if the player wants to end the game."""
        response = self.endingentry.get().lower()
        if response == 'y':
            self.client_socket.send(f"Play Again".encode())
            self.game_board.resetDefaultTurn()
            self.setGUI()
        elif response == 'n':
            self.client_socket.send(f"Fun Times".encode())
            self.game_board.resetDefaultTurn()
            self.game_board.updateGamesPlayed()
            self.game_board.resetGameBoard()
            self.showStats()
            self.root.update()
            exit()
        else:
            self.client_socket.send(f"Fun Times".encode())
            self.showStats()
            exit()
                       
    def showStats(self):
        """Displays final game statistics."""
        for widget in self.root.winfo_children():
            widget.destroy()
        player1, player2, gamesplayed, numwins, numlosses, numties = self.game_board.computeStats()
        gamesplayed -= 1
        end_label = tk.Label(self.root, text="The game has ended!")
        end_label.pack()
        stats_label = tk.Label(self.root, text="Final Statistics:")
        stats_label.pack()
        stats_text = (
            f"Player 1: {player1}\n"
            f"Games Played: {gamesplayed}\n"
            f"Number of Wins ({player1}): {numwins}\n"
            f"Number of Losses ({player1}): {numlosses}\n"
            f"Number of Ties: {numties}"
        )
        stats_display = tk.Label(self.root, text=stats_text)
        stats_display.pack()


if __name__ == "__main__":
    root = tk.Tk()
    game_board = BoardClass()
    player1 = Player1(root, game_board)
    player1.connectToP2()
    root.mainloop()

