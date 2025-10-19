import pygame

class Ball:
    """Represents the ball in the ping pong game"""
    
    def __init__(self, x, y, radius, speed):
        """
        Initialize ball
        
        Args:
            x: X position
            y: Y position
            radius: Ball radius
            speed: Ball speed
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.velocity_x = speed
        self.velocity_y = speed
        self.color = (255, 255, 255)
    
    def update(self):
        """Update ball position"""
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def check_wall_bounce(self, screen_height):
        """
        Check and handle bouncing off top and bottom walls
        
        Args:
            screen_height: Height of the game window
        """
        # Check top boundary
        if self.y - self.radius <= 0:
            self.velocity_y *= -1
            self.y = self.radius  # Position correction
        
        # Check bottom boundary
        elif self.y + self.radius >= screen_height:
            self.velocity_y *= -1
            self.y = screen_height - self.radius  # Position correction
    
    def display(self, screen):
        """Render ball on screen"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def get_rect(self):
        """Return rectangle for collision detection"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def reset(self, screen_width, screen_height):
        """Reset ball to center and reverse direction"""
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.velocity_x = -self.velocity_x
