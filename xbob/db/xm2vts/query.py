#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>

"""This module provides the Dataset interface allowing the user to query the
XM2VTS database in the most obvious ways.
"""

import os
from bob.db import utils
from .models import *
from .driver import Interface

INFO = Interface()

SQLITE_FILE = INFO.files()[0]

class Database(object):
  """The dataset class opens and maintains a connection opened to the Database.

  It provides many different ways to probe for the characteristics of the data
  and for the data itself inside the database.
  """

  def __init__(self):
    # opens a session to the database - keep it open until the end
    self.connect()
  
  def connect(self):
    """Tries connecting or re-connecting to the database"""
    if not os.path.exists(SQLITE_FILE):
      self.session = None

    else:
      self.session = utils.session_try_readonly(INFO.type(), SQLITE_FILE)

  def is_valid(self):
    """Returns if a valid session has been opened for reading the database"""

    return self.session is not None

  def assert_validity(self):
    """Raise a RuntimeError if the database backend is not available"""

    if not self.is_valid():
      raise RuntimeError, "Database '%s' cannot be found at expected location '%s'. Create it and then try re-connecting using Database.connect()" % (INFO.name(), SQLITE_FILE)

  def __group_replace_alias__(self, l):
    """Replace 'dev' by 'client' and 'eval' by 'client' in a list of groups, and 
       returns the new list"""
    if not l: return l
    elif isinstance(l, str): return self.__group_replace_alias__((l,))
    l2 = []
    for val in l:
      if(val == 'dev' or val == 'eval' or val == 'world'): l2.append('client')
      else: l2.append(val)
    return tuple(set(l2))

  def __check_validity__(self, l, obj, valid, default):
    """Checks validity of user input data against a set of valid values"""
    if not l: return default
    elif not isinstance(l, (tuple,list)): 
      return self.__check_validity__((l,), obj, valid, default)
    for k in l:
      if k not in valid:
        raise RuntimeError, 'Invalid %s "%s". Valid values are %s, or lists/tuples of those' % (obj, k, valid)
    return l

  def groups(self):
    """Returns the names of all registered groups"""

    return ProtocolPurpose.group_choices

  def client_groups(self):
    """Returns the names of the XM2VTS groups. This is specific to this database which 
    does not have separate training, development and evaluation sets."""

    return Client.group_choices

  def clients(self, protocol=None, groups=None):
    """Returns a list of :py:class:`.Client` for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the XM2VTS protocols ('lp1', 'lp2', 'darkened-lp1', 'darkened-lp2').
    
    groups
      The groups to which the clients belong either from ('dev', 'eval', 'world')
      or the specific XM2VTS ones from ('client', 'impostorDev', 'impostorEval')
      Note that 'dev', 'eval' and 'world' are alias for 'client'.
      If no groups are specified, then both clients are impostors are listed.

    Returns: A list containing all the clients which have the given properties.
    """

    self.assert_validity()
    groups = self.__group_replace_alias__(groups)
    if not groups:
      groups = ('client', 'impostorDev', 'impostorEval')
    # List of the clients
    q = self.session.query(Client).filter(Client.sgroup.in_(groups)).\
          order_by(Client.id)

    return list(q)

  def models(self, protocol=None, groups=None):
    """Returns a list of :py:class:`.Client` for the specific query by the user.
       Models correspond to Clients for the XM2VTS database (At most one model per identity).

    Keyword Parameters:

    protocol
      One of the XM2VTS protocols ('lp1', 'lp2', 'darkened-lp1', 'darkened-lp2').
    
    groups
      The groups to which the subjects attached to the models belong ('dev', 'eval', 'world')
      Note that 'dev', 'eval' and 'world' are alias for 'client'.
      If no groups are specified, then both clients are impostors are listed.

    Returns: A list containing all the models (model <-> client in XM2VTS) belonging 
             to the given group.
    """

    return self.clients(protocol, groups)

  def has_client_id(self, id):
    """Returns True if we have a client with a certain integer identifier"""

    self.assert_validity()
    return self.session.query(Client).filter(Client.id==id).count() != 0

  def objects(self, protocol=None, purposes=None, model_ids=None, groups=None, 
              classes=None):
    """Returns a list of :py:class:`.File` for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the XM2VTS protocols ('lp1', 'lp2', 'darkened-lp1', 'darkened-lp2').

    purposes
      The purposes required to be retrieved ('enrol', 'probe') or a tuple
      with several of them. If 'None' is given (this is the default), it is 
      considered the same as a tuple with all possible values. This field is
      ignored for the data from the "world" group.

    model_ids
      Only retrieves the files for the provided list of model ids (claimed 
      client id). The model ids are string.  If 'None' is given (this is 
      the default), no filter over the model_ids is performed.

    groups
      One of the groups ('dev', 'eval', 'world') or a tuple with several of them. 
      If 'None' is given (this is the default), it is considered the same as a 
      tuple with all possible values.

    classes
      The classes (types of accesses) to be retrieved ('client', 'impostor') 
      or a tuple with several of them. If 'None' is given (this is the 
      default), it is considered the same as a tuple with all possible values.

    Returns: A list of :py:class:`.File` objects.
    """

    self.assert_validity()

    VALID_PROTOCOLS = self.protocol_names()
    VALID_PURPOSES = self.purposes()
    VALID_GROUPS = self.groups()
    VALID_CLASSES = ('client', 'impostor')

    protocol = self.__check_validity__(protocol, "protocol", VALID_PROTOCOLS, VALID_PROTOCOLS)
    purposes = self.__check_validity__(purposes, "purpose", VALID_PURPOSES, VALID_PURPOSES)
    groups = self.__check_validity__(groups, "group", VALID_GROUPS, VALID_GROUPS)
    classes = self.__check_validity__(classes, "class", VALID_CLASSES, VALID_CLASSES)

    if(isinstance(model_ids,str)):
      model_ids = (model_ids,)

    # Now query the database
    retval = []
    if 'world' in groups:
      q = self.session.query(File).join(Client).join(ProtocolFile).join(ProtocolPurpose).join(Protocol).\
            filter(Client.sgroup == 'client').\
            filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup == 'world'))
      if model_ids:
        q = q.filter(Client.id.in_(model_ids))
      q = q.order_by(File.client_id, File.session_id, File.darkened, File.shot_id)
      retval += list(q)
  
    if ('dev' in groups or 'eval' in groups):
      if('enrol' in purposes):
        q = self.session.query(File).join(Client).join(ProtocolFile).join(ProtocolPurpose).join(Protocol).\
              filter(Client.sgroup == 'client').\
              filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(groups), ProtocolPurpose.purpose == 'enrol'))
        if model_ids:
          q = q.filter(Client.id.in_(model_ids))
        q = q.order_by(File.client_id, File.session_id, File.darkened, File.shot_id)
        retval += list(q)

      if('probe' in purposes):
        ltmp = []
        if( 'dev' in groups):
          ltmp.append('dev')
        if( 'eval' in groups):
          ltmp.append('eval')
        dev_eval = tuple(ltmp)
        if('client' in classes):
          q = self.session.query(File).join(Client).join(ProtocolFile).join(ProtocolPurpose).join(Protocol).\
                filter(Client.sgroup == 'client').\
                filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(groups), ProtocolPurpose.purpose == 'probe'))
          if model_ids:
            q = q.filter(Client.id.in_(model_ids))
          q = q.order_by(File.client_id, File.session_id, File.darkened, File.shot_id)
          retval += list(q)

        if('impostor' in classes):
          q = self.session.query(File).join(Client).join(ProtocolFile).join(ProtocolPurpose).join(Protocol).\
          ltmp = 'client'
          if( 'dev' in groups):
            ltmp.append('impostorDev')
          if( 'eval' in groups):
            ltmp.append('impostorEval')
          impostorGroups = tuple(ltmp)
          q = self.session.query(File).join(Client).join(ProtocolFile).join(ProtocolPurpose).join(Protocol).\
                filter(Client.sgroup.in_(ltmp)).\
                filter(and_(Protocol.name.in_(protocol), ProtocolPurpose.sgroup.in_(groups), ProtocolPurpose.purpose == 'probe'))
          retval += list(q)

    return list(set(retval)) # To remove duplicates

  def protocol_names(self):
    """Returns all registered protocol names"""

    self.assert_validity()
    l = self.protocols()
    retval = []
    for k in l: retval.append(str(k.name))
    return retval

  def protocols(self):
    """Returns all registered protocols"""

    self.assert_validity()
    return list(self.session.query(Protocol))

  def has_protocol(self, name):
    """Tells if a certain protocol is available"""

    self.assert_validity()
    return self.session.query(Protocol).filter(Protocol.name==name).count() != 0

  def protocol(self, name):
    """Returns the protocol object in the database given a certain name. Raises
    an error if that does not exist."""

    self.assert_validity()
    return self.session.query(Protocol).filter(Protocol.name==name).one()

  def purposes(self):
    """Returns the list of allowed purposes"""

    return ProtocolPurpose.purpose_choices

  def paths(self, ids, prefix='', suffix=''):
    """Returns a full file paths considering particular file ids, a given
    directory and an extension

    Keyword Parameters:

    id
      The ids of the object in the database table "file". This object should be
      a python iterable (such as a tuple or list).

    prefix
      The bit of path to be prepended to the filename stem

    suffix
      The extension determines the suffix that will be appended to the filename
      stem.

    Returns a list (that may be empty) of the fully constructed paths given the
    file ids.
    """

    self.assert_validity()

    fobj = self.session.query(File).filter(File.id.in_(ids))
    retval = []
    for p in ids:
      retval.extend([k.make_path(prefix, suffix) for k in fobj if k.id == p])
    return retval

  def reverse(self, paths):
    """Reverses the lookup: from certain stems, returning file ids

    Keyword Parameters:

    paths
      The filename stems I'll query for. This object should be a python
      iterable (such as a tuple or list)

    Returns a list (that may be empty).
    """

    self.assert_validity()

    fobj = self.session.query(File).filter(File.path.in_(paths))
    for p in paths:
      retval.extend([k.id for k in fobj if k.path == p])
    return retval

