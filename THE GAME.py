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
    level_screen_sprite.rect = level_screen_sprite.image.get_rect()
    level_screen_sprite.rect.x = 0
    level_screen_sprite.rect.y = 0

    starting_screens_sprites.add(level_screen_sprite)
    starting_screens_sprites.add(start_screen_sprite)

    # Adding sprites into groups
    ufo_sprites.draw(screen)
    ball_sprite.draw(screen)

    # Main Pygame variables
    running = True
    fps = 30

    start_screen_moving = 0
    level_screen_moving = 0

    mode = 'start screen'
    clock = pygame.time.Clock()

    # Sound
    pygame.mixer.music.load('data/sound.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    # Timers
    timer_for_sound = 0
    timer_for_victories_info = 0

    # Variables for login establishment
    name = ''
    symbols = 'qwertyuiopasdfghjklzxcvbmn_-)(1234567890йцукенгшщзхъэждлорпавыфячсмитьбю '

    # Indicators
    untouchable = False
    can_click_return = True

    # Other variables
    is_able_to_show_victories_info = False
    victories_string = ''
    player_score = 0
    robot_score = 0

    while running:
        screen.blit(background, (0, 0))

        # THE GAME
        if mode == 'the game screen':
            ball.collide_indicator += 1
            # Hard level
            if level_screen_sprite.rect.x >= 1000:
                if pygame.sprite.spritecollideany(blue_ufo, upper_border_sprite):
                    blue_ufo.vy += 1
                elif pygame.sprite.spritecollideany(blue_ufo, downer_border_sprite):
                    blue_ufo.vy += -1
                ball.speeds = ball.hard_speeds

                blue_ufo.image = load_image('big_blue_ufo.png', -1)

                y_pos_blue = blue_ufo.rect.y

                right_collide_line.rect = pygame.Rect(909, y_pos_blue, 2, 115)
                right_collide_line.image = pygame.Surface([2, 115])
            # Easy level
            elif level_screen_sprite.rect.x <= -1000:
                ball.speeds = ball.easy_speeds

            blue_ufo.rect.y += blue_ufo.vy

            # Ball out of field
            if (ball.rect.x <= -2500) or (ball.rect.x >= 3500):
                if ball.rect.x <= -2500:
                    robot_score += 1

                if ball.rect.x >= 3500:
                    player_score += 1

                ball.rect.x = ball.x
                ball.rect.y = ball.y

                # Assign speed to the ball depending on the selected level
                if level_screen_sprite.rect.x >= 1000:
                    ball.speeds = ball.hard_speeds
                elif level_screen_sprite.rect.x <= -1000:
                    ball.speeds = ball.easy_speeds

                ball.vx = random.choice(ball.speeds)
                ball.vy = random.choice(ball.speeds)

            # Implementation of moving the border behind the UFO
            ufo_sprites.update()
            ball_sprite.update()

            y_pos_red = red_ufo.rect.y
            y_pos_blue = blue_ufo.rect.y

            left_collide_line.update(y_pos_red)
            right_collide_line.update(y_pos_blue)

        # Events
        for event in pygame.event.get():
            # Stop the cycle after closing the program
            if event.type == pygame.QUIT:
                running = False

                # Animations
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (mode == 'start screen') and not untouchable:
                if pygame.mouse.get_pos()[0] <= 500:
                    start_screen_moving = -20
                else:
                    start_screen_moving = 20
                untouchable = True

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (mode == 'level screen') and not untouchable:
                if pygame.mouse.get_pos()[0] <= 500:
                    level_screen_moving = -20
                    ball.speeds = ball.easy_speeds
                else:
                    level_screen_moving = 20
                    ball.vx = random.choice(ball.hard_speeds)
                    ball.vy = random.choice(ball.hard_speeds)
                untouchable = True

            elif (event.type == pygame.KEYDOWN)\
                    and (mode == 'the game screen')\
                    and (event.key == pygame.K_UP)\
                    and red_ufo.can_run_up:
                red_ufo.moving_up = True
                red_ufo.moving_down = False

            elif (event.type == pygame.KEYDOWN)\
                    and (mode == 'the game screen')\
                    and (event.key == pygame.K_DOWN)\
                    and red_ufo.can_run_down:
                red_ufo.moving_down = True
                red_ufo.moving_up = False

            elif (event.type == pygame.KEYDOWN) and (mode == 'final_screen'):
                if event.key == pygame.K_BACKSPACE and len(name) > 0:
                    name = name[:len(name) - 1]

                elif event.unicode in symbols or event.unicode in symbols.upper():
                    if len(name) < 20:
                        name += event.unicode

                elif event.key == pygame.K_RETURN and can_click_return:
                    can_click_return = False

                    with open('logins.txt', mode='r') as logins_file:
                        lines = logins_file.readlines()
                        logins = []
                        for line in lines:
                            logins.append(line.split(',')[0])

                    if name in logins:
                        with open('logins.txt', mode='r') as logins_file:
                            lines = logins_file.readlines()
                            number = 0
                            for line in lines:
                                number += 1
                                if (line.split(',')[0] == name) and (len(lines) != 0):
                                    victories = line.split(',')[1]

                        if player_score == 3:
                            with open('logins.txt', mode='w') as logins_file:
                                for line in lines:
                                    if line.split(',')[0] == name:
                                        logins_file.write(f'{name},{str(int(victories) + 1)}\n')
                                    else:
                                        logins_file.write(f'{line}\n')

                        with open('logins.txt', mode='r') as logins_file:
                            lines = logins_file.readlines()
                            for line in lines:
                                if (line.split(',')[0] == name) and (len(lines) != 0):
                                    victories = line.split(',')[1]

                        victories_string = f'Вы выиграли {victories[0]} раз'

                    else:
                        if robot_score == 3:
                            with open('logins.txt', mode='a') as logins_file:
                                logins_file.write(f'{name},0\n')
                        else:
                            with open('logins.txt', mode='a') as logins_file:
                                logins_file.write(f'{name},1\n')

                        victories_string = 'Ваш аккаунт добавлен'
                    is_able_to_show_victories_info = True

        # Update
        if (start_screen_sprite.rect.x == 1000 or start_screen_sprite.rect.x == -1000)\
                and (mode == 'start screen'):
            start_screen_moving = 0
            untouchable = False
            mode = 'level screen'

        if (level_screen_sprite.rect.x == 1000 or level_screen_sprite.rect.x == -1000)\
                and (mode == 'level screen'):
            level_screen_moving = 0
            untouchable = False
            mode = 'the game screen'

        font = pygame.font.Font(None, 100)

        robot_score_text = font.render(str(robot_score), True, 'blue')
        player_score_text = font.render(str(player_score), True, 'red')

        start_screen_sprite.rect.x += start_screen_moving
        level_screen_sprite.rect.x += level_screen_moving

        upper_border_sprite.draw(screen)
        downer_border_sprite.draw(screen)
        ufo_sprites.draw(screen)
        ball_sprite.draw(screen)

        screen.blit(robot_score_text, [611, 29])
        screen.blit(player_score_text, [351, 508])

        starting_screens_sprites.draw(screen)

        # The final screen
        if (robot_score == 3) or (player_score == 3):
            mode = 'final_screen'
            screen.blit(background, (0, 0))

            login_font = pygame.font.Font('data/SF-Pro-Display-Bold.otf', 40)
            font = pygame.font.Font('data/SF-Pro-Display-Bold.otf', 25)

            if robot_score == 3:
                lose_or_win_text_1 = f'Увы, вы проиграли со счетом {str(robot_score)} : {str(player_score)}'
                lose_or_win_text_2 = 'Вы можете ввести своё имя и попробовать сыграть еще раз'
            else:
                lose_or_win_text_1 = f'Поздравляем, вы выиграли со счётом {str(player_score)} : {str(robot_score)}'
                lose_or_win_text_2 = 'Вы можете ввести своё имя, чтобы мы могли вас запомнить'
            login_string = f'Логин: {name}'

            if is_able_to_show_victories_info:
                victories_text = font.render(victories_string, True, pygame.Color('white'))
                screen.blit(victories_text, [200, 350])
                timer_for_victories_info += 1

            final_text_1 = font.render(lose_or_win_text_1, True, pygame.Color('white'))
            final_text_2 = font.render(lose_or_win_text_2, True, pygame.Color('white'))
            login_text = login_font.render(login_string, True, pygame.Color('white'))

            screen.blit(login_text, [200, 400, 40, 800])
            screen.blit(final_text_1, [200, 150])
            screen.blit(final_text_2, [200, 190])

            ball.vx = 0
            ball.vy = 0

            red_ufo.vy = 0
            blue_ufo.vy = 0

        if timer_for_victories_info == 600:
            running = False

        # Music should always play
        if timer_for_sound == 5100:
            pygame.mixer.music.pause()
            pygame.mixer.music.load('data/sound.mp3')
            pygame.mixer.music.play()
            timer_for_sound = 0

        clock.tick(fps)
        pygame.display.flip()
        timer_for_sound += 1
    pygame.quit()
