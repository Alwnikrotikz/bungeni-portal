# -*- coding: utf-8 -*-
#
# File: Bungeni.py
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


from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import ExternalMethod

##code-section module-header #fill in your manual code here
##/code-section module-header

def installWorkflows(self, package, out):
    """Install the custom workflows for this product."""

    productname = 'Bungeni'
    workflowTool = getToolByName(self, 'portal_workflow')

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                                        productname+'.'+'BungeniWorkflow',
                                        'createBungeniWorkflow')
    workflow = ourProductWorkflow(self, 'BungeniWorkflow')
    if 'BungeniWorkflow' in workflowTool.listWorkflows():
        print >> out, 'BungeniWorkflow already in workflows.'
    else:
        workflowTool._setObject('BungeniWorkflow', workflow)
    workflowTool.setChainForPortalTypes(['ATFile', 'LegislationFolder'], workflow.getId())

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                                        productname+'.'+'WestminsterBillWorkflow',
                                        'createWestminsterBillWorkflow')
    workflow = ourProductWorkflow(self, 'WestminsterBillWorkflow')
    if 'WestminsterBillWorkflow' in workflowTool.listWorkflows():
        print >> out, 'WestminsterBillWorkflow already in workflows.'
    else:
        workflowTool._setObject('WestminsterBillWorkflow', workflow)
    workflowTool.setChainForPortalTypes(['Bill'], workflow.getId())

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                                        productname+'.'+'SubWorkflow',
                                        'createSubWorkflow')
    workflow = ourProductWorkflow(self, 'SubWorkflow')
    if 'SubWorkflow' in workflowTool.listWorkflows():
        print >> out, 'SubWorkflow already in workflows.'
    else:
        workflowTool._setObject('SubWorkflow', workflow)
    workflowTool.setChainForPortalTypes(['BillSection', 'BillPage', 'HansardSection', 'HansardPage'], workflow.getId())

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                                        productname+'.'+'HansardWorkflow',
                                        'createHansardWorkflow')
    workflow = ourProductWorkflow(self, 'HansardWorkflow')
    if 'HansardWorkflow' in workflowTool.listWorkflows():
        print >> out, 'HansardWorkflow already in workflows.'
    else:
        workflowTool._setObject('HansardWorkflow', workflow)
    workflowTool.setChainForPortalTypes(['Hansard'], workflow.getId())

    ##code-section after-workflow-install #fill in your manual code here
    workflowTool.setDefaultChain('BungeniWorkflow')
    workflowTool.updateRoleMappings()
    ##/code-section after-workflow-install

    return workflowTool

def uninstallWorkflows(self, package, out):
    """Deinstall the workflows.

    This code doesn't really do anything, but you can place custom
    code here in the protected section.
    """

    ##code-section workflow-uninstall #fill in your manual code here
    workflowTool = getToolByName(self, 'portal_workflow')
    workflowTool.setDefaultChain('plone_workflow')
    workflowTool.updateRoleMappings()
    ##/code-section workflow-uninstall

    pass
