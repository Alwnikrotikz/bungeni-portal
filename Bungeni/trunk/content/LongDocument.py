# -*- coding: utf-8 -*-
#
# File: LongDocument.py
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
from Products.PloneHelpCenter.content.ReferenceManual import HelpCenterReferenceManual
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

LongDocument_schema = BaseFolderSchema.copy() + \
    getattr(HelpCenterReferenceManual, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class LongDocument(BaseFolder, HelpCenterReferenceManual):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (getattr(HelpCenterReferenceManual,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Long Document'

    meta_type = 'LongDocument'
    portal_type = 'LongDocument'
    allowed_content_types = ['LongDocumentSection', 'ATImage', 'ATFile', 'LongDocumentPage']
    filter_content_types = 1
    global_allow = 1
    #content_icon = 'LongDocument.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "A document consisting of multiple pages or sections."
    typeDescMsgId = 'description_edit_longdocument'

    _at_rename_after_creation = True

    schema = LongDocument_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declareProtected(permissions.View, 'getTOC')
    def getTOC(self,current,root):
        """ See HelpCenterReferenceManual.getTOC for documentation.
        We're only overriding the query.
        """
        if not root:
            root = self

        class Strategy(NavtreeStrategyBase):

            rootPath = '/'.join(root.getPhysicalPath())
            showAllParents = False

        strategy = Strategy()
        # Custom query for Bungeni:
        query=  {'path'        : '/'.join(root.getPhysicalPath()),
                 'portal_type' : ('LongDocumentSection', 'LongDocumentPage',),
                 'sort_on'     : 'getObjPositionInParent'}

        toc = buildFolderTree(self, current, query, strategy)['children']

        def buildNumbering(nodes, base=""):
            idx = 1
            for n in nodes:
                numbering = "%s%d." % (base, idx,)
                n['numbering'] = numbering
                buildNumbering(n['children'], numbering)
                idx += 1

        buildNumbering(toc)
        return toc


registerType(LongDocument, PROJECTNAME)
# end of class LongDocument

##code-section module-footer #fill in your manual code here
##/code-section module-footer



