import os
from datetime import date

from zope import interface, component
from zope.publisher.interfaces import NotFound
from zope.security.proxy import removeSecurityProxy
from zope.location.interfaces import ILocation
from zope.event import notify

from sqlalchemy import orm
from bungeni.alchemist import Session

from bungeni.core import interfaces
from bungeni.models import schema as dbschema
from bungeni.models import domain
from bungeni.core import audit, interfaces


def fileAddedSubscriber(ob, event):
    """ when a file is added notify the object it is added to """
    ob = removeSecurityProxy(ob)
    obj = audit.getAuditableParent(ob)
    if obj:
        event.description = u"File %s %s added" % (
                ob.file_title,
                ob.file_name)
        notify(audit.objectAttachment(obj, event))

def fileEditedSubscriber(ob, event):
    """ when a file is edited notify the parent object """
    ob = removeSecurityProxy(ob)
    obj = audit.getAuditableParent(ob)
    if obj:
        event.description = u"File %s %s edited" % (
                ob.file_title,
                ob.file_name)
        notify(audit.objectAttachment(obj, event))

# !+objectNewVersion_FILE(mr, jun-2011) rename, to reduce interference with 
# same named handler in audit.py
def objectNewVersion(ob, event):
    """When an object is versioned we copy the attachments to the version.
    """
    if type(ob) == domain.AttachedFileVersion:
        return
    ob = removeSecurityProxy(ob)
    session = Session()
    session.merge(ob)
    session.flush()
    ''' !+ATTACHED_FILE_VERSIONS(mr, sep-2011) consider alternative way to 
    handle versioning of attached_files (on versioning of head object) 
    i.e. to:
    a) to NEVER modify a db record of a file attachment
    b) if EDIT of an attachment is to be supported, expose an edit view, but
    saving a "modified" attachment means *replacing* it with a new record (and
    change-logging it as any other change?). Note, would need to record pointer
    back to "previous" version.
    c) explicit VERSIONING of an attachment (independently of its owning item) 
    should no longer be needed... given that any CHANGE in an attachment's info 
    cause a new version.
    d) versioning of an item (and of ots attachments at that time) now implies 
    only copying of FK refs to any attachments on the head object.
    
    The above has several advantages:
    
    - the several attachments are not needlessly copied over each time a head 
    object is versioned, thus reducing data duplication.
    - does not *lose* semantics in the persisted information i.e. currently a
    version of a head item points to a *version* of an attachment that is 
    in *most* cases *identical* to the "head attachment" it is versioning...
    but to know whether it *is* the same object some additional checking 
    would be needed. With this scheme, if the head item OR ANY version of it 
    have the *same logical* attachment then they would point to the SAME
    attachment db record.
    '''
    for attached_file in ob.head.attached_files:
        versions = interfaces.IVersioned(attached_file)
        version = versions.create('version created on object versioning: %s' %
                getattr(ob.change, 'description', ''))
        version.file_version_id = ob.version_id

