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
    self.assertEqual(len(db.clients(groups='client')), 200)
    self.assertEqual(len(db.clients(groups='dev')), 200)
    self.assertEqual(len(db.clients(groups='eval')), 200)
    self.assertEqual(len(db.clients(groups='world')), 200)
    self.assertEqual(len(db.clients(groups='impostorDev')), 25)
    self.assertEqual(len(db.clients(groups='impostorEval')), 70)
    self.assertEqual(len(db.models()), 295)
    self.assertEqual(len(db.models(groups='client')), 200)
    self.assertEqual(len(db.models(groups='dev')), 200)
    self.assertEqual(len(db.models(groups='eval')), 200)
    self.assertEqual(len(db.models(groups='world')), 200)
    self.assertEqual(len(db.models(groups='impostorDev')), 25)
    self.assertEqual(len(db.models(groups='impostorEval')), 70)


  def test02_objects(self):
    db = xbob.db.xm2vts.Database()
    self.assertEqual(len(db.objects()), 3440)
    # LP1
    self.assertEqual(len(db.objects(protocol='lp1')), 2360)
    self.assertEqual(len(db.objects(protocol='lp1', groups='world')), 600)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev')), 1400)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='enrol')), 600)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe')), 800)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe', classes='client')), 600)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe', classes='impostor')), 800)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe', model_ids=[3])), 800)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe', model_ids=[3], classes='client')), 3)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe', model_ids=[3], classes='impostor')), 797)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe', model_ids=[3,4])), 800)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe', model_ids=[3,4], classes='client')), 6)
    self.assertEqual(len(db.objects(protocol='lp1', groups='dev', purposes='probe', model_ids=[3,4], classes='impostor')), 800)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval')), 1560)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='enrol')), 600)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe')), 960)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe', classes='client')), 400)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe', classes='impostor')), 960)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe', model_ids=[3])), 960)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe', model_ids=[3], classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe', model_ids=[3], classes='impostor')), 958)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe', model_ids=[3,4])), 960)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe', model_ids=[3,4], classes='client')), 4)
    self.assertEqual(len(db.objects(protocol='lp1', groups='eval', purposes='probe', model_ids=[3,4], classes='impostor')), 960)
    # LP2
    self.assertEqual(len(db.objects(protocol='lp2')), 2360)
    self.assertEqual(len(db.objects(protocol='lp2', groups='world')), 800)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev')), 1400)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev', purposes='enrol')), 800)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev', purposes='probe')), 600)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev', purposes='probe', model_ids=[3])), 600)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev', purposes='probe', model_ids=[3], classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev', purposes='probe', model_ids=[3], classes='impostor')), 598)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev', purposes='probe', model_ids=[3,4])), 600)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev', purposes='probe', model_ids=[3,4], classes='client')), 4)
    self.assertEqual(len(db.objects(protocol='lp2', groups='dev', purposes='probe', model_ids=[3,4], classes='impostor')), 600)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval')), 1760)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval', purposes='enrol')), 800)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval', purposes='probe')), 960)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval', purposes='probe', model_ids=[3])), 960)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval', purposes='probe', model_ids=[3], classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval', purposes='probe', model_ids=[3], classes='impostor')), 958)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval', purposes='probe', model_ids=[3,4])), 960)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval', purposes='probe', model_ids=[3,4], classes='client')), 4)
    self.assertEqual(len(db.objects(protocol='lp2', groups='eval', purposes='probe', model_ids=[3,4], classes='impostor')), 960)
    # Darkened-LP1
    self.assertEqual(len(db.objects(protocol='darkened-lp1')), 2480)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='world')), 600)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev')), 1400)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='enrol')), 600)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe')), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe', classes='client')), 600)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe', classes='impostor')), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe', model_ids=[3])), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe', model_ids=[3], classes='client')), 3)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe', model_ids=[3], classes='impostor')), 797)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe', model_ids=[3,4])), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe', model_ids=[3,4], classes='client')), 6)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='dev', purposes='probe', model_ids=[3,4], classes='impostor')), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval')), 1680)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='enrol')), 600)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe')), 1080)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe', classes='client')), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe', classes='impostor')), 1080)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe', model_ids=[3])), 1080)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe', model_ids=[3], classes='client')), 4)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe', model_ids=[3], classes='impostor')), 1076)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe', model_ids=[3,4])), 1080)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe', model_ids=[3,4], classes='client')), 8)
    self.assertEqual(len(db.objects(protocol='darkened-lp1', groups='eval', purposes='probe', model_ids=[3,4], classes='impostor')), 1080)
    # Darkened-LP2
    self.assertEqual(len(db.objects(protocol='darkened-lp2')), 2480)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='world')), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev')), 1400)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev', purposes='enrol')), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev', purposes='probe')), 600)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev', purposes='probe', model_ids=[3])), 600)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev', purposes='probe', model_ids=[3], classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev', purposes='probe', model_ids=[3], classes='impostor')), 598)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev', purposes='probe', model_ids=[3,4])), 600)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev', purposes='probe', model_ids=[3,4], classes='client')), 4)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='dev', purposes='probe', model_ids=[3,4], classes='impostor')), 600)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval')), 1880)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval', purposes='enrol')), 800)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval', purposes='probe')), 1080)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval', purposes='probe', model_ids=[3])), 1080)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval', purposes='probe', model_ids=[3], classes='client')), 4)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval', purposes='probe', model_ids=[3], classes='impostor')), 1076)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval', purposes='probe', model_ids=[3,4])), 1080)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval', purposes='probe', model_ids=[3,4], classes='client')), 8)
    self.assertEqual(len(db.objects(protocol='darkened-lp2', groups='eval', purposes='probe', model_ids=[3,4], classes='impostor')), 1080)


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

