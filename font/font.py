from fontTools.ttLib import TTFont
from tqdm import tqdm

def font_changer(font_path, output_path, scale_factor):
    font = TTFont(font_path)
    glyf_table = font['glyf']
    hmtx_table = font['hmtx']
    name_table = font['name']

    # Adjust glyph widths  
    for glyph_name in tqdm(glyf_table.keys(), desc="Adjusting glyph widths"):
        glyph = glyf_table[glyph_name]
        if glyph.isComposite():
            continue
        if glyph.numberOfContours > 0:
            glyph.xMin = int(glyph.xMin * scale_factor)
            glyph.xMax = int(glyph.xMax * scale_factor)
            for i in range(len(glyph.coordinates)):
                x, y = glyph.coordinates[i]
                glyph.coordinates[i] = (int(x * scale_factor), y)
            hmtx_table[glyph_name] = (int(hmtx_table[glyph_name][0] * scale_factor), hmtx_table[glyph_name][1])

    # Update font name
    for record in name_table.names:
        if record.nameID == 1:  # Font Family name
            original_name = record.toUnicode()
            new_name = f"{original_name}{scale_factor}"
            record.string = new_name.encode('utf-16-be')
        elif record.nameID == 4:  # Full font name
            original_name = record.toUnicode()
            new_name = f"{original_name}{scale_factor}"
            record.string = new_name.encode('utf-16-be')

    font.save(output_path)
    print(f"Font saved to {output_path}")

font_path = r"F:\PSXISO\AC3\CUSTOM_TOOLS\TIMagery\ResourceHanRoundedCN-Medium.ttf"
output_path = "rss_medium_0.5475.ttf"
scale_factor = 0.5475  #宽度缩小值
font_changer(font_path, output_path, scale_factor)