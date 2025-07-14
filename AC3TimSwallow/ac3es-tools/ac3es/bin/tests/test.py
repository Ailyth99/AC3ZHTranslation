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
import unittest
import pathlib
import tempfile
import filecmp
import struct
import random
from ac3es.bin import merge
from ac3es.bin import split
from ac3es.exceptions import BinDetectException


class TestBin(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.assets_dir = pathlib.Path(__file__).parent.joinpath('assets')
        self.assets_list = pathlib.Path(__file__).parent.joinpath('assets_list.txt')
        self.assets_test_bin = pathlib.Path(__file__).parent.joinpath('assets_test.bin')

    def test_get_content(self):
        content_list_from_dir = [str(x.resolve()) for x in merge.get_content_list_from_single(self.assets_dir)]
        content_list_from_dir.sort()
        content_list_from_file = [str(x.resolve()) for x in merge.get_content_list_from_single(self.assets_list)]
        content_list_from_file.sort()

        for path in content_list_from_dir:
            self.assertFalse(path.endswith('bin_splitter_list.txt'))

        for path in content_list_from_file:
            self.assertFalse(path.endswith('bin_splitter_list.txt'))

        self.assertEqual(content_list_from_dir, content_list_from_file)

    def test_merge_all(self):
        content_list_from_dir = [x.resolve() for x in merge.get_content_list_from_single(self.assets_dir)]
        container = merge.merge_all(content_list_from_dir)

        with self.assets_test_bin.open('rb') as asset:
            data = asset.read()
            self.assertEqual(len(container), len(data))
            self.assertEqual(container, data)

    def test_merge_files(self):
        with tempfile.NamedTemporaryFile() as tmp_file:
            merge.merge_files_from_single(self.assets_dir, pathlib.Path(tmp_file.name))
            self.assertTrue(filecmp.cmp(tmp_file.name, self.assets_test_bin.resolve(), False))

    def test_split_header(self):
        offsets = [
            random.randint(20, 255),
            random.randint(20, 255),
            random.randint(20, 255),
            random.randint(20, 255),
            random.randint(20, 255)
        ]

        # remove duplicates
        offsets = list(set(offsets))

        # make sure we are monotonic
        offsets.sort()

        # test that index is correct
        with io.BytesIO() as artifact:
            artifact.write(struct.pack('<I', len(offsets)) + b''.join([struct.pack('<I', x) for x in offsets]))
            artifact.write(random.randbytes(offsets[-1] + 100))
            self.assertEqual(tuple(offsets), split.read_index(artifact))

        # test anomaly
        with io.BytesIO() as artifact:
            artifact.write(struct.pack('<I', len(offsets)) + b''.join([struct.pack('<I', x) for x in offsets]))
            artifact.write(random.randbytes(offsets[-1] + 100))
            self.assertEqual(tuple(offsets), split.read_index(artifact))

        # test anomaly
        with io.BytesIO() as artifact:
            offsets.append(offsets[-1])
            artifact.write(struct.pack('<I', len(offsets)) + b''.join([struct.pack('<I', x) for x in offsets]))
            artifact.write(random.randbytes(offsets[-1] * 2))
            self.assertRaises(BinDetectException, split.read_index, artifact)

    def test_split(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = pathlib.Path(tmp_dir)
            split.split_file(self.assets_test_bin, tmp_path)
            extracted_list = [x.resolve() for x in tmp_path.iterdir() if
                              x.is_file() and str(x).find('bin_splitter_list.txt') == -1]
            test_assets = ['lulu.tim', 'matisse.tim', 'occhietto.tim', 'occhietto_big.ulz']
            for found in extracted_list:
                self.assertTrue(filecmp.cmp(found, self.assets_dir.joinpath(test_assets.pop()), False))
