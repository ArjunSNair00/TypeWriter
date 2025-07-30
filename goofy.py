import pygame
import numpy as np
import random
import textwrap
from scipy.io import wavfile

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen setup
screen = pygame.display.set_mode((1000, 400))
pygame.display.set_caption("Goofy Soundboard + ADSR Typing")

# Font and colors
font = pygame.font.Font(None, 48)
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)

# Random list of sound file indices
sounds_list = np.random.randint(1, 21, size=20)

# Store typed characters
typed_text = ""

# ADSR envelope function
def apply_adsr(waveform, sample_rate, attack=0.01, decay=0.1, sustain=0.7, release=0.2):
    total_samples = len(waveform)
    
    a_samples = int(sample_rate * attack)
    d_samples = int(sample_rate * decay)
    r_samples = int(sample_rate * release)
    s_samples = max(0, total_samples - (a_samples + d_samples + r_samples))

    # Adjust for overflow
    total_env_samples = a_samples + d_samples + s_samples + r_samples
    if total_env_samples > total_samples:
        overflow = total_env_samples - total_samples
        r_samples = max(0, r_samples - overflow)

    # Create ADSR envelope
    attack_curve = np.linspace(0, 1, a_samples, endpoint=False)
    decay_curve = np.linspace(1, sustain, d_samples, endpoint=False)
    sustain_curve = np.full(s_samples, sustain)
    release_curve = np.linspace(sustain, 0, r_samples)

    envelope = np.concatenate((attack_curve, decay_curve, sustain_curve, release_curve))
    envelope = np.pad(envelope, (0, max(0, total_samples - len(envelope))), 'constant')

    # Apply envelope (mono or stereo)
    if waveform.ndim == 1:
        return waveform * envelope
    else:
        return waveform * envelope[:, np.newaxis]

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                typed_text = typed_text[:-1]
            else:
                typed_text += event.unicode

            # Pick a random sound
            sound_index = random.choice(sounds_list)
            sound_path = f"goofy_ahh_sounds - Song jump_{sound_index}.wav"

            try:
                # Load sound data
                sample_rate, data = wavfile.read(sound_path)

                # Normalize to float32
                if data.dtype == np.int16:
                    data = data.astype(np.float32) / 32768.0

                # Apply ADSR envelope
                data = apply_adsr(data, sample_rate)

                # Convert back to int16
                data = (data * 32767).astype(np.int16)

                # Play sound
                sound = pygame.sndarray.make_sound(data.copy())
                sound.play()

            except Exception as e:
                print(f"Error with {sound_path}: {e}")

    # Text wrapping
    max_chars_per_line = 50
    wrapped_lines = textwrap.wrap(typed_text, width=max_chars_per_line)

    # Render text lines
    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (30, 50 + i * 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()