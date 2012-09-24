#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>

"""Checks for installed files.
"""

import os
import sys

# Driver API
# ==========

def checkfiles(args):
  """Checks existence of files based on your criteria"""

  from .query import Database
  db = Database()

  r = db.objects(
      protocol=args.protocol,
      purposes=args.purposes,
      #model_ids=args.model_ids,
      groups=args.groups
      )

  # go through all files, check if they are available on the filesystem
  good = []
  bad = []
  for f in r:
    if os.path.exists(f.make_path(args.directory, args.extension)):
      good.append(f)
    else: 
      bad.append(f)

  # report
  output = sys.stdout
  if args.selftest:
    from bob.db.utils import null
    output = null()

  if bad:
    for f in bad:
      output.write('Cannot find file "%s"\n' % (f.make_path(args.directory, args.extension),))
    output.write('%d files (out of %d) were not found at "%s"\n' % \
      (len(bad), len(r), args.directory))

  return 0

def add_command(subparsers):
  """Add specific subcommands that the action "checkfiles" can use"""

  from argparse import SUPPRESS

  parser = subparsers.add_parser('checkfiles', help=checkfiles.__doc__)

  from .query import Database

  db = Database()

  parser.add_argument('-d', '--directory', dest="directory", default='', help="if given, this path will be prepended to every entry returned (defaults to '%(default)s')")
  parser.add_argument('-e', '--extension', dest="extension", default='', help="if given, this extension will be appended to every entry returned (defaults to '%(default)s')")
  parser.add_argument('-p', '--protocol', dest="protocol", default='', help="if given, limits the check to a particular subset of the data that corresponds to the given protocol (defaults to '%(default)s')", choices=db.protocol_names())
  parser.add_argument('-u', '--purposes', dest="purposes", default='', help="if given, this value will limit the output files to those designed for the given purposes. (defaults to '%(default)s')", choices=db.purposes())
  # TODO: model_ids
  parser.add_argument('-g', '--groups', dest="groups", default='', help="if given, this value will limit the output files to those belonging to a particular protocolar group. (defaults to '%(default)s')", choices=db.groups())
  parser.add_argument('-c', '--classes', dest="classes", default='', help="if given, this value will limit the output files to those belonging to the given classes. (defaults to '%(default)s')", choices=('client', 'impostor', ''))
  parser.add_argument('--self-test', dest="selftest", default=False,
      action='store_true', help=SUPPRESS)

  parser.set_defaults(func=checkfiles) #action
