import pygame
from projectile import Projectile
import time

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Resources/AstronautImages/down1.png")
        self.rect = self.image.get_rect(center=(2080, 1168))
        self.direction = pygame.math.Vector2()
        self.speed = 4
        self.hitbox = self.rect.inflate(-35, -20)
        self.current_room = 0
        self.obstacle_sprites = None
        self.door_sprites = None
        self.health = 3
        self.max_health = 3
        self.ammo = 50
        self.max_ammo = 50
        self.projectiles = []
        self.shooting_speed = 1
        self.projectile_count = 1

        # Animation settings
        self.last_pressed_key = None
        self.pressed_keys = set()
        self.animation_index = 0
        self.animation_speed = 0.08
        self.last_update = time.time()
        self.facing = 'down'  # default facing direction
        self.walk_left = self.load_walk_images('left')
        self.walk_right = self.load_walk_images('right')
        self.walk_up = self.load_walk_images('up')
        self.walk_down = self.load_walk_images('down')

    def load_walk_images(self, direction):
        return [
            pygame.image.load(f"Resources/AstronautImages/{direction}{i}.png")
            for i in range(1, 5)
        ]

    def set_sprites(self, obstacle_sprites, door_sprites):
        self.obstacle_sprites = obstacle_sprites
        self.door_sprites = door_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.facing = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.facing = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.shoot()

    def animate(self):
        current_time = time.time()
        if current_time - self.last_update > self.animation_speed:
            self.animation_index = (self.animation_index + 1) % 4
            self.last_update = current_time
            if self.facing == 'left':
                self.image = self.walk_left[self.animation_index]
            elif self.facing == 'right':
                self.image = self.walk_right[self.animation_index]
            elif self.facing == 'up':
                self.image = self.walk_up[self.animation_index]
            elif self.facing == 'down':
                self.image = self.walk_down[self.animation_index]

    def move(self):
        self.hitbox.x += self.direction.x * self.speed
        self.collision('h')
        self.hitbox.y += self.direction.y * self.speed
        self.collision('v')
        self.rect.center = self.hitbox.center

    def shoot(self):
        if self.ammo > 0:
            for _ in range(self.projectile_count):
                self.projectiles.append(Projectile(self.rect.center))
            self.ammo -= 1

    def apply_power_up(self, power_type):
        if power_type == "shooting_speed":
            self.shooting_speed = max(0.1, self.shooting_speed * 0.9)
        elif power_type == "projectile_count":
            self.projectile_count += 1
        elif power_type == "health":
            self.health = min(self.health + 1, self.max_health)
        elif power_type == "ammo":
            self.ammo = min(self.ammo + 15, self.max_ammo)
        elif power_type == "max_health":
            self.max_health += 1
        elif power_type == "max_ammo":
            self.max_ammo += 10

    def collision(self, direction):
        if direction == 'h':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'v':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
        for sprite in self.door_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.door_name == 'Merchant':
                    self.current_room = 0

    def update(self):
        self.input()
        self.move()
        if self.direction.magnitude() > 0:
            self.animate()
        for projectile in self.projectiles:
            projectile.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for projectile in self.projectiles:
            projectile.draw(screen)
