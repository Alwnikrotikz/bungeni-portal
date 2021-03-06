# -*- coding: utf-8 -*-
#
# File: testInterfaces.py
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

#
# Interface tests
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Interface import Implements

from Products.Bungeni.tests.testBungeni import testBungeni


from Interface.Verify import verifyClass


from Products.Bungeni.interfaces.IMemberOfParliament import IMemberOfParliament




from Products.Bungeni.interfaces.IClerk import IClerk





class testInterfaces(testBungeni):
        
    def testInterfacesForIMemberOfParliament(self):
        '''test interface compliance for class IMemberOfParliament'''

        
        for iface in Implements.flattenInterfaces(getattr(testInterfaces,'__implements__',[])):
            self.failUnless(verifyClass(iface, IMemberOfParliament))
        
    
            
    def testInterfacesForIClerk(self):
        '''test interface compliance for class IClerk'''

        
        for iface in Implements.flattenInterfaces(getattr(testInterfaces,'__implements__',[])):
            self.failUnless(verifyClass(iface, IClerk))
        
    
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testInterfaces))
    return suite

if __name__ == '__main__':
    framework()


