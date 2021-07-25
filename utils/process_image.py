import io
from PIL import Image, ImageDraw, ImageFont


def process_image(avatar, date):
    img = Image.open(io.BytesIO(avatar))

    # semitransparent rectangle overlay
    tint_color = (0, 0, 0)
    transparency = .5
    opacity = int(255 * transparency)
    img = img.convert('RGBA')
    overlay = Image.new('RGBA', img.size, tint_color + (0,))
    draw = ImageDraw.Draw(overlay)
    coordinates = [640, 460, 0, 180]
    draw.rectangle(
        coordinates,
        fill=tint_color + (opacity,))
    img = Image.alpha_composite(img, overlay)

    # vacation text overlay
    img = img.convert('RGB')
    font_type = ImageFont.truetype('utils/arial.ttf', 120, encoding='unic')
    draw = ImageDraw.Draw(img)
    text = f'В отпуске.\nБуду {date}'
    draw.text(
        xy=(20, 180),
        text=text,
        fill='white',
        font=font_type,
        stroke_width=2,
        stroke_fill='white')

    return img
