# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""User Workspaces

$Id: workspace.py 6567 2010-05-10 17:11:09Z mario.ruggier $
"""
log = __import__("logging").getLogger("bungeni.ui.workspace")

import sys

from zope import component
from zope import interface
from zope.app.publication.traversers import SimpleComponentTraverser
from zope.location.interfaces import ILocation
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IHTTPRequest
from zope.security.proxy import ProxyFactory
from zope.security.proxy import removeSecurityProxy
from zope.annotation.interfaces import IAnnotations

from sqlalchemy import sql

from ore.alchemist import Session

from bungeni.core.i18n import _
from bungeni.core.content import Section, QueryContent
from bungeni.core.proxy import LocationProxy
from bungeni.core.interfaces import ISchedulingContext
from bungeni.core.schedule import format_date
from bungeni.core.dc import IDCDescriptiveProperties

from bungeni.models import interfaces as model_interfaces
from bungeni.models import domain
from bungeni.models.utils import container_getter
from bungeni.models.utils import get_db_user_id
from bungeni.models.utils import get_roles
from bungeni.models.utils import get_group_ids_for_user_in_parliament 
from bungeni.models.utils import get_ministries_for_user_in_government
from bungeni.models.utils import get_current_parliament
from bungeni.models.utils import get_current_parliament_governments

from bungeni.ui.utils import url, misc, debug
from bungeni.ui import interfaces

# !+ move this to ui/browser.py
class BungeniBrowserView(BrowserView):
    
    # View subclasses may set a custom page_title by overriding this attribute
    # Note: title values are localized in the template itself.
    _page_title = None
    
    @property
    def page_title(self):
        """Formalize view.page_title as a view property to factor the logic for 
        determining the page title for a view out of the template. 
        Templates should always simply call view.page_title.
        """
        if self._page_title:
            return self._page_title
        if getattr(self.context, "title"):
            return self.context.title 
        try:
            # This is the equivalent of the ZPT expression "context/dc:title"
            # i.e. to "load the value of the variable context, then find a 
            # component that adapts that object to Dublin Core and read the 
            # title attribute of the component."
            return IDCDescriptiveProperties(self.context).title
        except (Exception,):
            debug.log_exc(sys.exc_info(), log_handler=log.debug)
            return "Bungeni"

def prepare_user_workspaces(event):
    """Determine the current principal's workspaces, depending on roles and
    group memberships. 
    
    "bungeni.Clerk", "bungeni.Speaker", "bungeni.MP"
        these roles get a parliament-level workspace
    
    "bungeni.Minister"
        "implied" role (by being a member of a ministry group) 
        gets a ministry-level workspace (for each ministry)
    
    "zope.Manager", "bungeni.Admin", "bungeni.Owner", "bungeni.Everybody", 
    "bungeni.Anybody"
        not relevant for user workspaces, no workspaces
        !+ should these get an owner-level (user) workspace?
    
    """
    request = event.request
    application = event.object # is bungeni.core.app.BungeniApp
    destination_url_path = url.get_destination_url_path(request)
    def need_to_prepare_workspaces(obj, req):
        return (
            # need only to do it when traversing "/", 
            # obj should be the BungeniApplication
            model_interfaces.IBungeniApplication.providedBy(obj)
            and
            # user is logged in
            interfaces.IBungeniAuthenticatedSkin.providedBy(req)
            and (
                # either the request should be for a view within /workspace
                # note: IWorkspaceSectionLayer is applied to the request by 
                # publication.apply_request_layer_by_url() that therefore must 
                # have already been called
                interfaces.IWorkspaceSectionLayer.providedBy(req)
                or 
                # or the request is for *the* Home Page (as in this case
                # we still need to know the user workspaces to be able to 
                # redirect appropriately)
                interfaces.IHomePageLayer.providedBy(req)
            )
        )
    if not need_to_prepare_workspaces(application, request):
        return
    
    # initialize a layer data object, for the views in the layer
    LD = IAnnotations(request)["layer_data"] = misc.bunch(
        workspaces=[], # workspace containers !+ unique?
        # !+ role-based workspaces: (role|group, workspace_container)
        # these are needed by the views, as we need them also here, we just
        # remember them to not need to calculate them again
        user_id=None,
        user_group_ids=None,
        government_id=None,
        ministries=None, # list of ministries (that are also workspaces)
    )
    
    LD.user_id = get_db_user_id()
    try:
        parliament = get_current_parliament(None)
        assert parliament is not None # force exception
        # we do get_roles under the current parliament as context, but we 
        # must also ensure that the BungeniApp is present somewhere along 
        # the __parent__ stack:
        parliament.__parent__ = application
        roles = get_roles(parliament)
        # "bungeni.Clerk", "bungeni.Speaker", "bungeni.MP"
        for role_id in roles:
            if role_id in ("bungeni.Clerk", "bungeni.Speaker", "bungeni.MP"):
                log.debug("adding parliament workspace %s (for role %s)" % (
                                                        parliament, role_id))
                LD.workspaces.append(parliament)
    
        # "bungeni.Minister"
        # need to check for ministry groups to which the principal belongs, and 
        # for each such ministry assign a ministry workspace
        LD.user_group_ids = get_group_ids_for_user_in_parliament(
                                    LD.user_id, parliament.group_id)
        LD.government_id = get_current_parliament_governments(
                                    parliament)[0].group_id # IndexError
        LD.ministries = get_ministries_for_user_in_government(
                                            LD.user_id, LD.government_id)
        log.debug(""" [prepare_user_workspaces]
            user_id:%s
            parliament:(%s, %s) 
            government_id:%s
            ministries:%s""" % (
                LD.user_id, 
                parliament.full_name, parliament.group_id, 
                LD.government_id, 
                [(m.full_name, m.group_id) for m in LD.ministries] ))
        for ministry in LD.ministries:
            log.debug("adding ministry workspace %s" % ministry)
            LD.workspaces.append(ministry)
    except (Exception,):
        debug.log_exc_info(sys.exc_info(), log_handler=log.info)
    
    # ensure unique workspaces, preserving order, retaining same list obj ref
    LD.workspaces[:] = [ workspace for i,workspace in enumerate(LD.workspaces) 
                         if LD.workspaces.index(workspace)==i ]
    
    # mark each workspace container with IWorkspaceContainer
    for workspace in LD.workspaces:
        interface.alsoProvides(workspace, interfaces.IWorkspaceContainer)
        log.debug(debug.interfaces(workspace))
    
    log.debug(" [prepare_user_workspaces] %s" % debug.interfaces(request))
    log.info(""" [prepare_user_workspaces] DONE:
        for: [request=%s][path=%s][path_info=%s]
        request.layer_data: %s""" % (
            id(request), destination_url_path, request.get("PATH_INFO"),
            IAnnotations(request).get("layer_data", None)))

# traversers

def workspace_resolver(context, request, name):
    """Get the workspace domain object identified by name.
    
    Raise zope.publisher.interfaces.NotFound if no container found.
    This is a callback for the "/workspace" Section (the context here), 
    to resolve which domain object is the workspace container.
    """
    if name.startswith("obj-"):
        obj_id = int(name[4:])
        for workspace in IAnnotations(request)["layer_data"].workspaces:
            if obj_id==workspace.group_id:
                log.debug("[workspace_resolver] name=%s workspace=%s context=%s" % (
                                        name, workspace, context))
                assert interfaces.IWorkspaceContainer.providedBy(workspace)
                assert ILocation.providedBy(workspace)
                # update location for workspace
                workspace.__parent__ = context
                workspace.__name__ = name
                return workspace
    raise NotFound(context, name, request)


class WorkspaceContainerTraverser(SimpleComponentTraverser):
    """Custom Workspace (domain IBungeniGroup object) container traverser.
    This object is the "root" of each user's workspace.
    """
    interface.implementsOnly(IPublishTraverse)
    component.adapts(interfaces.IWorkspaceContainer, IHTTPRequest)
    
    def __init__(self, context, request):
        assert interfaces.IWorkspaceContainer.providedBy(context)
        self.context = context # workspace domain object
        self.request = request
        log.debug(" __init__ %s context=%s url=%s" % (
                        self, self.context, request.getURL()))
    
    def publishTraverse(self, request, name):
        workspace = self.context
        _meth_id = "%s.publishTraverse" % self.__class__.__name__
        log.debug("%s: name=%s context=%s " % (_meth_id, name, workspace))
        if name=="pi":
            return getWorkSpacePISection(workspace)
        elif name=="archive":
            return getWorkSpaceArchiveSection(workspace)
        elif name=="calendar":
            #return ISchedulingContext(workspace)
            view = component.queryMultiAdapter(
                        (workspace, request), name="workspace-calendar")
            if view is None:
                raise NotFound(workspace, name)
            return view
        
        return super(WorkspaceContainerTraverser, 
                        self).publishTraverse(request, name)


# contexts

ARCHIVED = ("debated", "withdrawn", "response_complete", "elapsed")

# Note: for all the following QueryContent "sections", we want to keep 
# title=None so that no menu item for the entry will be displayed

def getWorkSpacePISection(workspace):
    """ /workspace/obj-id/pi -> non-ARCHIVED parliamentary items
    """
    s = Section(title=_(u"Parliamentary items"),
            description=_(u"Current parliamentary activity"),
            default_name="workspace-pi")
    interface.alsoProvides(s, interfaces.IWorkspacePIContext)
    s.__parent__ = workspace
    s.__name__ = "pi"
    s["questions"] = QueryContent(
            container_getter(workspace, 'questions',
            query_modifier=sql.not_(domain.Question.status.in_(ARCHIVED))),
            #title=_(u"Questions"),
            description=_(u"Questions"))
    s["motions"] = QueryContent(
            container_getter(workspace, 'motions',
                query_modifier=sql.not_(domain.Motion.status.in_(ARCHIVED))),
            #title=_(u"Motions"),
            description=_(u"Motions"))
    s["tableddocuments"] = QueryContent(
            container_getter(workspace, 'tableddocuments',
                query_modifier=sql.not_(domain.TabledDocument.status.in_(ARCHIVED))),
            #title=_(u"Tabled documents"),
            description=_(u"Tabled documents"))
    s["bills"] = QueryContent(
            container_getter(workspace, 'bills',
                query_modifier=sql.not_(domain.Bill.status.in_(ARCHIVED))),
            #title=_(u"Bills"),
            description=_(u"Bills"))
    s["agendaitems"] = QueryContent(
            container_getter(workspace, 'agendaitems',
                query_modifier=sql.not_(domain.AgendaItem.status.in_(ARCHIVED))),
            #title=_(u"Agenda items"),
            description=_(u" items"))
    s["committees"] = QueryContent(
            container_getter(workspace, 'committees'),
            #title=_(u"Committees"),
            description=_(u"Committees"))
    log.debug("WorkspacePISection %s" % debug.interfaces(s))
    return s

def getWorkSpaceArchiveSection(workspace):
    """ /workspace/obj-id/my-archive/ -> ARCHIVED parliamentary items 
    """
    s = Section(title=_(u"My archive"),
            description=_(u"My archive personal items"),
            default_name="workspace-archive")
    interface.alsoProvides(s, interfaces.IWorkspaceArchiveContext)
    s.__parent__ = workspace
    s.__name__ = "archive"
    s["questions"] = QueryContent(
            container_getter(workspace, 'questions',
                query_modifier=domain.Question.status.in_(ARCHIVED)),
            #title=_(u"Questions"),
            description=_(u"Questions"))
    s["motions"] = QueryContent(
            container_getter(workspace, 'motions',
                query_modifier=domain.Motion.status.in_(ARCHIVED)),
            #title=_(u"Motions"),
            description=_(u"Motions"))
    s["tableddocuments"] = QueryContent(
            container_getter(workspace, 'tableddocuments',
                query_modifier=domain.TabledDocument.status.in_(ARCHIVED)),
            #title=_(u"Tabled documents"),
            description=_(u"Tabled documents"))
    s["bills"] = QueryContent(
            container_getter(workspace, 'bills',
                query_modifier=domain.Bill.status.in_(ARCHIVED)),
            #title=_(u"Bills"),
            description=_(u"Bills"))
    s["agendaitems"] = QueryContent(
            container_getter(workspace, 'agendaitems',
                query_modifier=domain.AgendaItem.status.in_(ARCHIVED)),
            #title=_(u"Agenda items"),
            description=_(u" items"))
    log.debug("getWorkSpaceArchiveSection %s" % debug.interfaces(s))
    return s


''' !+ workspace section contexts:
the more logical approach [ForbiddenAttribute error on Section] for the PI and 
Archive workspace sections: the idea is to have WorkspaceContainerTraverser 
return an interfaces.IWorkspacePIContext(workspace_container), that would then 
be defined something like:

<adapter factory=".workspace.WorkspacePIContext" 
    for=".interfaces.IWorkspaceContainer" 
    provides=".interfaces.IWorkspacePIContext"
    permission="zope.Public" trusted="true" />

class WorkspacePIContext(Section):
    component.adapts(interfaces.IWorkspaceContainer, IHTTPRequest)
    interface.implements(interfaces.IWorkspacePIContext) 
    # interfaces.IWorkspaceSectionContext
    
    def __init__(self, context):
        # Section: title=None, description=None, default_name=None, 
        # marker=None, publishTraverseResolver=None
        super(WorkspacePIContext, self).__init__(
            title=_(u"Parliamentary items"),
            description=_(u"Current parliamentary activity"),
            default_name="workspace-pi")
        log.debug(" __init__ %s (context:%s)" % (self, context))
        self.context = context
        self.__parent__ = context
        self.__name__ = ""
        log.debug("WorkspacePIContext %s" % debug.interfaces(self))
        log.debug("WorkspacePIContext %s" % debug.location_stack(self))
        
        self["questions"] = self.get_questions()
    
    def get_questions(self):
        return QueryContent(
                container_getter(self.context, 'questions',
                query_modifier=sql.not_(domain.Question.status.in_(ARCHIVED))),
                #title=_(u"Questions"),
                description=_(u"Questions"))

# !+ also try using:
from zope.app.container.sample import SampleContainer
'''

class WorkspaceSchedulingContext(object):
    component.adapts(interfaces.IWorkspaceContainer)
    interface.implements(ISchedulingContext)
    
    def __init__(self, workspace):
        self.workspace = workspace
        self.group_id = workspace.group_id
        interface.alsoProvides(self, interfaces.IWorkspaceSchedulingContext)
        self.__parent__ = workspace
        self.__name__ = ""
        log.debug("WorkspaceSchedulingContext %s" % debug.location_stack(self))
        
    @property
    def label(self):
        group = self.get_group()
        if group is not None:
            return u"%s (%s)" % (group.short_name, group.full_name)
        return _(u"Unknown principal group")
    
    def get_group(self, name="group"):
        if self.group_id is None:
            return
        try:
            session = Session()
            group = session.query(domain.Group).filter_by(group_id=self.group_id)[0]
        except IndexError:
            raise RuntimeError("Group not found (%d)." % self.group_id)
        return group
    
    def get_sittings(self, start_date=None, end_date=None):
        try: 
            sittings = self.get_group().sittings
        except (AttributeError,):
            # e.g. ministry has no sittings attribute
            return {} # !+ should be a bungeni.models.domain.ManagedContainer
            # !+ could add sittings to a ministry
            #    could not have calendar appear for ministries
        if start_date is None and end_date is None:
            return sittings
        assert start_date and end_date
        unproxied = removeSecurityProxy(sittings)
        unproxied.subset_query = sql.and_(
            unproxied.subset_query,
            domain.GroupSitting.start_date.between(
                format_date(start_date),
                format_date(end_date))
            )
        unproxied.__parent__ = ProxyFactory(LocationProxy(
            unproxied.__parent__, container=self, name="group"))
        return sittings


# views
from bungeni.ui import z3evoque
from zope.app.pagetemplate import ViewPageTemplateFile

class WorkspaceSectionView(BungeniBrowserView):
    
    # the instance of the ViewProvideViewletManager
    provide = z3evoque.ViewProvideViewletManager()
    
    # evoque
    __call__ = z3evoque.PageViewTemplateFile("workspace.html#section_page")
    
    # zpt
    #__call__ = ViewPageTemplateFile("templates/workspace-section.pt")
    
    # set on request.layer_data
    user_id = None
    user_group_ids = None
    government_id = None
    ministries = None
    
    role_interface_mapping = {
        u'bungeni.Admin': interfaces.IAdministratorWorkspace,
        u'bungeni.Minister': interfaces.IMinisterWorkspace,
        u'bungeni.MP': interfaces.IMPWorkspace,
        u'bungeni.Speaker': interfaces.ISpeakerWorkspace,
        u'bungeni.Clerk': interfaces.IClerkWorkspace
    }
    
    def __init__(self, context, request):
        """self:zope.app.pagetemplate.simpleviewclass.SimpleViewClass -> 
                    templates/workspace-index.pt
           context:bungeni.core.content.Section
        """
        LD = IAnnotations(request)["layer_data"]
        assert interfaces.IWorkspaceSectionLayer.providedBy(request)
        assert LD.get("workspaces") is not None
        super(WorkspaceSectionView, self).__init__(context, request)
        cls_name = self.__class__.__name__ 
        # NOTE: Zope morphs this class's name to "SimpleViewClass from ..." 
        log.debug("%s.__init__ %s context=%s url=%s" % (
                            cls_name, self, self.context, request.getURL()))
        
        # transfer layer data items, for the view/template
        self.user_id = LD.user_id
        self.user_group_ids = LD.user_group_ids
        self.government_id = LD.government_id # may be None
        self.ministries = LD.ministries # may be None
        if self.ministries:
            interface.alsoProvides(self, interfaces.IMinisterWorkspace)
        
        # roles are function of the context, so always recalculate
        roles = get_roles(self.context)
        for role_id in roles:
            iface = self.role_interface_mapping.get(role_id)
            if iface is not None:
                interface.alsoProvides(self, iface)
        log.debug("%s.__init__ %s" % (cls_name, debug.interfaces(self)))
        
class WorkspacePIView(WorkspaceSectionView):
    def __init__(self, context, request):
        self.provide.default_provider_name = "bungeni.workspace-pi"
        super(WorkspacePIView, self).__init__(
                interfaces.IWorkspacePIContext(context), request)

class WorkspaceArchiveView(WorkspaceSectionView):
    def __init__(self, context, request):
        self.provide.default_provider_name = "bungeni.workspace-archive"
        super(WorkspaceArchiveView, self).__init__(
                interfaces.IWorkspaceArchiveContext(context), request)


