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
import os
import pathlib
import tempfile
import struct
import array
import logging
from lz77 import SlidingWindow

class UlzReader:
    """
    Read compressed Ulz files made for Ace Combat 3 version 0 and 2
    """

    def __init__(self, ulz_stream):
        """Accepts a stream for reading the Ulz data, this function reads
        the header and initializes the class"""
        self.ulz_stream = ulz_stream
        self.ulz_stream.seek(0)

        self.signature = self.ulz_stream.read(4)
        if self.signature != b'Ulz\x1A':
            raise Exception('The file is not an ulz archive')

        raw_uncompressed_size = self.ulz_stream.read(3)
        self.u_type = self.ulz_stream.read(1)
        if self.u_type != b'\x00' and self.u_type != b'\x02':
            raise Exception('Format "{}" not supported'.format(self.u_type))
        self.u_type = self.b2uint(self.u_type)

        self.uncompressed_size = self.b2uint(raw_uncompressed_size)

        raw_uncompressed_offset = self.ulz_stream.read(3)
        self.nbits = self.ulz_stream.read(1)
        self.nbits = self.b2uint(self.nbits)

        levels = {
            10: 1,
            11: 2,
            12: 4,
            13: 8
        }

        self.level = levels.get(self.nbits)

        self.uncompressed_offset = self.b2uint(raw_uncompressed_offset)
        raw_compressed_offset = self.ulz_stream.read(4)
        self.compressed_offset = self.b2uint(raw_compressed_offset[:-1])

        self.mask_run = ((1 << self.nbits) + 0xffff) & 0xFFFF

        self.flags = []
        self.flag_start = self.ulz_stream.tell()

        self.longest_jump = 0
        self.longest_run = 0
        self.count_compressed = 0
        self.count_uncompressed = 0

    def b2uint(self, b):
        return int.from_bytes(b, byteorder='little')

    def get_flags(self):
        """Reads the flags from the ulz stream 32 bits at a time, it
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
        """Flags have to be read in different ways regarding the Ulz
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
                    data = self.b2uint(self.ulz_stream.read(2))
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
        a look ahead buffer of 66 bytes. The rest is commonly used for
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

        self.reset()

    def reset(self):
        """Reset the internal state for a new compression."""
        self.flags = b''
        self.uncompressed_data = b''
        self.compressed_data = b''
        self.offset_compressed = None
        self.offset_uncompressed = None
        self.header = None
        self.sliding_window.reset()

    def pack_uncompressed_data(self):
        """
        Write the uncompressed bytes, it's aligned to 32 bits
        """
        self.uncompressed_set = []

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
        Creates 2 bytes for storing the jump and run, it depends strongly
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
        self.reset()  # Reset state before packing
        self.sliding_window.run()  # 确保运行压缩
        self.gen_flags()
        self.pack_uncompressed_data()
        self.pack_compressed()
        self.gen_header()
        
        # 添加日志输出
        logging.debug(f"Packed file: flags={len(self.flags)}, uncompressed={len(self.uncompressed_data)}, compressed={len(self.compressed_data)}")

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
            for chunk in self.grouper(32, bit_flags):
                flag_number = 0
                for x in chunk:
                    flag_number = (flag_number << 1) | (1 if x else 0)
                self.flags += struct.pack('<I', flag_number)

        elif self.ulz_type == 0:
            for chunk in self.grouper(31, bit_flags):
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
        # to end the decompression, the process ends when the code
        # loads in r11 0x00000000
        if self.ulz_type == 0:
            self.flags += b'\x00' * 4

    def save(self, dest_filename=None):
        """
        Save the compressed file
        """
        if not dest_filename:
            dest_filename = self.filename + '.ulz'

        with open(dest_filename, 'wb') as f:
            f.write(self.header)
            f.write(self.flags)
            f.write(self.uncompressed_data)
            f.write(self.compressed_data)
        
        # 添加日志输出
        logging.debug(f"Saved file: {dest_filename}, size={os.path.getsize(dest_filename)}")

    def grouper(self, n, iterable):
        "Collect data into fixed-length chunks or blocks"
        args = [iter(iterable)] * n
        return zip(*args)

def compress_file(input_file, output_file=None, ulz_type=2, level=2, store_only=False, create_parents=True, like_file=None, keep=False):
    input_file = pathlib.Path(input_file)
    original_input_file = pathlib.Path(input_file)

    if input_file.stat().st_size == 0:
        raise Exception('{} is empty'.format(input_file.resolve()))

    if not output_file:
        output_file = input_file.with_suffix('.ulz')
    else:
        output_file = pathlib.Path(output_file)

    # Remove the original extension from the output file name
    if output_file.suffixes:
        output_file = output_file.with_name(output_file.stem).with_suffix('.ulz')

    recompress_flag = input_file.resolve() == output_file.resolve()

    if not recompress_flag and create_parents:
        output_file.parent.mkdir(0o755, True, True)

    level2nbits = {
        1: 10,
        2: 11,
        4: 12,
        8: 13
    }
    nbits = None

    if like_file:
        try:
            like_file = pathlib.Path(like_file)
            with like_file.open('rb') as ulz_file:
                ulz_stream = io.BytesIO(ulz_file.read())
                ulz_like_file = UlzReader(ulz_stream)
                ulz_type = ulz_like_file.u_type
                nbits = ulz_like_file.nbits

        except IOError as err:
            raise Exception("Error reading the file {0}: {1}".format(like_file, err))
    else:
        nbits = level2nbits.get(level, None)
        if nbits is None:
            raise Exception('Select the correct compression level')

    tmp_input_dec = None
    if recompress_flag:
        tmp_input_dec = tempfile.NamedTemporaryFile(delete=False)
        with input_file.open('rb') as ulz_file:
            ulz_stream = io.BytesIO(ulz_file.read())
            ulz_input = UlzReader(ulz_stream)
            data = ulz_input.decompress()
            if not data:
                raise Exception('No actual data into {}'.format(ulz_input))
            tmp_input_dec.write(data)
            tmp_input_dec.flush()

        if ulz_like_file.u_type == ulz_input.u_type and ulz_like_file.level == ulz_input.level:
            print('SKIP ', input_file)
            os.unlink(tmp_input_dec.name)
            return None

        input_file = pathlib.Path(tmp_input_dec.name)

    try:
        ulz_writer = UlzWriter(
            str(input_file.resolve()),  # 确保使用字符串路径
            ulz_type,
            nbits,
            store_only
        )
        ulz_writer.pack_file()
        ulz_writer.save(str(output_file.resolve()))
        
        # 添加日志输出
        logging.info(f"Compressed file: {input_file} -> {output_file}")
        logging.info(f"Original size: {input_file.stat().st_size}, Compressed size: {output_file.stat().st_size}")
    except Exception as exp:
        logging.error(f"Compression error: {exp}")
        raise
    finally:
        if tmp_input_dec:
            tmp_input_dec.close()
            os.unlink(tmp_input_dec.name)

def decompress_file(ulz_path, dest_filename=None, create_parents=True, create_ulz_data=False, keep=False,
                    ulz_data_name='ulz_data'):
    file_path = pathlib.Path(ulz_path)

    try:
        with file_path.open('rb') as ulz_file:
            ulz_stream = io.BytesIO(ulz_file.read())
    except IOError as err:
        raise Exception("Error reading the file {0}: {1}".format(ulz_path, err))

    ulz_reader = UlzReader(ulz_stream)
    data = ulz_reader.decompress()

    if dest_filename:
        file_path = pathlib.Path(dest_filename)
    else:
        file_path = file_path.with_suffix('')

    data_type = '.dat'

    if data[0:4] == b'\x10\x00\x00\x00':
        data_type = '.tim'

    if create_ulz_data:
        file_path = pathlib.Path(file_path.parent, ulz_data_name, file_path.stem)

    file_path = file_path.resolve() if dest_filename else file_path.with_suffix(data_type)

    if create_parents or create_ulz_data:
        file_path.parent.mkdir(0o755, True, True)

    # Write the data directly to the final file
    with file_path.open('wb') as out_file:
        out_file.write(data)

    return data