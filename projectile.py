import pygame

class Projectile:
    def __init__(self, position):
        self.image = pygame.image.load("projectile.png")
        self.rect = self.image.get_rect(center=position)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
