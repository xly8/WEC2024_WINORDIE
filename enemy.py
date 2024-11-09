import pygame as pg
import random
import time

class Enemy(pg.sprite.Sprite):
    def __init__(self, monster_name, groups, obstacle_sprites, scale=1):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Screen dimensions
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720

        # Animation setup
        try:
            self.animation_frames = [
                pg.image.load(f"Resources/EnemyImages/enemy{i}.png").convert_alpha()
                for i in range(1, 5)
            ]
        except FileNotFoundError:
            print("Error: One or more animation frames are missing.")
            raise

        self.animation_index = 0
        self.animation_speed = 0.15
        self.last_update = time.time()

        # Initial image and position setup
        self.image = self.animation_frames[0]
        self.pos = pg.math.Vector2(self.get_random_edge_position())  # Use Vector2 consistently
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(0, -10)

        # Movement
        self.obstacle_sprites = obstacle_sprites
        self.direction = pg.math.Vector2()
        
        # Stats
        self.monster_name = monster_name
        self.health = 3
        self.exp = 10
        self.speed = 2
        self.damage = 1

    def animate(self):
        current_time = time.time()
        if current_time - self.last_update > self.animation_speed:
            self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
            self.last_update = current_time
            self.image = self.animation_frames[self.animation_index]

    def get_random_edge_position(self):
        """Generate a random position along screen edges"""
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            return (random.randint(0, self.SCREEN_WIDTH), -50)
        elif edge == 'bottom':
            return (random.randint(0, self.SCREEN_WIDTH), self.SCREEN_HEIGHT + 50)
        elif edge == 'left':
            return (-50, random.randint(0, self.SCREEN_HEIGHT))
        else:  # right
            return (self.SCREEN_WIDTH + 50, random.randint(0, self.SCREEN_HEIGHT))

    def move(self, player_pos):
        """Move towards the player"""
        if player_pos:
            enemy_pos = pg.math.Vector2(self.rect.center)
            target_pos = pg.math.Vector2(player_pos)

            direction = target_pos - enemy_pos

            if direction.length() > 0:
                self.direction = direction.normalize()
                self.pos += self.direction * self.speed  # Update position
                self.rect.topleft = self.pos
                self.hitbox.center = self.rect.center

    def take_damage(self, amount):
        """Reduce health, check for death."""
        self.health -= amount
        print(f"{self.monster_name} took {amount} damage, health: {self.health}")
        if self.health <= 0:
            print(f"{self.monster_name} defeated!")
            self.kill()

    def die(self):
        """Handle death logic."""
        print(f"{self.monster_name} has died.")
        # Optional: Add particle effects, sound effects, or drops
        self.kill()

    def update(self, player_pos=None, player=None):
        self.move(player_pos)
        self.animate()
        if player_pos:
            self.attack(player)


    def attack(self, player):
        """Damage the player if within range."""
        if self.hitbox.colliderect(player.hitbox):
            player.health -= self.damage

