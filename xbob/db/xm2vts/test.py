#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the XM2VTS database.
"""

import os, sys
import unittest
import xbob.db.xm2vts

class XM2VTSDatabaseTest(unittest.TestCase):
  """Performs various tests on the XM2VTS database."""

  def test01_clients(self):
    db = xbob.db.xm2vts.Database()
    self.assertEqual(len(db.clients()), 295)
    # TODO: add more specific tests

  def test02_objects(self):
    db = xbob.db.xm2vts.Database()
    self.assertEqual(len(db.objects()), 3440)
    # TODO: add more specific tests

  def test03_annotations(self):
    # Tests that for all files the annotated eye positions exist and are in correct order
    db = xbob.db.xm2vts.Database()

    for f in db.objects():
      annotations = db.annotations(f.id)
      self.assertTrue(annotations is not None)
      self.assertEqual(len(annotations), 2)
      self.assertTrue('leye' in annotations)
      self.assertTrue('reye' in annotations)
      self.assertEqual(len(annotations['reye']), 2)
      self.assertEqual(len(annotations['leye']), 2)
      # assert that the eye positions are not exchanged
      self.assertTrue(annotations['leye'][1] > annotations['reye'][1])

  def test04_driver_api(self):

    from bob.db.script.dbmanage import main
    self.assertEqual(main('xm2vts dumplist --self-test'.split()), 0)
    self.assertEqual(main('xm2vts dumplist --protocol=lp1 --class=client --group=dev --purpose=enrol --client=10 --self-test'.split()), 0)
    self.assertEqual(main('xm2vts checkfiles --self-test'.split()), 0)
    self.assertEqual(main('xm2vts reverse frontal/342/342_2_1 --self-test'.split()), 0)
    self.assertEqual(main('xm2vts path 3011 --self-test'.split()), 0)


