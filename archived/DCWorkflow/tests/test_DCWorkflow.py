##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Unit tests for DCWorkflow module.

$Id: test_DCWorkflow.py 40346 2005-11-23 17:15:03Z yuppie $
"""

from unittest import TestCase, TestSuite, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from Products.CMFCore.tests.base.dummy import DummyContent
from Products.CMFCore.tests.base.dummy import DummySite
from Products.CMFCore.tests.base.dummy import DummyTool
from Products.CMFCore.WorkflowTool import WorkflowTool

from zope.interface import Interface
from zope.component import provideHandler, adapter
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

class DCWorkflowDefinitionTests(TestCase):

    def setUp(self):
        self.site = DummySite('site')
        self.site._setObject( 'portal_types', DummyTool() )
        self.site._setObject( 'portal_workflow', WorkflowTool() )
        self._constructDummyWorkflow()

    def test_z2interfaces(self):
        from Interface.Verify import verifyClass
        from Products.CMFCore.interfaces.portal_workflow \
             import WorkflowDefinition as IWorkflowDefinition
        from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

        verifyClass(IWorkflowDefinition, DCWorkflowDefinition)

    def test_z3interfaces(self):
        try:
            from zope.interface.verify import verifyClass
            from Products.CMFCore.interfaces import IWorkflowDefinition
        except ImportError:
            # BBB: for Zope 2.7
            return
        from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

        verifyClass(IWorkflowDefinition, DCWorkflowDefinition)

    def _constructDummyWorkflow(self):
        from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

        wftool = self.site.portal_workflow
        wftool._setObject('wf', DCWorkflowDefinition('wf'))
        wftool.setDefaultChain('wf')
        wf = wftool.wf

        wf.states.addState('private')
        sdef = wf.states['private']
        sdef.setProperties( transitions=('publish',) )

        wf.states.addState('published')
        wf.states.setInitialState('private')

        wf.transitions.addTransition('publish')
        tdef = wf.transitions['publish']
        tdef.setProperties(title='', new_state_id='published', actbox_name='')

        wf.variables.addVariable('comments')
        vdef = wf.variables['comments']
        vdef.setProperties(description='',
                 default_expr="python:state_change.kwargs.get('comment', '')",
                 for_status=1, update_always=1)

    def _getDummyWorkflow(self):
        wftool = self.site.portal_workflow
        return wftool.wf

    def test_doActionFor(self):

        wftool = self.site.portal_workflow
        wf = self._getDummyWorkflow()

        dummy = self.site._setObject( 'dummy', DummyContent() )
        wftool.notifyCreated(dummy)
        self.assertEqual( wf._getStatusOf(dummy),
                          {'state': 'private', 'comments': ''} )
        wf.doActionFor(dummy, 'publish', comment='foo' )
        self.assertEqual( wf._getStatusOf(dummy),
                          {'state': 'published', 'comments': 'foo'} )

        # XXX more

    def test_events(self):
        
        events = []
        
        @adapter(IBeforeTransitionEvent)
        def _handleBefore(event):
            events.append(event)
        provideHandler(_handleBefore)
    
        @adapter(IAfterTransitionEvent)
        def _handleAfter(event):
            events.append(event)
        provideHandler(_handleAfter)
        
        wftool = self.site.portal_workflow
        wf = self._getDummyWorkflow()

        dummy = self.site._setObject( 'dummy', DummyContent() )
        wftool.notifyCreated(dummy)
        wf.doActionFor(dummy, 'publish', comment='foo', test='bar')
        
        self.assertEquals(4, len(events))
        
        evt = events[0]
        self.failUnless(IBeforeTransitionEvent.providedBy(evt))
        self.assertEquals(dummy, evt.object)
        self.assertEquals('private', evt.old_state.id)
        self.assertEquals('private', evt.new_state.id)
        self.assertEquals(None, evt.transition)
        self.assertEquals({}, evt.status)
        self.assertEquals(None, evt.kwargs)
        
        evt = events[1]
        self.failUnless(IAfterTransitionEvent.providedBy(evt))
        self.assertEquals(dummy, evt.object)
        self.assertEquals('private', evt.old_state.id)
        self.assertEquals('private', evt.new_state.id)
        self.assertEquals(None, evt.transition)
        self.assertEquals({}, evt.status)
        self.assertEquals(None, evt.kwargs)
        
        evt = events[2]
        self.failUnless(IBeforeTransitionEvent.providedBy(evt))
        self.assertEquals(dummy, evt.object)
        self.assertEquals('private', evt.old_state.id)
        self.assertEquals('published', evt.new_state.id)
        self.assertEquals('publish', evt.transition.id)
        self.assertEquals({'state': 'private', 'comments': ''}, evt.status)
        self.assertEquals({'test' : 'bar', 'comment' : 'foo'}, evt.kwargs)
        
        evt = events[3]
        self.failUnless(IAfterTransitionEvent.providedBy(evt))
        self.assertEquals(dummy, evt.object)
        self.assertEquals('private', evt.old_state.id)
        self.assertEquals('published', evt.new_state.id)
        self.assertEquals('publish', evt.transition.id)
        self.assertEquals({'state': 'private', 'comments': ''}, evt.status)
        self.assertEquals({'test' : 'bar', 'comment' : 'foo'}, evt.kwargs)

    def test_checkTransitionGuard(self):

        wftool = self.site.portal_workflow
        wf = self._getDummyWorkflow()
        dummy = self.site._setObject( 'dummy', DummyContent() )
        wftool.notifyCreated(dummy)
        self.assertEqual( wf._getStatusOf(dummy),
                          {'state': 'private', 'comments': ''} )

        # Check
        self.assert_(wf._checkTransitionGuard(wf.transitions['publish'],
                                              dummy))

        # Check with kwargs propagation
        self.assert_(wf._checkTransitionGuard(wf.transitions['publish'],
                                              dummy, arg1=1, arg2=2))

    def test_isActionSupported(self):

        wf = self._getDummyWorkflow()
        dummy = self.site._setObject( 'dummy', DummyContent() )

        # check publish
        self.assert_(wf.isActionSupported(dummy, 'publish'))

        # Check with kwargs.
        self.assert_(wf.isActionSupported(dummy, 'publish', arg1=1, arg2=2))

    # XXX more tests...


def test_suite():
    return TestSuite((
        makeSuite(DCWorkflowDefinitionTests),
        ))

if __name__ == '__main__':
    main(defaultTest='test_suite')
