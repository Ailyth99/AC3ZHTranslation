import struct
from PIL import Image

def convert_4bpp(data, width, height, clut):
    img = Image.new('P', (width, height))
    img.putpalette([value for color in clut for value in color[:3]])
    pixels = img.load()
    index = 0
    for y in range(height):
        for x in range(0, width, 2):
            byte = data[index]
            index += 1
            pixels[x, y] = byte & 0x0F
            if x + 1 < width:
                pixels[x + 1, y] = (byte >> 4) & 0x0F
    return img

def convert_8bpp(data, width, height, clut):
    img = Image.new('P', (width, height))
    img.putpalette([value for color in clut for value in color[:3]])
    pixels = img.load()
    index = 0
    for y in range(height):
        for x in range(width):
            byte = data[index]
            index += 1
            pixels[x, y] = byte
    return img

def convert_16bpp(data, width, height):
    img = Image.new('RGBA', (width, height))
    pixels = img.load()
    index = 0
    for y in range(height):
        for x in range(width):
            color = struct.unpack_from('<H', data, index)[0]
            index += 2
            r = (color & 0x1F) << 3
            g = ((color >> 5) & 0x1F) << 3
            b = ((color >> 10) & 0x1F) << 3
            a = 255 if color & 0x8000 == 0 else 0
            pixels[x, y] = (r, g, b, a)
    return img

def convert_24bpp(data, width, height):
    img = Image.new('RGBA', (width, height))
    pixels = img.load()
    index = 0
    for y in range(height):
        for x in range(width):
            b = data[index]
            g = data[index + 1]
            r = data[index + 2]
            index += 3
            pixels[x, y] = (r, g, b, 255)
    return img

def tim_to_bmp(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()
    
    id_tag = struct.unpack_from('<I', data, 0)[0]
    if id_tag != 0x00000010:
        raise ValueError("Not a valid TIM file")
    
    flag = struct.unpack_from('<I', data, 4)[0]
    has_clut = (flag & 0x8) != 0
    bpp = flag & 0x7
    
    index = 8
    clut = None
    if has_clut:
        clut_size = struct.unpack_from('<I', data, index)[0]
        index += 4
        clut_x = struct.unpack_from('<H', data, index)[0]
        clut_y = struct.unpack_from('<H', data, index + 2)[0]
        clut_colors = struct.unpack_from('<H', data, index + 4)[0]
        clut_count = struct.unpack_from('<H', data, index + 6)[0]
        index += 8
        clut = []
        for _ in range(clut_count):
            for _ in range(clut_colors):
                color = struct.unpack_from('<H', data, index)[0]
                index += 2
                r = (color & 0x1F) << 3
                g = ((color >> 5) & 0x1F) << 3
                b = ((color >> 10) & 0x1F) << 3
                a = 255 if color & 0x8000 == 0 else 0
                clut.append((r, g, b, a))
    
    img_size = struct.unpack_from('<I', data, index)[0]
    index += 4
    img_x = struct.unpack_from('<H', data, index)[0]
    img_y = struct.unpack_from('<H', data, index + 2)[0]
    img_width = struct.unpack_from('<H', data, index + 4)[0]
    img_height = struct.unpack_from('<H', data, index + 6)[0]
    index += 8
    
    if bpp == 0:
        img = convert_4bpp(data[index:], img_width * 4, img_height, clut)
    elif bpp == 1:
        img = convert_8bpp(data[index:], img_width * 2, img_height, clut)
    else:
        raise ValueError("Unsupported BPP value")
    
    img.save(output_path, bits=4 if bpp == 0 else 8)


#tim_to_bmp(r'test images\4_bpp_6_clut_vh2.tim', 'output.bmp')