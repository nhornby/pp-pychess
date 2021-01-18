import Engine
import random
import time

class Player():
    def __init__(self, color):
        self.color = color
    def get_color(self):
        return self.color
class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.move_prepared = ((-1,-1),(-1,-1))
    def get_name(self):
        """
        GUI method:
            returns the player type in a string format.
        """
        return "Human (Level ?)"
    def get_move(self, gs):
        """
        MOVE method:
            takes in a gamestate, returns a valid move if one has been created by human input.
            if no valid move has been inputted, returns None.
        """
        if Engine.is_valid_pos(self.move_prepared[0]) and Engine.is_valid_pos(self.move_prepared[1]):
            valid_moves = gs.gen_valid_moves()
            move = Engine.Move(self.move_prepared[0], self.move_prepared[1], gs.board)
            if move in valid_moves:
                return move
        return None
class RandomPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
    def get_name(self):
        """
        GUI method:
            returns the player type in a string format.
        """
        return "Random Player"
    def get_move(self, gs):
        """
        MOVE method:
            takes in a gamestate, returns a valid move at random.
            if no valid moves are available, returns None.
        """
        moves = gs.gen_valid_moves()
        if len(moves) != 0:
            return random.choice(moves)
        return None
class AIPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.DEPTH = 2
    def get_name(self):
        """
        GUI method:
            returns the player type in a string format.
        """
        return "AI Player"
    def get_move(self, gs):
        """
        MOVE method:
            takes in a gamestate, returns the best move.
            if no valid moves are available, returns None.
        """
        moves_to_look_at = gs.gen_valid_moves()
        if len(moves_to_look_at) == 0:
            print("Out of moves")
        best_move = None
        best_score = 1000000
        for move in moves_to_look_at:
            gs.make_move(move)
            gs.switch_turn()
            score = self.minimax(gs, True, -1000000, 1000000, self.DEPTH)
            gs.switch_turn()
            gs.undo_move()
            if score < best_score:
                best_score = score
                best_move = move
        return best_move
    def minimax(self, gs, isMaximizingPlayer, alpha, beta, depth):
        if depth == 0:
            if isMaximizingPlayer:
                return 2*evaluate_pieces(gs) + evaluate_positioning(gs)
            else:
                return -(2*evaluate_pieces(gs) + evaluate_positioning(gs))
        if not isMaximizingPlayer:
            moves_to_look_at = gs.gen_valid_moves()
            for move in moves_to_look_at:
                gs.make_move(move)
                gs.switch_turn()
                beta = min(beta, self.minimax(gs, not isMaximizingPlayer, alpha, beta, depth-1))
                gs.switch_turn()
                gs.undo_move()
                if beta <= alpha:
                    return beta
            return beta
        elif isMaximizingPlayer:
            moves_to_look_at = gs.gen_valid_moves()
            for move in moves_to_look_at:
                gs.make_move(move)
                gs.switch_turn()
                alpha = max(alpha, self.minimax(gs, not isMaximizingPlayer, alpha, beta, depth-1))
                gs.switch_turn()
                gs.undo_move()
                if beta <= alpha:
                    return alpha
            return alpha

# Methods for gamestate evaluation (used by AI player)
def evaluate_mobility(gs):
    score = 0
    score += len(gs.gen_valid_moves())
    gs.switch_turn()
    score -= len(gs.gen_valid_moves())
    gs.switch_turn()
    return score  
def evaluate_pieces(gs):
    score = 0
    for row in range(8):
        for col in range(8):
            if gs.board[row][col][0] == " ":
                continue
            piece_score = 0
            if gs.board[row][col][1] == "p":
                piece_score = 100
            elif gs.board[row][col][1] == "n":
                piece_score = 320
            elif gs.board[row][col][1] == "b":
                piece_score = 330
            elif gs.board[row][col][1] == "r":
                piece_score = 500
            elif gs.board[row][col][1] == "q":
                piece_score = 900
            elif gs.board[row][col][1] == "k":
                piece_score = 100000
                
            if gs.board[row][col][0] == gs.current_player:
                score += piece_score
            else:
                score -= piece_score
    return score  
def evaluate_positioning(gs):
    score = 0
    for row in range(8):
        for col in range(8):
            if gs.board[row][col][0] == " ":
                continue
            piece_score = 0
            if gs.board[row][col][1] == "p":
                piece_score = __evaluate_pawn(gs, (row, col))
            elif gs.board[row][col][1] == "n":
                piece_score = __evaluate_knight(gs, (row, col))
            elif gs.board[row][col][1] == "b":
                piece_score = __evaluate_bishop(gs, (row, col))
            elif gs.board[row][col][1] == "r":
                piece_score = __evaluate_rook(gs, (row, col))
            elif gs.board[row][col][1] == "q":
                piece_score = __evaluate_queen(gs, (row, col))
            elif gs.board[row][col][1] == "k":
                piece_score = __evaluate_king(gs, (row, col))
                
            if gs.board[row][col][0] == gs.current_player:
                score += piece_score
            else:
                score -= piece_score
    return score                 
def __evaluate_pawn(gs, pos): 
    pawn_color = gs.board[pos[0]][pos[1]][0]
    pawn_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]]
    if pawn_color == 'w':
        return pawn_table[pos[0]][pos[1]]
    if pawn_color == 'b':
        return pawn_table[7-pos[0]][7-pos[1]]
def __evaluate_knight(gs, pos): 
    knight_color = gs.board[pos[0]][pos[1]][0]
    knight_table = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]]
    if knight_color == 'w':
        return knight_table[pos[0]][pos[1]]
    if knight_color == 'b':
        return knight_table[7-pos[0]][7-pos[1]]
def __evaluate_bishop(gs, pos): 
    bishop_color = gs.board[pos[0]][pos[1]][0]
    bishop_table = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]]
    if bishop_color == 'w':
        return bishop_table[pos[0]][pos[1]]
    if bishop_color == 'b':
        return bishop_table[7-pos[0]][7-pos[1]]
def __evaluate_rook(gs, pos):
    rook_color = gs.board[pos[0]][pos[1]][0]
    rook_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]]
    if rook_color == 'w':
        return rook_table[pos[0]][pos[1]]
    if rook_color == 'b':
        return rook_table[7-pos[0]][7-pos[1]]
def __evaluate_queen(gs, pos):
    queen_color = gs.board[pos[0]][pos[1]][0]
    queen_table = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]]
    if queen_color == 'w':
        return queen_table[pos[0]][pos[1]]
    if queen_color == 'b':
        return queen_table[7-pos[0]][7-pos[1]]
def __evaluate_king(gs, pos):
    king_color = gs.board[pos[0]][pos[1]][0]
    king_table = [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]]
    if king_color == 'w':
        return king_table[pos[0]][pos[1]]
    if king_color == 'b':
        return king_table[7-pos[0]][7-pos[1]]