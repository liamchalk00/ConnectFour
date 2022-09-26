import random

class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

        # We do not need to return anything from a constructor!

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # the string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # bottom of the board
        s+= '\n'                        # next line
        s+= ' '                         # space
        for i in range(0, self.width):  # numbers under each line
            s+= str(i) + ' '

        # and the numbers underneath here

        return s       # the board is complete, return it

    def addMove(self, col, ox): 
        if self.data[0][col] != ' ':
            return
        for i in range(self.height):
            if self.data[i][col] != ' ':
                self.data[i-1][col] = ox
                break
        if self.data[self.height-1][col] == ' ':
            self.data[self.height-1][col] = ox
        return

    def clear(self):
        '''clears board'''
        width = self.width
        height = self.height
        self.data = [[' ']*width for row in range(height)]

    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'

    def allowsMove(self, col):
        """
        True if col is in-bounds + open False otherwise 
        """

        H = self.height 
        W = self.width
        D = self.data

        if col >= W or col < 0 :
            return False
        elif D[0][col] != ' ':
            return False
        else:
            return True 

    def isFull(self):
        """Should return True if the calling object (of type Board) 
        is completely full of checkers. It should return False otherwise. 
        """
        for col in range(self.width):
            if self.allowsMove(col):
                return False
        return True


    def delMove(self, col): 
        """
        opposite of addMove. 
        It should remove the top checker from the column c. 
        If the column is empty, then delMove should do nothing. 
        """
        H = self.height 
        W = self.width
        D = self.data
        
        for row in range(0, H):
            if self.data[row][col] != ' ':
                self.data[row][col] = ' '
                return
        

    def winsFor(self, ox):  
        ''' does ox win? '''
        H = self.height
        W = self.width
        D = self.data
        # Check for horizontal wins
        for row in range(0, H):
            for col in range(0, W - 3): # horizontal
                if D[row][col] == ox and \
                   D[row][col + 1] == ox and \
                   D[row][col + 2] == ox and \
                   D[row][col + 3] == ox:
                    return True
        for row in range(0, H - 3):
            for col in range(0, W): # vertical
                if D[row][col] == ox and D[row + 1][col] == ox and \
                    D[row + 2][col] == ox and \
                    D[row + 3][col] == ox:
                    return True
        for row in range(0, H - 3):
            for col in range(0, W - 3): # southeast
                if D[row][col] == ox and \
                    D[row + 1][col + 1] == ox and \
                    D[row + 2][col + 2] == ox and \
                    D[row + 3][col + 3] == ox: 
                    return True 
        for row in range(3, H):
            for col in range(0, W - 3): # northeast
                if D[row][col] == ox and \
                   D[row - 1][col + 1] == ox and \
                   D[row - 2][col + 2] == ox and \
                   D[row - 3][col + 3] == ox: 
                   return True

    def colsToWin(self, ox):
        """ Returns a list of columns at which ox would win on the next move
        """
        H = self.height
        W = self.width
        D = self.data
        
        
        colsToWinList = []
        for col in range(W):
            if self.allowsMove(col) == True:
                self.addMove(col, ox) 
                if self.winsFor(ox) == True:
                    colsToWinList = colsToWinList + [col]
                self.delMove(col)

        return colsToWinList
    

    def aiMove(self, ox):
        """Should return a single integer that is a legal column and move that first tries to win,
           and if it can't win, it should block, and if it can't do either, 
           it should choose to stay in the center
        """

        H = self.height
        W = self.width
        D = self.data

        enemy = 'X'
        if enemy == ox:
            enemy = 'O'

        # win move
        colsToWinList = self.colsToWin(ox)
        if colsToWinList != []:
            return colsToWinList[0]
        # block move
        elif self.colsToWin(enemy) != []:
            return self.colsToWin(enemy)[0]
        elif self.allowsMove(W//2) == True:
            return W//2
        else: 
            for index in range(W):
                if self.allowsMove(index) == True: 
                    return index

        
    def hostGame(self):
        """This method brings everything together 
        into the familiar game. It should host a game of Connect Four,
         using the methods listed above to do so. In particular, 
         it should alternate turns between 'X' (who will always go first) and 'O' 
         (who will always go second). It should ask the user (with the input function)
          to select a column number for each move.
        """
        print(self)
        while True:
            x = input('Input your move: ')
            if self.allowsMove(int(x)) == True:
                self.addMove(int(x), 'X')
                self.addMove(self.aiMove('O'), 'O')
                print(self)
                if self.isFull():
                    print('Tie!')
                    break
                elif self.winsFor('X'):
                    print('You Win!')
                    break
                elif self.winsFor('O'):
                    print('You Lose!')
                    break
            else:
                print("You can't go there!")
                
    def playGame(self, pForX, pForO, ss = False):
        """Plays a game of Connect Four.
           The players are objects of type Player p1 and p2 OR the string 'human'.
           If ss is True, it will "show scores" each time.
        """

        nextCheckerToMove = 'X'
        nextPlayerToMove = pForX

        while True:

            # print the current board
            print(self)

            # choose the next move
            if nextPlayerToMove == 'human':
                col = -1
                while not self.allowsMove(col):
                    col = int(input('Next col for ' + nextCheckerToMove + ': '))
            else: # it's a computer player
                if ss:
                    scores = nextPlayerToMove.scoresFor(self)
                    print((nextCheckerToMove + "'s"), 'Scores: ', [int(sc) for sc in scores])
                    print()
                    col = nextPlayerToMove.tiebreakMove(scores)
                else:
                    col = nextPlayerToMove.nextMove(self)

            # add the checker to the board
            self.addMove(col, nextCheckerToMove)

            # check if game is over
            if self.winsFor(nextCheckerToMove):
                print(self)
                print('\n' + nextCheckerToMove + ' wins! Congratulations!\n\n')
                break
            if self.isFull():
                print(self)
                print('\nThe game is a draw.\n\n')
                break

            # swap players
            if nextCheckerToMove == 'X':
                nextCheckerToMove = 'O'
                nextPlayerToMove = pForO
            else:
                nextCheckerToMove = 'X'
                nextPlayerToMove = pForX

        print('Come back 4 more!')


class Player: 
    """can choose moves so that it plays an arbitrarily sophisticated game of Connect Four."""
    def __init__(self, ox, tbt, ply):
        """ This constructor first takes in a one-character
         string ox: this will be either 'X' or 'O'. Second, it takes in tbt, 
         a string representing the tiebreaking type of the player. 
         It will be one of 'LEFT', 'RIGHT', or 'RANDOM'. 
         The third argument, ply, will be a nonnegative integer representing the 
         number of moves that the player should look into the future when evaluating
          where to go next. 
        """
        """Construct a player for a given checker, tie-breaking type,
           and ply."""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply
        self.width = 7
        self.height = 6
        self.data = [[' ']*7 for row in range(6)]

    def __repr__(self):
        """Create a string represenation of the player."""
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self): 
        """ return the other kind of checker or playing piece, i.e., 
        the piece being played by self's opponent. In particular, 
        if self is playing 'X', this method returns 'O' and vice-versa. 
        Just be sure to stick with capital-O!
        """
        if self.ox == 'X':
            return 'O'
        elif self.ox == 'O':
            return 'X'

    def scoreBoard(self, b):
        """This method should return a single float value 
        representing the score of the input b, 
        which you may assume will be an object of type Board. 
        This should return 100.0 if the board b is a win for self. 
        It should return 50.0 if it is neither a win nor a loss for self, 
        and it should return 0.0 if it is a loss for self (i.e., the opponent 
        has won).
        """
        H = 6
        W = 7
        D = self.data

        for col in range(W):
            if b.allowsMove(col) == True:
                if b.winsFor(self.ox) == True:
                    return 100.0 
                elif b.colsToWin(self.oppCh()) != []:
                    return 0.0
                else:
                    return 50.0
            
    def tiebreakMove(self, scores):
        """This method takes in scores, which will be a nonempty list of floating-point numbers. 
           If there is only one highest score in that scores list, this method should return 
           its COLUMN number, not the actual score.
           Thus, if the tiebreaking type is 'LEFT', then tiebreakMove should return the column
           of the leftmost highest score (not the score itself). 
           If the tiebreaking type is 'RIGHT', then tiebreakMove should return the column 
           of the rightmost highest score (not the score itself). 
           And if the tiebreaking type is 'RANDOM', then tiebreakMove should return the column 
           of the a randomly-chosen highest score (yet again, not the score itself).
        """  
        L=[]  #Scores
        maxIndices=[]   # takes L and returnes corresponding col of max scores

        # we must find max/es and then find the column numbers of the maxes
        for x in range(7):
            if scores[x] == max(scores):
                maxIndices += [x]

        if self.tbt == 'LEFT':   # self.tbt is string random, left or right
            """Take the scoreBoard list and place a ox in the leftmost high-scoring column
            """
            return maxIndices[0]
        if self.tbt == 'RIGHT':
            """Take the scoreBoard list and place a ox in the rightmost high-scoring column
            """
            return maxIndices[-1]
        if self.tbt == 'RANDOM':
            """Take the scoreBoard list and place a ox in the rightmost high-scoring column
            """
            return random.choice(maxIndices)

    def scoresFor(self, b):
        """Returns a list of scores, with the cth score representing the "goodness" 
           of the input board after the player moves to column c. And, "goodness" 
           is measured by what happens in the game after self.ply moves.
        """

        L=[]  #Scores
        scores = [50.0]*b.width

        for x in range(b.width):
            if b.allowsMove(x) == False:
                scores[x] = -1.0
            elif b.winsFor(x) == True:
                scores[x] = 100
            elif b.winsFor(self.oppCh()):
                scores[x] = 0.0
            elif self.ply == 0.0:
                scores[x] = 50.0
            elif self.ply > 0.0:
                b.addMove(x, self.ox)
                if b.isFull() == True:
                    scores[x] = -1.0
                if b.winsFor(self.ox) == True:
                    scores[x] = 100.0
                op = Player(self.oppCh(), self.tbt, self.ply-1)
                scores[x] = 100.0-max(op.scoresFor(b))
                b.delMove(x)
        return scores
            
    def nextMove(self, b):
        """Accepts a Board object b and returns the column number that the Player (self)
           should move to based on the .
        """
        scores = self.scoresFor(b)
        return self.tiebreakMove(scores)