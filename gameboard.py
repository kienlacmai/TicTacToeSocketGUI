class BoardClass():

    def __init__(self):
       
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.userturn = self.player1
        self.gamesplayed = 0
        self.numwins = {}
        self.numlosses = {}
        self.numties = 0
        
        self.board = [[' ', ' ', ' '] for i in range(3)]
        self.playerprofile = None

    def setPlayer1Name(self, user):
        self.player1 = user

    def setPlayer2Name(self, user):
        self.player2 = user
    
    def setPlayerProfile1(self): # necessary for stats printout
        self.playerprofile = self.player1
        
    def setPlayerProfile2(self): # necessary for stats printout
        self.playerprofile = self.player2

    def addWinLoss(self, user):
        self.numwins[user] = 0
        self.numlosses[user] = 0
        
    def resetDefaultTurn(self):
        self.userturn = self.player1

    def resetGameBoard(self): # resetting local board 
        self.board = [[' ', ' ', ' '] for i in range(3)] # include a reset for gui

    def resetPlayerTurn(self):
        self.userturn = self.player1
        
    def updateGamesPlayed(self):
        self.gamesplayed += 1

    def updateGameBoard(self, row, column, guiboard): # include updating gui board
        if self.board[row][column] == ' ':
            if self.userturn == self.player1:
                self.board[row][column] = 'X'
                guiboard[row][column].config(text='X')
            elif self.userturn == self.player2:
                self.board[row][column] = 'O'
                guiboard[row][column].config(text='O')
        else:
            raise ValueError
        
    def changePlayerTurn(self):
        if self.userturn == self.player1:
            self.userturn = self.player2
        else:
            self.userturn = self.player1
        
    def boardIsFull(self):
        for row in self.board:
            for col in row:
                if col == ' ':
                    return False
        self.numties += 1
        return True

    def isWinner(self) -> bool:
        """Checks for a winner in the game."""
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                self.numwins[self.userturn] += 1
                self.numlosses[self.player2 if self.userturn == self.player1 else self.player1] += 1
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                self.numwins[self.userturn] += 1
                self.numlosses[self.player2 if self.userturn == self.player1 else self.player1] += 1
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.numwins[self.userturn] += 1
            self.numlosses[self.player2 if self.userturn == self.player1 else self.player1] += 1
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.numwins[self.userturn] += 1
            self.numlosses[self.player2 if self.userturn == self.player1 else self.player1] += 1
            return True
        
        return False
    
    def computeStats(self):
        return self.player1, self.player2, self.gamesplayed, self.numwins[self.playerprofile], self.numlosses[self.playerprofile], self.numties
    
if __name__ == "__main__":
    pass
