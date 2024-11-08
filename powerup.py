import pygame
import random

class PowerUp:
    def __init__(self):
        self.image = pygame.image.load("powerup.png")
        self.rect = self.image.get_rect(center=(random.randint(0, 800), random.randint(0, 600)))
        self.type = random.choice(["health", "ammo", "shooting_speed", "projectile_count", "max_health", "max_ammo"])

    def apply(self, player):
        player.apply_power_up(self.type)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
