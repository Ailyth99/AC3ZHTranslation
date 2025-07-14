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


import io
import sys
from ac3es.cli import helpers


class UlzReader:
    """
    Read compressed Ulz files made for Ace Combat 3 version 0 and 2
    """

    def __init__(self, ulz_stream):
        """Accepts a strem for read the Ulz data, this function reads
        the header and initialize the class"""

        self.ulz_stream = ulz_stream
        self.ulz_stream.seek(0)

        self.signature = self.ulz_stream.read(4)
        if self.signature != b'Ulz\x1A':
            raise Exception('The file is not an ulz archive')

        raw_uncompressed_size = self.ulz_stream.read(3)
        self.u_type = self.ulz_stream.read(1)
        if self.u_type != b'\x00' and self.u_type != b'\x02':
            raise Exception('Format "{}" not supported'.format(self.u_type))
        self.u_type = helpers.b2uint(self.u_type)

        self.uncompressed_size = helpers.b2uint(raw_uncompressed_size)

        raw_uncompressed_offset = self.ulz_stream.read(3)
        self.nbits = self.ulz_stream.read(1)
        self.nbits = helpers.b2uint(self.nbits)

        levels = {
            10: 1,
            11: 2,
            12: 4,
            13: 8
        }

        self.level = levels.get(self.nbits)

        self.uncompressed_offset = helpers.b2uint(raw_uncompressed_offset)
        raw_compressed_offset = self.ulz_stream.read(4)
        self.compressed_offset = helpers.b2uint(raw_compressed_offset[:-1])

        self.mask_run = ((1 << self.nbits) + 0xffff) & 0xFFFF

        self.flags = []
        self.flag_start = self.ulz_stream.tell()

        self.longest_jump = 0
        self.longest_run = 0
        self.count_compressed = 0
        self.count_uncompressed = 0

    def get_flags(self):
        """Reads the flags form the ulz stream at 32bit at time, it
        returns the raw data"""

        curr = self.ulz_stream.tell()
        self.ulz_stream.seek(self.flag_start, 0)
        flags = self.ulz_stream.read(4)

        self.flag_start = self.flag_start + 4
        self.ulz_stream.seek(curr, 0)

        # from bytes to boolean, we invert the bits too
        num_flags = int.from_bytes(flags, byteorder='little')
        bool_flags = []
        for x in range(32):
            bool_flags.insert(
                0,
                False if num_flags & (1 << x) else True
            )
        bool_flags.reverse()
        return bool_flags

    def is_compressed_flag(self):
        """Flags has to be read in different ways regarding the Ulz
        version, this function makes the right decisions for ulzv0 and
        ulzV2. Returns True if we have to decompress the data."""

        try:
            is_comp = self.flags.pop()
        except IndexError:
            ba = self.get_flags()
            if self.u_type == 0:
                # The original decompressor checks for the sign in
                # the registry to figure out if we have to decompress
                # the data. It ignores the last bit because the process ends
                # when the register r11 (used for the flags) is empty.
                self.flags = ba[1:]
            else:
                # Version 2 is much simpler, uses all the bits in the
                # registry for decompression.
                self.flags = ba

            is_comp = self.flags.pop()

        return is_comp

    def decompress(self):
        """Decompress the ulz stream, returns an io.BytesIO instance"""

        c_seek = self.compressed_offset
        u_seek = self.uncompressed_offset
        decompressed_data = b''

        with io.BytesIO() as out_file:
            while out_file.tell() < self.uncompressed_size:

                if self.is_compressed_flag():
                    self.count_compressed += 1
                    self.ulz_stream.seek(c_seek, 0)
                    data = helpers.b2uint(self.ulz_stream.read(2))
                    c_seek = self.ulz_stream.tell()

                    jump = data & self.mask_run
                    jump += 1
                    run = data >> self.nbits
                    run += 3

                    self.longest_jump = max(jump, self.longest_jump)
                    self.longest_run = max(run, self.longest_run)

                    out_file.seek(0, 2)
                    curr_position = out_file.tell()
                    tmp_buff = b''

                    circular_index = 0
                    for r in range(run):
                        position = curr_position - jump + r
                        out_file.seek(position)
                        found_data = out_file.read(1)

                        if found_data == b'':
                            try:
                                found_data = tmp_buff[circular_index]
                                circular_index += 1
                            except IndexError:
                                circular_index = 0
                                found_data = tmp_buff[circular_index]

                        if isinstance(found_data, int):
                            found_data = found_data.to_bytes(1, 'little')

                        if out_file.tell() >= self.uncompressed_size:
                            tmp_buff = b''
                            sys.exit(-1)
                            break

                        tmp_buff += found_data

                    out_file.seek(0, 2)
                    out_file.write(tmp_buff)
                else:
                    self.count_uncompressed += 1
                    self.ulz_stream.seek(u_seek, 0)
                    udata = self.ulz_stream.read(1)
                    u_seek = self.ulz_stream.tell()
                    out_file.write(udata)

            self.ulz_stream.close()
            decompressed_data = out_file.getvalue()
        return decompressed_data
