from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes

pygame.init()
surface = pygame.display.set_mode((600, 400))

def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)
 
def start_the_game():
    pass
 
def level_menu():
    mainmenu._open(level)

# Menus
mainmenu = pygame_menu.Menu('Welcome', 600, 400, theme=themes.THEME_DARK)
mainmenu.add.text_input('Name: ', default='username', maxchar=20)
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Levels', level_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=themes.THEME_DARK)
level.add.selector('Difficulty:',[('Hard',1),('Medium',2),('Easy',3)], onchange=set_difficulty)

loading = pygame_menu.Menu('Loading the Game:', 600, 400, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200)
update_loading = pygame.USEREVENT + 0
 
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
 
    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
 
    pygame.display.update()



