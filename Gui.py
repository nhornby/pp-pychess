import pygame as p

# GUI sizing
WIDTH = 400
BAR = 0
HEIGHT = WIDTH + 2 * BAR
SQ_SIZE = WIDTH // 8

# Display options
MAX_FPS = 60
ANIMATION_SPEED = 3/MAX_FPS # Range from 0 to 1

# Color scheme
COLOR_LIGHT_SQUARE = (240, 217, 181)
COLOR_DARK_SQUARE = (180, 136, 99)
COLOR_LIGHT_HIGHLIGHTED = (111, 147, 170)
COLOR_DARK_HIGHLIGHTED = (59, 96, 140)
COLOR_BAR = (230, 230, 230)

# Fonts
LETTERING_ON_TILES = False
LETTERING_FONT_SIZE = 10

# Stores icon data
ICONS = {}

class Gui():
    def __init__(self):
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        p.display.set_caption("PyChess AI")
        self.__load_icons()

        self.white_view = True      # White-oriented view?
        self.animations = []        # List of Animation objects
        self.highlighted = []       # List of positions that are highlighted on the board.
        self.clicks = []            # List of positions that have been clicked.

    # Screen updates
    def update_screen(self, gamestate):
        """
        SCREEN method:
            draws the squares on the board
            draws the lettering on the board
            draws static pieces
            draws animating pieces
        """
        self.screen.fill(p.Color(COLOR_BAR))
        self.__draw_squares()
        if LETTERING_ON_TILES:
            self.__draw_lettering()
        self.__draw_static_pieces(gamestate)
        self.__draw_dynamic_pieces()

    # Click methods
    def store_click(self, gamestate):
        """
        CLICK method:
            stores the current mouse position to "clicks"
            updates the current highlighted spots on the board.
        """
        if len(self.clicks) < 2:
            if BAR < p.mouse.get_pos()[1] < WIDTH + BAR:
                if self.white_view:
                    self.clicks.append(((p.mouse.get_pos()[1] - BAR)//SQ_SIZE, (p.mouse.get_pos()[0])//SQ_SIZE))
                else:
                    self.clicks.append((7 - (p.mouse.get_pos()[1] - BAR)//SQ_SIZE, 7 - (p.mouse.get_pos()[0])//SQ_SIZE))
                self.highlighted = gamestate.gen_valid_pos_from(self.clicks[0])
    def clear_clicks(self):
        """
        CLICK method:
            clears any clicks stored in "clicks"
            clears any highlighted spots on the board.
        """
        self.clicks = []
        self.highlighted = []

    # Animation methods
    def store_animation(self, move):
        """
        ANIMATION method:
            stores the move passed in to "animations".
            this move will be animated until complete or clear_animations is run.
        REQUIRES: move is an object of type "Move"
        """
        self.animations.append(Animation(move, ANIMATION_SPEED))
    def update_animations(self):
        """
        ANIMATION method:
            progresses whichever current animations are unfinished.
            should be run while any animations are in progress.
        """
        for animation in self.animations:
            animation.progress += animation.speed
            if animation.progress > 1:
                self.animations.remove(animation)
    def clear_animations(self):
        """
        ANIMATION method:
            clears any moves passed in to "animations".
            effectively ends any current animations.
        """
        self.animations = []

    # Helper methods
    def __draw_squares(self):
        """
        HELPER METHOD:
            draws the board squares onto the screen
        REQUIRES: none
        MODIFIES: self.screen
        """
        colors = [p.Color(COLOR_LIGHT_SQUARE), p.Color(COLOR_DARK_SQUARE)]
        highlightedcolors = [p.Color(COLOR_LIGHT_HIGHLIGHTED), p.Color(COLOR_DARK_HIGHLIGHTED)]
        for r in range(8):
            for c in range(8):
                color = colors[((r+c)%2)]
                if self.white_view:
                    if (r, c) in self.highlighted:
                        color = highlightedcolors[((r+c)%2)]
                elif not self.white_view:
                    if (7-r,7-c) in self.highlighted:
                        color = highlightedcolors[((r+c)%2)]
                p.draw.rect(self.screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE + BAR, SQ_SIZE, SQ_SIZE))
    def __draw_lettering(self):
        """
        HELPER METHOD:
            draws the board square lettering onto the screen
        REQUIRES: none
        MODIFIES: self.screen
        """
        colors = [p.Color(COLOR_LIGHT_SQUARE), p.Color(COLOR_DARK_SQUARE)]
        font = p.font.Font(None, LETTERING_FONT_SIZE)

        for r in range(8):
            for c in range(8):
                color = colors[((r+c+1)%2)]
                img = font.render(self.__convert_to_lettering((r,c)), True, color)
                if self.white_view:
                    self.screen.blit(img, (c*SQ_SIZE + 2, r*SQ_SIZE + 2 + BAR))
                else:
                    self.screen.blit(img, ((7-c)*SQ_SIZE + 2, (7-r)*SQ_SIZE + 2 + BAR))
    def __draw_static_pieces(self, gamestate):
        """
        HELPER METHOD:
            draws the board pieces that are not animating
        """
        moving_pieces = []
        for animation in self.animations:
            moving_pieces.append(animation.move.start)
            moving_pieces.append(animation.move.end)

        for r in range(8):
            for c in range(8):
                if not (r, c) in moving_pieces:
                    piece = gamestate.board[r][c]
                    if piece != "  ":
                        if self.white_view:
                            self.screen.blit(ICONS[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE + BAR, SQ_SIZE, SQ_SIZE))
                        else:
                            self.screen.blit(ICONS[piece], p.Rect((7-c)*SQ_SIZE, (7-r)*SQ_SIZE + BAR, SQ_SIZE, SQ_SIZE))
    def __draw_dynamic_pieces(self):
        """
        HELPER METHOD:
            draws the board pieces that are animating
        """
        moving_pieces = []
        for animation in self.animations:
            moving_pieces.append(animation.move.start)
            moving_pieces.append(animation.move.end)
            
        for animation in self.animations:
            piece = animation.move.piece1
            m_start = animation.move.start
            m_end = animation.move.end
            if piece != "  ":
                r = (m_end[0] - m_start[0]) * animation.progress + m_start[0]
                c = (m_end[1] - m_start[1]) * animation.progress + m_start[1]
                if self.white_view:
                    self.screen.blit(ICONS[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE + BAR, SQ_SIZE, SQ_SIZE))
                else:
                    self.screen.blit(ICONS[piece], p.Rect((7-c)*SQ_SIZE, (7-r)*SQ_SIZE + BAR, SQ_SIZE, SQ_SIZE))
    def __load_icons(self):
        """
        HELPER METHOD:
            preloads the icons for use
        REQUIRES: a folder "icons" containing icons labeled in the format
                  (color char)(piece char).png
                  ex) white pawn is "icons/wp.png"
        MODIFIES: ICONS
        """
        pieces = ["bp","br","bn","bb","bq","bk","wp","wr","wn","wb","wq","wk"]
        for piece in pieces:
            ICONS[piece] = p.transform.scale(p.image.load("icons/" + piece + ".png"),(SQ_SIZE, SQ_SIZE))
    def __convert_to_lettering(self, pos):
        """
        HELPER METHOD:
            converts a (row, col) position to chess notation, returns the chess notation
        REQUIRES: pos is a (row, col) tuple
        MODIFIES: none
        """
        return ''.join(map(''.join, zip(chr(65 + pos[1]), chr(56 - pos[0]))))

class Animation():
    def __init__(self, move_in, speed_in):
        self.move = move_in                                 # Move that this animation is doing
        self.progress = 0                                   # Progress through the animation (0, 1)
        self.speed = speed_in
