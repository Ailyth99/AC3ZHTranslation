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
from ac3es.exceptions import CliException
from ac3es.cli import helpers
from ac3es.cli import BaseCliCommand
from ac3es.ulz import UlzReader, UlzWriter


class CliUlz(BaseCliCommand):

    def __init__(self):
        self.name = 'ulz'
        self.help = 'Compress, decompress and manipulate ULZ files.'

    def get_parser(self, subparsers):
        parser_ulz = subparsers.add_parser(self.name, help=self.help)
        sub_ulz = parser_ulz.add_mutually_exclusive_group()

        sub_ulz.add_argument(
            '--compress',
            '-c',
            metavar=('FILE'),
            help='Compress a file in ULZ format, recompress the file if already compressed.'
        )

        compression = parser_ulz.add_argument_group('compression')
        compression.add_argument(
            '--ulz-type', '-t',
            choices=(0, 2),
            type=int,
            help='Define the ulz version to use'
        )

        compression.add_argument(
            '--level',
            '-l',
            choices=(1, 2, 4, 8),
            type=int,
            help='Compression levels 1/2/4/8 uses a search buffer 1024/2048/4096/8192 bytes long.'
        )

        compression.add_argument(
            '--store-only',
            '-s',
            action='store_true',
            help='Store data on ulz file, needs anyway a compression level'
        )

        compression.add_argument(
            '--like-file',
            help='Get compression parameters from file'
        )

        sub_ulz.add_argument(
            '--decompress',
            '-d',
            metavar=('ULZ'),
            help='decompress the file in the current directory'
        )

        parser_ulz.add_argument(
            '--output-file',
            '-f',
            metavar=('FILE'),
            help='override output filename'
        )

        parser_ulz.add_argument(
            '--parents',
            '-p',
            action='store_true',
            help="Create directories for destination files if they don't exists"
        )

        parser_ulz.add_argument(
            '--keep',
            '-k',
            action='store_true',
            help='prompt before every removal or destructive change'
        )

        return subparsers

    def run_cmd(self, args):
        if args.decompress:
            self.decompress_file(
                args.decompress,
                args.output_file,
                args.parents,
                False,
                args.keep
            )
        elif args.compress:
            self.compress_file(
                args.compress,
                args.output_file,
                args.ulz_type,
                args.level,
                args.store_only,
                args.parents,
                args.like_file,
                args.keep
            )

    def decompress_file(self, ulz_path, dest_filename=None, create_parents=True, create_ulz_data=False, keep=False,
                        ulz_data_name='ulz_data'):
        """
        Decompress the files from command like using UlzReader
        """

        file_path = pathlib.Path(ulz_path)

        try:
            with file_path.open('rb') as ulz_file:
                ulz_stream = io.BytesIO(ulz_file.read())
        except IOError as err:
            raise CliException("Error reading the file {0}: {1}".format(ulz_path, err))

        ulz_reader = UlzReader(ulz_stream)
        data = ulz_reader.decompress()

        if dest_filename:
            file_path = pathlib.Path(dest_filename)

        data_type = '.dat'

        if data[0:4] == b'\x10\x00\x00\x00':
            data_type = '.tim'

        if create_ulz_data:
            file_path = pathlib.Path(file_path.parent, ulz_data_name, file_path.stem)

        file_path = file_path.resolve() if dest_filename else file_path.with_suffix(data_type)

        if create_parents or create_ulz_data:
            file_path.parent.mkdir(0o644, True, True)

        if keep:
            helpers.prompt_file_exists(str(file_path.resolve()))

        with file_path.open('wb') as out_file:
            out_file.write(data)

    def compress_file(self, input_file, output_file=None, ulz_type=2, level=2, store_only=False, create_parents=True,
                      like_file=None,
                      keep=False):
        """
        Compress the files using the classes UlzWriter
        """

        input_file = pathlib.Path(input_file)
        original_input_file = pathlib.Path(input_file)

        if input_file.stat().st_size == 0:
            raise CliException('{} is empty'.format(input_file.resolve()))

        if not output_file:
            output_file = input_file.with_suffix('.ulz')
        else:
            output_file = pathlib.Path(output_file)

        recompress_flag = input_file.resolve() == output_file.resolve()

        if not recompress_flag and keep:
            helpers.prompt_file_exists(output_file.resolve())

        if not recompress_flag and create_parents:
            output_file.parent.mkdir(0o644, True, True)

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
                raise CliException("Error reading the file {0}: {1}".format(like_file, err))
        else:
            nbits = level2nbits.get(level, None)
            if nbits is None:
                raise CliException('Select the correct compression level')

        # if input and output are the same, we are going to re-compress this file

        tmp_input_dec = None
        if recompress_flag:
            tmp_input_dec = tempfile.NamedTemporaryFile(delete=False)
            with input_file.open('rb') as ulz_file:
                ulz_stream = io.BytesIO(ulz_file.read())
                ulz_input = UlzReader(ulz_stream)
                data = ulz_input.decompress()
                if not data:
                    raise CliException('No actual data into {}'.format(ulz_input))
                tmp_input_dec.write(data)
                tmp_input_dec.flush()

            if ulz_like_file.u_type == ulz_input.u_type and ulz_like_file.level == ulz_input.level:
                print('SKIP ', input_file)
                os.unlink(tmp_input_dec.name)
                return None

            input_file = pathlib.Path(tmp_input_dec.name)

        try:
            ulz_writer = UlzWriter(
                input_file.resolve(),
                ulz_type,
                nbits,
                store_only
            )
            ulz_writer.pack_file()
            ulz_writer.save(str(output_file.resolve()))
        except ValueError as exp:
            raise CliException(
                '{} {} {} {} {}'.format(exp, input_file.resolve(), tmp_input_dec, original_input_file.resolve(),
                                        output_file))
        finally:
            if tmp_input_dec:
                print('ULZ {} type {}:{} level {}:{}'.format(output_file.resolve(), ulz_like_file.u_type,
                                                             ulz_input.u_type,
                                                             ulz_like_file.level, ulz_input.level))
                input_file.unlink()
