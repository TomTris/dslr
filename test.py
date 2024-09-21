from PIL import Image, ImageDraw, ImageFont

def draw_vertical_text(image, text, position, font, fill):
    rotated_text_image = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    draw_rotated = ImageDraw.Draw(rotated_text_image)
    
    draw_rotated.text((0, 0), '12345', font=font, fill=fill)
    bbox = draw_rotated.textbbox((0, 0), text, font=font)
    print(bbox)
    
    rotated_text_image = rotated_text_image.rotate(90, expand=True, fillcolor=(255, 255, 255, 0))
    
    image.paste(rotated_text_image, position, mask=rotated_text_image)
    
    return rotated_text_image

# Example usage
width, height = 400, 400
image = Image.new('RGBA', (width, height), (255, 255, 255, 255))
font = ImageFont.load_default()
text = "Vertical Text"

image = draw_vertical_text(image, text, (50, 50), font, (0, 0, 0, 255))

# Save or display the image
image.show()

alpha_composit(img1, img2)