import pygame as pg
import sys
import map
from player import *
from repairCenter import RepairCenter

class Game:
    def __init__(self):
        pg.display.init()
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        
        self.player = Player()
        self.main_map = map.Map('tsx/CastleMap.tmx',
                                self.player, (1194, 666))
        self.current_map = self.main_map
        self.current_map.update_player_info()
        self.delta_time = 1
        self.repair_center = RepairCenter(Player())
        self.shop = False
        self.run()
        
    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(60)
        pg.display.set_caption(f"FPS: {self.clock.get_fps()}")

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
    
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            if pg.key.get_pressed()[pg.K_p]:
                self.shop = not self.shop
            if self.shop:
                self.repair_center.display()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.current_map.run()


if __name__ == "__main__":
    game = Game()
    