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


from ac3es.cli import BaseCliCommand
from ac3es.tim import copy_tim_data


class CliTim(BaseCliCommand):
    def __init__(self):
        self.name = 'tim'
        self.help = 'Copy TIM header information and/or replace CLUT data'

    def get_parser(self, subparsers):
        tim_parser = subparsers.add_parser(
            name=self.name,
            help=self.help
        )

        tim_parser.add_argument(
            '--source-tim',
            '-s',
            required=True,
            metavar=('TIM_FILE'),
            help='Source TIM'
        )

        tim_parser.add_argument(
            '--copy-header',
            action='store_true',
            help='Copy the entire header data from source'
        )

        tim_parser.add_argument(
            '--copy-clut',
            action='store_true',
            help='Copy CLUT data from source'
        )

        tim_parser.add_argument(
            '--copy-vram',
            action='store_true',
            help='Copy V-RAM coordinates'
        )

        tim_parser.add_argument(
            '--set-vram-x',
            type=int,
            metavar=('X'),
            help='Set V-RAM coordinate X'
        )

        tim_parser.add_argument(
            '--set-vram-y',
            type=int,
            metavar=('Y'),
            help='Set V-RAM coordinate Y'
        )

        tim_parser.add_argument(
            'FILES',
            help="Apply the changes to one or more TIM files",
            nargs="+"
        )

        return subparsers

    def run_cmd(self, args):
        for tim_file in args.FILES:
            copy_tim_data(
                args.source_tim,
                tim_file,
                args.copy_clut,
                args.copy_vram,
                args.set_vram_x,
                args.set_vram_y,
                args.copy_header
            )
