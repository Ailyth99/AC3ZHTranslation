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
from ac3es.cli import helpers
from ac3es.ulz.lz77 import SlidingWindow
import array
import struct
import logging


class UlzWriter:
    signature = b'\x55\x6c\x7a\x1a'
    ulz_type = None
    nbits = None
    original_filesize = None
    flags = b''

    uncompressed_data = b''
    compressed_data = b''
    offset_compressed = None
    offset_uncompressed = None
    header = None
    sliding_window = None

    conf = {
        10: (1024, 66),
        11: (2048, 34),
        12: (4096, 18),
        13: (8192, 10)
    }

    def __init__(self, filename, ulz_type, nbits, store_only=False):
        """
        For creating a valid Ulz file we need 2 parameters, the type and
        nbits.

        The type can be 0 or 2, the difference is only how the flags
        are stored.

        nbits is the value used for correctly store the jump/run into
        the file, we have 4 type of nbits, for the TIM the most common
        value is 10 that is based on a search buffer of 1024 bytes and
        a look head uffer of 66 bytes. The rest is commonly used for
        compress binary files.

        Those values are extracted from the statistics of all the ulz
        files stored in the game.

        """

        if nbits not in self.conf.keys():
            raise Exception('nbits not valid', nbits)

        search_buffer, look_ahead_buffer = self.conf.get(nbits)

        self.filename = filename
        self.nbits = nbits

        self.sliding_window = SlidingWindow(
            self.filename,
            search_buffer,
            look_ahead_buffer,
            store_only
        )

        self.sliding_window.run()

        self.ulz_type = ulz_type
        self.original_filesize = self.sliding_window.file_size

        logging.debug('max_jump {0}\tmax_run {1}\tnbits {2}'.format(
            self.sliding_window.longest_jump,
            self.sliding_window.longest_run,
            self.nbits))

    def pack_uncompressed_data(self):
        """
        Write the uncompressed bytes, it's aligned to 32 bits
        """

        self.uncompressed_set = list()

        for x in self.sliding_window.compressed_data:
            if x['type'] == 'uncompressed':
                self.uncompressed_set.append(x['token'])

        self.uncompressed_data = array.array(
            'B',
            self.uncompressed_set
        ).tobytes()

        padding = len(self.uncompressed_data) % 4
        if padding:
            self.uncompressed_data += b'\x00' * (4 - padding)

        self.offset_uncompressed = 16 + len(self.flags)

    def pack_compressed(self):
        """
        Write compressed data stream, aligned to 32 bits
        """
        for opcode in self.sliding_window.compressed_data:
            if opcode['type'] == 'compressed':
                self.compressed_data += self.pack_jmp_run(
                    opcode['jmp'], opcode['run']
                )

        padding = len(self.compressed_data) % 4
        if padding:
            self.compressed_data += b'\x00' * (4 - padding)

        self.offset_compressed = self.offset_uncompressed + len(self.uncompressed_data)

        logging.debug("offset_compressed {:X}".format(self.offset_compressed))

    def pack_jmp_run(self, jump, run):
        """
        Creates 2 bytes for storing the jumo and run, it depends strongly
        on nbits value.
        """

        data = (((run - 3) << self.nbits) | (jump - 1)) & 0xFFFF
        return struct.pack('<H', data)

    def gen_header(self):
        """
        Creates the header for Ulz
        """

        self.header = b''.join([
            self.signature,
            struct.pack('<I', self.original_filesize)[0:3],
            struct.pack('B', self.ulz_type),
            struct.pack('<I', self.offset_uncompressed)[0:3],
            struct.pack('B', self.nbits),
            struct.pack('<I', self.offset_compressed),
        ])

    def pack_file(self):
        """
        Pack everything
        """
        self.gen_flags()
        self.pack_uncompressed_data()
        self.pack_compressed()
        self.gen_header()

    def gen_flags(self):
        """
        Creates the flags from the sliding window data
        """

        bit_flags = []
        for x in self.sliding_window.compressed_data:
            if x['type'] == 'compressed':
                bit_flags.append(False)
            else:
                bit_flags.append(True)

        if self.ulz_type == 2:
            for chunk in helpers.grouper(32, bit_flags, False):
                flag_number = 0
                for x in chunk:
                    flag_number = (flag_number << 1) | (1 if x else 0)
                self.flags += struct.pack('<I', flag_number)

        elif self.ulz_type == 0:
            for chunk in helpers.grouper(31, bit_flags, False):

                flag_number = 0
                # last bit always true
                for x in (chunk + (True,)):
                    flag_number = (flag_number << 1) | (1 if x else 0)

                self.flags += struct.pack('<I', flag_number)
        else:
            raise Exception('Ulz format not supported')

        padding = len(self.flags) % 4
        if padding:
            self.flags += b'\x00' * (4 - padding)

        # The decompression algorithm for ulz0 doesn't have any
        # counters for the final size like ulz2, it relies on the flag
        # to ends the decompression, the process ends when the code
        # loads in r11 0x00000000
        if self.ulz_type == 0:
            self.flags += b'\x00' * 4

    def save(self, dest_filename=None):
        """
        Saves the file
        """
        out_filename = dest_filename or self.filename + '.ulz'
        with open(out_filename, 'wb') as out_file:
            out_file.write(self.header)
            out_file.write(self.flags)
            out_file.write(self.uncompressed_data)
            out_file.write(self.compressed_data)

        logging.debug('wrote to ' + out_filename)


if __name__ == "__main__":
    import sys
    import logging.config

    logging.basicConfig(filename='comp.log', level=logging.DEBUG)
    u = UlzWriter(sys.argv[1], 0, 1024, 32)
    u.pack_file()
    u.save()
