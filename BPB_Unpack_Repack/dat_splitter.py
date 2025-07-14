import os
import pathlib
import struct
import typing

# ####################################################################
# ##                                                                ##
# ##  核心拆包逻辑 (从 bin_tool.py 移植)                            ##
# ##                                                                ##
# ####################################################################

def read_index(stream: typing.BinaryIO) -> typing.Tuple:
    """读取并解析BIN/DAT文件头部的索引区。"""
    stream.seek(0)
    index = []
    
    # 检查文件是否足够大以包含索引头
    if stream.seek(0, 2) < 4:
        raise Exception('File is too small to be a valid archive.')
    stream.seek(0)

    num_entries = int.from_bytes(stream.read(4), byteorder='little')
    
    # 基本的健全性检查
    if num_entries <= 0 or num_entries > 10000: # 假设文件数不会超过10000
        raise Exception(f'Invalid number of entries: {num_entries}. Not a valid archive.')

    prev_offset = None
    for _ in range(num_entries):
        offset = int.from_bytes(stream.read(4), byteorder='little')

        # 检查偏移量是否是递增的
        if prev_offset is not None and (prev_offset >= offset):
            raise Exception(f'Index from bin is incorrect, offsets are not monotonic {prev_offset} >= {offset}')
        else:
            prev_offset = offset

        index.append(offset)

    stream.seek(0, os.SEEK_END)
    file_size = stream.tell()
    
    # 检查最后一个偏移量是否有效
    if index[-1] >= file_size:
        raise Exception(f'Last offset is bigger or equal than filesize. Offset={index[-1]}, Size={file_size}')

    return tuple(index)

def extract_files(stream: typing.BinaryIO, dest_path: pathlib.Path, list_path: pathlib.Path = None):
    """根据索引提取所有子文件。"""
    entries = read_index(stream)
    pad_size = max(2, len(str(len(entries))))

    file_names = []
    stream.seek(0, 2)
    file_size = stream.tell()
    stream.seek(0)
    
    for index, offset in enumerate(entries):
        try:
            size = entries[index + 1] - offset
        except IndexError:
            # 这是最后一个文件
            size = file_size - offset

        stream.seek(offset)
        content = stream.read(size)
        
        # 智能判断文件扩展名
        extension = '.dat'
        if content and content[0:4] == b'\x10\x00\x00\x00':
            extension = '.tim'
        elif content and content[0:4] == b'Ulz\x1A':
            extension = '.ulz'

        dest_file_path = dest_path.joinpath(f'{index:{0}{pad_size}}{extension}')

        file_names.append(str(dest_file_path.resolve()))

        with dest_file_path.open('wb') as fdest_file:
            fdest_file.write(content)

    if list_path:
        with list_path.open('w', newline='\n', encoding='utf8') as list_txt:
            list_txt.write("\n".join(file_names))

def split_file(bin_path: pathlib.Path):
    """拆分单个BIN/DAT文件的入口函数。"""
    if not bin_path.exists():
        raise Exception(f"File {bin_path} does not exist")

    # 输出目录以.dat文件名为基础创建
    output_path = bin_path.parent.joinpath(bin_path.stem)
    # 文件列表也保存在输出目录中
    list_path = output_path.joinpath('filelist.txt')

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    with open(bin_path, 'rb') as bin_stream:
        extract_files(bin_stream, output_path, list_path)

# ####################################################################
# ##                                                                ##
# ##  主程序逻辑                                                      ##
# ##                                                                ##
# ####################################################################

def main():
    """主执行函数，负责用户交互和文件遍历。"""
    print("=" * 60)
    print("      Standalone DAT/BIN File Splitter Tool")
    print("=" * 60)
    print("This tool will recursively scan a folder for .dat files")
    print("and attempt to unpack them into subfolders.\n")
    
    # 循环获取有效的文件夹路径
    while True:
        try:
            folder_str = input("请输入要处理的包含DAT文件的根文件夹路径: ")
            folder_path = pathlib.Path(folder_str)
            if folder_path.is_dir():
                break
            else:
                print("错误: 输入的路径不是一个有效的文件夹，请重试。")
        except Exception as e:
            print(f"发生错误: {e}")

    print(f"\n开始处理文件夹: {folder_path}\n")

    processed_count = 0
    skipped_count = 0

    # 使用 os.walk 递归遍历所有子目录和文件
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith('.dat'):
                dat_path = pathlib.Path(dirpath) / filename
                processed_count += 1
                
                print(f"--> 正在尝试拆分: {dat_path}")
                
                # 使用 try...except 来捕获并处理拆包失败的情况
                try:
                    split_file(dat_path)
                    print(f"    [成功] 已成功拆分到文件夹: {dat_path.stem}")
                except Exception as e:
                    # 如果 split_file 抛出任何异常，说明这个DAT文件不是有效的包
                    skipped_count += 1
                    print(f"    [跳过] 无法拆分 {dat_path.name}。它可能不是一个有效的归档文件。")
                    # 如果需要详细的错误信息，可以取消下面这行的注释
                    # print(f"      (错误详情: {e})")

                print("-" * 50)

    print("\n处理完成！")
    print(f"总共尝试处理 {processed_count} 个 .dat 文件。")
    print(f"成功拆分 {processed_count - skipped_count} 个文件。")
    print(f"跳过 {skipped_count} 个无效或无法处理的文件。")


if __name__ == "__main__":
    main()
    input("\n按 Enter 键退出...")