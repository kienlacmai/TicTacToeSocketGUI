import tkinter as tk
import socket
import threading
from gameboard import BoardClass  # Import your gameboard module

class Player2():

    def __init__(self, root, game_board):
        self.root = root
        self.game_board = game_board
        self.server_socket = None
        self.client_socket = None
        self.guiboard = None
        self.is_waiting = False

    def startServer(self):
        self.root.title("Player2")
        self.root.geometry('400x400')
        host_label = tk.Label(self.root, text="Enter your host/IP Address:")
        host_label.pack()

        self.host_entry = tk.Entry(self.root)
        self.host_entry.pack()

        port_label = tk.Label(self.root, text="Enter your port number:")
        port_label.pack()

        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        start_server_button = tk.Button(self.root, text="Start Server", command=self.initializeServer)
        start_server_button.pack()

    def initializeServer(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())

        self.server_socket = self.create_server_socket(host, port)
        threading.Thread(target=self.waitForPlayer1).start()

    def create_server_socket(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        return server_socket

    def waitForPlayer1(self):
        self.root.title("Waiting for Connection...")
        self.client_socket, _ = self.server_socket.accept()
        self.enterUsername()

    def enterUsername(self):
        self.root.title("Connected to Opponent!")
        for widget in self.root.winfo_children():
            widget.destroy()  # Remove all previous widgets

        username_label = tk.Label(self.root, text="Enter your user name as (Player 2):")
        username_label.pack()

        self.userentry = tk.Entry(self.root)
        self.userentry.pack()

        submit_user_button = tk.Button(self.root, text="Submit", command=self.sendUsername)
        submit_user_button.pack()

    def sendUsername(self):
        p2user = self.userentry.get()
        self.client_socket.send(p2user.encode())
        
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
                button.grid(row=row+4, column=col)
                row_buttons.append(button)
            self.guiboard.append(row_buttons)

        self.root.update()
        self.disableButton()
        self.receiveMove()

    def receiveMove(self):
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

    def clickButton(self, row, col):
        
        self.game_board.updateGameBoard(row, col, self.guiboard)
        
        self.client_socket.send(f"{row},{col}".encode())  # Send move to Player 1
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
            
    def disableButton(self):
        for row in self.guiboard:
            for button in row:
                button.config(state="disabled")

    def enableButton(self):
        for row in self.guiboard:
            for button in row:
                button.config(state="normal")

    def endGame(self):
        for widget in self.root.winfo_children():
                widget.destroy()
        player1, player2, gamesplayed, numwins, numlosses, numties = self.game_board.computeStats()
        
        end_label = tk.Label(self.root, text="Game Over!")
        end_label.pack()

        stats_label = tk.Label(self.root, text="Statistics:")
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
        
        

if __name__ == "__main__":
    root = tk.Tk()
    game_board = BoardClass()
    player2 = Player2(root, game_board)
    player2.startServer()
    root.mainloop()





