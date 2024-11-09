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
        if keys[pygame.K_a]:
            self.move(-5, 0)
        if keys[pygame.K_d]:
            self.move(5, 0)
        if keys[pygame.K_w]:
            self.move(0, -5)
        if keys[pygame.K_s]:
            self.move(0, 5)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
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