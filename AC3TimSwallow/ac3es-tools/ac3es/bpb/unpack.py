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

import pathlib
from ac3es.exceptions import BinDetectException, CliException


def unpack_files(dest_path: pathlib.Path, bpb: pathlib.Path, bph: pathlib.Path) -> int:
    """
    Unpack ACE.BPB and ACE.BPH in a given directory

    :param dest_path: Directory to unpack
    :param bpb: ACE.BPB path
    :param bph: ACE.BPH path
    :return:
    """

    if not dest_path.is_dir():
        dest_path.mkdir(parents=True, exist_ok=True)

    if not bpb.is_file():
        raise CliException('BPB {} is not a file or is inaccessible'.format(bpb.resolve()))

    if not bph.is_file():
        raise CliException('BPH {} is not a file or is inaccessible'.format(bpb.resolve()))

    num_entries = None
    with bpb.open('rb') as bpb, bph.open('rb') as bph:

        # skip the header
        bph.read(16)
        num_entries = int.from_bytes(bph.read(4), byteorder='little')

        for idx in range(num_entries):
            raw_entry = bph.read(8)
            size = int.from_bytes(raw_entry[:3], byteorder='little') << 2
            position = int.from_bytes(raw_entry[4:], byteorder='little') * 0x800
            current_entry = dest_path / pathlib.Path(str(idx).zfill(4))
            unpack_all(current_entry, bpb, position, size)

    return num_entries


def unpack_all(dest_dir: pathlib.Path, bpb, start_offset: int, size: int):
    """
    Recursive function for unpacking chunks in BPB/BPH
    :param dest_dir:
    :param bpb:
    :param start_offset:
    :param size:
    :return:
    """
    bpb.seek(start_offset)
    num_entries = int.from_bytes(bpb.read(4), byteorder='little')

    try:
        if 0 < num_entries < 512:
            offsets = []
            for i in range(num_entries):
                offsets.append(int.from_bytes(bpb.read(4), byteorder='little'))
            is_sorted = all(offsets[i] < offsets[i + 1] for i in range(len(offsets) - 1))

            # let's check if we are dealing with another nested container
            if not is_sorted:
                raise BinDetectException('the list is not ordered ')
            if start_offset + offsets[-1] > start_offset + size:
                raise BinDetectException('chunk too big')

            for idx, chunk_offset in enumerate(offsets):
                chunk_size = None
                try:
                    chunk_size = offsets[idx + 1] - chunk_offset
                except IndexError:
                    chunk_size = size - chunk_offset

                unpack_all(
                    dest_dir.joinpath(f'{idx:04d}'),
                    bpb,
                    chunk_offset + start_offset,
                    chunk_size
                )

            return
    except BinDetectException:
        # if we get here chances are we not dealing with a container but with a file
        # we silently jump to this part and carry on
        pass

    bpb.seek(start_offset)
    content = bpb.read(size)

    extension = '.bin'
    if content[0:4] == b'\x10\x00\x00\x00':
        extension = '.tim'
    elif content[0:4] == b'Ulz\x1A':
        extension = '.ulz'

    filename = dest_dir.with_suffix(extension)

    filename.parent.mkdir(parents=True, exist_ok=True)

    with filename.open('wb') as part:
        part.write(content)
