import struct,os
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

def bmp_to_tim(input_path, output_path):
    img = Image.open(input_path)
    if img.mode != 'P':
        raise ValueError("Only 4BPP and 8BPP BMP images are supported")
    
    palette = img.getpalette()
    width, height = img.size
    data = img.tobytes()
    
    if len(palette) == 16 * 3:  # 4BPP
        bpp = 0
        clut_count = 1
        clut_colors = 16
        # Convert 4BPP data to TIM format
        tim_data = bytearray()
        for y in range(height):
            for x in range(0, width, 2):
                byte = (data[y * width + x + 1] << 4) | data[y * width + x]
                tim_data.append(byte)
    elif len(palette) == 256 * 3:  # 8BPP
        bpp = 1
        clut_count = 1
        clut_colors = 256
        tim_data = data
    else:
        raise ValueError("Unsupported BMP palette size")
    
    with open(output_path, 'wb') as f:
        # Write TIM header
        f.write(struct.pack('<I', 0x00000010))  # ID Tag for TIM Format
        f.write(struct.pack('<I', 0x00000008 | (bpp & 0x7)))  # TIM flag
        
        # Write CLUT data
        clut_size = 12 + clut_count * clut_colors * 2
        f.write(struct.pack('<I', clut_size))
        f.write(struct.pack('<HHHH', 0, 0, clut_colors, clut_count))
        
        for i in range(clut_colors):
            r = palette[i * 3] >> 3
            g = palette[i * 3 + 1] >> 3
            b = palette[i * 3 + 2] >> 3
            color = (r & 0x1F) | ((g & 0x1F) << 5) | ((b & 0x1F) << 10)
            f.write(struct.pack('<H', color))
        
        # Write image data
        img_size = 12 + len(tim_data)
        f.write(struct.pack('<I', img_size))
        f.write(struct.pack('<HHHH', 0, 0, width // (2 if bpp == 1 else 4), height))
        f.write(tim_data)


#bmp_to_tim('233.bmp', 'output.tim')

#batch
def batch_bmp2tim(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.bmp'):
            bmp_path = os.path.join(folder_path, filename)
            tim_path = os.path.splitext(bmp_path)[0] + '.tim'
            bmp_to_tim(bmp_path, tim_path)
            print(f"Converted {bmp_path} to {tim_path}")

#batch_bmp2tim(r'C:\AC3ES\TRANSED_IMGS\temp_bmp')
