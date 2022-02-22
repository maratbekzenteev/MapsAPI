import requests
import pygame
import sys
import os
import pygame_gui


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


point = ''
name = ''
MAP_NAME = 'map.png'
FPS = 30
long = 37.640280  # longitude, долгота
lat = 55.765665  # latitude, широта
scale = 1  # масштаб, по формуле из него выводится область показа
SCALE_TO_SPN = "str(10 ** (scale - 5))"
mode = "map"  # режим отображения

pygame.init()
size = 450, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Карта")

static_api = "http://static-maps.yandex.ru/1.x/"
response = requests.get(static_api, params={
    'll': str(long) + ',' + str(lat),
    'size': str(size[0]) + ',' + str(size[1] - 50),
    'spn': eval(SCALE_TO_SPN) + ',' + eval(SCALE_TO_SPN),
    'l': mode,
    'pt': point
})

manager = pygame_gui.UIManager((450, 500))
manager2 = pygame_gui.UIManager((450, 500))

name_enter = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((0, 0), (350, 25)),
    manager=manager)  # Ввод названия компании

find = pygame_gui.elements.ui_button.UIButton(
    relative_rect=pygame.Rect((350, 0), (100, 25)),
    text='Поиск!',
    manager=manager)  # Кнопка поиска

view = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Карта', "Спутник", "Гибрид"],
    starting_option='Карта',
    relative_rect=pygame.Rect((0, 25), (450, 25)),
    manager=manager)  # Выбор режима

with open(MAP_NAME, "wb") as file:
    file.write(response.content)
screen.blit(load_image(MAP_NAME), (0, 50))


def draw():  # Отрисовка карты
    global point
    response = requests.get(static_api, params={
        'll': str(long) + ',' + str(lat),
        'size': str(size[0]) + ',' + str(size[1] - 50),
        'spn': eval(SCALE_TO_SPN) + ',' + eval(SCALE_TO_SPN),
        'l': mode,
        'pt': point
    })
    with open(MAP_NAME, "wb") as file:
        file.write(response.content)
    screen.fill((0, 0, 0))
    screen.blit(load_image(MAP_NAME), (0, 50))


def search(names): # Поиск места
    global lat, long, point
    geocoder_request = 'http://geocode-maps.yandex.ru/1.x/?apikey=' + \
                       '40d1649f-0493-4b70-98ba-98533de7710b&geocode=' + names + \
                       '&format=json'
    response = requests.get(geocoder_request)
    if len(str(response)) != 0:
        json_response = response.json()
        try:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        except IndexError:
            print('Ничего нет')
        else:
            address = toponym["Point"]["pos"].split()
            long = float(address[0])
            lat = float(address[1])
            point = str(long) + ',' + str(lat)
            draw()


screen = pygame.display.set_mode(size)
running = True
new_frame = True  # флаг, показывающий необходимость повторной отрисовки
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0
    manager.draw_ui(screen)
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == view:
                    if str(event.text) == 'Карта':
                        mode = 'map'
                    elif str(event.text) == 'Спутник':
                        mode = 'sat'
                    else:
                        mode = 'skl'
                    draw()
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                name = name_enter.text
                if event.ui_element == find:
                    if len(name) > 0:
                        search(name)
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
                lat += 2 * float(eval(SCALE_TO_SPN))
                new_frame = True
            elif event.key == 1073741905:
                lat -= 2 * float(eval(SCALE_TO_SPN))
                new_frame = True
            elif event.key == 1073741904:
                long -= 2 * float(eval(SCALE_TO_SPN))
                new_frame = True
            elif event.key == 1073741903:
                long += 2 * float(eval(SCALE_TO_SPN))
                new_frame = True
            long = (long + 180) % 360 - 180
            lat = (lat + 90) % 180 - 90
            if scale < 1:
                scale = 1
            elif scale > 6:
                scale = 6
        manager.process_events(event)
    keys = pygame.key.get_pressed()
    # повторная отрисовка кадра
    if new_frame:
        draw()
        new_frame = False
        manager.draw_ui(screen)
    manager.update(time_delta)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
