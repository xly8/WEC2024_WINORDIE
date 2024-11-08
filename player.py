import pygame
from projectile import Projectile
import time
from spaceship import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Resources/AstronautImages/down1.png")
        self.rect = self.image.get_rect(center=(2080, 1168))
        self.direction = pygame.math.Vector2()
        self.stats = {"health": 3, "ammo": 50, "shooting_speed": 1, "projectile_count": 1, "max_health": 3, "max_ammo": 50, "speed": 4}
        self.upgrade_cost = {"health": 100, "ammo": 100, "shooting_speed": 100, "projectile_count": 100, "max_health": 100, "max_ammo": 100, "speed": 100}
        self.stats_level = {"health": 1, "ammo": 1, "shooting_speed": 1, "projectile_count": 1, "max_health": 1, "max_ammo": 1, "speed": 1}
        self.upgrade_stats = {"health": 1, "ammo": 15, "shooting_speed": 0.1, "projectile_count": 1, "max_health": 1, "max_ammo": 10, "speed": 1}
        self.upgrade_points = 1000
        self.max_stats = {"health": 10, "ammo": 100, "shooting_speed": 0.5, "projectile_count": 5, "max_health": 10, "max_ammo": 100, "speed": 10}
        self.speed = self.stats["speed"]
        self.is_ship = False
        self.hitbox = self.rect.inflate(-35, -20)
        self.current_room = 0
        self.obstacle_sprites = None
        self.door_sprites = None
        self.ship_sprites = None
        self.asteroid_sprites = None
        self.health = self.stats["health"]
        self.max_health = self.stats["max_health"]
        self.ammo = self.stats["ammo"]
        self.max_ammo = self.stats["max_ammo"]
        self.projectiles = []
        self.shooting_speed = self.stats["shooting_speed"]
        self.projectile_count = self.stats["projectile_count"]
        self.score = 0
        self.last_damage_time = time.time()
        self.damage_interval = 1  # Time (in seconds) between damage

        # Animation settings
        self.animation_index = 0
        self.animation_speed = 0.08
        self.last_update = time.time()
        self.facing = 'down'  # Default facing direction
        self.ship_up = self.load_ship_images()
        self.ship_down = self.rotate_images(self.ship_up, 180)
        self.ship_left = self.rotate_images(self.ship_up, 90)
        self.ship_right = self.rotate_images(self.ship_up, 270)
        self.walk_left = self.load_walk_images('left')
        self.walk_right = self.load_walk_images('right')
        self.walk_up = self.load_walk_images('up')
        self.walk_down = self.load_walk_images('down')


    def load_walk_images(self, direction):
        return [
            pygame.image.load(f"Resources/AstronautImages/{direction}{i}.png")
            for i in range(1, 5)
        ]
    
    def rotate_images(self, images, angle):
        return [pygame.transform.rotate(image, angle) for image in images]
    
    def load_ship_images(self):
        images = [
            pygame.image.load(f"Resources/ShipImages/ship{i}.png")
            for i in range(1, 5)
        ]
        # Scale images to be bigger
        scale_factor = 2  # Adjust this factor as needed
        return [pygame.transform.scale(image, (image.get_width() * scale_factor, image.get_height() * scale_factor)) for image in images]

    def set_sprites(self, obstacle_sprites, door_sprites, ship_sprites, asteroid_sprites):
        self.obstacle_sprites = obstacle_sprites
        self.door_sprites = door_sprites
        self.ship_sprites = ship_sprites
        self.asteroid_sprites = asteroid_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        # Reset direction
        self.direction = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.facing = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.facing = 'down'

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = 'right'
        else:
            self.direction.x = 0
                  

    def animate(self):
        current_time = time.time()
        if current_time - self.last_update > self.animation_speed:
            self.animation_index = (self.animation_index + 1) % 4
            self.last_update = current_time
            if self.is_ship:
                # Update ship animation for facing direction, including diagonals
                if self.direction.x > 0 and self.direction.y < 0:  # Up-Right
                    self.image = pygame.transform.rotate(self.ship_up[self.animation_index], -45)
                elif self.direction.x > 0 and self.direction.y > 0:  # Down-Right
                    self.image = pygame.transform.rotate(self.ship_down[self.animation_index], 45)
                elif self.direction.x < 0 and self.direction.y < 0:  # Up-Left
                    self.image = pygame.transform.rotate(self.ship_up[self.animation_index], 45)
                elif self.direction.x < 0 and self.direction.y > 0:  # Down-Left
                    self.image = pygame.transform.rotate(self.ship_down[self.animation_index], -45)
                else:
                    # Set straight directions
                    if self.facing == 'left':
                        self.image = self.ship_left[self.animation_index]
                    elif self.facing == 'right':
                        self.image = self.ship_right[self.animation_index]
                    elif self.facing == 'up':
                        self.image = self.ship_up[self.animation_index]
                    elif self.facing == 'down':
                        self.image = self.ship_down[self.animation_index]
            else:
                # Regular astronaut animation
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
            self.stats["max_health"] += 1
            self.max_health = self.stats["max_health"]
        elif power_type == "max_ammo":
            self.max_ammo += 10
        print(self.max_health)

    def collision(self, direction):
        current_time = time.time()
        if direction == 'h':
            for sprite in self.obstacle_sprites:
                if not self.is_ship:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
        if direction == 'v':
            for sprite in self.obstacle_sprites:
                if not self.is_ship:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
        for sprite in self.door_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.door_name == 'Merchant':
                    self.current_room = 0
        for sprite in self.ship_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if not self.is_ship:
                    self.is_ship = True
        for sprite in self.asteroid_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                print("touching asteroid")
                self.health -= 1
                sprite.take_damage(5)

    def update(self):
        self.input()
        self.move()
        if self.direction.magnitude() > 0:
            self.animate()
        for projectile in self.projectiles:
            projectile.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def get_level_by_index(self, index):
        return list(self.stats_level.values())[index]
