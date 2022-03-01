import pygame
import os
import sys
import random


# Collide lines for UFOs class
class CollideLines(pygame.sprite.Sprite):
    def __init__(self, collide_lines_location):
        # Using super __init__ of pygame.sprite
        super().__init__(collide_lines)

        # Initializing rect and image
        self.rect = pygame.Rect(90, 347, 2, 100)
        self.image = pygame.Surface([2, 100])
        self.image.fill((255, 255, 255))

        # Initializing sprite position in
        # dependence of necessary location
        if collide_lines_location == 'left':
            self.rect.y = 347
            self.rect.x = 90
        elif collide_lines_location == 'right':
            self.rect.x = 907
            self.rect.y = 150

    def update(self, y_pos):
        # Setting sprite position
        self.rect.y = y_pos


# Borders class
class Border(pygame.sprite.Sprite):
    def __init__(self, location):
        # Using super __init__ of pygame.sprite in
        # dependence of necessary location
        if location == 'upper':
            super().__init__(upper_border_sprite)
        elif location == 'downer':
            super().__init__(downer_border_sprite)

        # Initializing image in
        # dependence of necessary location
        if location == 'upper':
            self.image = load_image('upper_borderline.png', -1)
        elif location == 'downer':
            self.image = load_image('downer_borderline.png', -1)

        # Initializing rect
        self.rect = self.image.get_rect()

        # Initializing sprite position in
        # dependence of necessary location
        if location == 'upper':
            self.rect.y = 0
        elif location == 'downer':
            self.rect.y = 450


# Red UFO class
class RedUFO(pygame.sprite.Sprite):
    def __init__(self):
        # Using super __init__ of pygame.sprite
        super().__init__(ufo_sprites)

        # Initializing rect and image
        self.image = load_image('red_UFO.png', -1)
        self.rect = self.image.get_rect()

        # Initializing sprite position
        self.rect.x = 20
        self.rect.y = 347

        # Initializing sprite moving possibility variables
        self.moving_up = False
        self.moving_down = False
        self.can_run_up = True
        self.can_run_down = True

        # Initializing sprite speed
        self.vy = 0

    def update(self):
        # Moving
        if self.moving_up:
            # Setting UFO moving direction
            self.vy = -5
            self.rect.y += self.vy

        if self.moving_down:
            # Setting UFO moving direction
            self.vy = 5
            self.rect.y += self.vy

        # Setting moving possibility variables
        self.can_run_up = True
        self.can_run_down = True

        # Collide checking
        if pygame.sprite.spritecollideany(self, upper_border_sprite):
            # Setting moving possibility variables
            self.can_run_up = False
            self.moving_up = False

        if pygame.sprite.spritecollideany(self, downer_border_sprite):
            # Setting moving possibility variables
            self.can_run_down = False
            self.moving_down = False


# Blue UFO class
class BlueUFO(pygame.sprite.Sprite):
    def __init__(self):
        # Using super __init__ of pygame.sprite
        super().__init__(ufo_sprites)

        # Initializing rect and image
        self.image = load_image('blue_UFO.png', -1)
        self.rect = self.image.get_rect()

        # Initializing sprite position
        self.rect.x = 907
        self.rect.y = 150

        # Initializing sprite speed
        self.vy = 5

    def update(self):
        # Collide checking
        if pygame.sprite.spritecollideany(self, upper_border_sprite):
            # Setting UFO direction
            self.vy = 5

        elif pygame.sprite.spritecollideany(self, downer_border_sprite):
            # Setting UFO direction
            self.vy = -5


# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        # Using super __init__ of pygame.sprite
        super().__init__(ball_sprite)

        # Initializing ball radius
        radius = 20

        # Initializing sprite's basic position
        self.x = 475
        self.y = 274

        # Initializing an indicator to
        # prevent bugs
        self.collide_indicator = 0

        # Initializing rect and image
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)

        pygame.draw.circle(self.image, pygame.Color("orange"),
                           (radius, radius), radius)

        self.rect = pygame.Rect(self.x, self.y, 2 * radius, 2 * radius)

        # Initializing variants for speeds on easy/hard level
        self.easy_speeds = [-10, -9, -8, -7, 10, 9, 8, 7]
        self.hard_speeds = [-11, -12, -13, -14, 11, 12, 13, 14]

        # Basically setting ball speeds list into easy speeds
        self.speeds = self.easy_speeds

        # Initializing random speeds
        # in dependence of the chosen level
        self.vx = random.choice(self.speeds)
        self.vy = random.choice(self.speeds)

    def update(self):
        # Collide checking
        if pygame.sprite.spritecollideany(self, upper_border_sprite)\
                or pygame.sprite.spritecollideany(self, downer_border_sprite):
            # Setting ball's speed and moving direction
            if self.vy < 0:
                self.vy = -self.vy
                self.vy += 0.4
            else:
                self.vy = -self.vy
                self.vy -= 0.4

        if pygame.sprite.spritecollideany(self, collide_lines) and self.collide_indicator >= 5:
            # Showing UFO's collide lines as
            # an indicator of an accent
            # with UFOs
            collide_lines.draw(screen)

            # Setting ball's speed and moving direction
            if self.vx < 0:
                self.vx = -self.vx
                self.vx += 2
            else:
                self.vx = -self.vx
                self.vx -= 2

            # Setting indicator's value
            self.collide_indicator = 0

        # Setting ball's location
        self.rect = self.rect.move(self.vx, self.vy)


# Picture-adding function
def load_image(file, key=None):
    fullname = os.path.join('data', file)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if key is not None:
        image = image.convert()
        if key == -1:
            key = image.get_at((0, 0))
        image.set_colorkey(key)
    else:
        image = image.convert_alpha()

    return image


if __name__ == '__main__':
    # Initialazing Pygame
    pygame.init()
    pygame.display.set_caption('Cosmo Ball')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)

    # Initializing sprite groups
    starting_screens_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    ufo_sprites = pygame.sprite.Group()
    ball_sprite = pygame.sprite.Group()
    upper_border_sprite = pygame.sprite.Group()
    downer_border_sprite = pygame.sprite.Group()
    collide_lines = pygame.sprite.Group()

    # Background image
    background = load_image('background.png')

    # Initializing instances of classes
    left_collide_line = CollideLines('left')
    right_collide_line = CollideLines('right')

    upper_border = Border('upper')
    downer_border = Border('downer')

    red_ufo = RedUFO()
    blue_ufo = BlueUFO()

    ball = Ball()

    # Sprites
    start_screen_sprite = pygame.sprite.Sprite()
    start_screen_sprite.image = load_image("start_screen.png")
    start_screen_sprite.rect = start_screen_sprite.image.get_rect()
    start_screen_sprite.rect.x = 0
    start_screen_sprite.rect.y = 0

    level_screen_sprite = pygame.sprite.Sprite()
    level_screen_sprite.image = load_image("level_screen.png")
