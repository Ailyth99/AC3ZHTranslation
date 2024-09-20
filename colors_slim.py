import numpy as np
from PIL import Image
from collections import Counter
import struct


def reduce_colors(image_path, output_path, color_list=None):
    """
    Reduce image colors to a specified list or a maximum of 16 and save the processed image as 4bpp BMP format.

    Args:
        image_path (str): Input image path.
        output_path (str): Output image path.
        color_list (list): List of colors to reduce to (optional).
    """
    max_colors = 16
    try:
        image = Image.open(image_path).convert('RGB')
        data = np.array(image)

        if color_list:
            # Convert hex color list to RGB tuples
            color_list = [tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) for color in color_list]
            most_common_colors = color_list
        else:
            colors = data.reshape(-1, 3)
            color_counts = Counter(map(tuple, colors))
            most_common_colors = [color for color, _ in color_counts.most_common(max_colors)]

        # Create a palette in BGR format
        palette = []
        for color in most_common_colors:
            palette.extend(color[::-1])  # Reverse RGB to BGR
        palette += [0] * (768 - len(palette))

        # Convert image data to palette indices
        new_data = np.array([np.argmin(np.linalg.norm(most_common_colors - pixel, axis=1)) for pixel in data.reshape(-1, 3)]).reshape(data.shape[:2])

        # Save as 4bpp BMP
        save_4bpp_bmp(new_data, image.width, image.height, palette, output_path)

        print(f"Image processed and saved to: {output_path}")
    except Exception as e:
        print(f"Image processing failed: {e}")

def save_4bpp_bmp(data, width, height, palette, output_path):
    # Create BMP header
    header = struct.pack('<2sIHHIIIIHHIIIIII', 
                         b'BM',  # Magic number
                         54 + ((width + 1) // 2) * height,  # File size
                         0, 0,  # Reserved
                         54,  # Data offset
                         40,  # Info header size
                         width, height,  # Width and height
                         1,  # Planes
                         4,  # Bits per pixel
                         0,  # Compression
                         ((width + 1) // 2) * height,  # Image size
                         0, 0,  # X and Y resolution
                         len(palette) // 3,  # Colors used
                         0)  # Important colors

    # Create palette data
    palette_data = struct.pack(f'<{len(palette)}B', *palette)

    # Create pixel data
    pixel_data = bytearray()
    for y in range(height - 1, -1, -1):  # Flip vertically
        for x in range(0, width, 2):
            pixel_data.append(((data[y, x + 1] << 4) | data[y, x]).astype(np.uint8))

    # Write BMP file
    with open(output_path, 'wb') as f:
        f.write(header)
        f.write(palette_data)
        f.write(pixel_data)

input_image = "ma1.png"
output_image = "output.bmp"
color_list = ["#000000", "#809898", "#98C8C0", "#D0F8F0"]

reduce_colors(input_image, output_image, color_list)