# -*- coding: utf-8 -*-
#
# File: Portfolio.py
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
from Products.ATContentTypes.content.document import ATDocument
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Archetypes.ReferenceEngine import ContentReferenceCreator
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    RelationField(
        name='Minister',
        widget=ReferenceWidget(
            label='Minister',
            label_msgid='Bungeni_label_Minister',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='portfolio_minister'
    ),

    RelationField(
        name='AssistentMinister',
        widget=ReferenceWidget(
            label='Assistentminister',
            label_msgid='Bungeni_label_AssistentMinister',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='portfolio_assistentminister'
    ),

    RelationField(
        name='notMinister',
        vocabulary='getParliamentMembershipVocab',
        widget=ReferenceWidget(
            label='Notminister',
            label_msgid='Bungeni_label_notMinister',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='Minister'
    ),

    RelationField(
        name='notAssistantMinister',
        vocabulary='getParliamentMembershipVocab',
        widget=ReferenceWidget(
            label='Notassistantminister',
            label_msgid='Bungeni_label_notAssistantMinister',
            i18n_domain='Bungeni',
        ),
        multiValued=1,
        relationship='AssistantMinister'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Portfolio_schema = BaseSchema.copy() + \
    getattr(ATDocument, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Portfolio(BaseContent, ATDocument, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IPortfolio)

    meta_type = 'Portfolio'
    _at_rename_after_creation = True

    schema = Portfolio_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getParliamentMembershipVocab')
    def getParliamentMembershipVocab(self):
        """
        """
        pass


registerType(Portfolio, PROJECTNAME)
# end of class Portfolio

##code-section module-footer #fill in your manual code here
##/code-section module-footer



