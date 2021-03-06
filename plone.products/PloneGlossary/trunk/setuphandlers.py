# -*- coding: utf-8 -*-
## Copyright (C) 2007 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# $Id: setuphandlers.py 56062 2007-12-21 19:10:04Z glenfant $

"""
Handlers for GS
"""
from content.PloneGlossary import PloneGlossary
from utils import registerGlossary, LOG
import config

def registerGlossaries(context):
    if context.readDataFile('ploneglossary.txt') is None:
        # GS sometimes sucks. Without this, GS will always try to run this
        # whatever product is imported
        return

    site = context.getSite()
    registerGlossary(site, PloneGlossary, LOG)
    if config.INSTALL_EXAMPLES:
        from Products.PloneGlossary.examples.exampleglossary import ExampleGlossary
        registerGlossary(site, ExampleGlossary, LOG)
    return "Glossary(ies) registered"

