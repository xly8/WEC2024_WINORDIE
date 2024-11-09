import pygame
from projectile import Projectile
from player import Player

class Ship(Player):
    def __init__(self):
        super().__init__()
        self.projectiles = []

    def shoot(self):
        if self.ammo > 0:
            for _ in range(self.projectile_count):
                self.projectiles.append(Projectile(self.rect.center))
            self.ammo -= 1

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move(-self.move_speed, 0)
        if keys[pygame.K_d]:
            self.move(self.move_speed, 0)
        if keys[pygame.K_w]:
            self.move(0, self.move_speed)
        if keys[pygame.K_s]:
            self.move(0, -self.move_speed)
        if keys[pygame.K_SPACE]:
            self.shoot()

        for projectile in self.projectiles:
            projectile.update()

    def draw(self, screen):
        super().draw(screen)  # Use Player's draw method
        for projectile in self.projectiles:
            projectile.draw(screen)

    def apply_power_up(self, power_type):
        if power_type == "shooting_speed":
            self.shooting_speed = max(0.1, self.shooting_speed * 0.9)
        elif power_type == "health":
            self.health = min(self.health + 1, self.max_health)
        elif power_type == "ammo":
            self.ammo = min(self.ammo + 15, self.max_ammo)
        elif power_type == "move_speed":
            self.move_speed = min(self.move_speed + 1, 10)
