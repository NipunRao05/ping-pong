import pygame

class Paddle:
    """Represents a paddle in the ping pong game"""
    
    def __init__(self, x, y, width, height, speed):
        """
        Initialize paddle
        
        Args:
            x: X position
            y: Y position
            width: Paddle width
            height: Paddle height
            speed: Movement speed
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = (255, 255, 255)
    
    def move_up(self):
        """Move paddle up"""
        self.y -= self.speed
        if self.y < 0:
            self.y = 0
    
    def move_down(self, screen_height):
        """Move paddle down with boundary checking"""
        self.y += self.speed
        if self.y + self.height > screen_height:
            self.y = screen_height - self.height
    
    def display(self, screen):
        """Render paddle on screen"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        """Return rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
