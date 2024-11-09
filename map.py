import pygame as pg
import sys
import random
from pytmx import load_pygame
from tile import *


class Map:
    def __init__(self, directory, player, startpos):
        self.active = True
        self.directory = directory
        self.player = player
        self.startpos = startpos
        self.tmx_data = load_pygame(directory)
        self.display_surface = pg.display.get_surface()
        self.door_sprites = pg.sprite.Group()
        self.background_sprites = NoSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()
        self.ground_sprites = NoSortCameraGroup()
        self.ship_sprites = pg.sprite.Group()
        self.visible_sprites = YSortCameraGroup()
        self.visible_sprites.add(self.player)
        self.load_map()
        
    def load_map(self):
        for layer in self.tmx_data.visible_layers:
            ship_list = {'Ship'}
            ground_list = {'Ground', 'Carpet', 'Walkthrough objects'}
            object_list = {'Objects', 'Buildings', 'Walls', 'WallOutline', 'Decorations'}
            decor_list = {'WallDecor', 'Castle Decor'}
            for x, y, surf in layer.tiles():
                pos = (x * 16, y * 16)
                if layer.name == 'Doors':
                    Door(pos, (self.visible_sprites, self.door_sprites), surf)
                if layer.name == 'Star Background':
                    Tile(pos, self.background_sprites, surf)
                if layer.name in ship_list:
                    Tile(pos, (self.visible_sprites, self.ship_sprites), surf)
                elif layer.name in ground_list:
                    Tile(pos, self.ground_sprites, surf)
                elif layer.name in object_list:
                    Tile(pos, (self.visible_sprites, self.obstacle_sprites), surf)
                elif layer.name == 'Border':
                    Tile(pos, (self.visible_sprites, self.obstacle_sprites),
                         pg.image.load('Resources/blank.png'))
                elif layer.name in decor_list:
                    Tile(pos, self.visible_sprites, surf)
    
    def update_player_info(self, pos=0):
        self.player.set_sprites(self.obstacle_sprites,
                                self.door_sprites, self.ship_sprites)
    
    def run(self):
        if self.active:
            self.background_sprites.custom_draw(self.player)
            self.ground_sprites.custom_draw(self.player)
            self.visible_sprites.custom_draw(self.player)
            self.obstacle_sprites.update()
            self.ground_sprites.update()
            self.visible_sprites.update()
            self.door_sprites.update()
    

                

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
