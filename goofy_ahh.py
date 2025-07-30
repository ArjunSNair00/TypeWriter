import pygame
import numpy as np
import random
import textwrap

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1000, 300))
pygame.display.set_caption("Goofy Soundboard + Typing")

font = pygame.font.Font(None, 48)
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)


sounds_list = np.random.randint(1, 21, size=20)

# Store typed characters
typed_text = ""

running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Handle backspace separately
            if event.key == pygame.K_BACKSPACE:
                typed_text = typed_text[:-1]
            else:
                typed_text += event.unicode

            # Play a random sound
            sound_index = random.choice(sounds_list)
            sound_path = f"goofy_ahh_sounds - Song jump_{sound_index}.wav"
            try:
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
            except pygame.error:
                print(f"Could not load: {sound_path}")

    # Wrap the text to fit in screen width
    max_chars_per_line = 50  # adjust based on font size & screen width
    wrapped_lines = textwrap.wrap(typed_text, width=max_chars_per_line)

    # Render each line
    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (30, 50 + i * 50))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
