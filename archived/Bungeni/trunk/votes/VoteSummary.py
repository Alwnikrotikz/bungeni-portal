# -*- coding: utf-8 -*-
#
# File: VoteSummary.py
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
from Products.Bungeni.votes.Vote import Vote
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='Pass',
        widget=BooleanField._properties['widget'](
            label='Pass',
            label_msgid='Bungeni_label_Pass',
            i18n_domain='Bungeni',
        )
    ),

    IntegerField(
        name='NumberOfAye',
        widget=IntegerField._properties['widget'](
            label='Numberofaye',
            label_msgid='Bungeni_label_NumberOfAye',
            i18n_domain='Bungeni',
        )
    ),

    IntegerField(
        name='NumberOfNay',
        widget=IntegerField._properties['widget'](
            label='Numberofnay',
            label_msgid='Bungeni_label_NumberOfNay',
            i18n_domain='Bungeni',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

VoteSummary_schema = BaseSchema.copy() + \
    getattr(Vote, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class VoteSummary(BaseContent, Vote):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(Vote,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'VoteSummary'

    meta_type = 'VoteSummary'
    portal_type = 'VoteSummary'
    allowed_content_types = [] + list(getattr(Vote, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'VoteSummary.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "VoteSummary"
    typeDescMsgId = 'description_edit_votesummary'

    _at_rename_after_creation = True

    schema = VoteSummary_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(VoteSummary, PROJECTNAME)
# end of class VoteSummary

##code-section module-footer #fill in your manual code here
##/code-section module-footer



