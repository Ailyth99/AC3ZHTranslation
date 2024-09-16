import wx
import struct
import os
from ulz_compress import compress_file, decompress_file

MAGIC = 0x10
TYPE_24BPP = 0x03
TYPE_16BPP = 0x02
TYPE_8BPP = 0x09
TYPE_4BPP = 0x08

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'AC3TIMagery V0.9 by Lilith', style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER)
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.left_panel = self.create_left_panel()
        self.sizer.Add(self.left_panel, 0, wx.ALL | wx.EXPAND, 5)
        
        self.right_panel = self.create_right_panel()
        self.sizer.Add(self.right_panel, 1, wx.ALL | wx.EXPAND, 5)
        
        self.panel.SetSizer(self.sizer)
        
        self.SetSize((645, 660))
        self.SetMinSize((645, 660))
        self.SetMaxSize((700, 700))
        
        self.Layout()
        
        self.bitmap = None

    def create_left_panel(self):
        left_panel = wx.Panel(self.panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.image_panel = wx.Panel(left_panel, size=(330, 250))
        self.image_panel.Bind(wx.EVT_PAINT, self.on_paint)
        left_sizer.Add(self.image_panel, 0, wx.ALL | wx.EXPAND, 5)
        
        self.info_text = wx.TextCtrl(left_panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(330, 245))
        left_sizer.Add(self.info_text, 0, wx.ALL | wx.EXPAND, 5)
        
        self.header_replace_button = wx.Button(left_panel, label="Header Replace")
        self.header_replace_button.Bind(wx.EVT_BUTTON, self.on_header_replace)
        left_sizer.Add(self.header_replace_button, 0, wx.ALL | wx.EXPAND, 5)
        
        left_panel.SetSizer(left_sizer)
        return left_panel

    def create_right_panel(self):
        right_panel = wx.Panel(self.panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.file_picker = wx.FilePickerCtrl(right_panel, message="Select a TIM file")
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_selected)
        right_sizer.Add(self.file_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        self.clut_choice = wx.Choice(right_panel, choices=[], size=(150, -1))
        self.clut_choice.Bind(wx.EVT_CHOICE, self.on_clut_selected)
        right_sizer.Add(self.clut_choice, 0, wx.ALL | wx.EXPAND, 5)
        
        self.export_button = wx.Button(right_panel, label="Export TIM with this CLUT")
        self.export_button.Bind(wx.EVT_BUTTON, self.on_export_tim)
        right_sizer.Add(self.export_button, 0, wx.ALL | wx.EXPAND, 5)
        
        self.clut_panel = wx.Panel(right_panel, size=(320, 240))
        self.clut_panel.Bind(wx.EVT_PAINT, self.on_clut_paint)
        self.clut_panel.Bind(wx.EVT_RIGHT_DOWN, self.on_clut_right_click)
        right_sizer.Add(self.clut_panel, 0, wx.ALL | wx.EXPAND, 5)
        
        right_sizer.Add(wx.StaticText(right_panel, label="Layer Merge"), 0, wx.ALL, 5)
        
        self.layer1_picker = wx.FilePickerCtrl(right_panel, message="Select first TIM layer")
        right_sizer.Add(self.layer1_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        self.layer2_picker = wx.FilePickerCtrl(right_panel, message="Select second TIM layer")
        right_sizer.Add(self.layer2_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        self.merge_button = wx.Button(right_panel, label="Merge Layers")
        self.merge_button.Bind(wx.EVT_BUTTON, self.on_merge_layers)
        right_sizer.Add(self.merge_button, 0, wx.ALL | wx.EXPAND, 5)
        
        right_sizer.Add(wx.StaticText(right_panel, label="Tools"), 0, wx.ALL, 5)
        
        tools_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.ulz_compress_button = wx.Button(right_panel, label="ULZ Compress")
        self.ulz_compress_button.Bind(wx.EVT_BUTTON, self.on_ulz_compress)
        tools_sizer.Add(self.ulz_compress_button, 1, wx.ALL | wx.EXPAND, 5)
        
        self.ulz_decompress_button = wx.Button(right_panel, label="ULZ Decompress")
        self.ulz_decompress_button.Bind(wx.EVT_BUTTON, self.on_ulz_decompress)
        tools_sizer.Add(self.ulz_decompress_button, 1, wx.ALL | wx.EXPAND, 5)
        
        right_sizer.Add(tools_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        right_panel.SetSizer(right_sizer)
        return right_panel

    def on_file_selected(self, event):
        filepath = self.file_picker.GetPath()
        fmemory = open_and_read_file(filepath)
        pixels, imgwidth, imgheight, header_info, cluts = process_file(fmemory, filepath)
        self.info_text.SetValue(header_info)
        self.image_panel.SetSize((imgwidth, imgheight))
        self.image_width = imgwidth
        self.image_height = imgheight
        self.all_pixels = pixels
        self.cluts = cluts
        self.clut_choice.Set([f"CLUT {i+1}" for i in range(len(cluts))])
        self.clut_choice.SetSelection(0)
        self.selected_clut = 0
        self.update_bitmap()
        self.Refresh()

    def on_clut_selected(self, event):
        self.selected_clut = self.clut_choice.GetSelection()
        self.update_bitmap()
        self.image_panel.Refresh()
        self.clut_panel.Refresh()

    def update_bitmap(self):
        self.bitmap = create_bitmap(self.all_pixels[self.selected_clut], self.image_width, self.image_height)

    def on_clut_paint(self, event):
        if hasattr(self, 'cluts') and self.cluts:
            dc = wx.PaintDC(self.clut_panel)
            clut = self.cluts[self.selected_clut]
            rows = (len(clut) + 15) // 16
            for i, color in enumerate(clut):
                x = (i % 16) * 16
                y = (i // 16) * 16
                dc.SetBrush(wx.Brush(wx.Colour(color[0], color[1], color[2])))
                dc.DrawRectangle(x, y, 16, 16)

    def on_clut_right_click(self, event):
        menu = wx.Menu()
        item = menu.Append(wx.ID_ANY, "复制全部调色板色值")
        menu.Bind(wx.EVT_MENU, self.on_copy_clut_values, item)
        self.clut_panel.PopupMenu(menu)
        menu.Destroy()

    def on_copy_clut_values(self, event):
        if hasattr(self, 'cluts') and self.cluts:
            clut = self.cluts[self.selected_clut]
            color_values = ','.join([f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}" for c in clut])
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(color_values))
                wx.TheClipboard.Close()
                wx.MessageBox("调色板色值已复制到剪贴板", "复制成功", wx.OK | wx.ICON_INFORMATION)

    def on_paint(self, event):
        if self.bitmap:
            dc = wx.PaintDC(self.image_panel)
            dc.Clear()
            panel_width, panel_height = self.image_panel.GetSize()
            bitmap_width, bitmap_height = self.bitmap.GetSize()
            x = (panel_width - bitmap_width) // 2
            y = (panel_height - bitmap_height) // 2
            dc.DrawBitmap(self.bitmap, x, y)

    def on_export_tim(self, event):
        filepath = self.file_picker.GetPath()
        fmemory = open_and_read_file(filepath)
        selected_clut = self.selected_clut
        new_filepath = f"{filepath}_clut{selected_clut + 1}.tim"
        export_tim(fmemory, selected_clut, new_filepath)
        wx.MessageBox(f"TIM file exported to {new_filepath}", "Export Complete", wx.OK | wx.ICON_INFORMATION)

    def on_merge_layers(self, event):
        layer1_path = self.layer1_picker.GetPath()
        layer2_path = self.layer2_picker.GetPath()
        if not layer1_path or not layer2_path:
            wx.MessageBox("Please select both TIM layers", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        layer1_memory = open_and_read_file(layer1_path)
        layer2_memory = open_and_read_file(layer2_path)
        
        merged_tim = merge_tim_layers(layer1_memory, layer2_memory)
        if merged_tim:
            output_path = os.path.join(os.path.dirname(layer1_path), "merged.tim")
            with open(output_path, "wb") as f:
                f.write(merged_tim)
            wx.MessageBox(f"Merged TIM saved to {output_path}", "Merge Complete", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Failed to merge TIM layers. Make sure both files are compatible TIM images.", "Error", wx.OK | wx.ICON_ERROR)

    def on_header_replace(self, event):
        dialog = HeaderReplaceDialog(self)
        dialog.ShowModal()

    def on_ulz_compress(self, event):
        with wx.FileDialog(self, "Select file to compress", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            input_path = fileDialog.GetPath()
            output_path = input_path + ".ulz"

            try:
                compress_file(input_path, output_file=output_path, level=1)
                wx.MessageBox(f"File compressed successfully: {output_path}", "Success", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error compressing file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def on_ulz_decompress(self, event):
        with wx.FileDialog(self, "Select ULZ file to decompress", wildcard="ULZ files (*.ulz)|*.ulz",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            input_path = fileDialog.GetPath()
            output_path = input_path.replace(".ulz", "")

            try:
                data = decompress_file(input_path)
                if data[:4] == b'\x10\x00\x00\x00':
                    output_path += ".tim"
                else:
                    output_path += ".dat"
                with open(output_path, "wb") as f:
                    f.write(data)
                wx.MessageBox(f"File decompressed successfully: {output_path}", "Success", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error decompressing file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

class HeaderReplaceDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Header Replace")
        panel = wx.Panel(self)
        
        wx.StaticText(panel, label="Original TIM:")
        self.original_picker = wx.FilePickerCtrl(panel, message="Select original TIM")
        wx.StaticText(panel, label="Modified TIM:")        
        self.modified_picker = wx.FilePickerCtrl(panel, message="Select modified TIM")
        self.replace_button = wx.Button(panel, label="Replace Header")
        self.replace_button.Bind(wx.EVT_BUTTON, self.on_replace)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="Original TIM:"), 0, wx.LEFT | wx.TOP, 5)
        sizer.Add(self.original_picker, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(wx.StaticText(panel, label="Modified TIM:"), 0, wx.LEFT | wx.TOP, 5)
        sizer.Add(self.modified_picker, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.replace_button, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)
        
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        dialog_sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(dialog_sizer)
        self.Fit()

    def on_replace(self, event):
        original_path = self.original_picker.GetPath()
        modified_path = self.modified_picker.GetPath()
        
        if not original_path or not modified_path:
            wx.MessageBox("Please select both original and modified TIM files", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        original_memory = open_and_read_file(original_path)
        modified_memory = open_and_read_file(modified_path)
        
        _, _, _, _, original_cluts = process_file(original_memory, original_path)
        original_image_org_x, original_image_org_y = self.get_image_vram_coordinates(original_memory)
        original_palette_org_x, original_palette_org_y = self.get_palette_vram_coordinates(original_memory)
        
        self.set_image_vram_coordinates(modified_memory, original_image_org_x, original_image_org_y)
        self.set_palette_vram_coordinates(modified_memory, original_palette_org_x, original_palette_org_y)
        
        output_path = os.path.join(os.path.dirname(modified_path), "header_replaced.tim")
        with open(output_path, "wb") as f:
            f.write(modified_memory)
        
        wx.MessageBox(f"Header replaced TIM saved to {output_path}", "Replace Complete", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def get_image_vram_coordinates(self, fmemory):
        tim_type = unpack4bytes(fmemory[4:8])
        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
            image_data_start = 0x14 + unpack2bytes_le(fmemory[0x12:0x14]) * 16 * 2
            image_org_x = unpack2bytes_le(fmemory[image_data_start + 0x04:image_data_start + 0x06])
            image_org_y = unpack2bytes_le(fmemory[image_data_start + 0x06:image_data_start + 0x08])
        elif tim_type in [TYPE_16BPP, TYPE_24BPP]:
            image_org_x = unpack2bytes_le(fmemory[0x0C:0x0E])
            image_org_y = unpack2bytes_le(fmemory[0x0E:0x10])
        else:
            image_org_x = unpack2bytes_le(fmemory[0x18:0x1A])
            image_org_y = unpack2bytes_le(fmemory[0x1A:0x1C])
        return image_org_x, image_org_y

    def set_image_vram_coordinates(self, fmemory, image_org_x, image_org_y):
        tim_type = unpack4bytes(fmemory[4:8])
        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
            image_data_start = 0x14 + unpack2bytes_le(fmemory[0x12:0x14]) * 16 * 2
            fmemory[image_data_start + 0x04:image_data_start + 0x06] = image_org_x.to_bytes(2, 'little')
            fmemory[image_data_start + 0x06:image_data_start + 0x08] = image_org_y.to_bytes(2, 'little')
        elif tim_type in [TYPE_16BPP, TYPE_24BPP]:
            fmemory[0x0C:0x0E] = image_org_x.to_bytes(2, 'little')
            fmemory[0x0E:0x10] = image_org_y.to_bytes(2, 'little')
        else:
            fmemory[0x18:0x1A] = image_org_x.to_bytes(2, 'little')
            fmemory[0x1A:0x1C] = image_org_y.to_bytes(2, 'little')

    def get_palette_vram_coordinates(self, fmemory):
        tim_type = unpack4bytes(fmemory[4:8])
        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
            palette_org_x = unpack2bytes_le(fmemory[0x0C:0x0E])
            palette_org_y = unpack2bytes_le(fmemory[0x0E:0x10])
        else:
            palette_org_x = 0
            palette_org_y = 0
        return palette_org_x, palette_org_y

    def set_palette_vram_coordinates(self, fmemory, palette_org_x, palette_org_y):
        tim_type = unpack4bytes(fmemory[4:8])
        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
            fmemory[0x0C:0x0E] = palette_org_x.to_bytes(2, 'little')
            fmemory[0x0E:0x10] = palette_org_y.to_bytes(2, 'little')

def open_and_read_file(filename):
    with open(filename, "rb") as f:
        return bytearray(f.read())

def unpack4bytes(data):
    return struct.unpack('<I', bytes(data))[0]

def unpack2bytes(data):
    return struct.unpack('<H', bytes(data))[0]

def unpack2bytes_le(data):
    return int.from_bytes(data, 'little')

def process_file(fmemory, filepath):
    magic = unpack4bytes(fmemory[0:4])
    tim_type = unpack4bytes(fmemory[4:8])
    print(f"Debug: Magic number: 0x{magic:08X}, TIM type: 0x{tim_type:08X}")

    if magic != MAGIC:
        return [], 0, 0, "File is not a .tim image file", []

    header_info = f"{filepath} Information\n"
    header_info += f"Size:\t{len(fmemory)} bytes\n"
    header_info += f"Magic:\t0x{magic:08X}\n"
    header_info += f"Type:\t0x{tim_type:08X}\n"

    if tim_type in [TYPE_4BPP, TYPE_8BPP]:
        palette_org_x = unpack2bytes_le(fmemory[0x0C:0x0E])
        palette_org_y = unpack2bytes_le(fmemory[0x0E:0x10])
        clut_count = unpack2bytes_le(fmemory[0x12:0x14])
        header_info += f"Palette Org X:\t{palette_org_x} (0x{palette_org_x:04X})\n"
        header_info += f"Palette Org Y:\t{palette_org_y} (0x{palette_org_y:04X})\n"
        header_info += f"CLUT Count:\t{clut_count} (0x{clut_count:04X})\n"
        
        clut_size = 16 if tim_type == TYPE_4BPP else 256
        total_clut_size = clut_count * clut_size * 2
        
        image_data_start = 0x14 + total_clut_size
        
        image_org_x = unpack2bytes_le(fmemory[image_data_start + 0x04:image_data_start + 0x06])
        image_org_y = unpack2bytes_le(fmemory[image_data_start + 0x06:image_data_start + 0x08])
    elif tim_type in [TYPE_16BPP, TYPE_24BPP]:
        image_org_x = unpack2bytes_le(fmemory[0x0C:0x0E])
        image_org_y = unpack2bytes_le(fmemory[0x0E:0x10])
    else:
        image_org_x = unpack2bytes_le(fmemory[0x18:0x1A])
        image_org_y = unpack2bytes_le(fmemory[0x1A:0x1C])
    
    header_info += f"Image Org X:\t{image_org_x} (0x{image_org_x:04X})\n"
    header_info += f"Image Org Y:\t{image_org_y} (0x{image_org_y:04X})\n"

    if tim_type == TYPE_24BPP:
        pixels, width, height = process_24bpp(fmemory)
        cluts = [[]]
        header_info += f"BitMode:\t24BPP\n"
    elif tim_type == TYPE_16BPP:
        pixels, width, height = process_16bpp(fmemory)
        cluts = [[]]
        header_info += f"BitMode:\t16BPP\n"
    elif tim_type == TYPE_8BPP:
        pixels, width, height, clut_info, cluts = process_8bpp(fmemory)
        header_info += f"BitMode:\t8BPP\n"
    elif tim_type == TYPE_4BPP:
        pixels, width, height, clut_info, cluts = process_4bpp(fmemory)
        header_info += f"BitMode:\t4BPP\n"
    else:
        return [], 0, 0, "Unsupported .tim file type", []

    header_info += f"Width:\t{width}\n"
    header_info += f"Height:\t{height}\n"
    print(f"Debug: Header info: {header_info}")

    return pixels, width, height, header_info, cluts

def process_24bpp(fmemory):
    data_size = unpack4bytes(fmemory[8:12]) - 0x14 + 8
    image_width = int(unpack2bytes(fmemory[16:18])) * 2 // 3
    image_height = unpack2bytes(fmemory[18:20])
    pixels = [None] * (image_height * image_width)
    color_data = fmemory[0x14:]
    x = 0
    y = 0
    while y < data_size:
        pixels[x] = (color_data[y], color_data[y+1], color_data[y+2])
        x += 1
        y += 3
    return [pixels], image_width, image_height

def process_16bpp(fmemory):
    offset = 8
    data_size = unpack2bytes(fmemory[offset:offset + 2]) - 0x14 + 8
    image_width = unpack2bytes(fmemory[offset + 8:offset + 10])
    image_height = unpack2bytes(fmemory[offset + 10:offset + 12])
    pixels = [None] * (image_height * image_width)
    color_data = fmemory[0x14:]
    x = 0
    while x * 2 < data_size:
        pixels[x] = getpixeldata(color_data, x)
        x += 1
    pixels = [(0, 0, 0) if p is None else p for p in pixels]
    return [pixels], image_width, image_height

def getpixeldata(datatable, position):
    value = datatable[position*2:position*2 + 2]
    if len(value) < 2:
        return (0, 0, 0)
    color = unpack2bytes(value)
    mask = 0b011111
    red = color & mask
    green = (color >> 5) & mask
    blue = (color >> 10) & mask
    if blue >= 0b100000:
        return (0, 0, 0)
    return (red * 8, green * 8, blue * 8)

def process_8bpp(fmemory):
    end_of_clut = unpack4bytes(fmemory[8:12]) + 8
    clut_size = unpack2bytes(fmemory[16:18])
    clut_nb = unpack2bytes(fmemory[18:20])
    clut_memory = fmemory[20:end_of_clut]
    clut = [[getpixeldata(clut_memory, clut_size * _2 + _1) for _1 in range(clut_size)] for _2 in range(clut_nb)]
    offset = end_of_clut + 12
    indices = fmemory[offset:]
    image_width = unpack2bytes(fmemory[end_of_clut + 8:end_of_clut + 10]) * 2
    image_height = unpack2bytes(fmemory[end_of_clut + 10:end_of_clut + 12])
    pixels = [[None for _ in range(image_height * image_width)] for _ in range(len(clut))]
    for x in range(len(clut)):
        for i in range(image_height * image_width):
            position = indices[i]
            pixels[x][i] = clut[x][position]
    return pixels, image_width, image_height, "", clut

def process_4bpp(fmemory):
    end_of_clut = unpack4bytes(fmemory[8:12]) + 8
    clut_size = unpack2bytes(fmemory[16:18])
    clut_nb = unpack2bytes(fmemory[18:20])
    clut_memory = fmemory[20:end_of_clut]
    clut = [[getpixeldata(clut_memory, clut_size * _2 + _1) for _1 in range(clut_size)] for _2 in range(clut_nb)]
    offset = end_of_clut + 12
    indices = fmemory[offset:]
    image_width = unpack2bytes(fmemory[end_of_clut + 8:end_of_clut + 10]) * 4
    image_height = unpack2bytes(fmemory[end_of_clut + 10:end_of_clut + 12])
    pixels = [[None for _ in range(image_height * image_width)] for _ in range(len(clut))]
    for x in range(len(clut)):
        i = 0
        j = 0
        while j != image_height * image_width // 2:
            position = indices[j]
            pixels[x][i] = clut[x][position & 0b00001111]
            pixels[x][i + 1] = clut[x][position >> 4]
            i += 2
            j += 1
    return pixels, image_width, image_height, "", clut

def create_bitmap(pixels, width, height):
    image = wx.Image(width, height)
    for y in range(height):
        for x in range(width):
            color = pixels[y * width + x]
            image.SetRGB(x, y, color[0], color[1], color[2])
    return wx.Bitmap(image)

def export_tim(fmemory, selected_clut, new_filepath):
    tim_type = unpack4bytes(fmemory[4:8])
    if tim_type not in [TYPE_4BPP, TYPE_8BPP]:
        return

    fmemory[18:20] = (1).to_bytes(2, 'little')

    end_of_clut = unpack4bytes(fmemory[8:12]) + 8
    clut_size = unpack2bytes(fmemory[16:18])
    clut_memory = fmemory[20:end_of_clut]
    selected_clut_data = clut_memory[selected_clut * clut_size * 2:(selected_clut + 1) * clut_size * 2]

    fmemory[20:20 + clut_size * 2] = selected_clut_data

    with open(new_filepath, "wb") as f:
        f.write(bytearray(fmemory[:end_of_clut + 12 + len(fmemory[end_of_clut + 12:])]))

def merge_tim_layers(layer1, layer2):
    if layer1[:8] != layer2[:8]:
        print("Debug: Layers are not the same type")
        return None
    
    tim_type = unpack4bytes(layer1[4:8])
    if tim_type not in [TYPE_4BPP, TYPE_8BPP]:
        print("Debug: Unsupported TIM type for merging")
        return None
    
    end_of_clut1 = unpack4bytes(layer1[8:12]) + 8
    end_of_clut2 = unpack4bytes(layer2[8:12]) + 8
    clut_size = unpack2bytes(layer1[16:18])
    
    if layer1[end_of_clut1:] != layer2[end_of_clut2:]:
        print("Debug: Image data is not the same")
        return None
    
    merged_clut = layer1[20:end_of_clut1] + layer2[20:end_of_clut2]
    print(f"Debug: Merged CLUT size: {len(merged_clut)}")
    
    new_clut_count = unpack2bytes(layer1[18:20]) + unpack2bytes(layer2[18:20])
    print(f"Debug: New CLUT count: {new_clut_count}")
    
    merged_tim = bytearray(layer1[:8])
    
    new_clut_size = len(merged_clut) + 12
    merged_tim += new_clut_size.to_bytes(4, 'little')
    
    merged_tim += bytearray(layer1[12:16])
    merged_tim += clut_size.to_bytes(2, 'little')
    merged_tim += new_clut_count.to_bytes(2, 'little')
    merged_tim += merged_clut
    
    merged_tim += bytearray(layer1[end_of_clut1:])
    
    print(f"Debug: Merged TIM size: {len(merged_tim)}")
    print(f"Debug: Original layer1 size: {len(layer1)}")
    print(f"Debug: Original layer2 size: {len(layer2)}")
    
    return merged_tim

def main():
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()