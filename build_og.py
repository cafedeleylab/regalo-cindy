from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
from pathlib import Path

WIDTH, HEIGHT = 1200, 630
out = Path(__file__).with_name('og-cindy.png')
image = Image.new('RGB', (WIDTH, HEIGHT))
pixels = image.load()
for y in range(HEIGHT):
    for x in range(WIDTH):
        radial = max(0, 1 - math.hypot((x - 560) / 800, (y - 250) / 530))
        base = (151 + 58 * radial, 155 + 56 * radial, 164 + 53 * radial)
        pixels[x, y] = tuple(int(max(0, min(255, c))) for c in base)

rng = random.Random(19)
glow = Image.new('RGBA', (WIDTH, HEIGHT))
glow_draw = ImageDraw.Draw(glow)
for _ in range(88):
    x = rng.randrange(WIDTH)
    y = rng.randrange(HEIGHT)
    r = rng.choice([1, 1, 1, 2, 2, 3])
    glow_draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 255, 255, rng.randrange(60, 155)))
soft = glow.filter(ImageFilter.GaussianBlur(5))
image = Image.alpha_composite(image.convert('RGBA'), soft)
image = Image.alpha_composite(image, glow)

draw = ImageDraw.Draw(image)
font_path = '/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf'
font_bold = ImageFont.truetype(font_path, 112)
lines = [('Con Cariño', font_bold, 170), ('para Cindy', font_bold, 300)]
for text, font, y in lines:
    box = draw.textbbox((0, 0), text, font=font)
    width = box[2] - box[0]
    if width > 1080:
        font = ImageFont.truetype(font_path, int(font.size * 1080 / width))
        box = draw.textbbox((0, 0), text, font=font)
        width = box[2] - box[0]
    x = (WIDTH - width) / 2 - box[0]
    draw.text((x, y), text, font=font, fill=(8, 8, 8, 255))
image.convert('RGB').save(out, optimize=True)
print(out)
