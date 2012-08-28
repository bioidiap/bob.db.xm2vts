#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
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
from .query import Database

class XM2VTSDatabaseTest(unittest.TestCase):
  """Performs various tests on the XM2VTS database."""

  def test01_manage_dumplist_1(self):

    from bob.db.script.dbmanage import main

    self.assertEqual(main('xm2vts dumplist --self-test'.split()), 0)

  def test02_manage_dumplist_2(self):
    
    from bob.db.script.dbmanage import main

    self.assertEqual(main('xm2vts dumplist --protocol=lp1 --classes=client --groups=dev --purposes=enrol --self-test'.split()), 0)

  def test03_manage_checkfiles(self):

    from bob.db.script.dbmanage import main

    self.assertEqual(main('xm2vts checkfiles --self-test'.split()), 0)
