# -*- coding: utf-8 -*-
##
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
## along with this program; see the file LICENSE. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# $Id: PloneGlossaryTestCase.py 54137 2007-11-19 14:49:42Z glenfant $
"""
Base test case for PloneGlossary
"""

# Python imports
import re
import os
import time
import Globals

# Zope imports
from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager

# CMF imports
from Products.CMFCore.utils import getToolByName

# Plone imports
from Products.PloneTestCase import PloneTestCase

from Products.PloneGlossary.config import INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE

# Globals
portal_name = 'portal'
portal_owner = 'portal_owner'
default_user = PloneTestCase.default_user
default_password = PloneTestCase.default_password

class PloneGlossaryTestCase(PloneTestCase.PloneTestCase):

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()

        # Configure tool
        self.glossary_tool = getToolByName(self.portal, 'portal_glossary')
        self.mb_tool = getToolByName(self.portal, 'portal_membership')
        prop_tool = getToolByName(self.portal, 'portal_properties')
        self.site_charset = prop_tool.site_properties.default_charset

    def beforeTearDown(self):
        """Remove all the stuff again.
        """

        pass

    def loginAsPortalOwner(self):
        '''Use if you need to manipulate an article as member.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)

    def encodeInSiteCharset(self, text):
        """Text is unicode text"""

        return text.encode(self.site_charset)

    def buildPrettyId(self, title):
        """Returns pretty id from title"""

        regexp = re.compile(r'[^ a-z]')
        pretty_id = regexp.sub('', title.lower())
        return pretty_id

    def addDocument(self, container, doc_title, doc_text):
        """Add document in container"""

        doc_id = self.buildPrettyId(doc_title)

        container.invokeFactory(
            type_name='Document',
            id=doc_id,
            title=doc_title,
            text=doc_text)

        return getattr(container, doc_id)

    def addFrenchDocument(self, container, doc_title):
        """Add french document in container"""

        return self.addDocument(container, doc_title, self.getFrenchText())

    def addEnglishDocument(self, container, doc_title):
        """Add english document in container"""

        return self.addDocument(container, doc_title, self.getEnglishText())

    def getFrenchText(self):
        """Returns french text"""

        return self.encodeInSiteCharset(u"""D\xe9finition d'un terme.""")

    def getEnglishText(self):
        """Returns french text"""

        return self.encodeInSiteCharset(u"""Term definition.""")

    def addGlossaryDefinition(self, glossary, title, definition=None, variants=()):
        """Add new glossary definition in a glossary"""

        if definition is None:
            definition = self.encodeInSiteCharset(u'Definition of term')

        id = self.buildPrettyId(title)
        glossary.invokeFactory(
            type_name='PloneGlossaryDefinition',
            id=id,
            title=title,
            definition=definition,
            variants=variants)

        term = getattr(glossary, id)
        return term

    def addGlossary(self, container, glossary_title, term_titles):
        """Add glossary in container with definitions"""

        # Add glossary
        glossary_id = self.buildPrettyId(glossary_title)
        container.invokeFactory(
            type_name='PloneGlossary',
            id=glossary_id,
            title=glossary_title)

        glossary = getattr(container, glossary_id)

        # Add terms
        for term_title in term_titles:
            self.addGlossaryDefinition(glossary, term_title)

        return glossary

    def addExampleGlossary(self, container, glossary_title, term_titles):
        """Add example type glossary in container with definitions"""

        # Add glossary
        glossary_id = self.buildPrettyId(glossary_title)
        container.invokeFactory(
            type_name='ExampleGlossary',
            id=glossary_id,
            title=glossary_title)

        glossary = getattr(container, glossary_id)

        # Add terms
        for term_title in term_titles:
            self.addExampleGlossaryDefinition(glossary, term_title)

        return glossary

    def addExampleGlossaryDefinition(self, glossary, title,
                                     definition=None, variants=()):
        """Add new example glossary definition in a glossary"""

        if definition is None:
            definition = self.encodeInSiteCharset(u'Definition of term')

        id = self.buildPrettyId(title)
        glossary.invokeFactory(
            type_name='ExampleGlossaryDefinition',
            id=id,
            title=title,
            definition=definition,
            variants=variants)

        term = getattr(glossary, id)
        return term

os.environ[INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE] = 'True'
from Products.PloneGlossary import config
config.UNITTESTS = True

# Install PloneGlossary
ZopeTestCase.installProduct('MimetypesRegistry')
ZopeTestCase.installProduct('PortalTransforms')
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('PloneGlossary')

# Setup Plone site
PloneTestCase.setupPloneSite(products=['Archetypes', 'PloneGlossary'])
