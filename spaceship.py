import pygame
import math
import time

# Constants
MAX_SPEED = 1000
ACCELERATION = 100
FRICTION = 0.01
ROTATION_SPEED = 200
BULLET_SPEED = 400

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()
        self.image = pygame.Surface((10, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 10, 4))
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=position)

        radian_angle = math.radians(angle)
        self.velocity = pygame.Vector2(math.cos(radian_angle), math.sin(radian_angle)) * BULLET_SPEED

    def update(self, delta_time):
        self.rect.center += self.velocity * delta_time
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, start_position):
        super().__init__()
        self.animation_frames = [
            pygame.image.load(f"Resources/ShipImages/ship{i}.png") for i in range(1, 5)
        ]
        self.animation_index = 0
        self.animation_speed = 0.08
        self.last_update = time.time()

        self.original_image = self.animation_frames[0]
        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_position)

        self.angle = 0
        self.direction = pygame.Vector2(0, -1)  # Initial direction is upward
        self.momentum = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(start_position)

        self.active = False  # Initially inactive

    def activate(self):
        self.active = True

    def animate(self):
        current_time = time.time()
        if current_time - self.last_update > self.animation_speed:
            self.animation_index = (self.animation_index + 1) % 4
            self.last_update = current_time
            self.original_image = self.animation_frames[self.animation_index]
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def rotate(self, direction, delta_time):
        if direction == "left":
            self.angle -= ROTATION_SPEED * delta_time
        elif direction == "right":
            self.angle += ROTATION_SPEED * delta_time

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def accelerate(self, delta_time):
        radian_angle = math.radians(self.angle)
        new_direction = pygame.Vector2(math.cos(radian_angle), math.sin(radian_angle))
        self.momentum += new_direction * ACCELERATION * delta_time
        if self.momentum.length() > MAX_SPEED:
            self.momentum.scale_to_length(MAX_SPEED)

    def apply_friction(self):
        if self.momentum.length() > 0:
            self.momentum *= (1 - FRICTION)
            if self.momentum.length() < 0.05:
                self.momentum = pygame.Vector2(0, 0)

    def shoot(self):
        return Bullet(self.rect.center, self.angle)

    def update(self, delta_time, keys=None):
        if not self.active:
            return
        
        self.animate()
        if keys and keys[pygame.K_a]:
            self.rotate("left", delta_time)
        if keys and keys[pygame.K_d]:
            self.rotate("right", delta_time)
        if keys and keys[pygame.K_w]:
            self.accelerate(delta_time)

        self.apply_friction()
        self.position += self.momentum * delta_time
        self.rect.center = (round(self.position.x), round(self.position.y))
