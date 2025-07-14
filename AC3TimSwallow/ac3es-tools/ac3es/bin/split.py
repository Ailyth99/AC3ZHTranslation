# -*- coding: utf-8 -*-
#  This file is part of AC3ES Tools.
#
#  AC3ES Tools is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  AC3ES Tools is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AC3ES Tools.  If not, see <http://www.gnu.org/licenses/>.
import os
import pathlib
import typing

from ac3es.exceptions import CliException, BinDetectException


# Sometimes files contained in ACE.BPB are packed in this bin
# (or dat, the name actually doesn't matter) container file.
#
# Files are store sequentially, without any information about the
# original filename or original size.
#
# The header is composed by the number of entries and a collection
# of pointers to those files.

def split_file(bin_path: pathlib.Path, output_path: pathlib.Path = None, list_path: str = None):
    if not bin_path.exists():
        raise CliException("File {} does not exists", format(bin_path))

    if not output_path:
        output_path = bin_path.parent.joinpath(bin_path.name + '_bin_splitter')

    if not list_path:
        list_path = pathlib.Path(output_path).joinpath('bin_splitter_list.txt')

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    with open(bin_path, 'rb') as bin_stream:
        split_stream(bin_stream, output_path, list_path)


def split_stream(stream: typing.BinaryIO, dest_path: pathlib.Path, list_path: pathlib.Path):
    """
    Split a binary stream into single files

    :param stream: Stream interface to the buffer
    :param dest_path: Path to the destination directory
    :param list_path: Path to the list file
    :return:
    """
    stream.seek(0)
    extract_files(stream, dest_path, list_path)


def read_index(stream: typing.BinaryIO) -> typing.Tuple:
    """Read the pointers to each file stored.

    :return: List
    """

    stream.seek(0)
    index = []
    num_entries = int.from_bytes(
        stream.read(4),
        byteorder='little'
    )

    prev_offset = None
    for _ in range(num_entries):
        offset = int.from_bytes(stream.read(4), byteorder='little')

        if prev_offset is not None and (prev_offset == offset or prev_offset > offset):
            raise BinDetectException(f'Index from bin is incorrect, offsets are not monotonic {prev_offset} {offset}')
        else:
            prev_offset = offset

        index.append(offset)

    stream.seek(0, os.SEEK_END)
    file_size = stream.tell()
    if index[-1] > file_size or index[-1] == file_size:
        raise BinDetectException(f'Last offset is bigger or equal than filesize offset={index[-1]} size={file_size}')

    return tuple(index)


def extract_files(stream: typing.BinaryIO, dest_path: pathlib.Path, list_path: pathlib.Path = None):
    """
    Perform the action to write the files and generate a list of filenames
    :param stream: Stream to the chunk of data to unpack
    :param dest_path: Destination path for the files
    :param list_path: Path to the list file
    :return:
    """
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
