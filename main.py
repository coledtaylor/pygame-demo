import pygame
import pygame_gui
from game_board import CoordinatePlane
from User import User
from gui import GUIManager

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

# Initialize Pygame, create a screen surface, and other necessary variables

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Create instances of CoordinatePlane, User, and GUIManager
coordinate_plane = CoordinatePlane()
user = User("Player1")
gui_manager = GUIManager(WINDOW_WIDTH, WINDOW_HEIGHT)

# Assign cells to the user
coordinate_plane.assign_user_cells(user)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        gui_manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            button = pygame.mouse.get_pressed()
            coordinate_plane.handle_mouse_down(
                pos, button[0], gui_manager, user)

    coordinate_plane.update(time_delta)
    gui_manager.update(time_delta)

    screen.fill((0, 0, 0))
    coordinate_plane.draw(screen)
    gui_manager.draw(screen)

    pygame.display.update()

pygame.quit()
