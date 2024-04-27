import pygame
import sys
from classes import Button
from classes import Slider
import os

pygame.init()
pygame.mixer.init() 

# Define colors
BACKGROUND_COL = (34, 34, 34)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (45, 134, 200)
DARK_RED = (160, 60, 60)

# Define constants for UI
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 800
PAD_SIZE = 21.8
PADDING = 4
NUM_ROWS = 5
NUM_COLS = 64
DEFAULT_TEMPO = 120

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

SOUNDS = [
    "kick1.wav",
    "hat1.wav",
    "snare1.wav",
    "8081.wav",
    "snare2.wav"
]
sounds = [pygame.mixer.Sound(sound_file) for sound_file in SOUNDS]

sounds_mapped = {
    "kick1.wav": 0,
    "hat1.wav": 1,
    "snare1.wav": 2,
    "8081.wav": 3,
    "snare2.wav": 4
}

sound_names = [
    "Kick",
    "Hat",
    "Snare",
    "808",
    "Snare 2"
]

# Initialize Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Beat Sequencer")

# Create a 2D list to store the state of each pad
pads_state = [[False for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def draw_pads(current_column, playing):
    # Calculate the total width and height of the grid
    grid_width = NUM_COLS * (PAD_SIZE + PADDING) + PADDING
    grid_height = NUM_ROWS * (PAD_SIZE + PADDING) + PADDING

    # Calculate the starting position to center the grid
    start_x = (SCREEN_WIDTH - grid_width) // 2
    start_y = (SCREEN_HEIGHT - grid_height) // 2

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if col < len(pads_state[row]):
                x = start_x + col * (PAD_SIZE + PADDING)
                y = start_y + row * (PAD_SIZE + PADDING)
                if (col // 4) % 2 == 0:
                    color = GRAY
                else:
                    color = BLACK
                if playing and col == current_column:
                    pygame.draw.rect(screen, RED, (x, y, PAD_SIZE, PAD_SIZE))
                elif pads_state[row][col]:
                    pygame.draw.rect(screen, GREEN, (x, y, PAD_SIZE, PAD_SIZE))
                else:
                    pygame.draw.rect(screen, color, (x, y, PAD_SIZE, PAD_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, PAD_SIZE, PAD_SIZE), 1)
                if col == 0:
                    sound_name = sound_names[row]
                    font = pygame.font.Font(None, 24)
                    text = font.render(sound_name, True, WHITE)
                    screen.blit(text, (x - text.get_width() - 5, y + (PAD_SIZE - text.get_height()) // 2))
            else:
                break

def button_clicks(mouse_x, mouse_y, beginner_button, intermediate_button, advanced_button, clear_button):
    global NUM_COLS
    global PAD_SIZE

    if beginner_button.clicked((mouse_x, mouse_y)):
        print("Beginner button clicked")
        NUM_COLS = 16
        PAD_SIZE = 50
        beginner_button.is_pressed = True
        beginner_button.button.fill(DARK_RED)
        advanced_button.is_pressed = False
        advanced_button.button.fill(BLUE)
    elif intermediate_button.clicked((mouse_x, mouse_y)):
        print("Intermediate button clicked")
        NUM_COLS = 32
        PAD_SIZE = 30 
        intermediate_button.is_pressed = True
        intermediate_button.button.fill(DARK_RED)
        advanced_button.is_pressed = False
        advanced_button.button.fill(BLUE)
    elif advanced_button.clicked((mouse_x, mouse_y)):
        print("Advanced button clicked")
        NUM_COLS = 64
        PAD_SIZE = 21.8
        advanced_button.is_pressed = True
        advanced_button.button.fill(DARK_RED)

    elif clear_button.clicked((mouse_x, mouse_y)):
        print("Clear button clicked")
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                pads_state[row][col] = False
        clear_button.button.fill(RED)
    

def load_sounds():
    sounds = {}
    sound_folder = "sounds"  # Your sound folder
    for file_name in os.listdir(sound_folder):
        if file_name.endswith(".wav"):
            name = os.path.splitext(file_name)[0]
            sound = pygame.mixer.Sound(os.path.join(sound_folder, file_name))
            sounds[name] = sound
    return sounds
    

# Main loop
def main():
    global NUM_COLS
    global PAD_SIZE
    running = True
    playing = False
    current_column = 0
    last_played_time = 0  # Variable to store the last time a column was played

    clock = pygame.time.Clock()

    beginner_button = Button((100, 30), "Beginner", (20, 20))
    intermediate_button = Button((100, 30), "Intermediate", (SCREEN_WIDTH / 2 - 100, 20))
    advanced_button = Button((100, 30), "Advanced", (SCREEN_WIDTH - 120, 20))
    clear_button = Button((100, 30), "Clear", (20, SCREEN_HEIGHT - 50))
    clear_button.button.fill(RED)

    advanced_button.is_pressed = True
    advanced_button.button.fill(DARK_RED)
    beginner_button.reset_color()
    intermediate_button.reset_color()
    advanced_button.render(screen)

    # tempo_slider.value = 90
    tempo_slider = Slider((400, 60), (200, 20), 0.5, 60, 120, orientation="horizontal")
    tempVal = (tempo_slider.max_val + tempo_slider.min_val) / 2 + 60  # Initial value for tempo

    # Update the current column initially
    current_column = 0

    # Creating sliders for sound volumes
    slider_width = 100
    total_width = slider_width * len(SOUNDS)
    slider_x = (SCREEN_WIDTH - total_width) // 2  # Center the sliders horizontally
    slider_y = SCREEN_HEIGHT - 150
    sound_sliders = []

    font1 = pygame.font.Font(None, 36)
    font2 = pygame.font.Font(None, 26)

    for i in range(len(SOUNDS)):
        sound_sliders.append(Slider((slider_x, slider_y), (95, 100), 0.5, 0, 100, orientation="vertical"))
        slider_x += slider_width

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Reset all button colors
                    beginner_button.reset_color()
                    intermediate_button.reset_color()
                    advanced_button.reset_color()

                    # Get the mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if the click occurred within a button's area
                    button_clicks(mouse_x, mouse_y, beginner_button, intermediate_button, advanced_button, clear_button)

                    for slider in sound_sliders:
                        if slider.container_rect.collidepoint((mouse_x, mouse_y)):
                            slider.dragging = True

                    if tempo_slider.container_rect.collidepoint((mouse_x, mouse_y)):
                        tempo_slider.dragging = True
                    else:
                        # Check if a pad was clicked
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        # Calculate the starting position of the grid
                        grid_width = NUM_COLS * (PAD_SIZE + PADDING) + PADDING
                        grid_height = NUM_ROWS * (PAD_SIZE + PADDING) + PADDING
                        start_x = (SCREEN_WIDTH - grid_width) // 2
                        start_y = (SCREEN_HEIGHT - grid_height) // 2

                        # Adjust mouse click positions based on the grid's repositioning
                        mouse_x -= start_x
                        mouse_y -= start_y
                        for row in range(NUM_ROWS):
                            for col in range(NUM_COLS):
                                x = col * (PAD_SIZE + PADDING) + PADDING
                                y = row * (PAD_SIZE + PADDING) + PADDING
                                if x <= mouse_x <= x + PAD_SIZE and y <= mouse_y <= y + PAD_SIZE:
                                    # Toggle pad state
                                    pads_state[row][col] = not pads_state[row][col]

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    tempo_slider.dragging = False

                    for slider in sound_sliders:
                        slider.dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if tempo_slider.dragging:

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    tempo_slider.move_slider(mouse_x, mouse_y)
                    
                    tempVal = float( tempo_slider.get_value())
                    
                    print(f"Tempo value: {tempVal}")
                for slider in sound_sliders:
                    if slider.dragging:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        slider.move_slider(mouse_x, mouse_y)
                        

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Start/stop playing
                    playing = not playing
                    current_column = 0

        current_time = pygame.time.get_ticks()
        if playing and current_time - last_played_time >= tempVal:
            last_played_time = current_time
            for row in range(NUM_ROWS):
                if pads_state[row][current_column]:
                    # Play sound corresponding to the row
                    # Get the sound file associated with the row
                    sound_file = SOUNDS[sounds_mapped.get(row, row)]
                    sound_index = SOUNDS.index(sound_file)
                    # Play the sound
                    sounds[sound_index].set_volume(sound_sliders[sound_index].get_value() / 100)
                    sounds[sound_index].play()
                    print(f"Playing sound for row {row}, column {current_column}")  # Replace with sound playback code

            current_column = (current_column + 1) % NUM_COLS

        # Clear the screen
        screen.fill(BACKGROUND_COL)

        # Draw pads
        draw_pads(current_column, playing)

        beginner_button.render(screen)
        intermediate_button.render(screen)
        advanced_button.render(screen)
        clear_button.render(screen)

        tempo_slider.render(screen)
        for slider in sound_sliders:
            slider.render(screen)
            sound_name = sound_names[sound_sliders.index(slider)]
            text = font2.render(sound_name, True, WHITE)
            screen.blit(text, (slider.container_rect.centerx - text.get_width() // 2, slider.container_rect.bottom + 5))

        volume_text = font1.render("VOLUME MIXER", True, WHITE)
        
        screen.blit(volume_text, (SCREEN_WIDTH // 2 - volume_text.get_width() // 2 - 50, SCREEN_HEIGHT - 50))

        tempo_label = font2.render("Tempo", True, WHITE)
        screen.blit(tempo_label, (tempo_slider.container_rect.centerx - tempo_label.get_width() // 2, 
                                   tempo_slider.container_rect.y - tempo_label.get_height() - 10))
        # Add "faster" label to the left of the tempo slider
        faster_label = font2.render("Faster", True, WHITE)
        screen.blit(faster_label, (tempo_slider.container_rect.x - faster_label.get_width() - 20, 
                                   tempo_slider.container_rect.centery - faster_label.get_height() // 2))
        # Add "slower" label to the right of the tempo slider
        slower_label = font2.render("Slower", True, WHITE)
        screen.blit(slower_label, (tempo_slider.container_rect.right + 20, 
                                   tempo_slider.container_rect.centery - slower_label.get_height() // 2))


        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()