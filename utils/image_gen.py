from PIL import Image, ImageDraw, ImageFont
import io
import discord

def create_welcome_card(member: discord.Member) -> io.BytesIO:
    # Create a basic image
    width, height = 800, 300
    background_color = (25, 25, 25)
    text_color = (255, 255, 255)
    accent_color = (0, 153, 255) # Discord Blue-ish

    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Draw Logic (to be refined with better assets later)
    # For now, just text
    
    # Check for font, otherwise load default
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw Welcome Text
    draw.text((width//2, height//2 - 50), f"Welcome to the Server!", fill=accent_color, font=font_large, anchor="mm")
    draw.text((width//2, height//2 + 20), f"{member.name}", fill=text_color, font=font_small, anchor="mm")

    # Save to buffer
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer
