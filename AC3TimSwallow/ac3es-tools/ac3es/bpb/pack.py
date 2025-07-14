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

import dataclasses
import typing
import struct
import pathlib


@dataclasses.dataclass
class BPBData:
    header: bytes
    offsets: typing.List[bytes]
    chunks: typing.List[bytes]


def pack_recursive(root_dir: pathlib.Path) -> BPBData:
    chunks = []
    for entry in sorted(root_dir.iterdir()):
        if entry.name.startswith('.'):
            continue

        if entry.is_dir():
            bpb_chunk = pack_recursive(entry)
            chunks.append(
                bpb_chunk.header + b''.join(bpb_chunk.offsets) + b''.join(bpb_chunk.chunks)
            )
        else:
            with entry.open('rb') as f:
                chunks.append(f.read())

    header = struct.pack('<I', len(chunks))
    start_offset = 4 + len(chunks) * 4
    offsets = []
    current_offset = 0
    for entry in chunks:
        offsets.append(
            struct.pack('<I', start_offset + current_offset)
        )
        current_offset += len(entry)

    return BPBData(header=header, offsets=offsets, chunks=chunks)


def pack_files(source_path: pathlib.Path, dest_bpb: pathlib.Path, dest_bph: pathlib.Path):
    if not source_path.is_dir():
        raise Exception(f'{source_path} is not a directory!')

    with dest_bpb.open('wb') as bpb, dest_bph.open('wb') as bph:
        # some info in the BPH, probably the revision number in their SVN
        # among other internal info to track down the files
        bph.write(b'AC3E\x03\x00\x00\x00\x27\x04\x00\x00\x84\x14\x00\x00')

        # let's add the number of elements
        pieces = pack_recursive(source_path)
        bph.write(struct.pack('<I', len(pieces.chunks)))

        for chunk in pieces.chunks:
            bph.write(struct.pack('<I', len(chunk) >> 2 | 0xE0000000))

            # we save the relative number of sector from the start of the file
            bph.write(struct.pack('<I', int(bpb.tell() / 0x800)))
            bpb.write(chunk)

            # and add some padding to align
            if len(chunk) % 0x800 > 0:
                bpb.write(b'\x00' * (0x800 - (len(chunk) % 0x800)))
