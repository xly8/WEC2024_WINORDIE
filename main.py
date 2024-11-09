import pygame as pg
import sys
import map
from player import *  # Keep the original player if needed
from repairCenter import RepairCenter
from spaceship import Spaceship, Bullet  # Import your spaceship and bullet classes

class Game:
    def __init__(self):
        pg.display.init()
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        self.in_ship = False
        # Initialize Spaceship in addition to Player, if keeping both
        self.player = Player()  # Keep this if needed
        self.spaceship = Spaceship()
        self.main_map = map.Map(
            directory='tsx/CastleMap.tmx',
            player=self.player,
            spaceship=self.spaceship,  # Add spaceship parameter
            in_ship=self.in_ship,
            startpos=(1194, 666)
        )
        self.current_map = self.main_map
        self.current_map.update_player_info()
        self.delta_time = 1
        self.repair_center = RepairCenter(Player())
        self.shop = False
        self.run()
        
    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(60) / 1000  # in seconds for smooth animation
        pg.display.set_caption(f"FPS: {self.clock.get_fps()}")

        # Update Spaceship and Bullets

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # Fire bullet from spaceship
                    bullet = self.spaceship.shoot()
                    self.bullets.add(bullet)
                    
                # Toggle the shop as in the original functionality
                elif event.key == pg.K_p:
                    self.shop = not self.shop
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.current_map.run()
        
        # Draw the spaceship and bullets
        
        # Display shop if active
        if self.shop:
            self.repair_center.display()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()

# Main game execution
if __name__ == "__main__":
    game = Game()