import pygame as pg
import sys
import random
from pytmx import load_pygame
from tile import *


class Map:
    def __init__(self, directory, player, startpos):
        self.directory = directory
        self.player = player
        self.startpos = startpos
        self.tmx_data = load_pygame(directory)
        self.background_sprites = NoSortCameraGroup()
        self.load_map()
        
    def load_map(self):
        for layer in self.tmx_data.visible_layers:
            space_list = {'Space'}
            object_list = {'Walls', "Objects"}
            decor_list = {'Stars'}
            for x, y, surf in layer.tiles():
                pos = (x * 16, y * 16)
                if layer.name in space_list:
                    Tile(pos, self.background_sprites, surf)

                

class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)



class NoSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
