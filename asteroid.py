import pygame
import random
import time
import math

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, target=(1952, 1024)):
        super().__init__()
        self.image = pygame.image.load("Resources/AsteroidImages/explode1.png")
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.health = 10
        self.speed = 0.5
        self.target = target
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
        
        # Timer for speed increase
        self.last_speed_increase = time.time()  # Track when the speed was last increased
        self.speed_increase_interval = 10  # Seconds

    def load_asteroid_images(self):
        """Load explosion images for the asteroid death animation."""
        return [
            pygame.image.load(f"Resources/AsteroidImages/explode{i}.png")
            for i in range(1, 8)
        ]

    def update(self):
        """Update asteroid position or play explosion animation if dying."""
        if self.health > 0 and not self.is_dying:
            self.increase_speed_over_time()
            self.move()
        else:
            self.animate()
            
    def increase_speed_over_time(self):
        """Increase speed by 1 every 30 seconds."""
        current_time = time.time()
        if current_time - self.last_speed_increase >= self.speed_increase_interval:
            self.speed += 0.5  # Increase speed by 0.5
            self.last_speed_increase = current_time  # Reset the timer
            print(f"Asteroid speed increased to: {self.speed}")
    
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
            self.take_damage(10)
            return

        # Update the asteroid's position by moving along the normalized direction vector
        move_vector = (target_position - current_position).normalize() * self.speed
        self.rect.centerx += move_vector.x
        self.rect.centery += move_vector.y
        
        self.hitbox.center = self.rect.center

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
                self.hitbox = pygame.Rect(0, 0, 0, 0)
            else:
                self.kill()

    def draw(self, screen):
        """Draw the asteroid or its explosion animation on the screen."""
        screen.blit(self.image, self.rect)
