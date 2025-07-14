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
from ac3es.info import InfoFile
import json


class CliInfo(BaseCliCommand):

    def __init__(self):
        self.name = 'info'
        self.help = 'Try to identify files and print useful information'
        self.args = None

    def get_parser(self, subparsers):
        parser_info = subparsers.add_parser(self.name, help=self.help)
        parser_info.add_argument(
            'FILES',
            help="One or more file to get info",
            nargs="+"
        )
        parser_info.add_argument('--format', '-f',
                                 choices=['list', 'csv', 'json'],
                                 default='list',
                                 help='Print output in different file formats')

        return subparsers

    def run_cmd(self, args):
        self.args = args
        self.guess(args.FILES)

    def guess(self, file_list):
        info = InfoFile()
        stats = []
        for x in file_list:
            stats.append(info.detect(x))

        if self.args.format == 'json':
            print(json.dumps(stats, indent=2))
        elif self.args.format == 'csv':
            print("\t".join(map(str, stats[0].keys())))
            for line in stats:
                print("\t".join(map(str, line.values())))
        else:
            pad_len = 15
            if stats:
                pad_len = len(max(stats[0].keys(), key=len))

            for item in stats:
                for key, value in item.items():
                    print(key.rjust(pad_len, ' '), value)
                print()
