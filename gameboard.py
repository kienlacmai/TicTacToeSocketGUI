"""This module handles the logistics of creating and updating a Tic Tac Toe Game."""

class BoardClass():
    """
    Represents the game board for a Tic Tac Toe game.

    Attributes:
        player1 (str): Name of Player 1.
        player2 (str): Name of Player 2.
        userturn (str): Name of the player whose turn it is.
        gamesplayed (int): Number of games played.
        numwins (dict): Dictionary mapping players to their number of wins.
        numlosses (dict): Dictionary mapping players to their number of losses.
        numties (int): Number of tied games.
        board (list): 2D list representing the game board.
        playerprofile (str): Profile of the current player for stats.

    Methods:
        setPlayer1Name(user): Sets the name of Player 1.
        setPlayer2Name(user): Sets the name of Player 2.
        setPlayerProfile1(): Sets the player profile to Player 1.
        setPlayerProfile2(): Sets the player profile to Player 2.
        addWinLoss(user): Adds initial win and loss counts for a user.
        resetDefaultTurn(): Resets the default turn to Player 1.
        resetGameBoard(): Resets the game board to its default state.
        resetPlayerTurn(): Resets the player turn to Player 1.
        updateGamesPlayed(): Updates the games played count.
        updateGameBoard(row, column, guiboard): Updates the game board and GUI.
        changePlayerTurn(): Changes the player turn to the other player.
        boardIsFull(): Checks if the game board is full.
        isWinner() -> bool: Checks if there's a winner in the game.
        computeStats(): Computes and returns game statistics.
    """
    
    def __init__(self):
        """Initializes the BoardClass instance."""
       
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.userturn = self.player1
        self.gamesplayed = 0
        self.numwins = {}
        self.numlosses = {}
        self.numties = 0
        self.board = [[' ', ' ', ' '] for i in range(3)]
        self.playerprofile = None


    def setPlayer1Name(self, user: str):
        """Sets the name of Player 1.

        Args:
            user (str): The name of Player 1.
        """
        self.player1 = user


    def setPlayer2Name(self, user: str):
        """Sets the name of Player 2.

        Args:
            user (str): The name of Player 2.
        """
        self.player2 = user

    
    def setPlayerProfile1(self):
        """Sets the player profile to Player 1."""
        self.playerprofile = self.player1

        
    def setPlayerProfile2(self):
        """Sets the player profile to Player 2."""
        self.playerprofile = self.player2


    def addWinLoss(self, user: str):
        """Adds initial win and loss counts for a user.

        Args:
            user (str): The user to add win and loss counts for.
        """
        self.numwins[user] = 0
        self.numlosses[user] = 0

        
    def resetDefaultTurn(self):
        """Resets the default turn to Player 1."""
        self.userturn = self.player1


    def resetGameBoard(self):
        """Resets the local game board to its default state."""
        self.board = [[' ', ' ', ' '] for i in range(3)]


    def resetPlayerTurn(self):
        """Resets the player turn to Player 1."""
        self.userturn = self.player1
        
        
    def updateGamesPlayed(self):
        """Updates the games played count."""
        self.gamesplayed += 1


    def updateGameBoard(self, row: int, column: int, guiboard: list):
        """Updates the game board and GUI.

        Args:
            row (int): Row index of the game board.
            column (int): Column index of the game board.
            guiboard (list): 2D list of GUI buttons representing the game board.
        """
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
        """Changes the player turn to the other player."""
        if self.userturn == self.player1:
            self.userturn = self.player2
        else:
            self.userturn = self.player1

        
    def boardIsFull(self) -> bool:
        """Checks if the game board is full.

        Returns:
            bool: True if the game board is full, False otherwise.
        """
        for row in self.board:
            for col in row:
                if col == ' ':
                    return False
        self.numties += 1
        return True


    def isWinner(self) -> bool:
        """Checks if there's a winner in the game.

        Returns:
            bool: True if there's a winner, False otherwise.
        """
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

    
    def computeStats(self) -> tuple:
        """Computes and returns game statistics.

        Returns:
            tuple: A tuple containing player names, games played, wins, losses, and ties.
        """
        return self.player1, self.player2, self.gamesplayed, self.numwins[self.playerprofile], self.numlosses[self.playerprofile], self.numties

    
if __name__ == "__main__":
    pass
