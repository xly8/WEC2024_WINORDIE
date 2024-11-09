import pygame as pg
import sys
import random
from pytmx import load_pygame
from tile import *
from asteroid import Asteroid
from ui import UI
from enemy import Enemy
import time
from spaceship import Spaceship

class Map:
    def __init__(self, directory, player, spaceship, in_ship, startpos):
        self.active = True
        self.in_ship = in_ship
        self.directory = directory
        self.player = player

        # Add invincibility attributes to player
        self.player.last_hit_time = time.time()
        self.player.invincibility_duration = 1.0  # 1 second invincibility
        self.spaceship = spaceship

        self.startpos = startpos
        self.tmx_data = load_pygame(directory)
        self.display_surface = pg.display.get_surface()

        # Initialize sprite groups
        self.asteroid_sprites = pg.sprite.Group()
        self.door_sprites = pg.sprite.Group()
        self.background_sprites = NoSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()
        self.ground_sprites = NoSortCameraGroup()
        self.ship_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.visible_sprites = YSortCameraGroup()

        self.visible_sprites.add(self.player)
        self.visible_sprites.add(self.spaceship)
        
      
        self.load_map()
        self.spawn_asteroids(5)
        self.enemy_num = 5
        self.spawn_enemies(self.enemy_num)
        self.ui = UI()

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
                elif layer.name == 'Star Background':
                    Tile(pos, self.background_sprites, surf)
                elif layer.name in ship_list:
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
        self.player.set_sprites(
            self.obstacle_sprites,
            self.door_sprites,
            self.ship_sprites,
            self.asteroid_sprites  # Include asteroid_sprites here
        )
    
    def run(self):
        if self.active:
            reference = self.spaceship if self.in_ship else self.player
            self.background_sprites.custom_draw(reference)
            self.ground_sprites.custom_draw(reference)
            self.visible_sprites.custom_draw(reference)
            self.obstacle_sprites.update()
            self.ground_sprites.update()
            self.visible_sprites.update()
            self.door_sprites.update()
            self.asteroid_sprites.update()

            # Update enemies and player collisions
            self.update_enemies()
            self.ui.display(self.player)
            
    def spawn_asteroids(self, count):
        for _ in range(count):
            pos = (random.randint(0, 1280), random.randint(0, 720))
            asteroid = Asteroid(pos)
            self.asteroid_sprites.add(asteroid)
            self.visible_sprites.add(asteroid)
    
    def spawn_enemies(self, count):
        """Spawn a number of enemies at random edge positions"""
        for _ in range(count):
            enemy = Enemy(
                monster_name='enemy1',
                groups=[self.visible_sprites, self.enemy_sprites],
                obstacle_sprites=self.obstacle_sprites
            )
            self.enemy_sprites.add(enemy)


    def update_enemies(self):
        """Update all enemies with player position and handle collision."""
        current_time = time.time()
        for enemy in self.enemy_sprites:
            enemy.update(self.player.rect.center, self.player)

            # Collision detection with player
            if enemy.hitbox.colliderect(self.player.hitbox):
                if current_time - self.player.last_hit_time >= self.player.invincibility_duration:
                    self.player.health -= enemy.damage
                    self.player.last_hit_time = current_time
                    print(f"Player hit! Health: {self.player.health}")

                    # Check for game over
                    if self.player.health <= 0:
                        print("Game over!")                        
            
    def collide_asteroids(self):
        for asteroid in self.asteroid_sprites:
            if asteroid.hitbox.colliderect(self.player.hitbox):
                self.player.health -= 1
                asteroid.take_damage(5)
                if asteroid.health <= 0:
                    asteroid.kill()

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
