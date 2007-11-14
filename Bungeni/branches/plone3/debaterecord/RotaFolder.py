# -*- coding: utf-8 -*-
#
# File: RotaFolder.py
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
from Products.Bungeni.interfaces.IRotaFolder import IRotaFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Bungeni.config import *

# additional imports from tagged value 'import'
from Products.OrderableReferenceField import OrderableReferenceField

##code-section module-header #fill in your manual code here
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Products.Archetypes.utils import log
##/code-section module-header

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].default_method = "defaultTitle"
schema = Schema((

    OrderableReferenceField(
        name='ReportersForSitting',
        vocabulary='getReportersForSittingVocab',
        widget=OrderableReferenceField._properties['widget'](
            macro_edit="reportersforsitting_edit",
            label='Reportersforsitting',
            label_msgid='Bungeni_label_ReportersForSitting',
            i18n_domain='Bungeni',
        ),
        allowed_types=['Staff'],
        relationship="rotafolder_reportersforsitting",
        relation_implementation="basic"
    ),

    ComputedField(
        name='RotaFrom',
        widget=ComputedField._properties['widget'](
            label='Rotafrom',
            label_msgid='Bungeni_label_RotaFrom',
            i18n_domain='Bungeni',
        )
    ),

    ComputedField(
        name='RotaTo',
        widget=ComputedField._properties['widget'](
            label='Rotato',
            label_msgid='Bungeni_label_RotaTo',
            i18n_domain='Bungeni',
        )
    ),

    copied_fields['title'],

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RotaFolder_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RotaFolder(OrderedBaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IRotaFolder, IRotaFolder)

    meta_type = 'RotaFolder'
    _at_rename_after_creation = True

    schema = RotaFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getRotaFrom')
    def getRotaFrom(self):
        """
        """
        parent = self
        while parent.portal_type != 'Sitting':
            parent = parent.aq_parent
        return parent.start()

    security.declarePublic('getRotaTo')
    def getRotaTo(self):
        """
        """
        parent = self
        while parent.portal_type != 'Sitting':
            parent = parent.aq_parent
        return parent.end()

    security.declarePublic('publishRota')
    def publishRota(self, state_change, kw):
        """ Do everything that needs to be done when the Rota is
        published.
        """
        # Finalize RotaItems (make them non-editable).
        items = self.contentValues(
                    filter={'portal_type': 'RotaItem'})
        workflow_tool = getToolByName(self, 'portal_workflow')
        for item in items:
            try:
                workflow_tool.doActionFor(item, 'finalize',
                        comment='Finalize as part of Rota publication')
            except WorkflowException, e:
                log('publishRota> %s: %s'%(self.getId(), e))

        self._createRotaDocument()
        self._notifySubscribers()

    security.declarePublic('retractRota')
    def retractRota(self, state_change, kw):
        """
        """
        # Retract RotaItems (make them editable again).
        items = self.contentValues(
                    filter={'portal_type': 'RotaItem'})
        workflow_tool = getToolByName(self, 'portal_workflow')
        for item in items:
            workflow_tool.doActionFor(item, 'retract',
                    comment='Retract as part of Rota retraction')

        self.manage_delObjects('rota-document')

    security.declarePublic('defaultTitle')
    def defaultTitle(self):
        """
        """
        parent = self.aq_parent
        while parent.Type() != 'Sitting':
            parent = parent.aq_parent
        return 'Rota for %s'%(parent.Title())

    security.declarePublic('reindexOnReorder')
    def reindexOnReorder(self, parent):
        """ Catalog ordering support """
        # Copied from PloneTool.reindexOnReorder
        # We're just indexing some more.
        mtool = getToolByName(self, 'portal_membership')
        if not mtool.checkPermission(permissions.ModifyPortalContent, parent):
            return
        cat = getToolByName(self, 'portal_catalog')
        cataloged_objs = cat(path = {'query':'/'.join(parent.getPhysicalPath()),
                                     'depth': 1})
        for brain in cataloged_objs:
            obj = brain.getObject()
            # Don't crash when the catalog has contains a stale entry
            if obj is not None:
                cat.reindexObject(obj,['getObjPositionInParent', 'Title'],)
            else:
                # Perhaps we should remove the bad entry as well?
                log('Object in catalog no longer exists, cannot reindex: %s.'% brain.getPath())

    security.declarePrivate('_createRotaDocument')
    def _createRotaDocument(self):
        """
        """
        items = self.contentValues(
                    filter={'portal_type': 'RotaItem'})
        paragraph = "%s: %s (for %s to %s)\n %s\n\n"
        title = "Rota for %s on %s"%(
            self.aq_parent.aq_parent.Title(),
            self.getRotaFrom().Date())
        paragraphs = ["%s\n%s\n\n"%(title, '='*len(title))]
        for item in items:
            paragraphs.append(paragraph%(
                item.getItemOrder()+1,
                item.getItemFromWithLead().TimeMinutes(),
                item.getItemFrom().TimeMinutes(),
                item.getItemTo().TimeMinutes(),
                item.getReporter().Title(),
                ))
        portal_types = getToolByName(self, 'portal_types')
        # Use constructContent to bypass allowed types constraint.
        did = portal_types.constructContent('Document', self,
                'rota-document',
                title=title,
                text=''.join(paragraphs))
        document = getattr(self, did)
        plone_utils = getToolByName(self, 'plone_utils')
        plone_utils.editMetadata(document, format='text/x-rst')

        # XXX
        self.REQUEST.RESPONSE.redirect(document.absolute_url())

    security.declarePrivate('_notifySubscribers')
    def _notifySubscribers(self):
        """ Send the summary rota document to all the subscribers
        """
        # TODO Consider making this more sophisticated: allow teams as
        # subscribers (mail to all team members); maybe use one of the
        # newsletter products to do the sending more reliably, with more
        # features ..
        rota_tool = getToolByName(self, 'portal_rotatool')
        properties_tool = getToolByName(self, 'portal_properties')
        subscribers = rota_tool.getRotaSubscribers()
        rota_document = getattr(self, 'rota-document')
        if not rota_document:
            return
        for s in subscribers:
            email = s.getEmail()
            if email:
                self.MailHost.send(rota_document.getRawText(), email,
                        properties_tool.email_from_address,
                        subject=rota_document.Title())
            else:
                log('notifySubscribers> %s has no email address'%s.Title())

    security.declareProtected(permissions.ModifyPortalContent, 'initializeArchetype')
    def initializeArchetype(self, **kwargs):
        OrderedBaseFolder.initializeArchetype(self, **kwargs)

        if self.isTemporary():
            log('initializeArchetype> Not yet.')
            return

        rt = getToolByName(self, 'portal_rotatool')

        self.setReportersForSitting(self.REQUEST.form['ReportersForSitting'])
        reporters = self.getReportersForSitting()

        # Get the lead/extra times as a fraction of a day (1440 minutes)
        lead_time_fraction = rt.getReportingLeadTime() / 1440.00
        extra_time_fraction = (
                (rt.getExtraTakes() * rt.getTakeLength()) / 1440.00)

        start_time = self.getRotaFrom() - lead_time_fraction
        end_time = self.getRotaTo() + extra_time_fraction
        duration_in_minutes = (end_time - start_time) * 1440.00
        iterations = duration_in_minutes / rt.getTakeLength()
        reporter_index = 0

        # Generate the rota
        for n in range(iterations):
            if reporter_index == len(reporters):
                reporter_index = 0
            r = reporters[reporter_index]
            reporter_index += 1
            ri_id = self.generateUniqueId('RotaItem')
            self.invokeFactory('RotaItem', ri_id, Reporter=r.UID())


registerType(RotaFolder, PROJECTNAME)
# end of class RotaFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



