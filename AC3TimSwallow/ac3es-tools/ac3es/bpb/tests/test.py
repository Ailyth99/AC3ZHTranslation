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

import filecmp
import pathlib
import tempfile
import unittest
from ac3es.bpb import pack
from ac3es.bpb import unpack


class TestBPB(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.assets_dir = pathlib.Path(__file__).parent.joinpath('assets')
        self.test_bpb = pathlib.Path(__file__).parent.joinpath('T_ACE.BPB')
        self.test_bph = pathlib.Path(__file__).parent.joinpath('T_ACE.BPH')

    def test_pack(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir_path = pathlib.Path(tmp_dir)
            some_bpb = tmp_dir_path.joinpath('ACE.BPB')
            some_bph = tmp_dir_path.joinpath('ACE.BPH')
            pack.pack_files(self.assets_dir, some_bpb, some_bph)

            self.assertTrue(filecmp.cmp(self.test_bph.resolve(), some_bph.resolve(), False))
            self.assertTrue(filecmp.cmp(self.test_bpb.resolve(), some_bpb.resolve(), False))

    def test_unpack(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir_path = pathlib.Path(tmp_dir)
            unpack.unpack_files(tmp_dir_path, self.test_bpb, self.test_bph)
            test_assets = ['lulu.tim', 'matisse.tim', 'occhietto.tim', 'occhietto_big.ulz']
            for found in tmp_dir_path.iterdir():
                self.assertTrue(filecmp.cmp(found, self.assets_dir.joinpath(test_assets.pop()), False))
