# -*- coding: utf-8 -*-
## Copyright (C) 2007 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# $Id: config.py 54658 2007-11-29 14:04:01Z glenfant $
"""
Global configuration data
"""

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from customconfig import *

# ZCTextIndex patch setup

# don't patch by default
PATCH_ZCTextIndex = False

# condition for adding glossaries items in indexed text
INDEX_SEARCH_GLOSSARY = ('SearchableText',)

# CMF imports
from Products.CMFCore import permissions as CMFCorePermissions

from Products.CMFPlone.utils import getFSVersionTuple
PLONE_VERSION = getFSVersionTuple()[:2] # as (2, 1)
del getFSVersionTuple

PROJECTNAME = 'PloneGlossary'
I18N_DOMAIN = PROJECTNAME.lower()
GLOBALS = globals()
SKINS_DIR = 'skins'
CONFIGLET_ICON = "ploneglossary_tool.gif"
PLONEGLOSSARY_TOOL = 'portal_glossary'
PLONEGLOSSARY_CATALOG = 'glossary_catalog'
UNITTESTS = False # Forced to True in unit tests framework
INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE = 'PLONEGLOSSARY_INSTALL_EXAMPLES'
import os
INSTALL_EXAMPLES = bool(UNITTESTS or
                        os.environ.get(INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE))
del os
