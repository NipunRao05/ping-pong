import pygame
import os
from game.paddle import Paddle
from game.ball import Ball

class GameEngine:
    """Main game engine that manages game state and logic"""
    
    def __init__(self, screen_width, screen_height):
        """
        Initialize game engine
        
        Args:
            screen_width: Width of game window
            screen_height: Height of game window
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Ping Pong Game")
        
        # Initialize game objects
        self.player_paddle = Paddle(30, screen_height // 2 - 60, 10, 120, 6)
        self.ai_paddle = Paddle(screen_width - 40, screen_height // 2 - 60, 10, 120, 5)
        self.ball = Ball(screen_width // 2, screen_height // 2, 10, 5)
        
        # Score tracking
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5
        
        # Game state
        self.game_over = False
        self.winner = None
        
        # Clock for frame rate
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Load sound effects
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects for the game"""
        try:
            # Try to load sound files from sounds directory
            self.paddle_hit_sound = pygame.mixer.Sound('sounds/paddle_hit.wav')
            self.wall_bounce_sound = pygame.mixer.Sound('sounds/wall_bounce.wav')
            self.score_sound = pygame.mixer.Sound('sounds/score.wav')
            
            # Set volumes higher (0.0 to 1.0) - INCREASED VOLUMES
            self.paddle_hit_sound.set_volume(1.0)  # Maximum volume
            self.wall_bounce_sound.set_volume(0.8)  # High volume
            self.score_sound.set_volume(1.0)  # Maximum volume
            
            # Set mixer volume (additional boost)
            pygame.mixer.music.set_volume(1.0)
            
            print("Sound effects loaded successfully!")
            print(f"Paddle hit volume: {self.paddle_hit_sound.get_volume()}")
            print(f"Wall bounce volume: {self.wall_bounce_sound.get_volume()}")
            print(f"Score volume: {self.score_sound.get_volume()}")
        except Exception as e:
            # If sounds can't be loaded, create placeholder
            print(f"Could not load sound files: {e}")
            print("Game will run without sound effects.")
            self.paddle_hit_sound = None
            self.wall_bounce_sound = None
            self.score_sound = None
    
    def play_sound(self, sound):
        """
        Play a sound effect if it exists
        
        Args:
            sound: pygame.mixer.Sound object to play
        """
        if sound is not None:
            # Stop any previous instance and play fresh
            sound.stop()
            channel = sound.play()
            if channel:
                channel.set_volume(1.0)  # Ensure channel volume is maximum
    
    def check_paddle_collision(self, paddle):
        """
        Enhanced collision detection with position correction
        
        Args:
            paddle: Paddle object to check collision with
            
        Returns:
            bool: True if collision occurred
        """
        ball_rect = self.ball.get_rect()
        paddle_rect = paddle.get_rect()
        
        if ball_rect.colliderect(paddle_rect):
            # Determine which side of paddle was hit
            ball_center_x = self.ball.x
            paddle_center_x = paddle.x + paddle.width / 2
            
            # Reverse horizontal velocity
            self.ball.velocity_x = -self.ball.velocity_x
            
            # Position correction to prevent ball getting stuck
            if ball_center_x < paddle_center_x:
                # Ball hit from left side
                self.ball.x = paddle.x - self.ball.radius
            else:
                # Ball hit from right side
                self.ball.x = paddle.x + paddle.width + self.ball.radius
            
            # Play paddle hit sound
            self.play_sound(self.paddle_hit_sound)
            print("Paddle hit sound played")  # Debug message
            
            return True
        return False
    
    def check_wall_bounce(self):
        """Check collision with top and bottom walls"""
        if self.ball.y - self.ball.radius <= 0 or self.ball.y + self.ball.radius >= self.screen_height:
            self.ball.velocity_y *= -1
            
            # Position correction
            if self.ball.y - self.ball.radius <= 0:
                self.ball.y = self.ball.radius
            else:
                self.ball.y = self.screen_height - self.ball.radius
            
            # Play paddle hit sound (changed from wall_bounce_sound)
            self.play_sound(self.paddle_hit_sound)
            print("Wall bounce sound played (using paddle hit)")  # Debug message
    
    def check_score(self):
        """Check if ball passed paddle (scoring)"""
        if self.ball.x - self.ball.radius <= 0:
            self.ai_score += 1
            # Play score sound
            self.play_sound(self.score_sound)
            print("Score sound played (AI scored)")  # Debug message
            self.check_game_over()
            if not self.game_over:
                # Add delay to hear the sound
                pygame.time.delay(200)
                self.ball.reset(self.screen_width, self.screen_height)
        elif self.ball.x + self.ball.radius >= self.screen_width:
            self.player_score += 1
            # Play score sound
            self.play_sound(self.score_sound)
            print("Score sound played (Player scored)")  # Debug message
            self.check_game_over()
            if not self.game_over:
                # Add delay to hear the sound
                pygame.time.delay(200)
                self.ball.reset(self.screen_width, self.screen_height)
    
    def check_game_over(self):
        """Check if either player has reached winning score"""
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player"
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner = "AI"
    
    def display_game_over(self):
        """Display game over screen once, then wait for replay input."""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 100)
        font_medium = pygame.font.Font(None, 50)
        font_small = pygame.font.Font(None, 40)

        winner_text = font_large.render(f"{self.winner} Wins!", True, (255, 255, 0))
        winner_rect = winner_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 150))
        self.screen.blit(winner_text, winner_rect)

        score_text = font_medium.render(f"Final Score: {self.player_score} - {self.ai_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 70))
        self.screen.blit(score_text, score_rect)

        replay_title = font_medium.render("Play Again?", True, (255, 255, 255))
        replay_title_rect = replay_title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 10))
        self.screen.blit(replay_title, replay_title_rect)

        option1_text = font_small.render("Press 3 - Best of 3", True, (0, 255, 0))
        option2_text = font_small.render("Press 5 - Best of 5", True, (0, 255, 255))
        option3_text = font_small.render("Press 7 - Best of 7", True, (255, 165, 0))
        exit_text = font_small.render("Press ESC - Exit Game", True, (255, 100, 100))

        self.screen.blit(option1_text, option1_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 70)))
        self.screen.blit(option2_text, option2_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 115)))
        self.screen.blit(option3_text, option3_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 160)))
        self.screen.blit(exit_text, exit_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 210)))

        pygame.display.flip()

        # Wait for replay input here (only once, not in main loop)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.reset_game(2)
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.reset_game(3)
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.reset_game(4)
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            self.clock.tick(15)  # Limit frame rate to reduce flicker
        
    def reset_game(self, new_winning_score):
        """
        Reset game to initial state with new winning score
        
        Args:
            new_winning_score: New score required to win
        """
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.winning_score = new_winning_score
        
        # Reset paddle positions
        self.player_paddle.y = self.screen_height // 2 - 60
        self.ai_paddle.y = self.screen_height // 2 - 60
        
        # Reset ball
        self.ball.x = self.screen_width // 2
        self.ball.y = self.screen_height // 2
        self.ball.velocity_x = self.ball.speed
        self.ball.velocity_y = self.ball.speed
    
    def update_ai(self):
        """Simple AI logic for computer paddle"""
        if self.ball.y > self.ai_paddle.y + self.ai_paddle.height / 2:
            self.ai_paddle.move_down(self.screen_height)
        elif self.ball.y < self.ai_paddle.y + self.ai_paddle.height / 2:
            self.ai_paddle.move_up()
    
    def update(self):
        """Update all game objects"""
        if not self.game_over:
            # Update ball position
            self.ball.update()
            
            # Check wall bounces (top and bottom) - with sound
            self.check_wall_bounce()
            
            # Check paddle collisions - with sound
            self.check_paddle_collision(self.player_paddle)
            self.check_paddle_collision(self.ai_paddle)
            
            # Check scoring - with sound
            self.check_score()
            
            # Update AI
            self.update_ai()
    
    def render(self):
        """Render all game objects"""
        self.screen.fill((0, 0, 0))
        
        # Draw center line
        for i in range(0, self.screen_height, 20):
            pygame.draw.rect(self.screen, (255, 255, 255), 
                           (self.screen_width // 2 - 2, i, 4, 10))
        
        # Draw paddles and ball
        self.player_paddle.display(self.screen)
        self.ai_paddle.display(self.screen)
        self.ball.display(self.screen)
        
        # Draw scores
        font = pygame.font.Font(None, 74)
        player_text = font.render(str(self.player_score), True, (255, 255, 255))
        ai_text = font.render(str(self.ai_score), True, (255, 255, 255))
        self.screen.blit(player_text, (self.screen_width // 4, 20))
        self.screen.blit(ai_text, (3 * self.screen_width // 4, 20))
        
        # Display current game mode
        mode_font = pygame.font.Font(None, 30)
        mode_text = mode_font.render(f"First to {self.winning_score}", True, (150, 150, 150))
        mode_rect = mode_text.get_rect(center=(self.screen_width // 2, self.screen_height - 20))
        self.screen.blit(mode_text, mode_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.clock.tick(self.fps)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle replay options when game is over
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_3:
                            # Best of 3: First to 2 wins
                            self.reset_game(2)
                        elif event.key == pygame.K_5:
                            # Best of 5: First to 3 wins
                            self.reset_game(3)
                        elif event.key == pygame.K_7:
                            # Best of 7: First to 4 wins
                            self.reset_game(4)
                        elif event.key == pygame.K_ESCAPE:
                            running = False
            
            # Handle player input during gameplay
            if not self.game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.player_paddle.move_up()
                if keys[pygame.K_s]:
                    self.player_paddle.move_down(self.screen_height)
            
            # Update and render
            self.update()
            self.render()
            
            # Display game over screen if game ended
            if self.game_over:
                self.display_game_over()
        
        pygame.quit()
