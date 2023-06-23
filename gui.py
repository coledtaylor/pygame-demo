import pygame
import pygame_gui


class GUIManager:
    def __init__(self, window_width, window_height):
        self.manager = pygame_gui.UIManager((window_width, window_height))
        self.info_window = None

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self, screen):
        self.manager.draw_ui(screen)

    def show_info_window(self, text):
        self.info_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((350, 275), (340, 210)), visible=True, manager=self.manager
        )
        info_text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(10, 10, 280, 130),
            html_text=text,
            manager=self.manager,
            container=self.info_window.get_container(),
        )
        info_text_box.enable_word_wrap = True

        self.info_window.show()
