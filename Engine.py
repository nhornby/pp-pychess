class Gamestate():
    """
    GAMESTATE CLASS:
        contains current board state (self.board) as a 2D array of strings
            ex) white pawn would be represented as "wp" on board,
        contains current player (self.current_player) as a char ('b'/'w')
        contains any past moves that have been made on the board as a list of "Move" objects
    """

    def __init__(self):
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wn","wb","wq","wk","wb","wn","wr"]]
        self.current_player = 'w'
        self.past_moves = []

        self.whiteking_loc = (7, 4)
        self.blackking_loc = (0, 4)
    
    # Engine actions
    def make_move(self, move):
        """
        ACTION method:
            makes the move passed in

            self.board is modified
            the move is added self.past_moves

            handles pawn promotions
        """
        if is_valid_pos(move.start) and is_valid_pos(move.end):
            self.board[move.start[0]][move.start[1]] = "  "
            self.board[move.end[0]][move.end[1]] = move.piece1
            self.past_moves.append(move)

            # Handle pawn promotions
            if move.piece1[1] == 'p':
                if (move.end[0] == 0 and move.piece1[0] == 'w'): # If a white pawn reached the end
                    self.board[move.end[0]][move.end[1]] = 'wq'
                if (move.end[0] == 7 and move.piece1[0] == 'b'): # If a black pawn reached the end
                    self.board[move.end[0]][move.end[1]] = 'bq'
            if move.piece1 == "wk":
                self.whiteking_loc = move.end
            elif move.piece1 == 'bk':
                self.blackking_loc = move.end
    def undo_move(self):
        """
        ACTION method:
            undoes the previous move

            self.board rolls back one move
            self.past_moves is popped
        """
        if len(self.past_moves) != 0:
            move = self.past_moves.pop()
            self.board[move.start[0]][move.start[1]] = move.piece1
            self.board[move.end[0]][move.end[1]] = move.piece2

            if move.piece1 == "wk":
                self.whiteking_loc = move.start
            elif move.piece1 == "bk":
                self.blackking_loc = move.start
    def reset_game(self):
        """
        ACTION method:
            resets the entire game
            puts white as current player
        """
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wn","wb","wq","wk","wb","wn","wr"]]
        self.current_player = 'w'
        self.past_moves = []

        self.whiteking_loc = (7, 4)
        self.blackking_loc = (0, 4)
    def switch_turn(self):
        """
        ACTION method:
            switches the current player
        """
        if self.current_player == 'w':
            self.current_player = 'b'
        else:
            self.current_player = 'w'

    # Engine logic
    def is_check(self):
        """
        LOGIC method:
            returns true if the current player is in check.
        """
        friendly_king = self.whiteking_loc if self.current_player == 'w' else self.blackking_loc

        self.switch_turn()
        possible_enemy_moves = self.gen_possible_moves()
        self.switch_turn()

        for move in possible_enemy_moves:
            if move.end == friendly_king:
                return True
        return False
    def is_checkmate(self):
        """
        LOGIC method:
            returns true if the current player is in a checkmate.
        """
        if len(self.gen_valid_moves()) == 0 and self.is_check():
            return True
        return False
    def is_stalemate(self):
        """
        LOGIC method:
            returns true if the current player is in a stalemate.
        """
        if len(self.gen_valid_moves()) == 0 and not self.is_check():
            return True
        return False
    def gen_valid_moves(self):
        """
        CHESS LOGIC:
            generates and returns a list of all valid moves that can be made on the board,
            given the current game state and player. Takes into account moves that are invalid
            due to "check."

            returns an empty list if there are no valid moves
        REQUIRES: none
        MODIFIES: none
        """
        # Get possible moves
        possible_moves = self.gen_possible_moves()
        valid_moves = []

        for f_move in possible_moves:
            self.make_move(f_move)
            if not self.is_check():
                valid_moves.append(f_move)
            self.undo_move()
        return valid_moves
    def gen_possible_moves(self):
        """
        CHESS LOGIC:
            generates and returns a list of all possible moves that can be made on the board,
            given the current game state and player. Does not take into account "check."

            returns an empty list if there are no possible moves
        REQUIRES: none
        MODIFIES: none
        """
        move_list = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col][0] == self.current_player:
                    if self.board[row][col][1] == 'p':
                        self.__gen_pawn_moves(move_list, (row,col))
                    elif self.board[row][col][1] == 'r':
                        self.__gen_rook_moves(move_list, (row,col))
                    elif self.board[row][col][1] == 'b':
                        self.__gen_bishop_moves(move_list, (row,col))
                    elif self.board[row][col][1] == 'q':
                        self.__gen_queen_moves(move_list, (row,col))
                    elif self.board[row][col][1] == 'k':
                        self.__gen_king_moves(move_list, (row,col))
                    elif self.board[row][col][1] == 'n':
                        self.__gen_knight_moves(move_list, (row,col))
        return move_list

    # Helper methods: (gui)
    def gen_valid_pos_from(self, pos):
        possible = []
        if self.board[pos[0]][pos[1]][0] == self.current_player:
            if self.board[pos[0]][pos[1]][1] == 'p':
                self.__gen_pawn_moves(possible, (pos[0],pos[1]))
            elif self.board[pos[0]][pos[1]][1] == 'r':
                self.__gen_rook_moves(possible, (pos[0],pos[1]))
            elif self.board[pos[0]][pos[1]][1] == 'b':
                self.__gen_bishop_moves(possible, (pos[0],pos[1]))
            elif self.board[pos[0]][pos[1]][1] == 'q':
                self.__gen_queen_moves(possible, (pos[0],pos[1]))
            elif self.board[pos[0]][pos[1]][1] == 'k':
                self.__gen_king_moves(possible, (pos[0],pos[1]))
            elif self.board[pos[0]][pos[1]][1] == 'n':
                self.__gen_knight_moves(possible, (pos[0],pos[1]))
        valid = []
        for move in possible:
            self.make_move(move)
            if not self.is_check():
                valid.append(move.end)
            self.undo_move()
        return valid

    # Helper methods: (move generation)
    def __gen_pawn_moves(self, possible_moves, pos):
        """
        HELPER METHOD:
            generates possibly valid pawn moves

            takes in an empty list and a position.
            generates all possible moves from this position for a pawn.
            (could still be in check after making this move)

        REQUIRES: possible_moves is a list of 'Move' object, pos is a tuple (r, c)
        MODIFIES: possible_moves
        """
        d_r = 1
        if self.current_player == 'w':
            d_r = -1

        # Moving forward
        aheadone = (pos[0] + d_r, pos[1])
        if is_valid_pos(aheadone):
            if self.board[aheadone[0]][aheadone[1]][0] == ' ':
                possible_moves.append(Move(pos, aheadone, self.board))
                aheadtwo = (pos[0] + 2 * d_r, pos[1])
                if (d_r == -1 and pos[0] == 6) or (d_r == 1 and pos[0] == 1):
                    if is_valid_pos(aheadtwo):
                        if self.board[aheadtwo[0]][aheadtwo[1]][0] == ' ':
                            possible_moves.append(Move(pos, aheadtwo, self.board))
        # Attacking
        attack_l = (pos[0] + d_r, pos[1] - 1)
        if is_valid_pos(attack_l):
            if self.board[attack_l[0]][attack_l[1]][0] == opposite_color(self.current_player):
                possible_moves.append(Move(pos, attack_l, self.board))
        attack_r = (pos[0] + d_r, pos[1] + 1)
        if is_valid_pos(attack_r):
            if self.board[attack_r[0]][attack_r[1]][0] == opposite_color(self.current_player):
                possible_moves.append(Move(pos, attack_r, self.board))
    def __gen_rook_moves(self, possible_moves, pos):
        """
        HELPER METHOD:
            generates possibly valid rook moves

            takes in an empty list and a position.
            generates all possible moves from this position for a rook.
            (could still be in check after making this move)

        REQUIRES: possible_moves is a list of 'Move' object, pos is a tuple (r, c)
        MODIFIES: possible_moves
        """
        for (row, col) in ((1,0),(-1,0),(0,1),(0,-1)):
            for dist in range(1, 8):
                pos2 = (pos[0] + dist * row, pos[1] + dist * col)
                if is_valid_pos(pos2):
                    color = self.board[pos2[0]][pos2[1]][0]
                    if color != self.current_player:
                        possible_moves.append(Move(pos, pos2, self.board))
                    if color != ' ':
                        break
                else:
                    break
    def __gen_bishop_moves(self, possible_moves, pos1):
        """
        HELPER METHOD:
            generates possibly valid bishop moves

            takes in an empty list and a position.
            generates all possible moves from this position for a bishop.
            (could still be in check after making this move)

        REQUIRES: possible_moves is a list of 'Move' object, pos is a tuple (r, c)
        MODIFIES: possible_moves
        """
        for (row, col) in ((-1,-1),(-1,1),(1,-1),(1,1)):
            for dist in range(1, 8):
                pos2 = (pos1[0] + dist * row, pos1[1] + dist * col)
                if is_valid_pos(pos2):
                    color = self.board[pos2[0]][pos2[1]][0]
                    if color != self.current_player:
                        possible_moves.append(Move(pos1, pos2, self.board))
                    if color != ' ':
                        break
                else:
                    break
    def __gen_queen_moves(self, possible_moves, pos1):
        """
        HELPER METHOD: 
            generates possibly valid queen moves

            takes in an empty list and a position.
            generates all possible moves from this position for a queen.
            (could still be in check after making this move)

        REQUIRES: possible_moves is a list of 'Move' object, pos is a tuple (r, c)
        MODIFIES: possible_moves
        """
        for (row, col) in ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
            for dist in range(1, 8):
                pos2 = (pos1[0] + dist * row, pos1[1] + dist * col)
                if is_valid_pos(pos2):
                    color = self.board[pos2[0]][pos2[1]][0]
                    if color != self.current_player:
                        possible_moves.append(Move(pos1, pos2, self.board))
                    if color != ' ':
                        break
                else:
                    break
    def __gen_king_moves(self, possible_moves, pos1):
        """
        HELPER METHOD:
            generates possibly valid king moves

            takes in an empty list and a position.
            generates all possible moves from this position for a king.
            (could still be in check after making this move)

        REQUIRES: possible_moves is a list of 'Move' object, pos is a tuple (r, c)
        MODIFIES: possible_moves
        """
        for (row, col) in ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
            pos2 = (pos1[0] + row, pos1[1] + col)
            if is_valid_pos(pos2):
                color = self.board[pos2[0]][pos2[1]][0]
                if color != self.current_player:
                    possible_moves.append(Move(pos1, pos2, self.board))
    def __gen_knight_moves(self, possible_moves, pos1):
        """
        HELPER METHOD:
            generates possibly valid knight moves

            takes in an empty list and a position.
            generates all possible moves from this position for a knight.
            (could still be in check after making this move)

        REQUIRES: possible_moves is a list of 'Move' object, pos is a tuple (r, c)
        MODIFIES: possible_moves
        """
        for (row, col) in ((-1, -2),(1, -2),(-2,-1),(2,-1),(-2,1),(2,1),(-1,2),(1,2)):
            pos2 = (pos1[0] + row, pos1[1] + col)
            if is_valid_pos(pos2):
                color = self.board[pos2[0]][pos2[1]][0]
                if color != self.current_player:
                    possible_moves.append(Move(pos1, pos2, self.board))

class Move():
    """
    MOVE CLASS:
        pod class, used for saving move data

        contains a starting position (self.start)
        contains an ending position (self.end)
        contains a string containing the piece that was at "start" (self.piece1)
        contains a string containing the piece that was at "end" (self.piece2)
        contains a move_id used for comparing moves (r1,c1)->(r2,c2) means move_id = r1c1r2c2
    """

    def __init__(self, startSq, endSq, board):
        self.start = startSq
        self.end = endSq
        self.piece1 = board[self.start[0]][self.start[1]]
        self.piece2 = board[self.end[0]][self.end[1]]
        self.move_id = self.start[0] * 1000 + self.start[1] * 100 + self.end[0] * 10 + self.end[1]
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.move_id == other.move_id)

def opposite_color(color):
    """
    HELPER METHOD:
        returns opposite color of whatever color is passed in

        opposite_color('w') = 'b'
        opposite_color('b') = 'w'
    """
    if color == 'b':
        return 'w'
    else:
        return 'b'
def is_valid_pos(position):
    """
    HELPER METHOD:
        returns true if "position" is a valid (row, col) tuple on the chessboard
        returns false if it is not
    """
    if ((0 <= position[0] < 8) and (0 <= position[1] < 8)):
        return True
    return False
