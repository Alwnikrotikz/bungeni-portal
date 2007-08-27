# -*- coding: utf-8 -*-
#
# File: Portfolio.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.6.0-beta-svn
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from Products.ATContentTypes.content.document import ATDocument
from Products.Archetypes.ReferenceEngine import ContentReferenceCreator
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.Archetypes.utils import DisplayList
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

class Portfolio(BaseContent, ATDocument):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(ATDocument,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Portfolio'

    meta_type = 'Portfolio'
    portal_type = 'Portfolio'
    allowed_content_types = [] + list(getattr(ATDocument, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Portfolio.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Portfolio"
    typeDescMsgId = 'description_edit_portfolio'

    _at_rename_after_creation = True

    schema = Portfolio_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getParliamentMembershipVocab')
    def getParliamentMembershipVocab(self):
        """
        return all current parliament members
        """
        catalog = getToolByName(self, 'portal_catalog')
        path = '/'.join(self.parliaments.getPhysicalPath())
        proxies = catalog(
                path={'query': path, 'depth':1},
                portal_type='Team Membership',
                review_state='active')
        return DisplayList([(p.UID, p.Title) for p in proxies])


registerType(Portfolio, PROJECTNAME)
# end of class Portfolio

##code-section module-footer #fill in your manual code here
##/code-section module-footer



