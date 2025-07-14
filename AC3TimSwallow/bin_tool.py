import os
import pathlib
import struct
import typing

def split_file(bin_path: pathlib.Path):
    if not bin_path.exists():
        raise Exception(f"File {bin_path} does not exist")

    output_path = bin_path.parent.joinpath(bin_path.stem)
    list_path = output_path.joinpath('filelist.txt')

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    with open(bin_path, 'rb') as bin_stream:
        split_stream(bin_stream, output_path, list_path)

def split_stream(stream: typing.BinaryIO, dest_path: pathlib.Path, list_path: pathlib.Path):
    stream.seek(0)
    extract_files(stream, dest_path, list_path)

def read_index(stream: typing.BinaryIO) -> typing.Tuple:
    stream.seek(0)
    index = []
    num_entries = int.from_bytes(stream.read(4), byteorder='little')

    prev_offset = None
    for _ in range(num_entries):
        offset = int.from_bytes(stream.read(4), byteorder='little')

        if prev_offset is not None and (prev_offset == offset or prev_offset > offset):
            raise Exception(f'Index from bin is incorrect, offsets are not monotonic {prev_offset} {offset}')
        else:
            prev_offset = offset

        index.append(offset)

    stream.seek(0, os.SEEK_END)
    file_size = stream.tell()
    if index[-1] > file_size or index[-1] == file_size:
        raise Exception(f'Last offset is bigger or equal than filesize offset={index[-1]} size={file_size}')

    return tuple(index)

def extract_files(stream: typing.BinaryIO, dest_path: pathlib.Path, list_path: pathlib.Path = None):
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
            size = file_size - offset

        stream.seek(offset)
        content = stream.read(size)
        extension = '.dat'
        if content[0:4] == b'\x10\x00\x00\x00':
            extension = '.tim'
        elif content[0:4] == b'Ulz\x1A':
            extension = '.ulz'

        dest_file_path = dest_path.joinpath(f'{index:{0}{pad_size}}{extension}')

        file_names.append(str(dest_file_path.resolve()))

        with dest_file_path.open('wb') as fdest_file:
            fdest_file.write(content)

    if list_path:
        with list_path.open('w', newline='\n', encoding='utf8') as list_txt:
            list_txt.write("\n".join(file_names))

def merge_files_from_list(list_path: pathlib.Path, dest_path: pathlib.Path):
    content_list = get_content_list_from_file(list_path)
    content_list.sort()
    merge_files(content_list, dest_path)

def get_content_list_from_file(list_path: pathlib.Path):
    if not list_path.exists():
        raise Exception(f"File {list_path} does not exist")

    content_list = [
        pathlib.Path(x.strip()) for x in list_path.read_text().split("\n") if x.strip()
    ]
    content_list = [x.resolve() for x in content_list]

    return content_list

def merge_files(content_list: typing.List[pathlib.Path], dest_path: pathlib.Path):
    artefact = merge_all(content_list)
    with dest_path.open('wb') as dp:
        dp.write(artefact)

def merge_all(content_list: typing.List[pathlib.Path]) -> bytes:
    chunks = []
    for filename in content_list:
        real_path = str(pathlib.Path(filename).resolve())

        if not os.path.isfile(real_path):
            raise Exception(f'File {real_path} does not exist')

        with open(real_path, 'rb') as entry_file:
            entry = entry_file.read()
            entry = entry + b'\x00' * (len(entry) % 4)
            chunks.append(entry)

    header = struct.pack('<I', len(chunks))
    start_offset = 4 + len(chunks) * 4
    offsets = []
    current_offset = 0
    for entry in chunks:
        offsets.append(
            struct.pack('<I', start_offset + current_offset)
        )
        current_offset += len(entry)

    return header + b''.join(offsets) + b''.join(chunks)
