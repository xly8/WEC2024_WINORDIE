import pygame
import random
import time
import math

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, target=(1952, 1024)):
        super().__init__()
        self.image = pygame.image.load("Resources/AsteroidImages/explode1.png")
        self.rect = self.image.get_rect(center=pos)
        self.health = 20
        self.speed = 2
        self.target = target  # Destination coordinates (2080, 1168)
        self.is_dying = False  # Track if asteroid is in the dying state

        # Calculate the direction vector to the target
        self.direction = pygame.math.Vector2(self.target) - pygame.math.Vector2(self.rect.center)
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()  # Normalize to unit vector

        # Animation variables
        self.asteroid_dying = self.load_asteroid_images()
        self.animation_index = 0
        self.last_update = time.time()
        self.animation_speed = 0.1

    def load_asteroid_images(self):
        """Load explosion images for the asteroid death animation."""
        return [
            pygame.image.load(f"Resources/AsteroidImages/explode{i}.png")
            for i in range(1, 8)
        ]

    def update(self):
        """Update asteroid position or play explosion animation if dying."""
        if self.health > 0 and not self.is_dying:
            self.move()
        else:
            self.animate()
    
    def move(self):
        """Move the asteroid toward the target."""
        # Calculate the distance to the target to ensure it stops upon reaching
        current_position = pygame.math.Vector2(self.rect.center)
        target_position = pygame.math.Vector2(self.target)
        distance_to_target = current_position.distance_to(target_position)

        # Check if the asteroid is close enough to the target
        if distance_to_target < self.speed:
            # Snap to the target position and stop moving
            self.rect.center = self.target
            self.take_damage(20)
            return

        # Update the asteroid's position by moving along the normalized direction vector
        move_vector = (target_position - current_position).normalize() * self.speed
        self.rect.centerx += move_vector.x
        self.rect.centery += move_vector.y

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

    def draw(self, screen):
        """Draw the asteroid or its explosion animation on the screen."""
        screen.blit(self.image, self.rect)
