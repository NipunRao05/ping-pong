import pygame
from game.game_engine import GameEngine

def main():
    """Initialize and run the Ping Pong game"""
    pygame.init()
    
    # Screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    # Create game engine instance
    game = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Run the game
    game.run()

if __name__ == "__main__":
    main()
