# encoding: utf-8

from zope import component
from bungeni.core.workflows.notification import Notification
from bungeni.core.workflows import interfaces
from bungeni.core import globalsettings as prefs
from bungeni.core.i18n import _
import zope.securitypolicy.interfaces
import bungeni.core.workflows.utils as utils
from bungeni.core.workflows import dbutils

class conditions:
    @staticmethod
    def is_scheduled(info, context):
        return dbutils.isItemScheduled(context.tabled_document_id)

class actions:
    @staticmethod
    def denyAllWrites(tabled_document):
        """
        remove all rights to change the question from all involved roles
        """
    #    rpm = zope.securitypolicy.interfaces.IRolePermissionMap( tabled_document )
    #    rpm.denyPermissionToRole( 'bungeni.tabled_document.edit', u'bungeni.Owner' )
    #    rpm.denyPermissionToRole( 'bungeni.tabled_document.edit', u'bungeni.Clerk' )
    #    rpm.denyPermissionToRole( 'bungeni.tabled_document.edit', u'bungeni.Speaker' )
    #    rpm.denyPermissionToRole( 'bungeni.tabled_document.edit', u'bungeni.MP' )
    #    rpm.denyPermissionToRole( 'bungeni.tabled_document.delete', u'bungeni.Owner' )
    #    rpm.denyPermissionToRole( 'bungeni.tabled_document.delete', u'bungeni.Clerk' )
    #    rpm.denyPermissionToRole( 'bungeni.tabled_document.delete', u'bungeni.Speaker' )
    #    rpm.denyPermissionToRole( 'bungeni.tabled_document.delete', u'bungeni.MP' )    

    @staticmethod
    def postpone(info,context):
        utils.setTabledDocumentHistory(info,context)

    @staticmethod
    def create( info, context ):
        user_id = utils.getUserId()
        if not user_id:
            user_id ='-'
        zope.securitypolicy.interfaces.IPrincipalRoleMap( context ).assignRoleToPrincipal( u'bungeni.Owner', user_id)   
        utils.setParliamentId(info, context)
        owner_id = utils.getOwnerId( context )
        if owner_id and (owner_id != user_id):
            zope.securitypolicy.interfaces.IPrincipalRoleMap( context 
                ).assignRoleToPrincipal( u'bungeni.Owner', owner_id)  

    @staticmethod
    def submit( info, context ):
        utils.setSubmissionDate(info, context)


    @staticmethod
    def received_by_clerk( info, context ):
        utils.createVersion(info, context)   

    @staticmethod
    def require_edit_by_mp( info, context ):
        utils.createVersion(info,context)


    @staticmethod
    def complete( info, context ):
        utils.createVersion(info,context)
 

    @staticmethod
    def approve( info, context ):
        utils.setApprovalDate(info,context)

    @staticmethod
    def reject( info, context ):
        pass

    @staticmethod
    def require_amendment( info, context ):
        utils.createVersion(info,context)


    @staticmethod
    def complete_clarify( info, context ):
        utils.createVersion(info,context)


    @staticmethod
    def mp_clarify( info, context ):
        utils.createVersion(info,context)


    @staticmethod
    def schedule( info, context ):
        pass

    @staticmethod
    def defer( info, context):
        pass

    @staticmethod
    def elapse( info, context ):
        pass

    @staticmethod
    def schedule( info, context ):
        pass

    @staticmethod
    def debate( info, context ):
        pass

    @staticmethod
    def withdraw( info, context ):  
        pass

class SendNotificationToMemberUponReceipt(Notification):
    component.adapts(interfaces.ITabledDocumentReceivedEvent)

    body = _('notification_email_to_member_upon_receipt_of_tabled_document',
             default="TabledDocument received.")
    
    @property
    def subject(self):
        return u'TabledDocument received: %s' % self.context.short_name

    @property
    def condition(self):
        return self.context.receive_notification

    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()
    
class SendNotificationToClerkUponSubmit(Notification):
    """Send notification to Clerk's office upon submit.

    We need to settings from a global registry to determine whether to
    send this notification and where to send it to.
    """

    component.adapts(interfaces.ITabledDocumentSubmittedEvent)

    body = _('notification_email_to_clerk_upon_submit_of_tabled_document',
             default="TabledDocument submitted.")

    @property
    def subject(self):
        return u'TabledDocument submitted: %s' % self.context.short_name

    @property
    def condition(self):
        return prefs.getClerksOfficeRecieveNotification()
    
    @property
    def recipient_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponReject(Notification):
    """Issued when a tabled_document was rejected by the speakers office.
    Sends a notice that the TabledDocument was rejected"""

    component.adapts(interfaces.ITabledDocumentRejectedEvent)

    body = _('notification_email_to_member_upon_rejection_of_tabled_document',
             default="TabledDocument rejected.")

    @property
    def subject(self):
        return u'TabledDocument rejected: %s' % self.context.short_name

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getSpeakersOfficeEmail()

class SendNotificationToMemberUponNeedsClarification(Notification):
    """Issued when a tabled_document needs clarification by the MP
    sends a notice that the tabled_document needs clarification"""

    component.adapts(interfaces.ITabledDocumentClarifyEvent)

    body = _('notification_email_to_member_upon_need_clarification_of_tabled_document',
             default="Your tabled_document needs to be clarified.")

    @property
    def subject(self):
        return u'TabledDocument needs clarification: %s' % self.context.short_name

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponDeferred(Notification):
    """Issued when a tabled_document was deferred by Clerk's office."""

    component.adapts(interfaces.ITabledDocumentDeferredEvent)

    body = _('notification_email_to_member_upon_defer_of_tabled_document',
             default="TabledDocument deferred.")

    @property
    def subject(self):
        return u'TabledDocument deferred: %s' % self.context.short_name

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getSpeakersOfficeEmail()

class SendNotificationToMemberUponSchedule(Notification):
    """Issued when a tabled_document was scheduled by Speakers office.
    Sends a Notice that the tabled_document is scheduled for ... """

    component.adapts(interfaces.ITabledDocumentScheduledEvent)

    body = _('notification_email_to_member_upon_schedule_of_tabled_document',
             default="TabledDocument scheduled.")

    @property
    def subject(self):
        return u'TabledDocument scheduled: %s' % self.context.short_name

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponPostponed(Notification):
    """Issued when a tabled_document was postponed by the speakers office.
    sends a notice that the tabled_document could not be debated and was postponed"""

    component.adapts(interfaces.ITabledDocumentPostponedEvent)

    body = _('notification_email_to_member_upon_postpone_of_tabled_document',
             default="TabledDocument postponed.")

    @property
    def subject(self):
        return u'TabledDocument postponed: %s' % self.context.short_name

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

class SendNotificationToMemberUponDebated(Notification):
    """Issued when a tabled_document was debated."""

    component.adapts(interfaces.ITabledDocumentDebatedEvent)

    body = _('notification_email_to_member_upon_debate_of_tabled_document',
             default=u"TabledDocument was debated.")
    @property
    def subject(self):
        return u'TabledDocument was debated: %s' % self.context.short_name

    @property
    def condition(self):
        return self.context.receive_notification
    
    @property
    def from_address(self):
        return prefs.getClerksOfficeEmail()

