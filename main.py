import pygame as p

import Engine
import Gui
import Player

def main():
    # Initialize pygame and resources
    p.init()
    clock = p.time.Clock()

    # Initialize the Game, GUI, Animations, etc.
    gui = Gui.Gui()
    gs = Engine.Gamestate()

    # Initialize Players
    player1 = Player.HumanPlayer('w')
    player2 = Player.AIPlayer('b')

    # Start board displaying
    gui.update_screen(gs)

    # Game Loop
    running = True
    while running:
        for g_e in p.event.get():
            if g_e.type == p.QUIT:                  # Event: Quit
                running = False
            elif g_e.type == p.MOUSEBUTTONDOWN:     # Event: Mouse pressed
                gui.store_click(gs)
                gui.update_screen(gs)
            elif g_e.type == p.KEYDOWN:             # Event: Key pressed
                if g_e.key == p.K_r:                    # Key: r (reset)
                    gs.reset_game()                              # Reset the game
                    gui.clear_animations()                  # Clear animations
                    gui.clear_clicks()                      # Clear clicks
                    gui.update_screen(gs)                   # Re-draw
                elif g_e.key == p.K_c:                  # Key: c (change color)
                    oldp1color = player1.color              # Switch the colors
                    player1.color = player2.color
                    player2.color = oldp1color
                    gui.white_view = not gui.white_view     # Switch the view
                    
                    gs.reset_game()                         # Reset the game
                    gui.clear_animations()                  # Clear animations
                    gui.clear_clicks()                      # Clear clicks
                    gui.update_screen(gs)                   # Re-draw

        if len(gui.animations) == 0:                # Animating = False
            move = player1.get_move(gs) if gs.current_player == player1.get_color() else player2.get_move(gs)
            if move is not None:                        # If a move can be made
                gui.store_animation(move)
                gs.make_move(move)
                gs.switch_turn()

            if len(gui.clicks) == 2:                    # If a click-move is ready
                if gs.current_player == player1.color and isinstance(player1, Player.HumanPlayer):
                    player1.move_prepared = gui.clicks
                elif gs.current_player == player2.color and isinstance(player2, Player.HumanPlayer):
                    player2.move_prepared = gui.clicks
                gui.clear_clicks()
                gui.update_screen(gs)
        else:                                       # Animating = True
            gui.update_animations()
            gui.update_screen(gs)

        clock.tick(Gui.MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()
