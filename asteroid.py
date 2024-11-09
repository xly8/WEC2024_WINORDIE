import pygame
import random
import time

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Resources/AsteroidImages/explode1.png")
        self.rect = self.image.get_rect(center=pos)
        self.health = 20
        self.speed = 2
        self.asteroid_dying = self.load_asteroid_images()  # Load explosion images
        self.is_dying = False  # Track if asteroid is in the dying state
        self.animation_index = 0  # Track the current frame of animation
        self.last_update = time.time()  # Track the last time the frame was updated
        self.animation_speed = 0.1  # Control the speed of the animation (seconds between frames)

    def load_asteroid_images(self):
        """Load explosion images for the asteroid death animation."""
        return [
            pygame.image.load(f"Resources/AsteroidImages/explode{i}.png")
            for i in range(1, 8)
        ]

    def update(self):
        """Update asteroid position or play explosion animation if dying."""
        if not self.is_dying:
            self.move()
        else:
            self.animate()
    
    def move(self):
        """Move the asteroid to the left and remove it when off screen."""
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

    def take_damage(self, amount):
        """Reduce health by the specified amount and trigger death if health <= 0."""
        self.health -= amount
        if self.health <= 0 and not self.is_dying:
            self.is_dying = True  # Start the explosion animation

    def animate(self):
        """Animate the explosion frames and remove asteroid when done."""
        current_time = time.time()
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            if self.animation_index < len(self.asteroid_dying) - 1:
                # Advance to the next explosion frame
                self.animation_index += 1
                self.image = self.asteroid_dying[self.animation_index]
            else:
                self.kill()

    def kill(self):
        """Handle the removal of the asteroid from the game."""
        # Placeholder for removal logic: remove from game lists or groups
        pass

    def draw(self, screen):
        """Draw the asteroid or its explosion animation on the screen."""
        screen.blit(self.image, self.rect)