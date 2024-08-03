from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_instagram_post(background_path, text, font_path, font_size=60, output_path='output.jpg',blur=10):
    # Open the background image
    background = Image.open(background_path)
    
    # Resize and crop the background to 1080x1350
    aspect_ratio = 1080 / 1350
    bg_aspect_ratio = background.width / background.height
    if bg_aspect_ratio > aspect_ratio:
        new_width = int(background.height * aspect_ratio)
        offset = (background.width - new_width) // 2
        background = background.crop((offset, 0, offset + new_width, background.height))
    else:
        new_height = int(background.width / aspect_ratio)
        offset = (background.height - new_height) // 2
        background = background.crop((0, offset, background.width, offset + new_height))
    background = background.resize((1080, 1350), Image.LANCZOS)
    
    # Apply blur to the background
    blurred_background = background.filter(ImageFilter.GaussianBlur(radius=blur))
    
    # Create a drawing object
    draw = ImageDraw.Draw(blurred_background)
    
    # Load the font
    font = ImageFont.truetype(font_path, font_size)
    
    # Wrap text
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        current_line = words[0]
        for word in words[1:]:
            line_width = draw.textlength(current_line + " " + word, font=font)
            if line_width <= max_width:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
    
    # Calculate wrapped text
    max_width = 900  # Leave some margin
    wrapped_text = wrap_text(text, font, max_width)
    
    # Calculate total text height
    line_height = font.size  # Use font.size instead of getsize
    total_text_height = len(wrapped_text) * line_height
    
    # Calculate starting y position to center the text block
    y_text = (1350 - total_text_height) // 2
    
    # Draw the wrapped text
    for line in wrapped_text:
        line_width = draw.textlength(line, font=font)
        x_text = (1080 - line_width) // 2
        draw.text((x_text, y_text), line, font=font, fill='white')
        y_text += line_height
    
    # Save the image
    blurred_background.save(output_path, quality=95)
    print(f"Image saved as {output_path}")