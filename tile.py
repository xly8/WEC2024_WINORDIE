import pygame as pg
import sys

class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups, surface=pg.Surface((16, 16))):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -8)