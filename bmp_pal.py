from PIL import Image
from collections import Counter

def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb[::-1]  # 将RGB颜色转换为BGR顺序

def get_image_colors(image_path):
    img = Image.open(image_path)
    palette = img.getpalette()
    color_counts = img.getcolors()
    colors = []
    for count, index in color_counts:
        color = tuple(palette[index*3:index*3+3])
        colors.append(f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}")
    return list(set(colors))

def update_bmp_palette(image_path, new_palette_hex):
    # 检查调色板颜色与图像颜色是否匹配
    image_colors = get_image_colors(image_path)
    palette_colors = list(set(new_palette_hex))
    print("调色板颜色:", palette_colors)
    print("图像颜色:", image_colors)
    if Counter(c.lower() for c in image_colors) != Counter(c.lower() for c in palette_colors):
        raise ValueError("调色板颜色与图像颜色不匹配")

    with open(image_path, 'rb') as f:
        bmp_data = bytearray(f.read())
    
    # BMP文件头偏移量
    file_header_size = 14
    dib_header_size = 40
    palette_start = file_header_size + dib_header_size
    
    # 将新的调色板颜色从hex转换为BGR
    new_palette = []
    for hex_color in new_palette_hex:
        new_palette.extend(hex_to_bgr(hex_color))
    
    # 更新调色板
    for i in range(16):
        bmp_data[palette_start + i*4 : palette_start + i*4 + 3] = new_palette[i*3 : i*3 + 3]
        bmp_data[palette_start + i*4 + 3] = 0  # 保持调色板的保留字节为0
    
    # 保存新的BMP图像
    with open('updated_image.bmp', 'wb') as f:
        f.write(bmp_data)

# 示例调色板（16个颜色）

mc_clut0 = [
    "#000000", "#809898", "#98C8C0", "#D0F8F0",
    "#000000", "#809898", "#98C8C0", "#D0F8F0",
    "#000000", "#809898", "#98C8C0", "#D0F8F0",
    "#000000", "#809898", "#98C8C0", "#D0F8F0"
]

mc_clut1 = [
    "#000000", "#000000", "#000000", "#000000",
    "#809898", "#809898", "#809898", "#809898",
    "#98C8C0", "#98C8C0", "#98C8C0", "#98C8C0",
    "#D0F8F0", "#D0F8F0", "#D0F8F0", "#D0F8F0"
]

# 更新BMP图像的调色板
update_bmp_palette('F:\\PSXISO\\AC3\\CUSTOM_TOOLS\\TIMagery\\ma1.bmp', mc_clut0)