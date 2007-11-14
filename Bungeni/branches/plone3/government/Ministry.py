# -*- coding: utf-8 -*-
#
# File: Ministry.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='shortTitle',
        widget=StringWidget(
            label='Shorttitle',
            label_msgid='Bungeni_label_shortTitle',
            i18n_domain='Bungeni',
        )
    ),

    RelationField(
        name='ministrys',
        widget=ReferenceWidget(
            label='Ministrys',
            label_msgid='Bungeni_label_ministrys',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='supersedes'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Ministry_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Ministry(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IMinistry)

    meta_type = 'Ministry'
    _at_rename_after_creation = True

    schema = Ministry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Ministry, PROJECTNAME)
# end of class Ministry

##code-section module-footer #fill in your manual code here
##/code-section module-footer



