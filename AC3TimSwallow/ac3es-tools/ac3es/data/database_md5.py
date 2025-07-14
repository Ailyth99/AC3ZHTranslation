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


class DatabaseMD5:
    header = (
        'DISK EXE ID',
        'DISK NO.',
        'SIZE (BIN IMAGE / BYTE)',
        'MD5 CHECKSUM (BIN IMAGE)',
        'MD5 ACE.BPB',
        'MD5 ACE.BPH',
        'MD5 ACE.BIN',
        'DATE MASTER'
    )

    database = (
        ('SLPS_020.20',
         '1',
         '716,287,488',
         '30f7dce98b6901290cb26c9baf27268f',
         '935bdbcb0c32f991c88a87d8643d0173',
         '1926254f332e61a6d753d92ad0a0165b',
         '75ee0a43693e7c1ea70e0d9784db6d76',
         '27/05/1999 01:20:00'),
        ('SLPS_020.21',
         '2',
         '723,813,888',
         '50760963ae8a26ea0188b165f05b33a1',
         '935bdbcb0c32f991c88a87d8643d0173',
         '1926254f332e61a6d753d92ad0a0165b',
         '75ee0a43693e7c1ea70e0d9784db6d76',
         '27/05/1999 01:20:00'),
        ('SLPS_020.20',
         '1',
         '716,240,448',
         '86fd694677098d26909086895404f571',
         '17fbd78d7e4b3c5643561fcad3ce9ef1',
         '48c988931078f5ed310619e2065cac16',
         '4948fa35ae276eb146a59b414ce59abc',
         '20/05/1999 02:00:00'),
        ('SLPS_020.21',
         '2',
         '723,766,848',
         'c3909981452f1506290121b2763beb24',
         '17fbd78d7e4b3c5643561fcad3ce9ef1',
         '48c988931078f5ed310619e2065cac16',
         '4948fa35ae276eb146a59b414ce59abc',
         '20/05/1999 02:00:00'),
        ('SLPS_020.20',
         '1',
         '716,287,488',
         '30f7dce98b6901290cb26c9baf27268f',
         '935bdbcb0c32f991c88a87d8643d0173',
         '1926254f332e61a6d753d92ad0a0165b',
         '75ee0a43693e7c1ea70e0d9784db6d76',
         '27/05/1999 01:20:00'),
        ('SLPS_020.21',
         '2',
         '723,813,888',
         '50760963ae8a26ea0188b165f05b33a1',
         '935bdbcb0c32f991c88a87d8643d0173',
         '1926254f332e61a6d753d92ad0a0165b',
         '75ee0a43693e7c1ea70e0d9784db6d76',
         '27/05/1999 01:20:00'),
        ('SLPS_912.14',
         '1',
         '716,240,448',
         '86fd694677098d26909086895404f571',
         '17fbd78d7e4b3c5643561fcad3ce9ef1',
         '48c988931078f5ed310619e2065cac16',
         '4948fa35ae276eb146a59b414ce59abc',
         '20/05/1999 02:00:00'),
        ('SLPS_912.15',
         '2',
         '723,766,848',
         'c3909981452f1506290121b2763beb24',
         '17fbd78d7e4b3c5643561fcad3ce9ef1',
         '48c988931078f5ed310619e2065cac16',
         '4948fa35ae276eb146a59b414ce59abc',
         '20/05/1999 02:00:00'),
    )

    def find(self, md5):
        for row in self.database:
            for col in row:
                if col == md5:
                    return dict(zip(self.header, row))
        return None
