import pygame
import sys
import traceback
import hero
import world
import soldier
import socket
import time
import pickle

from pygame.locals import *
from random import *

bg_size = width, height = 480, 480
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('Dungeon')

BLACK = 0, 0, 0
WHITE = 255, 255, 255

GAME_LEVEL = 1
NUM_WALLS = 10
NUM_ENEMIES = 0

pygame.init()
pygame.mixer.init()
background = pygame.image.load('images/background.png').convert()

soldier_startx = 100
soldier_starty = 100
soldier_speed = 4
soldier_width = 100
soldier_height = 100


def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def message(text):
    large_text = pygame.font.Font("freesansbold.ttf", 115)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((width / 2), (height / 2))
    screen.blit(text_surf, text_rect)
    pygame.display.update()

    time.sleep(2)


def wait_connect():
    message("Waiting")


def connect():

    # create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    # get local machine name
    host = socket.gethostname()

    port = 9999

    # connection to hostname on the port.
    sock.connect((host, port))

    # Receive no more than 1024 bytes

    return sock


def main():
    delay = 100
    my_hero = hero.Hero((45, 45), bg_size[0], bg_size[1])

    soldier_one = soldier.SoldierTypeOne((90, 90), bg_size[0], bg_size[1])
    soldier_two = soldier.SoldierTypeOne((180, 180), bg_size[0], bg_size[1])
    soldier_three = soldier.SoldierTypeOne((300, 300), bg_size[0], bg_size[1])

    soldier_list = [soldier_one, soldier_two, soldier_three]

    playing = True

    the_server = connect()

    while True:
        try:
            the_server.recv(4096)
        except socket.error:
            screen.fill(WHITE)
            wait_connect()
            pygame.display.update()
            print('aaaaa')
            pass
        else:
            break

    movement = []

    while playing:
        fps = 60
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP] or key_pressed[K_w]:
            my_hero.moveup()
            movement.append("U")
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            my_hero.movedown()
            movement.append("D")
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            my_hero.moveleft()
            movement.append("L")
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            my_hero.moveright()
            movement.append("R")
        else:
            movement.append("S")

        data = pickle.dumps(movement)
        the_server.send(data)

        movement = []

        screen.blit(background, (0, 0))

        if my_hero.active:
            screen.blit(my_hero.init_image, my_hero.rect)

        for sol in soldier_list:
            screen.blit(sol.init_image, sol.rect)
            sol.move()

        receive = the_server.recv(512)
        #print(receive.decode('ascii'))

        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
