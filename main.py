import pygame as pg
import sys


class Game:
    def __init__(self):
        pg.display.init()
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        self.delta_time = 1
        
    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(60)
        pg.display.set_caption(f"FPS: {self.clock.get_fps()}")
    
    def run(self):
        while True:
            self.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
    def draw(self):
        pass

if __name__ == "__main__":
    game = Game()
    