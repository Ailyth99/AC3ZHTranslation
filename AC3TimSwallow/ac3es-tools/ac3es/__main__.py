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

import ac3es.cli
import ac3es.cli.helpers
from ac3es.cli import BaseCliCommand
from ac3es.exceptions import CliException
import sys
import argparse

# we need to import the classes even if we don't use them directly
from ac3es.bin import CliBin
from ac3es.bpb import CliBpb
from ac3es.info import CliInfo
from ac3es.tim import CliTim
from ac3es.ulz import CliUlz

if __name__ == '__main__':

    epilog = """Example:

    Compress an image and put the output into the same directory
      {0} ulz --compress image.tim --ulz-type=2 --level=1

    or define another destination
      {0} ulz --compress jap_0002.tim --ulz-type=2 --level=1 --output-file=mycompress.ulz

    Get what parameters use from the original file
      {0} info BPB/0386/0001/0000.ulz

    Work on bin containers
      {0} bin --split=BPB/0114/0007.bin --out-directory=splitted/0007 --out-list=splitted/0007.txt
      {0} bin --merge-list=splitted/0007.txt --out-bin=mod_0007.bin

    More parameters are available, just type help for the sub command
      {0} ulz --help
      {0} info --help
      {0} bin --help
      {0} tim --help
      {0} bpb --help

    Report bugs to: infrid@infrid.com
    AC3ES Tools Version {1}
    Homepage: <https://loadwordteam.com/>
    """.format(sys.argv[0], ac3es.cli.VERSION)

    parser = argparse.ArgumentParser(
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(help='Commands', dest='command')
    commands = {}

    for cmd in BaseCliCommand.__subclasses__():
        single_command = cmd()
        subparsers = single_command.get_parser(subparsers)
        commands[single_command.name] = single_command

    args = parser.parse_args()

    try:
        if commands.get(args.command, None):
            commands.get(args.command).run_cmd(args)
        else:
            parser.print_help()

    except CliException as e:
        print(e)
        sys.exit(-1)
