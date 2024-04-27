import pygame
pygame.init()
pygame.mixer.init() 
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (64, 84, 199)
DARK_RED = (112, 13, 13)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

class Button:
    def __init__(self, size, text, pos):
        self.pos = pos
        self.size = size
        self.text = text
        self.font = pygame.font.Font(pygame.font.get_default_font(), size[1] // 2)
        self.button = pygame.Surface(size).convert()
        self.button.fill(BLUE)
        self.pressed_color = DARK_RED
        self.is_pressed = False
        self.rect = self.button.get_rect(topleft=self.pos)

    def render(self, window):
        window.blit(self.button, self.pos)
        text_surface, text_rect = text_objects(self.text, self.font)
        text_rect.center = self.rect.center
        window.blit(text_surface, text_rect)

    def clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_pressed = True
            self.button.fill(self.pressed_color)
            return True
        return False
    
    def reset_color(self):
        if self.text != "Clear":
            self.is_pressed = False
            self.button.fill(BLUE)
            


class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min_val: int, max_val: int, orientation: str = "horizontal"):
        self.pos = pos
        self.size = size
        self.orientation = orientation
        if orientation == "horizontal":
            self.slider_left_pos = pos[0] - (size[0]//2)
            self.slider_right_pos = pos[0] + (size[0]//2)
            self.slider_top_pos = pos[1] - (size[1]//2)
            self.slider_bottom_pos = pos[1] + (size[1]//2)
        else:
            self.slider_left_pos = pos[0] - (size[1]//2)
            self.slider_right_pos = pos[0] + (size[1]//2)
            self.slider_top_pos = pos[1] - (size[0]//2)
            self.slider_bottom_pos = pos[1] + (size[0]//2)
        self.colour = RED

        self.min_val = min_val
        self.max_val = max_val
        self.initial_val = initial_val
        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        if orientation == "horizontal":
            self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val * (self.slider_right_pos - self.slider_left_pos) - 5, self.slider_top_pos, 10, self.size[1])
        else:
            self.button_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos + self.initial_val * (self.slider_bottom_pos - self.slider_top_pos) - 5, self.size[0], 10)
        self.dragging = False

    def move_slider(self, mouse_x, mouse_y):
        if self.orientation == "horizontal":
            if self.slider_left_pos <= mouse_x <= self.slider_right_pos:
                self.button_rect.centerx = mouse_x
        else:
            if self.slider_top_pos <= mouse_y <= self.slider_bottom_pos:
                self.button_rect.centery = mouse_y
        
    def render(self, app):
        pygame.draw.rect(app, GRAY, self.container_rect)
        if self.dragging:
            pygame.draw.rect(app, GREEN, self.button_rect)
        else:
            pygame.draw.rect(app, RED, self.button_rect)

    def get_value(self):
        if self.orientation == "horizontal":
            val_range = self.max_val - self.min_val
            button_val = self.button_rect.centerx - self.slider_left_pos
        else:
            val_range = self.max_val - self.min_val
            button_val = self.slider_bottom_pos - self.button_rect.centery

        return (button_val / val_range) * (self.max_val - self.min_val) + self.min_val



class DropdownMenu:
    def __init__(self, options, position):
        self.options = options
        self.rect = pygame.Rect(position, (150, 30))
        self.open = False
        self.selected_option = None
        self.font = pygame.font.Font(None, 24)
        self.update_text()

    def update_text(self):
        if self.selected_option is None:
            self.text = self.font.render("Select sound", True, BLACK)
        else:
            self.text = self.font.render(self.selected_option, True, BLACK)
        
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        surface.blit(self.text, self.text_rect)

        if self.open:
            for i, option in enumerate(self.options):
                rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                pygame.draw.rect(surface, GRAY, rect)
                pygame.draw.rect(surface, BLACK, rect, 2)
                text = self.font.render(option, True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
            elif self.open:
                for i, option in enumerate(self.options):
                    rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if rect.collidepoint(event.pos):
                        self.selected_option = option
                        self.update_text()
                        self.open = False

        

    
