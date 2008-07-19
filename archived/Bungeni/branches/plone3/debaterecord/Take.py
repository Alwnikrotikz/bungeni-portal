# -*- coding: utf-8 -*-
#
# File: Take.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from zope.interface import implements
import interfaces
from Products.ATContentTypes.content.file import ATFile
from Products.Bungeni.interfaces.ITake import ITake
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Relations.field import RelationField
from Products.Bungeni.config import *

# additional imports from tagged value 'import'
from appy.pod import renderer

##code-section module-header #fill in your manual code here
import os
import time
import tempfile
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.utils import getToolByName
import Products.Bungeni
##/code-section module-header

schema = Schema((

    RelationField(
        name='RotaItem',
        vocabulary='getRotaItemVocab',
        widget=ReferenceWidget(
            macro_edit="rotaitem_edit",
            label='Rotaitem',
            label_msgid='Bungeni_label_RotaItem',
            i18n_domain='Bungeni',
        ),
        multiValued=0,
        relationship='take_rotaitem'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Take_schema = BaseFolderSchema.copy() + \
    getattr(ATFile, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Take(BaseFolder, BrowserDefaultMixin, ATFile):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ITake, ITake)

    meta_type = 'Take'
    _at_rename_after_creation = True

    schema = Take_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getNextRotaItem')
    def getNextRotaItem(self):
        """
        """
        rota_items = self.getRotaItems()
        if not rota_items:
            self.plone_log('getNextRotaItem> No items') #DBG
            return []
        for ri in rota_items:
            if not ri.getTake():
                break
        # return the first RotaItem w/o a take, or the last one.
        self.plone_log('getNextRotaItem> %s: %s'%(ri.getId(), ri.UID())) #DBG
        return ri.UID()

    security.declarePublic('getRotaItemVocab')
    def getRotaItemVocab(self):
        """
        """
        ris = self.getRotaItems()
        return DisplayList([(ri.UID(), ri.Title()) for ri in ris])

    security.declarePublic('getRotaItems')
    def getRotaItems(self):
        """
        """
        parent = self
        while parent.portal_type != 'DebateRecordFolder':
            parent = parent.aq_parent
        rf = parent.contentValues(
                filter={'portal_type': 'RotaFolder'})
        if rf:
            rota_items = rf[0].contentValues(
                    filter={'portal_type': 'RotaItem'})
            return rota_items
        else:
            return []

    security.declarePublic('getNotAddableTypes')
    def getNotAddableTypes(self):
        """ A take can have only one transcription.
        """
        transcription = self.contentIds(
                filter={'portal_type': 'TakeTranscription'})
        if transcription:
            return ['TakeTranscription', ]
        return []

    security.declarePrivate('_generateTakeTranscription')
    def _generateTakeTranscription(self):
        """
        """
        # from ipdb import set_trace; set_trace()
        # Get our associated RotaItem
        self.setRotaItem(self.REQUEST.form['RotaItem'])
        ri = self.getRotaItem()

        # Add a new transcription
        t_id = self.generateUniqueId('TakeTranscription')
        self.invokeFactory('TakeTranscription', t_id,
                title=self.getRotaItem().Title())
        tt = self[t_id]

        # Use a template to generate a new document
        #DBG from ipdb import set_trace; set_trace()
        # fd, fn = tempfile.mkstemp()
        tempFileName = '/tmp/%s.%f.%s' % (self._at_uid, time.time(), 'odt')
        r = renderer.Renderer(
                '%s/taketranscription.odt' % os.path.dirname(
                    Products.Bungeni.__file__),
                {'InsertedText': ri.Title()},
                tempFileName)
        r.run()

        # Set that document on our transcription
        new_file = open(tempFileName, 'rb')
        tt.setFile(new_file)
        os.remove(tempFileName)

    security.declarePublic('initializeArchetype')
    def initializeArchetype(self, **kwargs):
        BaseFolder.initializeArchetype(self, **kwargs)
        ATFile.initializeArchetype(self, **kwargs)

        if self.isTemporary():
            log('initializeArchetype> Not yet!') #DBG
            return
        self._generateTakeTranscription()

    security.declarePublic('objectIds')
    def objectIds(self,spec=None, filter=None):
        """
        """
        return BaseFolder.objectIds(self, spec)

    security.declarePublic('objectValues')
    def objectValues(self,spec=None, filter=None):
        """
        """
        return BaseFolder.objectValues(self, spec)


registerType(Take, PROJECTNAME)
# end of class Take

##code-section module-footer #fill in your manual code here
##/code-section module-footer



