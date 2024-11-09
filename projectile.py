import pygame

class Projectile:
    def __init__(self, position):
        self.image = pygame.image.load("Resources/WeaponImages/FirstWeapon.png")
        self.rect = self.image.get_rect(center=position)
        self.speed = -10

    def update(self):
        # self.rect.y += self.speed
        pass

    def draw(self, screen):
        # screen.blit(self.image, self.rect)
        pass