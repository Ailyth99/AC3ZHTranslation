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

from ac3es.cli import BaseCliCommand
from ac3es.bin import split_file
from ac3es.bin import merge_files_from_single, merge_files_from_multi


class CliBin(BaseCliCommand):

    def __init__(self):
        self.name = 'bin'
        self.help = 'Split and merge bin container files'

    def get_parser(self, subparsers):

        parser_bin = subparsers.add_parser(
            self.name,
            help=self.help
        )
        sub_bin_splitter = parser_bin.add_mutually_exclusive_group()

        sub_bin_splitter.add_argument(
            '--split',
            '-s',
            metavar=('BIN_FILE'),
            help='Split a bin container'
        )

        bin_splitter = parser_bin.add_argument_group('bin split')
        bin_splitter.add_argument(
            '--out-directory',
            '-d',
            metavar=('DIRECTORY'),
            help='Output directory where to store the bin\'s components'
        )

        bin_splitter.add_argument(
            '--out-list',
            '-f',
            metavar=('DIRECTORY'),
            help='Save a components\' list to a txt'
        )

        sub_bin_splitter.add_argument(
            '--merge-dir',
            metavar=('DIR'),
            help='Create a bin file from a directory, entries will be sorted alphabetically'
        )

        sub_bin_splitter.add_argument(
            '--merge-list',
            metavar=('FILE_LIST'),
            help='Use a file with filenames to create a bin, sorts the names first alphabetically'
        )

        sub_bin_splitter.add_argument(
            '--merge-files',
            metavar=('FILES'),
            nargs='+',
            help='Reconstruct a bin file starting from a list of given filenames, no sort applies'
        )

        bin_splitter.add_argument(
            '--out-bin',
            '-b',
            metavar=('FILE_BIN'),
            help='Output bin filename'
        )

        bin_splitter.add_argument(
            '--verbose',
            '-v',
            action='store_true',
            help='Print more information while merges'
        )

        return subparsers

    def run_cmd(self, args):
        if args.split:
            split_file(
                pathlib.Path(args.split),
                pathlib.Path(args.out_directory) if args.out_directory else None,
                args.out_list
            )
        elif args.merge_dir:
            merge_files_from_single(
                pathlib.Path(args.merge_dir),
                pathlib.Path(args.out_bin),
                args.verbose
            )
        elif args.merge_list:
            merge_files_from_single(
                pathlib.Path(args.merge_list),
                pathlib.Path(args.out_bin),
                args.verbose
            )
        elif args.merge_files:
            merge_files_from_multi(
                [pathlib.Path(x).resolve() for x in args.merge_files],
                pathlib.Path(args.out_bin),
                args.verbose
            )
