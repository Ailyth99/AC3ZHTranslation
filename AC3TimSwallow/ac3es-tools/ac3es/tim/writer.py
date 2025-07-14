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
import struct

from ac3es.exceptions import CliException, NotTimException
from ac3es.tim import TimReader


def copy_tim_data(source_path, dest_path, replace_clut=False, replace_vram=False, vram_x=None, vram_y=None,
                  replace_header=False):
    if pathlib.Path(source_path).resolve() == pathlib.Path(dest_path).resolve():
        raise CliException('cannot operate on the same file')

    try:
        with open(source_path, 'rb') as source_stream, open(dest_path, 'rb+') as dest_stream:
            source_tim = TimReader(source_stream)
            dest_tim = TimReader(dest_stream)

            if replace_header:
                source_stream.seek(0)
                header = source_stream.read(source_tim.offsets['header_end'])
                dest_stream.seek(0)
                dest_stream.write(header)

            if replace_clut:
                if source_tim.bpp not in (4, 8):
                    raise CliException('Source is {}bpp, clut data is only for 4bpp or 8bpp'.format(source_tim.bpp))

                if dest_tim.bpp not in (4, 8):
                    raise CliException('Destination is {}bpp, clut data is only for 4bpp or 8bpp'.format(dest_tim.bpp))

                if dest_tim.bpp != source_tim.bpp:
                    raise CliException(
                        'BBP must to be the same, source {}bpp, destination {}bpp'.format(source_tim.bpp, dest_tim.bpp))

                source_stream.seek(source_tim.offsets['clut_header_start'], 0)
                clut = source_stream.read(
                    source_tim.offsets['clut_header_end'] - source_tim.offsets['clut_header_start']
                )
                dest_stream.seek(dest_tim.offsets['clut_header_start'], 0)
                dest_stream.write(clut)

            if replace_vram:
                dest_stream.seek(dest_tim.offsets['vram_x'], 0)
                dest_stream.write(struct.pack('<H', source_tim.vram_x))
                dest_stream.seek(dest_tim.offsets['vram_y'], 0)
                dest_stream.write(struct.pack('<H', source_tim.vram_y))

            if vram_x is not None:
                if vram_x < 0 or vram_x > 65535:
                    raise CliException('vram-x out of range (0-65535)')

                dest_stream.seek(dest_tim.offsets['vram_x'], 0)
                dest_stream.write(struct.pack('<H', vram_x))

            if vram_y is not None:
                if vram_y < 0 or vram_y > 65535:
                    raise CliException('vram-y out of range (0-65535)')

                dest_stream.seek(dest_tim.offsets['vram_y'], 0)
                dest_stream.write(struct.pack('<H', vram_y))
    except NotTimException as e:
        raise CliException(str(e))
