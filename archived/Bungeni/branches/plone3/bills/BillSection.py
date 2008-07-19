# -*- coding: utf-8 -*-
#
# File: BillSection.py
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
from zope import interface
from zope.interface import implements
import interfaces
from Products.PloneHelpCenter.content.ReferenceManualSection import HelpCenterReferenceManualSection
from Products.AuditTrail.interfaces.IAuditable import IAuditable
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BillSection_schema = BaseFolderSchema.copy() + \
    getattr(HelpCenterReferenceManualSection, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class BillSection(HelpCenterReferenceManualSection, BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IBillSection, IAuditable)

    meta_type = 'BillSection'
    _at_rename_after_creation = True

    schema = BillSection_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(BillSection, PROJECTNAME)
# end of class BillSection

##code-section module-footer #fill in your manual code here
##/code-section module-footer



