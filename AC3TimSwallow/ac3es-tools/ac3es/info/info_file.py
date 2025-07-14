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

from ac3es.cli.helpers import md5_for_file
from ac3es.tim import TimReader
from ac3es.ulz.helpers import get_ulz_info
from ac3es.data.database_md5 import DatabaseMD5
from ac3es.exceptions import NotTimException


class InfoFile:
    """
    Check the hash of files or analyze the ulz
    """
    db_md5 = DatabaseMD5()

    def detect(self, path):
        if path[-3:] == 'ulz':
            return get_ulz_info(path)

        try:
            return TimReader.get_tim_info(path)
        except NotTimException:
            pass

        hash_value = md5_for_file(path)
        return self.db_md5.find(hash_value)
