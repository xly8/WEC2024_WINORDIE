import pygame as pg
import sys
import map
from player import *


class UI:
    def __init__(self):
        # general
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font('imgs/BreatheFireIii-PKLOB.ttf', 20)

        # bar setup
        self.health_bar_rect = pg.Rect(15, 15, 250, 25)

    def show_bar(self, current, max_amount, bg_rect, color):
        pg.draw.rect(self.display_surface, 'white', bg_rect)

        # determine the ratio of the health bar
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # display the health bar
        pg.draw.rect(self.display_surface, color, current_rect)

    def show_text(self, current, max_amount):
        self.health_surf = self.font.render(
            f'Health: {int(current)}/{int(max_amount)}', False, 'white')
        self.health_rect = self.health_surf.get_rect(
            topleft=self.health_bar_rect.bottomleft)

        self.display_surface.blit(self.health_surf, self.health_rect)

    def show_score(self, exp):
        text_surf = self.font.render(f'Score: {int(exp)}', False, 'white')
        self.text_rect = text_surf.get_rect(topleft=self.health_rect.bottomleft)

        self.display_surface.blit(text_surf, self.text_rect)
        
    def show_ammo(self, ammo):
        text_surf = self.font.render(f'Ammo: {int(ammo)}', False, 'white')
        text_rect = text_surf.get_rect(topleft=self.text_rect.bottomleft)

        self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.max_health, self.health_bar_rect, 'red')

        self.show_text(player.health, player.max_health)

        self.show_score(player.score)
        
        self.show_ammo(player.ammo)