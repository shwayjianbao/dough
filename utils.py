import pygame
import os

def load_sprite_sheet(folder, frame_width, frame_height, fallback_color=(128, 128, 128)):
    """
    Load all frames from a sprite sheet folder.
    Each frame should be a separate PNG file named 0.png, 1.png, ...
    Returns a list of pygame.Surface objects.
    If no images found, returns a list with one colored surface.
    """
    frames = []
    i = 0
    while True:
        frame_path = os.path.join(folder, f"{i}.png")
        if not os.path.exists(frame_path):
            break
        image = pygame.image.load(frame_path).convert_alpha()
        image = pygame.transform.scale(image, (frame_width, frame_height))
        frames.append(image)
        i += 1
    if not frames:
        # Return a default colored surface if no images found
        surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        surf.fill(fallback_color)
        frames.append(surf)
    return frames

def load_sound(path):
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None