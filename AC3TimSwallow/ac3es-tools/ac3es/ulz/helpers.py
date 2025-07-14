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

from ac3es.exceptions import CliException
from ac3es.ulz import UlzReader
from ac3es.cli import helpers


def get_ulz_info(ulz_path):
    try:
        with open(ulz_path, 'rb') as ulz_file:
            ulz_stream = io.BytesIO(ulz_file.read())
            ulz = UlzReader(ulz_stream)
            ulz.decompress()

            return {
                'path': ulz_path,
                'type': ulz.u_type,
                'level': ulz.level,
                'nbits': ulz.nbits,
                'longest_jump': ulz.longest_jump,
                'longest_run': ulz.longest_run,
                'ulz_size': os.path.getsize(ulz_path),
                'file_size': ulz.uncompressed_size,
                'md5': helpers.md5_for_file(ulz_path)
            }

    except IOError as err:
        raise CliException("Error reading the file {0}: {1}".format(ulz_path, err))
