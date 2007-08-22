# -*- coding: utf-8 -*-
#
# File: Office.py
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
from Products.Bungeni.groups.BungeniTeam import BungeniTeam
from Products.Bungeni.groups.BungeniTeam import BungeniTeam
from Products.Relations.field import RelationField
from Products.Bungeni.config import *

##code-section module-header #fill in your manual code here
from Products.TeamSpace.permissions import *
##/code-section module-header

schema = Schema((

    RelationField(
        name='Chairperson',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Chairperson',
            label_msgid='Bungeni_label_Chairperson',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='office_chairperson'
    ),

    RelationField(
        name='DeputyChairperson',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Deputychairperson',
            label_msgid='Bungeni_label_DeputyChairperson',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='office_deputychairperson'
    ),

    RelationField(
        name='Secretary',
        vocabulary='getMembershipVocab',
        widget=ReferenceWidget(
            label='Secretary',
            label_msgid='Bungeni_label_Secretary',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='office_secretary'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Office_schema = BaseSchema.copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    getattr(BungeniTeam, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Office(BungeniTeam):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BungeniTeam,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Office'

    meta_type = 'Office'
    portal_type = 'Office'
    allowed_content_types = [] + list(getattr(BungeniTeam, 'allowed_content_types', [])) + list(getattr(BungeniTeam, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Office.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Office"
    typeDescMsgId = 'description_edit_office'

    _at_rename_after_creation = True

    schema = Office_schema

    ##code-section class-header #fill in your manual code here
    actions = BungeniTeam.actions
    ##/code-section class-header

    # Methods

    security.declarePublic('setChairperson')
    def setChairperson(self,value,**kw):
        """
        """
        # Team:
        if value:
            uid = value[0]
            member = self.portal_bungenimembershiptool.getMemberByUID(uid)
            member_roles = self._get_member_roles(member, ['Chairperson'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Chairperson']
        return field.set(self, value, **kw)

    security.declarePublic('setDeputyChairperson')
    def setDeputyChairperson(self,value,**kw):
        """
        """
        # Team:
        if value:
            uid = value[0]
            member = self.portal_bungenimembershiptool.getMemberByUID(uid)
            member_roles = self._get_member_roles(member, ['DeputyChairperson'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['DeputyChairperson']
        return field.set(self, value, **kw)

    security.declarePublic('setSecretary')
    def setSecretary(self,value,**kw):
        """
        """
        # Team:
        if value:
            uid = value[0]
            member = self.portal_bungenimembershiptool.getMemberByUID(uid)
            member_roles = self._get_member_roles(member, ['Secretary'])
            self.manage_updateRoles(member_roles)
        # Field:
        field = self.Schema()['Secretary']
        return field.set(self, value, **kw)

    security.declareProtected(ManageTeam, 'manage_updateRoles')
    def manage_updateRoles(self,member_roles,REQUEST):
        """ Constrain some roles
        """
        constrained_roles = {
                'Chairperson': 1,
                'DeputyChairperson': 1, # TODO: verify
                'Secretary': 1,
                }
        self._constrainMembershipRoles(constrained_roles, member_roles)
        # Delegate to super
        BungeniTeam.manage_updateRoles(self,member_roles,REQUEST=None)


registerType(Office, PROJECTNAME)
# end of class Office

##code-section module-footer #fill in your manual code here
##/code-section module-footer



