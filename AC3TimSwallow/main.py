import wx
import struct
import os,pathlib,time
import bin_tool,subprocess
from img_convert import bmp_to_tim

MAGIC = 0x10
TYPE_24BPP = 0x03
TYPE_16BPP = 0x02
TYPE_8BPP = 0x09
TYPE_4BPP = 0x08

class TIMFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        if len(filenames) > 0:
            file_path = filenames[0]
            if file_path.lower().endswith('.tim'):
                wx.CallAfter(self.window.handle_dropped_file, file_path)
                return True
        return False

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'AC3TimSwallow 1.5 by aikika', style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)
        icon = wx.Icon("bin/morrigan.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.left_panel = self.create_left_panel()
        self.sizer.Add(self.left_panel, 0, wx.ALL | wx.EXPAND, 5)
        
        self.right_panel = self.create_right_panel()
        self.sizer.Add(self.right_panel, 1, wx.ALL | wx.EXPAND, 5)
        
        self.panel.SetSizer(self.sizer)
        
        self.SetSize((680, 620))
        self.SetMinSize((680, 620))
        self.SetMaxSize((750, 700))
        
        self.Layout()
        
        self.bitmap = None
        self.SetDropTarget(TIMFileDropTarget(self))
        
        self.image_panel.Bind(wx.EVT_RIGHT_DOWN, self.on_image_right_click)
        self.Bind(wx.EVT_MENU, self.on_save_as_bmp, id=wx.ID_SAVEAS)
    
    def handle_dropped_file(self, file_path):
        self.file_picker.SetPath(file_path)
        self.on_file_selected(None)

    def create_left_panel(self):
        left_panel = wx.Panel(self.panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.image_panel = wx.Panel(left_panel, size=(330, 250))
        self.image_panel.Bind(wx.EVT_PAINT, self.on_paint)
        left_sizer.Add(self.image_panel, 0, wx.ALL | wx.EXPAND, 5)
        
        self.info_text = wx.TextCtrl(left_panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(330, 230))
        left_sizer.Add(self.info_text, 0, wx.ALL | wx.EXPAND, 5)
        
        self.header_replace_button = wx.Button(left_panel, label="替换 VRAM 坐标")
        self.header_replace_button.Bind(wx.EVT_BUTTON, self.on_header_replace)
        left_sizer.Add(self.header_replace_button, 0, wx.ALL | wx.EXPAND, 5)
        
        self.edit_vram_button = wx.Button(left_panel, label="编辑 VRAM 坐标")
        self.edit_vram_button.Bind(wx.EVT_BUTTON, self.on_edit_vram)
        left_sizer.Add(self.edit_vram_button, 0, wx.ALL | wx.EXPAND, 5)
        
        left_panel.SetSizer(left_sizer)
        return left_panel

    def create_right_panel(self):
        right_panel = wx.Panel(self.panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.file_picker = wx.FilePickerCtrl(right_panel, message="选择一个 TIM 文件")
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_selected)
        right_sizer.Add(self.file_picker, 0, wx.ALL | wx.EXPAND, 5)
        
        self.clut_choice = wx.Choice(right_panel, choices=[], size=(150, -1))
        self.clut_choice.Bind(wx.EVT_CHOICE, self.on_clut_selected)
        right_sizer.Add(self.clut_choice, 0, wx.ALL | wx.EXPAND, 5)
        
        self.clut_panel = wx.Panel(right_panel, size=(320, 256))
        self.clut_panel.SetBackgroundColour(wx.Colour(211, 211, 211))
        self.clut_panel.Bind(wx.EVT_PAINT, self.on_clut_paint)
        self.clut_panel.Bind(wx.EVT_RIGHT_DOWN, self.on_clut_right_click)
        self.clut_panel.Bind(wx.EVT_LEFT_DOWN, self.on_clut_click)
        right_sizer.Add(self.clut_panel, 0, wx.ALL | wx.EXPAND, 5)
        
        self.export_button = wx.Button(right_panel, label="使用所选 CLUT 导出 TIM")
        self.export_button.Bind(wx.EVT_BUTTON, self.on_export_tim)
        right_sizer.Add(self.export_button, 0, wx.ALL | wx.EXPAND, 5)
        
        right_sizer.Add(wx.StaticText(right_panel, label="工具"), 0, wx.ALL, 5)
        
        tools_sizer = wx.BoxSizer(wx.VERTICAL)
        
        ulz_tools_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ulz_compress_button = wx.Button(right_panel, label="ULZ 压缩")
        self.ulz_compress_button.Bind(wx.EVT_BUTTON, self.on_ulz_compress)
        ulz_tools_sizer.Add(self.ulz_compress_button, 1, wx.RIGHT, 5)
        
        self.ulz_decompress_button = wx.Button(right_panel, label="ULZ 解压")
        self.ulz_decompress_button.Bind(wx.EVT_BUTTON, self.on_ulz_decompress)
        ulz_tools_sizer.Add(self.ulz_decompress_button, 1)
        
        tools_sizer.Add(ulz_tools_sizer, 0, wx.EXPAND | wx.BOTTOM, 5)
        
        bin_tools_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bin_split_button = wx.Button(right_panel, label="解包 BIN/DAT")
        self.bin_split_button.Bind(wx.EVT_BUTTON, self.on_split_bin)
        bin_tools_sizer.Add(self.bin_split_button, 1, wx.RIGHT, 5)
        
        self.bin_merge_button = wx.Button(right_panel, label="封包 BIN/DAT")
        self.bin_merge_button.Bind(wx.EVT_BUTTON, self.on_merge_bin)
        bin_tools_sizer.Add(self.bin_merge_button, 1)
        
        tools_sizer.Add(bin_tools_sizer, 0, wx.EXPAND)
        
        right_sizer.Add(tools_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        self.bmp_to_ulz_button = wx.Button(right_panel, label="BMP 转 TIM")
        self.bmp_to_ulz_button.Bind(wx.EVT_BUTTON, self.on_bmp_to_ulz)
        right_sizer.Add(self.bmp_to_ulz_button, 0, wx.ALL | wx.EXPAND, 5)
        
        right_panel.SetSizer(right_sizer)
        return right_panel

    def on_file_selected(self, event):
        filepath = self.file_picker.GetPath()
        fmemory = open_and_read_file(filepath)
        pixels, imgwidth, imgheight, header_info, cluts = process_file(fmemory, filepath)
        self.info_text.SetValue(header_info)
        self.image_panel.SetSize((imgwidth, imgheight))
        self.image_panel.SetBackgroundColour(wx.Colour(211, 211, 211))  
        self.image_width = imgwidth
        self.image_height = imgheight
        self.all_pixels = pixels
        self.cluts = cluts
        self.clut_choice.Set([f"色板 {i+1} / {len(cluts)}" for i in range(len(cluts))])
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
            for i, color in enumerate(clut):
                x = (i % 16) * 16
                y = (i // 16) * 16
                alpha = color[3] if len(color) > 3 else 255
                dc.SetBrush(wx.Brush(wx.Colour(color[0], color[1], color[2], alpha)))
                dc.DrawRectangle(x, y, 16, 16)

                if alpha < 255:
                    points = [wx.Point(x + 15, y + 15), wx.Point(x + 8, y + 15), wx.Point(x + 15, y + 8)]
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255), wx.BRUSHSTYLE_SOLID))
                    dc.DrawPolygon(points)

                # 调试信息
                # print(f"Color: {color}, Alpha: {alpha}")

    def on_clut_click(self, event):
        if hasattr(self, 'cluts') and self.cluts:
            clut = self.cluts[self.selected_clut]
            x, y = event.GetPosition()
            index = (y // 16) * 16 + (x // 16)
            if index < len(clut):
                color = clut[index]
                dialog = ColorInfoDialog(self, color)
                dialog.ShowModal()

    def on_clut_right_click(self, event):
        menu = wx.Menu()
        item = menu.Append(wx.ID_ANY, "复制所有 CLUT 颜色")
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
                wx.MessageBox("CLUT 颜色已复制到剪贴板", "复制成功", wx.OK | wx.ICON_INFORMATION)

    def on_paint(self, event):
        dc = wx.PaintDC(self.image_panel)
        dc.Clear()
        dc.SetBackground(wx.Brush(wx.Colour(211, 211, 211)))  
        dc.Clear()
        if self.bitmap:
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
        wx.MessageBox(f"TIM 文件已导出至 {new_filepath}", "导出完成", wx.OK | wx.ICON_INFORMATION)

    def on_header_replace(self, event):
        if self.bitmap:
            modified_path = self.file_picker.GetPath()
            dialog = HeaderReplaceDialog(self, modified_path=modified_path)
            dialog.ShowModal()
        else:
            dialog = HeaderReplaceDialog(self)
            dialog.ShowModal()

    def on_edit_vram(self, event):
        if self.bitmap:
            original_path = self.file_picker.GetPath()
            dialog = EditVRAMDialog(self, original_path)
            dialog.ShowModal()
        else:

            dialog = EditVRAMDialog(self)
            dialog.ShowModal()

    def on_ulz_compress(self, event):
        with wx.FileDialog(self, "选择要压缩的文件", wildcard="所有文件 (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            input_path = fileDialog.GetPath()

            try:
                compress_ulz(input_path)
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(os.path.dirname(input_path), f"{base_name}.ulz")
                wx.MessageBox(f"文件压缩成功: {output_path}", "成功", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"压缩文件时出错: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def on_ulz_decompress(self, event):
        with wx.FileDialog(self, "选择要解压的 ULZ 文件", wildcard="ULZ 文件 (*.ulz)|*.ulz",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            input_path = fileDialog.GetPath()
            temp_output_path = input_path.replace(".ulz", "")

            try:
                decompress_ulz(input_path, temp_output_path)
                
                with open(temp_output_path, 'rb') as f:
                    header = f.read(4)

                if header == b'\x10\x00\x00\x00':
                    final_output_path = temp_output_path + ".tim"
                else:
                    final_output_path = temp_output_path + ".dat"
                
                os.rename(temp_output_path, final_output_path)
                
                wx.MessageBox(f"文件解压成功: {final_output_path}", "成功", wx.OK | wx.ICON_INFORMATION)

            except Exception as e:
                wx.MessageBox(f"处理过程中出错: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def on_split_bin(self, event):
        with wx.FileDialog(self, "选择 BIN 或 DAT 文件", wildcard="BIN/DAT 文件 (*.bin;*.dat)|*.bin;*.dat", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            bin_path = pathlib.Path(fileDialog.GetPath())
            try:
                bin_tool.split_file(bin_path)
                wx.MessageBox(f"BIN 文件已成功拆分到 {bin_path.stem} 文件夹", "成功", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"拆分 BIN 文件失败: {e}", "错误", wx.OK | wx.ICON_ERROR)

    def on_merge_bin(self, event):
        with wx.FileDialog(self, "选择 filelist.txt", wildcard="文本文件 (*.txt)|*.txt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            list_path = pathlib.Path(fileDialog.GetPath())
            with wx.FileDialog(self, "保存合并后的 BIN 文件", wildcard="BIN 文件 (*.bin)|*.bin", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as saveDialog:
                if saveDialog.ShowModal() == wx.ID_CANCEL:
                    return

                dest_path = pathlib.Path(saveDialog.GetPath())
                try:
                    bin_tool.merge_files_from_list(list_path, dest_path)
                    
                    wx.MessageBox(f"BIN 文件合并成功!\n路径: {dest_path}", "成功", wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"处理文件失败: {e}", "错误", wx.OK | wx.ICON_ERROR)

    def compress_ulz(self, input_file, output_file):
        command = [
            'bin/ac3es_tools.exe', 'ulz', '--compress', input_file, '--ulz-type=2', '--level=1', '--output', output_file
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Compression failed: {result.stderr}")
        return result.stdout

    def on_image_right_click(self, event):
        if self.bitmap:
            menu = wx.Menu()
            save_as_bmp_item = menu.Append(wx.ID_SAVEAS, "另存为 BMP")
            self.Bind(wx.EVT_MENU, self.on_save_as_bmp, save_as_bmp_item)
            self.PopupMenu(menu)
            menu.Destroy()

    def on_save_as_bmp(self, event):
        with wx.FileDialog(self, "保存 BMP 文件", wildcard="BMP 文件 (*.bmp)|*.bmp",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            save_path = fileDialog.GetPath()
            tim_path = self.file_picker.GetPath()
            self.convert_tim_to_bmp(tim_path, save_path)

    def convert_tim_to_bmp(self, tim_path, bmp_path):
        command = ['bin/tim2bmp.exe', tim_path, bmp_path]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            wx.MessageBox(f"转换 TIM 到 BMP 时出错: {result.stderr}", "错误", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(f"BMP 文件已保存至 {bmp_path}", "保存完成", wx.OK | wx.ICON_INFORMATION)

    def on_bmp_to_ulz(self, event):
        dialog = BMPToULZDialog(self)
        dialog.ShowModal()


class BMPToULZDialog(wx.Dialog):
	def __init__(self, parent):
		super().__init__(parent, title="BMP 转 TIM")
		panel = wx.Panel(self)
		
		radio_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.single_layer_radio = wx.RadioButton(panel, label="单层 TIM", style=wx.RB_GROUP)
		self.double_layer_radio = wx.RadioButton(panel, label="双层 TIM")
		self.single_layer_radio.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
		self.double_layer_radio.Bind(wx.EVT_RADIOBUTTON, self.on_radio_change)
		radio_sizer.Add(self.single_layer_radio, 0, wx.ALL, 5)
		radio_sizer.Add(self.double_layer_radio, 0, wx.ALL, 5)
		
		bmp_label = wx.StaticText(panel, label="选择要转换的 BMP (对于双层 TIM, 请按 CLUT 顺序选择)")
		self.bmp_picker = wx.FilePickerCtrl(panel, message="选择 BMP 文件", wildcard="BMP 文件 (*.bmp)|*.bmp")
		
		self.bmp_picker2 = wx.FilePickerCtrl(panel, message="选择第二个 BMP 文件", wildcard="BMP 文件 (*.bmp)|*.bmp")
		self.bmp_picker2.Hide()
		
		tim_label = wx.StaticText(panel, label="选择原始 TIM")
		self.tim_picker = wx.FilePickerCtrl(panel, message="选择原始 TIM 文件", wildcard="TIM 文件 (*.tim)|*.tim")
		
		self.info_text = wx.StaticText(panel, label="用于获取原始 TIM 的 VRAM 坐标")
		
		self.ulz_compress_checkbox = wx.CheckBox(panel, label="将新 TIM 压缩为 ULZ")
		
		self.process_button = wx.Button(panel, label="开始处理")
		self.process_button.Bind(wx.EVT_BUTTON, self.on_process)
		self.log_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(400, 100))
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(radio_sizer, 0, wx.ALL, 5)
		sizer.Add(bmp_label, 0, wx.ALL, 5)
		sizer.Add(self.bmp_picker, 0, wx.ALL | wx.EXPAND, 5)
		sizer.Add(self.bmp_picker2, 0, wx.ALL | wx.EXPAND, 5)
		sizer.Add(tim_label, 0, wx.ALL, 5)
		sizer.Add(self.tim_picker, 0, wx.ALL | wx.EXPAND, 5)
		sizer.Add(self.info_text, 0, wx.ALL, 5)
		sizer.Add(self.ulz_compress_checkbox, 0, wx.ALL, 5)  
		sizer.Add(self.process_button, 0, wx.ALL | wx.EXPAND, 5)
		sizer.Add(self.log_text, 1, wx.ALL | wx.EXPAND, 5)
		
		panel.SetSizer(sizer)
		dialog_sizer = wx.BoxSizer(wx.VERTICAL)
		dialog_sizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(dialog_sizer)
		self.Fit()

	def on_radio_change(self, event):
		if self.double_layer_radio.GetValue():
			self.bmp_picker2.Show()
		else:
			self.bmp_picker2.Hide()
		self.Layout()

	def on_process(self, event):
		bmp_path = self.bmp_picker.GetPath()
		tim_path = self.tim_picker.GetPath()
		if not bmp_path.lower().endswith('.bmp'):
			wx.MessageBox("请选择一个 BMP 文件", "错误", wx.OK | wx.ICON_ERROR)
			return
		if not tim_path.lower().endswith('.tim'):
			wx.MessageBox("请选择一个 TIM 文件", "错误", wx.OK | wx.ICON_ERROR)
			return

		if self.double_layer_radio.GetValue():
			bmp_path2 = self.bmp_picker2.GetPath()
			if not bmp_path2.lower().endswith('.bmp'):
				wx.MessageBox("请选择第二个 BMP 文件", "错误", wx.OK | wx.ICON_ERROR)
				return
			try:
				base_name = os.path.splitext(os.path.basename(bmp_path))[0]
				
				tim_output_path1 = bmp_path.replace('.bmp', '.tim')
				tim_output_path2 = bmp_path2.replace('.bmp', '.tim')
				bmp_to_tim(bmp_path, tim_output_path1)
				bmp_to_tim(bmp_path2, tim_output_path2)
				self.log_text.AppendText(f"{os.path.basename(bmp_path)} 已成功转换为 {base_name}.tim\n")
				self.log_text.AppendText(f"{os.path.basename(bmp_path2)} 已成功转换为 {os.path.basename(tim_output_path2)}\n")
				
				merged_tim_output_path = os.path.join(os.path.dirname(tim_output_path1), f"{base_name}_merged.tim")
				print(f"Running command: bin/AC3LayerMerger.exe {tim_output_path1} {tim_output_path2} {merged_tim_output_path}")
				subprocess.run(["bin/AC3LayerMerger.exe", tim_output_path1, tim_output_path2, merged_tim_output_path], check=True)
				self.log_text.AppendText(f"{os.path.basename(tim_output_path1)} 和 {os.path.basename(tim_output_path2)} 已成功合并为 {os.path.basename(merged_tim_output_path)}\n开始替换 VRAM 坐标...\n")
				time.sleep(2)
					
				original_memory = open_and_read_file(tim_path)
				merged_memory = open_and_read_file(merged_tim_output_path)
				image_org_x, image_org_y = self.get_image_vram_coordinates(original_memory)
				palette_org_x, palette_org_y = self.get_palette_vram_coordinates(original_memory)
				self.set_image_vram_coordinates(merged_memory, image_org_x, image_org_y)
				self.set_palette_vram_coordinates(merged_memory, palette_org_x, palette_org_y)
				with open(merged_tim_output_path, "wb") as f:
					f.write(merged_memory)
				self.log_text.AppendText(f"{os.path.basename(merged_tim_output_path)} 已成功获取原始 VRAM 坐标\n")
				
				if self.ulz_compress_checkbox.GetValue():
					self.log_text.AppendText("开始 ULZ 压缩...\n")
					compress_ulz(merged_tim_output_path)
					self.log_text.AppendText(f"{os.path.basename(merged_tim_output_path)} 已成功压缩为 {base_name}_merged.ulz\n")
				
				self.log_text.AppendText(f"转换完成, 转换后的 {os.path.basename(merged_tim_output_path)} 和 {base_name}_merged.ulz 已保存到 {os.path.dirname(bmp_path)}\n")
			except Exception as e:
				wx.MessageBox(f"处理过程中出错: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)
		else:
			try:
				base_name = os.path.splitext(os.path.basename(bmp_path))[0]
				
				tim_output_path = bmp_path.replace('.bmp', '.tim')
				bmp_to_tim(bmp_path, tim_output_path)
				self.log_text.AppendText(f"{os.path.basename(bmp_path)} 已成功转换为 {base_name}.tim\n")
				
				original_memory = open_and_read_file(tim_path)
				new_memory = open_and_read_file(tim_output_path)
				image_org_x, image_org_y = self.get_image_vram_coordinates(original_memory)
				palette_org_x, palette_org_y = self.get_palette_vram_coordinates(original_memory)
				self.set_image_vram_coordinates(new_memory, image_org_x, image_org_y)
				self.set_palette_vram_coordinates(new_memory, palette_org_x, palette_org_y)
				with open(tim_output_path, "wb") as f:
					f.write(new_memory)
				self.log_text.AppendText(f"{base_name}.tim 已成功获取原始 VRAM 坐标\n")
				
				if self.ulz_compress_checkbox.GetValue():
					self.log_text.AppendText("开始 ULZ 压缩...\n")
					compress_ulz(tim_output_path)
					self.log_text.AppendText(f"{base_name}.tim 已成功压缩为 {base_name}.ulz\n")
				
				self.log_text.AppendText(f"转换完成, 转换后的 {base_name}.tim 和 {base_name}.ulz 已保存到 {os.path.dirname(bmp_path)}\n")
			except Exception as e:
				wx.MessageBox(f"处理过程中出错: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

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

def compress_ulz(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(os.path.dirname(input_file), f"{base_name}.ulz")
    command = [
        'bin/ac3es_tools.exe', 'ulz', '--compress', input_file, '--ulz-type=2', '--level=1', '--output', output_file
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Compression failed: {result.stderr}")
    return result.stdout

def decompress_ulz(input_file, output_file):
    command = [
        'bin/ac3es_tools.exe', 'ulz', '--decompress', input_file, '--output', output_file
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Decompression failed: {result.stderr}")
    return result.stdout

class HeaderReplaceDialog(wx.Dialog):
    def __init__(self, parent, original_path=None, modified_path=None):
        super().__init__(parent, title="替换 VRAM XY 坐标")
        panel = wx.Panel(self)
        
        wx.StaticText(panel, label="原始 TIM:")
        self.original_picker = wx.FilePickerCtrl(panel, message="选择原始 TIM")
        if original_path:
            self.original_picker.SetPath(original_path)
        wx.StaticText(panel, label="修改后的 TIM:")        
        self.modified_picker = wx.FilePickerCtrl(panel, message="选择修改后的 TIM")
        if modified_path:
            self.modified_picker.SetPath(modified_path)
        self.replace_button = wx.Button(panel, label="替换 VRAM XY 坐标")
        self.replace_button.Bind(wx.EVT_BUTTON, self.on_replace)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="原始 TIM:"), 0, wx.LEFT | wx.TOP, 5)
        sizer.Add(self.original_picker, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(wx.StaticText(panel, label="修改后的 TIM:"), 0, wx.LEFT | wx.TOP, 5)
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
            wx.MessageBox("请同时选择原始和修改后的 TIM 文件", "错误", wx.OK | wx.ICON_ERROR)
            return
        
        original_memory = open_and_read_file(original_path)
        modified_memory = open_and_read_file(modified_path)
        
        _, _, _, _, original_cluts = process_file(original_memory, original_path)
        original_image_org_x, original_image_org_y = self.get_image_vram_coordinates(original_memory)
        original_palette_org_x, original_palette_org_y = self.get_palette_vram_coordinates(original_memory)
        
        self.set_image_vram_coordinates(modified_memory, original_image_org_x, original_image_org_y)
        self.set_palette_vram_coordinates(modified_memory, original_palette_org_x, original_palette_org_y)
        
        base_name = os.path.splitext(os.path.basename(modified_path))[0]
        output_path = os.path.join(os.path.dirname(modified_path), f"{base_name}_replace.tim")
        with open(output_path, "wb") as f:
            f.write(modified_memory)
        
        wx.MessageBox(f"新 TIM 文件已保存至 {output_path}", "替换完成", wx.OK | wx.ICON_INFORMATION)
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

class EditVRAMDialog(wx.Dialog):
    def __init__(self, parent, original_path=None):
        super().__init__(parent, title="编辑 VRAM 坐标")
        panel = wx.Panel(self)
        
        self.mode_single = wx.RadioButton(panel, label="修改单个 TIM", style=wx.RB_GROUP)
        self.mode_batch = wx.RadioButton(panel, label="批量修改 TIM")
        self.mode_single.SetValue(True)
        self.mode_single.Bind(wx.EVT_RADIOBUTTON, self.on_mode_change)
        self.mode_batch.Bind(wx.EVT_RADIOBUTTON, self.on_mode_change)
        
        picker_panel = wx.Panel(panel)
        self.file_picker = wx.FilePickerCtrl(picker_panel, message="选择 TIM 文件")
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_selected)
        
        self.folder_picker = wx.DirPickerCtrl(picker_panel, message="选择文件夹")
        self.folder_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_folder_selected)
        self.folder_picker.Hide()
        
        picker_sizer = wx.BoxSizer(wx.VERTICAL)
        picker_sizer.Add(self.file_picker, 0, wx.EXPAND)
        picker_sizer.Add(self.folder_picker, 0, wx.EXPAND)
        picker_panel.SetSizer(picker_sizer)
        
        self.vram_info = wx.StaticText(panel, label="X 范围: 0-1023, Y 范围: 0-511")
        self.vram_palette_x = wx.StaticText(panel, label="VRAM 色板 X:")
        self.vram_palette_x_value = wx.StaticText(panel, label="", size=(100, -1))
        self.vram_palette_x_input = wx.TextCtrl(panel, size=(100, -1))
        
        self.vram_palette_y = wx.StaticText(panel, label="VRAM 色板 Y:")
        self.vram_palette_y_value = wx.StaticText(panel, label="", size=(100, -1))
        self.vram_palette_y_input = wx.TextCtrl(panel, size=(100, -1))
        
        self.vram_image_x = wx.StaticText(panel, label="VRAM 图像 X:")
        self.vram_image_x_value = wx.StaticText(panel, label="", size=(100, -1))
        self.vram_image_x_input = wx.TextCtrl(panel, size=(100, -1))
        
        self.vram_image_y = wx.StaticText(panel, label="VRAM 图像 Y:")
        self.vram_image_y_value = wx.StaticText(panel, label="", size=(100, -1))
        self.vram_image_y_input = wx.TextCtrl(panel, size=(100, -1))
        
        self.write_button = wx.Button(panel, label="保存更改")
        self.write_button.Bind(wx.EVT_BUTTON, self.on_write_vram)
        
        self.log_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        
        self.sizer = wx.GridBagSizer(5, 5)
        self.sizer.Add(self.mode_single, pos=(0, 0), span=(1, 1), flag=wx.ALL, border=5)
        self.sizer.Add(self.mode_batch, pos=(0, 1), span=(1, 1), flag=wx.ALL, border=5)
        self.sizer.Add(picker_panel, pos=(1, 0), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.vram_info, pos=(2, 0), span=(1, 3), flag=wx.ALL, border=5)
        
        self.sizer.Add(self.vram_palette_x, pos=(3, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.sizer.Add(self.vram_palette_x_value, pos=(3, 1), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.sizer.Add(self.vram_palette_x_input, pos=(3, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        
        self.sizer.Add(self.vram_palette_y, pos=(4, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.sizer.Add(self.vram_palette_y_value, pos=(4, 1), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.sizer.Add(self.vram_palette_y_input, pos=(4, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        
        self.sizer.Add(self.vram_image_x, pos=(5, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.sizer.Add(self.vram_image_x_value, pos=(5, 1), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.sizer.Add(self.vram_image_x_input, pos=(5, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        
        self.sizer.Add(self.vram_image_y, pos=(6, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.sizer.Add(self.vram_image_y_value, pos=(6, 1), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.sizer.Add(self.vram_image_y_input, pos=(6, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        
        self.sizer.Add(self.write_button, pos=(7, 0), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.log_text, pos=(8, 0), span=(6, 3), flag=wx.EXPAND | wx.ALL, border=5)
        
        panel.SetSizer(self.sizer)
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        dialog_sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(dialog_sizer)
        self.SetMinSize((300, 450))  
        self.SetSize((300, 450))  
        self.Fit()

        if original_path:
            self.file_picker.SetPath(original_path)
            self.load_vram_coordinates(original_path)

    def on_mode_change(self, event):
        if self.mode_batch.GetValue():
            self.file_picker.Hide()
            self.folder_picker.Show()
            self.clear_coordinate_values() 
            self.vram_info.SetLabel("批量修改, X 范围: 0-1023, Y 范围: 0-511")
        else:
            self.folder_picker.Hide()
            self.file_picker.Show()
            self.vram_info.SetLabel("X 范围: 0-1023, Y 范围: 0-511")
        self.Layout()

    def clear_coordinate_values(self):
        self.vram_palette_x_value.SetLabel("")
        self.vram_palette_y_value.SetLabel("")
        self.vram_image_x_value.SetLabel("")
        self.vram_image_y_value.SetLabel("")
        self.vram_palette_x_input.SetValue("")
        self.vram_palette_y_input.SetValue("")
        self.vram_image_x_input.SetValue("")
        self.vram_image_y_input.SetValue("")

    def on_file_selected(self, event):
        filepath = self.file_picker.GetPath()
        if self.mode_single.GetValue():
            self.load_vram_coordinates(filepath)

    def on_folder_selected(self, event):
        folderpath = self.folder_picker.GetPath()

    def load_vram_coordinates(self, filepath):
        fmemory = open_and_read_file(filepath)
        tim_type = unpack4bytes(fmemory[4:8])
        
        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
            palette_org_x = unpack2bytes_le(fmemory[0x0C:0x0E])
            palette_org_y = unpack2bytes_le(fmemory[0x0E:0x10])
            self.vram_palette_x_value.SetLabel(str(palette_org_x))
            self.vram_palette_y_value.SetLabel(str(palette_org_y))
            self.vram_palette_x_input.SetValue(str(palette_org_x))
            self.vram_palette_y_input.SetValue(str(palette_org_y))
        else:
            self.vram_palette_x_value.SetLabel("无")
            self.vram_palette_y_value.SetLabel("无")
            self.vram_palette_x_input.SetValue("")
            self.vram_palette_y_input.SetValue("")
        
        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
            clut_count = unpack2bytes_le(fmemory[0x12:0x14])
            total_clut_size = clut_count * (16 if tim_type == TYPE_4BPP else 256) * 2
            image_data_start = 0x14 + total_clut_size
            image_org_x = unpack2bytes_le(fmemory[image_data_start + 0x04:image_data_start + 0x06])
            image_org_y = unpack2bytes_le(fmemory[image_data_start + 0x06:image_data_start + 0x08])
        elif tim_type in [TYPE_16BPP, TYPE_24BPP]:
            image_org_x = unpack2bytes_le(fmemory[0x0C:0x0E])
            image_org_y = unpack2bytes_le(fmemory[0x0E:0x10])
        else:
            image_org_x = unpack2bytes_le(fmemory[0x18:0x1A])
            image_org_y = unpack2bytes_le(fmemory[0x1A:0x1C])
        
        self.vram_image_x_value.SetLabel(str(image_org_x))
        self.vram_image_y_value.SetLabel(str(image_org_y))
        self.vram_image_x_input.SetValue(str(image_org_x))
        self.vram_image_y_input.SetValue(str(image_org_y))

    def on_write_vram(self, event):
        self.log_text.Clear()
        if self.mode_single.GetValue():
            self.modify_single_tim()
        else:
            self.modify_batch_tim()

    def modify_single_tim(self):
        filepath = self.file_picker.GetPath()
        fmemory = open_and_read_file(filepath)
        tim_type = unpack4bytes(fmemory[4:8])
        
        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
            palette_org_x = int(self.vram_palette_x_input.GetValue())
            palette_org_y = int(self.vram_palette_y_input.GetValue())
            fmemory[0x0C:0x0E] = palette_org_x.to_bytes(2, 'little')
            fmemory[0x0E:0x10] = palette_org_y.to_bytes(2, 'little')
        
        image_org_x = int(self.vram_image_x_input.GetValue())
        image_org_y = int(self.vram_image_y_input.GetValue())
        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
            clut_count = unpack2bytes_le(fmemory[0x12:0x14])
            total_clut_size = clut_count * (16 if tim_type == TYPE_4BPP else 256) * 2
            image_data_start = 0x14 + total_clut_size
            fmemory[image_data_start + 0x04:image_data_start + 0x06] = image_org_x.to_bytes(2, 'little')
            fmemory[image_data_start + 0x06:image_data_start + 0x08] = image_org_y.to_bytes(2, 'little')
        elif tim_type in [TYPE_16BPP, TYPE_24BPP]:
            fmemory[0x0C:0x0E] = image_org_x.to_bytes(2, 'little')
            fmemory[0x0E:0x10] = image_org_y.to_bytes(2, 'little')
        else:
            fmemory[0x18:0x1A] = image_org_x.to_bytes(2, 'little')
            fmemory[0x1A:0x1C] = image_org_y.to_bytes(2, 'little')
        
        with open(filepath, "wb") as f:
            f.write(fmemory)
        
        self.log_text.AppendText(f"VRAM 坐标已写入 {filepath}\n")

    def modify_batch_tim(self):
        folder_path = self.folder_picker.GetPath()
        self.log_text.AppendText(f"开始批量修改文件夹: {folder_path}\n")
        
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.tim'):
                filepath = os.path.join(folder_path, filename)
                self.log_text.AppendText(f"正在处理文件: {filename}\n")
                
                try:
                    with open(filepath, "rb+") as f:
                        fmemory = bytearray(f.read())
                        tim_type = unpack4bytes(fmemory[4:8])
                        
                        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
                            palette_org_x = int(self.vram_palette_x_input.GetValue())
                            palette_org_y = int(self.vram_palette_y_input.GetValue())
                            fmemory[0x0C:0x0E] = palette_org_x.to_bytes(2, 'little')
                            fmemory[0x0E:0x10] = palette_org_y.to_bytes(2, 'little')
                            self.log_text.AppendText(f"  色板坐标已设置为 ({palette_org_x}, {palette_org_y})\n")
                        
                        image_org_x = int(self.vram_image_x_input.GetValue())
                        image_org_y = int(self.vram_image_y_input.GetValue())
                        if tim_type in [TYPE_4BPP, TYPE_8BPP]:
                            clut_count = unpack2bytes_le(fmemory[0x12:0x14])
                            total_clut_size = clut_count * (16 if tim_type == TYPE_4BPP else 256) * 2
                            image_data_start = 0x14 + total_clut_size
                            fmemory[image_data_start + 0x04:image_data_start + 0x06] = image_org_x.to_bytes(2, 'little')
                            fmemory[image_data_start + 0x06:image_data_start + 0x08] = image_org_y.to_bytes(2, 'little')
                        elif tim_type in [TYPE_16BPP, TYPE_24BPP]:
                            fmemory[0x0C:0x0E] = image_org_x.to_bytes(2, 'little')
                            fmemory[0x0E:0x10] = image_org_y.to_bytes(2, 'little')
                        else:
                            fmemory[0x18:0x1A] = image_org_x.to_bytes(2, 'little')
                            fmemory[0x1A:0x1C] = image_org_y.to_bytes(2, 'little')
                        
                        self.log_text.AppendText(f"  图像坐标已设置为 ({image_org_x}, {image_org_y})\n")
                        
                        f.seek(0)
                        f.write(fmemory)
                        f.flush()
                        os.fsync(f.fileno())
                    
                    self.log_text.AppendText(f"  VRAM 坐标已写入 {filepath}\n")
                except Exception as e:
                    self.log_text.AppendText(f"  处理 {filename} 时出错: {str(e)}\n")
        
        self.log_text.AppendText(f"文件夹 {folder_path} 中的所有 TIM 文件批量修改完成\n")



class ColorInfoDialog(wx.Dialog):
    def __init__(self, parent, color):
        super().__init__(parent, title="颜色信息", style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
        panel = wx.Panel(self)
        
        color_hex = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"
        self.color_text = wx.TextCtrl(panel, value=color_hex, style=wx.TE_READONLY)
        self.copy_button = wx.Button(panel, label="复制颜色值")
        self.copy_button.Bind(wx.EVT_BUTTON, self.on_copy)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.color_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.copy_button, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)
        
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        dialog_sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(dialog_sizer)
        self.Fit()
        self.Centre()  

    def on_copy(self, event):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.color_text.GetValue()))
            wx.TheClipboard.Close()
        self.EndModal(wx.ID_OK)  

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
        return [], 0, 0, "文件不是 .tim 图像文件", []

    header_info = f"{filepath} 文件信息\n"
    header_info += f"Magic:\t0x{magic:08X}\n"
    header_info += f"Type:\t0x{tim_type:08X}\n"

    palette_org_x, palette_org_y = 0, 0
    if tim_type in [TYPE_4BPP, TYPE_8BPP]:
        palette_org_x = unpack2bytes_le(fmemory[0x0C:0x0E])
        palette_org_y = unpack2bytes_le(fmemory[0x0E:0x10])
        clut_count = unpack2bytes_le(fmemory[0x12:0x14])
        header_info += f"CLUT 数量:\t{clut_count} (0x{clut_count:04X})\n"
        
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

    if tim_type == TYPE_24BPP:
        pixels, width, height = process_24bpp(fmemory)
        cluts = [[]]
        header_info += f"位深度:\t24BPP\n"
    elif tim_type == TYPE_16BPP:
        pixels, width, height = process_16bpp(fmemory)
        cluts = [[]]
        header_info += f"位深度:\t16BPP\n"
    elif tim_type == TYPE_8BPP:
        pixels, width, height, clut_info, cluts = process_8bpp(fmemory)
        header_info += f"位深度:\t8BPP\n"
    elif tim_type == TYPE_4BPP:
        pixels, width, height, clut_info, cluts = process_4bpp(fmemory)
        header_info += f"位深度:\t4BPP\n"
    else:
        return [], 0, 0, "不支持的 .tim 文件类型", []

    header_info += f"宽度:\t{width}\n"
    header_info += f"高度:\t{height}\n"
    header_info += f"色板 X:\t{palette_org_x} (0x{palette_org_x:04X})\n"
    header_info += f"色板 Y:\t{palette_org_y} (0x{palette_org_y:04X})\n"
    header_info += f"图像 X:\t{image_org_x} (0x{image_org_x:04X})\n"
    header_info += f"图像 Y:\t{image_org_y} (0x{image_org_y:04X})\n"

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
        return (0, 0, 0, 255)
    color = unpack2bytes(value)
    mask = 0b011111
    red = color & mask
    green = (color >> 5) & mask
    blue = (color >> 10) & mask
    alpha = 255 if (color & 0x8000) == 0 else 0
    return (red * 8, green * 8, blue * 8, alpha)

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
            # SetRGBTuple takes a tuple of (r,g,b)
            image.SetRGB(x, y, color[0], color[1], color[2])
            # SetAlpha is separate
            if len(color) > 3:
                # wx.Image needs an alpha channel buffer initialized first
                if not image.HasAlpha():
                    image.InitAlpha()
                image.SetAlpha(x, y, color[3])
    return wx.Bitmap(image)


def export_tim(fmemory, selected_clut, new_filepath):
    tim_type = unpack4bytes(fmemory[4:8])
    if tim_type not in [TYPE_4BPP, TYPE_8BPP]:
        return

    # Set the CLUT count to 1
    fmemory[18:20] = (1).to_bytes(2, 'little')

    end_of_clut = unpack4bytes(fmemory[8:12]) + 8
    clut_size = unpack2bytes(fmemory[16:18])
    clut_memory = fmemory[20:end_of_clut]
    selected_clut_data = clut_memory[selected_clut * clut_size * 2:(selected_clut + 1) * clut_size * 2]

    new_fmemory = bytearray(fmemory[:20])
    new_fmemory += selected_clut_data

    image_data_start = 0x14 + clut_size * 2
    new_fmemory += fmemory[end_of_clut:image_data_start]
    new_fmemory += fmemory[end_of_clut:]

    new_clut_size = len(selected_clut_data) + 12
    new_fmemory[8:12] = new_clut_size.to_bytes(4, 'little')

    with open(new_filepath, "wb") as f:
        f.write(new_fmemory)

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
    
    image_data_start = 0x14 + new_clut_count * clut_size * 2
    print(f"Debug: Image data start offset: {image_data_start}")
    
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