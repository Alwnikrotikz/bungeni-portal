# -*- coding: utf-8 -*-
#
# File: testDebateRecordFolder.py
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

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) DebateRecordFolder
#

from Testing import ZopeTestCase
from Products.Bungeni.config import *
from Products.Bungeni.tests.testBungeni import testBungeni

# Import the tested classes
from Products.Bungeni.debaterecord.DebateRecordFolder import DebateRecordFolder

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testDebateRecordFolder(testBungeni):
    """Test-cases for class(es) DebateRecordFolder."""

    ##code-section class-header_testDebateRecordFolder #fill in your manual code here
    ##/code-section class-header_testDebateRecordFolder

    def afterSetUp(self):
        pass

    # from class DebateRecordFolder:
    def test_getReportersForSittingVocab(self):
        pass

    # from class DebateRecordFolder:
    def test_getSpaceTeamsDefault(self):
        pass

    # from class DebateRecordFolder:
    def test_getNotAddableTypes(self):
        pass

    # from class DebateRecordFolder:
    def test_getItemsByAudiencesAndSections(self):
        pass

    # from class BungeniTeamSpace:
    def test_getAllTeamsDisplayList(self):
        pass

    # from class BungeniTeamSpace:
    def test_editTeams(self):
        pass

    # Manually created methods

    def test_getReportersMembershipVocab(self):
        pass

    def test_getReportersVocab(self):
        pass

    def test_getReporters(self):
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testDebateRecordFolder))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


