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

    def set_sprites(self, obstacle_sprites, door_sprites):
        self.obstacle_sprites = obstacle_sprites
        self.door_sprites = door_sprites

    def input(self):
        # gets the key inputs from the pygame module and stores it in a variable
        keys = pygame.key.get_pressed()
        # changes the direction of the player based on the key pressed
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
            # resets direction to 0 if no key is currently being pressed
        else:
            self.direction.y = 0
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
        

    def move(self):
        self.hitbox.x += self.direction.x * self.speed
        self.collision('h')
        self.hitbox.y += self.direction.y * self.speed
        self.collision('v')
        self.rect.center = self.hitbox.center
        
    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]
    def get_level_by_index(self, index):
        return list(self.stats.values())[index]

    def update(self):
        self.input()
        self.move()
        
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
    
    def collision(self, direction):
        # collision detection method with one argument for vertical and horizontal
        if direction == 'h':
            # checks if there is any collisions with the sprite if it is moving horizontally
            # if so, depending on the direction will move the player to left or right of obstacle
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        # same concept as above but for the vertical collisions
        if direction == 'v':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
        for sprite in self.door_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.door_name == 'Merchant':
                    self.current_room = 0
        
