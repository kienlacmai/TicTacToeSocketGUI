import tkinter as tk
import socket
from gameboard import BoardClass

class Player1():

 import tkinter as tk
import socket
from gameboard import BoardClass

class Player1():

    def __init__(self, root, game_board):
        self.root = root
        self.game_board = game_board
        self.client_socket = None
        self.gameheading = tk.Label(self.root, text="Default")
        self.gamesubheading = tk.Label(self.root, text="Default")
        self.turn_label = tk.Label(self.root, text="Default")
        self.guiboard = None
        

    def connectToP2(self):
        self.root.title("Player1")
        self.root.geometry('400x400')
        connectip = tk.Label(self.root, text="Enter Player 2's host name/IP address: ")
        connectip.pack()

        ipentry = tk.Entry(self.root)
        ipentry.pack()

        connectport = tk.Label(self.root, text="Enter the port to use: ")
        connectport.pack()

        portentry = tk.Entry(self.root)
        portentry.pack()

        initialize = tk.Button(self.root, text="Connect", command=lambda: self.attemptConnection(connectip, ipentry, connectport, portentry, initialize))
        initialize.pack()

    def attemptConnection(self, connectip, ipentry, connectport, portentry, initialize):
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
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            return client_socket

    def showRetryPrompt(self):
        cannotconnect = tk.Label(self.root, text="An connection error occurred. Would you like to try again? (y/n):")
        cannotconnect.pack()

        cannotentry = tk.Entry(self.root)
        cannotentry.pack()

        retryatt = tk.Button(self.root, text="Submit", command=lambda: self.determineIfRetry(cannotconnect, cannotentry, retryatt))
        retryatt.pack()

    def determineIfRetry(self, cannotconnect, cannotentry, retryatt):
        response = cannotentry.get().lower()
        cannotconnect.destroy() #
        cannotentry.destroy() #
        retryatt.destroy() #
        if response == 'y':
            self.retryConnection()
        elif response == 'n':
            self.root.destroy()
            exit()
        else:
            self.root.destroy()
            exit()
        
    def retryConnection(self):
        self.root.after(0, self.connectToP2)

    def enterUsername(self):
        self.root.title("Connected to Opponent!")

        enteruser = tk.Label(self.root, text="Enter your user name as (Player 1):")
        enteruser.pack()

        userentry = tk.Entry(self.root)
        userentry.pack()

        submituser = tk.Button(self.root, text="Submit", command=lambda: self.sendAndReceiveUser(enteruser, userentry, submituser))
        submituser.pack()

    def sendAndReceiveUser(self,enteruser,userentry,submituser):
        p1user = userentry.get()
        self.client_socket.send(p1user.encode())
        
        p2user = self.client_socket.recv(1024).decode()
        
        self.game_board.setPlayer1Name(p1user)
        self.game_board.setPlayer2Name(p2user)
        self.game_board.numwins[p1user] = 0
        self.game_board.numwins[p2user] = 0
        self.game_board.numlosses[p1user] = 0
        self.game_board.numlosses[p2user] = 0
        self.game_board.setPlayerProfile1()

        enteruser.destroy()
        userentry.destroy()
        submituser.destroy()

        self.root.title("Player 1 - Tic Tac Toe")
        self.root.update()
        self.setGUI()

    def setGUI(self):
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
        self.game_board.updateGameBoard(row, col, self.guiboard)
        
        self.client_socket.send(f"{row},{col}".encode()) #send to player 2
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

        
        
    def disableButton(self):
        for row in self.guiboard:
            for button in row:
                button.config(state="disabled")

    def enableButton(self):
        for row in self.guiboard:
            for button in row:
                button.config(state="normal")
                
    def endGame(self):

        endinglabel = tk.Label(self.root, text="The game has ended... Play again? (y/n)")
        endinglabel.grid(row=9, column=1)

        self.endingentry = tk.Entry()
        self.endingentry.grid(row=10,column=1)

        endingsubmit = tk.Button(self.root, text="Submit", command=self.determineIfEnd)
        endingsubmit.grid(row=11,column=1)

        self.root.update()
        
    def determineIfEnd(self):
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
        for widget in self.root.winfo_children():
                widget.destroy()
        player1, player2, gamesplayed, numwins, numlosses, numties = self.game_board.computeStats()
        gamesplayed -= 1
        end_label = tk.Label(self.root, text="Game Over!")
        end_label.pack()
        
        stats_label = tk.Label(self.root, text="Statistics:")
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

