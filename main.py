
from pathlib import Path
import math

import pygame
from PIL import Image

from animation import generate_frames


#output

out = Path("output")
out.mkdir(exist_ok=True)

frames = generate_frames(12)

#frejmovi
for i, frame in enumerate(frames):
    frame.save(
        out / f"frame_{i:02}.png"
    )

# =================================
# GIF
# =================================

frames[0].save(
    out / "butterfly.gif",
    save_all=True,
    append_images=frames[1:],
    duration=85,
    loop=0,
    disposal=2
)

#spritesheet

w, h = frames[0].size

sheet = Image.new(
    "RGBA",
    (w * len(frames), h),
    (0, 0, 0, 0)
)

for i, frame in enumerate(frames):
    sheet.paste(frame, (i * w, 0))

sheet.save(
    out / "butterfly_spritesheet.png"
)

# Static preview
frames[0].resize(
    (512, 512),
    Image.Resampling.NEAREST
).save(
    out / "butterfly_preview.png"
)

#pygame preview

pygame.init()

screen = pygame.display.set_mode(
    (600, 420)
)

pygame.display.set_caption(
    "Butterfly V5"
)

clock = pygame.time.Clock()

sprites = [
    pygame.image.fromstring(
        frame.tobytes(),
        frame.size,
        "RGBA"
    ).convert_alpha()
    for frame in frames
]

t = 0.0
running = True

while running:
    dt = clock.tick(60) / 1000.0
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((23, 16, 31))

    frame_index = int(t * 12) % len(sprites)

    sprite = pygame.transform.scale(
        sprites[frame_index],
        (256, 256)
    )

    # Gentle vertical floating
    float_y = 75 + math.sin(t * 2) * 12

    screen.blit(
        sprite,
        (172, round(float_y))
    )

    pygame.display.flip()

pygame.quit()
