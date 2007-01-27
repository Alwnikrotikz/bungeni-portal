# -*- coding: utf-8 -*-
#
# File: testBill.py
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

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) Bill
#

from Testing import ZopeTestCase
from Products.Bungeni.config import *
from Products.Bungeni.tests.BungeniTest import BungeniTest

# Import the tested classes
from Products.Bungeni.content.Bill import Bill

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testBill(BungeniTest):
    """Test-cases for class(es) Bill."""

    ##code-section class-header_testBill #fill in your manual code here
    ##/code-section class-header_testBill

    def afterSetUp(self):
        pass

    # from class Bill:
    def test_getTOC(self):
        pass

    # Manually created methods

    def test_operation_1(self):
        pass

    def test_operation_2(self):
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testBill))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


