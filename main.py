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
scale = 15  # параметр z, масштаб
mode = 'map' # режим отображения

pygame.init()
size = 650, 450
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Карта")

static_api = "http://static-maps.yandex.ru/1.x/"
response = requests.get(static_api, params={
    'll': str(long) + ',' + str(lat),
    'size': str(size[0]) + ',' + str(size[1]),
    'z': scale,
    'l': mode
})

with open(MAP_NAME, "wb") as file:
    file.write(response.content)
screen.blit(load_image(MAP_NAME), (0, 0))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keys = pygame.key.get_pressed()
