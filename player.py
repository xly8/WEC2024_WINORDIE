import pygame 
from projectile import Projectile
import time

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Resources/AstronautImages/down1.png")
        self.rect = self.image.get_rect(center=(2080, 1168))
        self.health = 3
        self.max_health = 3
        self.ammo = 50
        self.max_ammo = 50
        self.projectiles = []
        self.shooting_speed = 1
        self.projectile_count = 1

        # Character Animation settings
        self.last_pressed_key = None
        self.pressed_keys = set()
        self.animation_index = 0
        self.animation_speed = 0.08
        self.last_update = time.time()
        self.facing = 'down'  # default facing direction
        self.walk_left = [
            pygame.image.load("Resources/AstronautImages/left1.png"),
            pygame.image.load("Resources/AstronautImages/left2.png"),
            pygame.image.load("Resources/AstronautImages/left3.png"),
            pygame.image.load("Resources/AstronautImages/left4.png")
        ]
        self.walk_right = [
            pygame.image.load("Resources/AstronautImages/right1.png"),
            pygame.image.load("Resources/AstronautImages/right2.png"),
            pygame.image.load("Resources/AstronautImages/right3.png"),
            pygame.image.load("Resources/AstronautImages/right4.png")
        ]
        self.walk_up = [
            pygame.image.load("Resources/AstronautImages/up1.png"),
            pygame.image.load("Resources/AstronautImages/up2.png"),
            pygame.image.load("Resources/AstronautImages/up3.png"),
            pygame.image.load("Resources/AstronautImages/up4.png")
        ]
        self.walk_down = [
            pygame.image.load("Resources/AstronautImages/down1.png"),
            pygame.image.load("Resources/AstronautImages/down2.png"),
            pygame.image.load("Resources/AstronautImages/down3.png"),
            pygame.image.load("Resources/AstronautImages/down4.png")
        ]
    
    def set_sprites(self, obstacle_sprites, door_sprites):
        self.obstacle_sprites = obstacle_sprites
        self.door_sprites = door_sprites

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

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.ammo > 0:
            for _ in range(self.projectile_count):
                self.projectiles.append(Projectile(self.rect.center))
            self.ammo -= 1

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False
        
        # Track key presses and releases
        for key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
            if keys[key]:
                if key not in self.pressed_keys:
                    self.last_pressed_key = key
                    self.pressed_keys.add(key)
            else:
                self.pressed_keys.discard(key)
                if key == self.last_pressed_key:
                    self.last_pressed_key = None if not self.pressed_keys else list(self.pressed_keys)[-1]

        # Move based on last pressed key
        if self.last_pressed_key == pygame.K_a:
            self.move(-5, 0)
            self.facing = 'left'
            moving = True
        elif self.last_pressed_key == pygame.K_d:
            self.move(5, 0)
            self.facing = 'right'
            moving = True
        elif self.last_pressed_key == pygame.K_w:
            self.move(0, -5)
            self.facing = 'up'
            moving = True
        elif self.last_pressed_key == pygame.K_s:
            self.move(0, 5)
            self.facing = 'down'
            moving = True

        # Shooting
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Animation handling
        if moving:
            self.animate()
        else:
            # Reset to standing frame
            if self.facing == 'left':
                self.image = self.walk_left[0]
            elif self.facing == 'right':
                self.image = self.walk_right[0]
            elif self.facing == 'up':
                self.image = self.walk_up[0]
            elif self.facing == 'down':
                self.image = self.walk_down[0]

        for projectile in self.projectiles:
            projectile.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for projectile in self.projectiles:
            projectile.draw(screen)
            
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