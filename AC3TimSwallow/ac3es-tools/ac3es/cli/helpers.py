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
import hashlib
import sys

from itertools import zip_longest
from ac3es.exceptions import CliException


def md5_for_file(path, block_size=256 * 128):
    """
    Block size directly depends on the block size of your filesystem
    to avoid performances issues
    Here I have blocks of 4096 octets (Default NTFS)
    """
    md5 = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                md5.update(chunk)
    except IOError:
        raise CliException("Cannot read file {}".format(path))

    return md5.hexdigest()


def prompt_file_exists(filename):
    if os.path.isfile(filename):
        print('Overwrite the file {0}? [y/n]'.format(filename), end=' ')
        choice = None
        while choice not in ('y', 'n'):
            choice = input().lower()
            if choice == 'n' or choice == 'no':
                print('abort...')
                sys.exit(-1)
            elif choice == 'y' or choice == 'yes':
                break
            else:
                print('Please answer with yes/no', end=' ')


def b2uint(number):
    """Simple function for convert the bytes in little endian to
    integer"""

    return int.from_bytes(number, byteorder='little', signed=False)


def grouper(n, iterable, fillvalue=None):
    """
    Used for packing the flags

    grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)
