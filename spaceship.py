import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800  # Increased screen size for better view

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)  # Color when accelerating
WHITE = (255, 255, 255)

# Player settings
MAX_SPEED = 1000           # Increase max speed for better control
ACCELERATION = 100        # High acceleration for instant feedback
FRICTION = 0.01         # Reduced friction for slower deceleration
ROTATION_SPEED = 200    # Degrees per second for rotation
BULLET_SPEED = 400      # Speed of the bullet

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()
        self.image = pygame.Surface((10, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.image, WHITE, (0, 0, 10, 4))
        
        # Rotate bullet image to match player's angle
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=position)

        # Set movement direction based on angle
        radian_angle = math.radians(angle)
        self.velocity = pygame.Vector2(math.cos(radian_angle), math.sin(radian_angle)) * BULLET_SPEED

    def update(self, delta_time):
        # Move the bullet
        self.rect.center += self.velocity * delta_time
        
        # Remove the bullet if it goes off screen
        if not (0 <= self.rect.x <= WIDTH) or not (0 <= self.rect.y <= HEIGHT):
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, start_position):
        super().__init__()
        
        # Original image (a pointy arrow pointing right by default)
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, BLUE, [(50, 25), (0, 5), (0, 45)])  # Pointy arrow shape pointing right
        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_position)
        
        # Initial attributes
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)  # Default direction vector
        self.momentum = pygame.Vector2(0, 0)   # Momentum vector for smooth movement
        self.position = pygame.Vector2(start_position)  # Use floating-point position for smoother movement

    def rotate(self, direction, delta_time):
        """Rotates the player."""
        if direction == "left":  # Counterclockwise rotation
            self.angle -= ROTATION_SPEED * delta_time
        elif direction == "right":  # Clockwise rotation
            self.angle += ROTATION_SPEED * delta_time

        # Update the rotated image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.position)  # Update rect based on floating-point position

    def accelerate(self, delta_time):
        """Accelerates the player forward by adding to momentum."""
        radian_angle = math.radians(self.angle)
        new_direction = pygame.Vector2(math.cos(radian_angle), math.sin(radian_angle))

        # Apply acceleration in the current direction without resetting previous momentum
        self.momentum += new_direction * ACCELERATION * delta_time
        
        # Limit momentum to MAX_SPEED for both x and y combined
        if self.momentum.length() > MAX_SPEED:
            self.momentum.scale_to_length(MAX_SPEED)

    def apply_friction(self):
        """Applies friction to reduce momentum gradually."""
        if self.momentum.length() > 0:
            self.momentum *= (1 - FRICTION)  # Reduce momentum by friction rate
            if self.momentum.length() < 0.05:  # Stop small residual motion
                self.momentum = pygame.Vector2(0, 0)

    def shoot(self):
        """Creates a bullet traveling in the current facing direction."""
        return Bullet(self.rect.center, self.angle)

    def update(self, delta_time, keys):
        """Updates player movement and rotation based on keys pressed."""
        if keys[pygame.K_a]:  # Rotate counterclockwise
            self.rotate("left", delta_time)
        if keys[pygame.K_d]:  # Rotate clockwise
            self.rotate("right", delta_time)
        if keys[pygame.K_w]:  # Accelerate forward
            self.accelerate(delta_time)
            # Change color when moving forward
            self.original_image.fill((0, 0, 0, 0))  # Clear previous drawing
            pygame.draw.polygon(self.original_image, LIGHT_BLUE, [(50, 25), (0, 5), (0, 45)])
        else:
            # Set color back to default if not moving forward
            self.original_image.fill((0, 0, 0, 0))  # Clear previous drawing
            pygame.draw.polygon(self.original_image, BLUE, [(50, 25), (0, 5), (0, 45)])

        # Update image with current rotation and color
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.position)  # Update rect based on floating-point position

        # Apply friction to gradually slow down
        self.apply_friction()

        # Update floating-point position based on momentum
        self.position += self.momentum * delta_time

        # Update rect position based on rounded floating-point position for display
        self.rect.center = (round(self.position.x), round(self.position.y))

        # Keep the player on screen
        if self.rect.left < 0:
            self.position.x = self.rect.width // 2
        if self.rect.right > WIDTH:
            self.position.x = WIDTH - self.rect.width // 2
        if self.rect.top < 0:
            self.position.y = self.rect.height // 2
        if self.rect.bottom > HEIGHT:
            self.position.y = HEIGHT - self.rect.height // 2


class Game:
    def __init__(self):
        # Screen setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WASD Rotating Arrow with Shooting")
        self.clock = pygame.time.Clock()

        # Sprite setup
        self.player = Player(start_position=(WIDTH // 2, HEIGHT // 2))
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()  # Group to hold bullets
        
        # Running state
        self.running = True

    def handle_events(self):
        """Handles game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Shoot bullet
                    bullet = self.player.shoot()
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)

    def update(self, delta_time):
        """Updates all game elements."""
        keys = pygame.key.get_pressed()
        self.player.update(delta_time, keys)  # Only pass keys to player update
        self.bullets.update(delta_time)  # Only update bullets without keys

    def draw(self):
        """Draws all game elements to the screen."""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # Convert to seconds
            self.handle_events()
            self.update(delta_time)
            self.draw()
        
        pygame.quit()


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
