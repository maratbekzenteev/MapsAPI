import requests
import pygame
import sys
import os


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


MAP_NAME = 'map.png'

long = 37.640280  # longitude, долгота
lat = 55.765665  # latitude, широта
scale = 1  # масштаб, по формуле из него выводится область показа
SCALE_TO_SPN = "str(10 ** (scale - 5))"
mode = "map"  # режим отображения

pygame.init()
size = 450, 450
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Карта")

static_api = "http://static-maps.yandex.ru/1.x/"
response = requests.get(static_api, params={
    'll': str(long) + ',' + str(lat),
    'size': str(size[0]) + ',' + str(size[1]),
    'spn': eval(SCALE_TO_SPN) + ',' + eval(SCALE_TO_SPN),
    'l': mode
})

with open(MAP_NAME, "wb") as file:
    file.write(response.content)
screen.blit(load_image(MAP_NAME), (0, 0))
pygame.display.flip()

running = True
new_frame = False  # флаг, показывающий необходимость повторной отрисовки
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741899:
                scale -= 1
                new_frame = True
            elif event.key == 1073741902:
                scale += 1
                new_frame = True
            elif event.key == 1073741906:
                lat += 4 * float(eval(SCALE_TO_SPN))
                new_frame = True
            elif event.key == 1073741905:
                lat -= 4 * float(eval(SCALE_TO_SPN))
                new_frame = True
            elif event.key == 1073741904:
                long -= 4 * float(eval(SCALE_TO_SPN))
                new_frame = True
            elif event.key == 1073741903:
                long += 4 * float(eval(SCALE_TO_SPN))
                new_frame = True
            long = (long + 180) % 360 - 180
            lat = (lat + 90) % 180 - 90
            if scale < 1:
                scale = 1
            elif scale > 6:
                scale = 6
    keys = pygame.key.get_pressed()

    # повторная отрисовка кадра
    if new_frame:
        response = requests.get(static_api, params={
            'll': str(long) + ',' + str(lat),
            'size': str(size[0]) + ',' + str(size[1]),
            'spn': eval(SCALE_TO_SPN) + ',' + eval(SCALE_TO_SPN),
            'l': mode
        })

        with open(MAP_NAME, "wb") as file:
            file.write(response.content)
        screen.fill((0, 0, 0))
        screen.blit(load_image(MAP_NAME), (0, 0))
        pygame.display.flip()
        new_frame = False
