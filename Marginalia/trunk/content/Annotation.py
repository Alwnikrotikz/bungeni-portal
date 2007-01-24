# -*- coding: utf-8 -*-
#
# File: Annotation.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 1.5.1-svn
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
from Products.Marginalia.config import *

##code-section module-header #fill in your manual code here
from DateTime import DateTime
##/code-section module-header

schema = Schema((

    StringField(
        name='url',
        widget=StringWidget(
            label='Url',
            label_msgid='Marginalia_label_url',
            i18n_domain='Marginalia',
        )
    ),

    StringField(
        name='range',
        widget=StringWidget(
            label='Range',
            label_msgid='Marginalia_label_range',
            i18n_domain='Marginalia',
        )
    ),

    StringField(
        name='note',
        widget=StringWidget(
            label='Note',
            label_msgid='Marginalia_label_note',
            i18n_domain='Marginalia',
        )
    ),

    StringField(
        name='access',
        widget=StringWidget(
            label='Access',
            label_msgid='Marginalia_label_access',
            i18n_domain='Marginalia',
        )
    ),

    StringField(
        name='quote',
        widget=StringWidget(
            label='Quote',
            label_msgid='Marginalia_label_quote',
            i18n_domain='Marginalia',
        )
    ),

    StringField(
        name='quote_title',
        widget=StringWidget(
            label='Quote_title',
            label_msgid='Marginalia_label_quote_title',
            i18n_domain='Marginalia',
        )
    ),

    StringField(
        name='quote_author',
        widget=StringWidget(
            label='Quote_author',
            label_msgid='Marginalia_label_quote_author',
            i18n_domain='Marginalia',
        )
    ),

    StringField(
        name='link',
        widget=StringWidget(
            label='Link',
            label_msgid='Marginalia_label_link',
            i18n_domain='Marginalia',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Annotation_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Annotation(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Annotation'

    meta_type = 'Annotation'
    portal_type = 'Annotation'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Annotation.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Annotation"
    typeDescMsgId = 'description_edit_annotation'

    _at_rename_after_creation = False

    schema = Annotation_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getUID')
    def getUID(self):
        """
        """
        return 'tag:%s,%s:%s' % ('localhost', DateTime().year, self.getId())


registerType(Annotation, PROJECTNAME)
# end of class Annotation

##code-section module-footer #fill in your manual code here
##/code-section module-footer



