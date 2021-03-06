# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Forms Viewlets

$Id$
"""
log = __import__("logging").getLogger("bungeni.ui.forms.viewlets")

from dateutil import relativedelta
import datetime
import calendar
from zope import interface
from zope.viewlet import manager, viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy
from zc.resourcelibrary import need
from zope.publisher.interfaces import NotFound
from zope.dublincore.interfaces import IDCDescriptiveProperties
import sqlalchemy.sql.expression as sql

#from bungeni.alchemist.ui import DynamicFields, EditFormViewlet
from bungeni.alchemist import Session
from bungeni.alchemist import utils
from bungeni.alchemist.interfaces import IContentViewManager
from bungeni.alchemist.container import stringKey

import bungeni.core.globalsettings as prefs
from bungeni.core.interfaces import ISchedulingContext

from bungeni.models import domain, interfaces
from bungeni.models.utils import get_groups_held_for_user_in_parliament
from bungeni.models.utils import get_parliament_for_group_id

from bungeni.ui.i18n import _
from bungeni.ui import browser
from bungeni.ui import table
from bungeni.ui.utils import url, misc, date
from fields import BungeniAttributeDisplay
from interfaces import (ISubFormViewletManager,
                        ISubformRssSubscriptionViewletManager)
from bungeni.ui.interfaces import IBungeniAuthenticatedSkin
from bungeni.utils import register
from bungeni.capi import capi

# !+SubformViewlet(mr, oct-2010) in this usage case this this should really
# be made to inherit from browser.BungeniViewlet (but, note that
# table.AjaxContainerListing already inherits from BungeniBrowserView).


@register.viewlet_manager(name="bungeni.subform.manager")
class SubFormViewletManager(manager.WeightOrderedViewletManager):
    """Display subforms.
    """
    interface.implements(ISubFormViewletManager)

    def filter(self, viewlets):
        viewlets = super(SubFormViewletManager, self).filter(viewlets)
        return [
            (name, viewlet) for name, viewlet in viewlets
            if viewlet.for_display ]


class SubformViewlet(table.AjaxContainerListing):
    """A container listing of the items indicated by "sub_attr_name".
    """

    template = ViewPageTemplateFile("templates/generic-sub-container.pt")

    def render(self):
        need("yui-datatable")
        return self.template()

    def __init__(self, context, request, view, manager):
        # The parent for SubformViewlets is the context (not the view)
        self.__parent__ = context
        self._context = context
        # !+_context(mr, oct-2010) using self.__parent__ to get to context 
        # gives recursion error: 
        # zope/publisher/browser.py", line 849, in __getParent 
        # return getattr(self, '_parent', self.context)
        self.request = request
        self.manager = manager

    sub_attr_name = None
    @property
    def context(self):
        return getattr(self._context, self.sub_attr_name)

    @property
    def view_name(self):
        return self.sub_attr_name # self.context.__name__

    @property
    def for_display(self):
        return len(self.context) > 0


# RSS

@register.viewlet_manager(name="bungeni.content.rss")
class SubformRssSubscriptionViewletManager(manager.WeightOrderedViewletManager):
    """Displays rss subscription data."""
    interface.implements(ISubformRssSubscriptionViewletManager)

# IBill, IQuestion, ITabledDocument, IAgendaItem, IMotion, ...
@register.viewlet(interfaces.IBungeniParliamentaryContent, 
    layer=IBungeniAuthenticatedSkin, 
    manager=ISubformRssSubscriptionViewletManager,
    name="keep-zca-happy-rsslink",
    protect=register.PROTECT_VIEWLET_PUBLIC
    )
class RssLinkViewlet(viewlet.ViewletBase):
    """Simply renders link for users to subscribe to current paliamentary item.
    """
    render = ViewPageTemplateFile("templates/rss-link.pt")
    
    @property
    def already_subscribed(self):
        """Checks if user has already subscribed to the current item.
        """
        session = Session()
        user = session.query(domain.User).filter(
                domain.User.login == self.request.principal.id).first()
        # If we've not found the user we should not allow to subscribe
        if user is None:
            return True
        return removeSecurityProxy(self.context) in user.subscriptions

#

@register.viewlet(interfaces.IParliament,
    manager=IContentViewManager,
    name="bungeni.viewlet.session",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class SessionViewlet(SubformViewlet):
    sub_attr_name = "sessions"
    weight = 50

class SignatoriesViewlet(SubformViewlet):
    sub_attr_name = "signatories"

@register.viewlet(interfaces.IParliament,
    manager=IContentViewManager,
    name="bungeni.viewlet.government",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class GovernmentViewlet(SubformViewlet):
    sub_attr_name = "governments"
    weight = 40


@register.viewlet(interfaces.IParliament,
    manager=IContentViewManager,
    name="bungeni.viewlet.member-of-parliament",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class MemberOfParliamentViewlet(SubformViewlet):
    sub_attr_name = "parliamentmembers"
    weight = 20

class SittingAttendanceViewlet(SubformViewlet):
    sub_attr_name = "attendance"
    weight = 55

class SittingReportsViewlet(SubformViewlet):
    form_name = "Reports" # !+
    sub_attr_name = "sreports"
    weight = 60

@register.viewlet(interfaces.ISitting,
    manager=ISubFormViewletManager,
    name="bungeni.viewlet.sitting-items",
    protect={"bungeni.item_schedule.View": register.VIEWLET_DEFAULT_ATTRS})
class SittingScheduleViewlet(SubformViewlet):
    sub_attr_name = "items"
    weight = 70
    form_name = _("items scheduled")
    
    @property
    def formatter(self):
        formatter = super(SittingScheduleViewlet, self).formatter
        formatter.data_view = "/jsonlisting-schedule-documents"
        return formatter

class MinistersViewlet(SubformViewlet):
    sub_attr_name = "ministers"

class BillsViewlet(SubformViewlet):
    sub_attr_name = "bills"

class QuestionsViewlet(SubformViewlet):
    sub_attr_name = "questions"

class AgendaItemsViewlet(SubformViewlet):
    sub_attr_name = "agendaitems"

class MinistriesViewlet(SubformViewlet):
    sub_attr_name = "ministries"

@register.viewlet(interfaces.IParliament,
    manager=IContentViewManager,
    name="bungeni.viewlet.committees",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class CommitteesViewlet(SubformViewlet):
    sub_attr_name = "committees"
    weight = 10

class CommitteeStaffViewlet(SubformViewlet):
    sub_attr_name = "committeestaff"

class CommitteeMembersViewlet(SubformViewlet):
    sub_attr_name = "committeemembers"


@register.viewlet(interfaces.IBungeniGroup, 
    manager=ISubFormViewletManager,
    name="keep-zca-happy-addresses",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class AddressesViewlet(SubformViewlet):
    sub_attr_name = "addresses"
    weight = 99
    @property
    def form_name(self):
        return _(u"Contacts")


@register.viewlet(interfaces.IParliament,
    manager=IContentViewManager,
    name="bungeni.viewlet.political-groups",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class PoliticalGroupsViewlet(SubformViewlet):
    sub_attr_name = "politicalgroups"
    weight = 30

class OfficeMembersViewlet(SubformViewlet):
    sub_attr_name = "officemembers"

class PoliticalGroupMembersViewlet(SubformViewlet):
    sub_attr_name = "group_members"

class SittingsViewlet(SubformViewlet):
    sub_attr_name = "sittings"

# BungeniAttributeDisplay
# !+BungeniViewlet(mr) make these inherit from browser.BungeniViewlet

class PersonInfo(BungeniAttributeDisplay):
    """Bio Info / personal data about the MP.
    """
    for_display = True
    mode = "view"

    form_name = _(u"Personal Info")
    view_id = "personal-info"

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.__parent__ = context.__parent__
        self.manager = manager
        self.query = None
        md = utils.get_descriptor(domain.User)
        self.form_fields = md.fields #.select("user_id", "start_date", "end_date")

    def update(self):
        user_id = self.context.user_id
        parent = self.context.__parent__
        self.query = Session().query(domain.User
            ).filter(domain.User.user_id == user_id)
        self.context = self.query.all()[0]
        self.context.__parent__ = parent
        super(PersonInfo, self).update()

@register.viewlet(interfaces.IFeatureSchedule,
    manager=ISubFormViewletManager,
    name="doc-minutes",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class DocMinutesViewlet(browser.BungeniItemsViewlet):
    """Render a tree of schedule discussions
    """ 
 
    render = ViewPageTemplateFile("templates/doc-minutes.pt")

    def __init__(self, context, request, view, manager):
        self.request = request
        self.context = context
        self.manager = manager
        trusted = removeSecurityProxy(context)
        try:
            self.item_id = trusted.doc_id
        except AttributeError:
            self.for_display = False
            return

    def _get_items(self):
        item_type = capi.get_type_info(self.context).workflow_key
        query = Session().query(domain.ItemSchedule).filter(
            sql.and_(
                domain.ItemSchedule.item_id == self.item_id,
                domain.ItemSchedule.item_type == item_type
            )
        )
        items = []
        for item in query.all():
            items.append(dict(
                sitting_name=IDCDescriptiveProperties(item.sitting).title,
                sitting_venue=(
                    IDCDescriptiveProperties(item.sitting.venue).title
                    if item.sitting.venue else _(u"Unknown venue")),
                minutes=[ dict(text=minute.body) 
                    for minute in item.itemdiscussions
                ]
            ))
        if not items:
            self.for_display = False
        return items
            
    
    def update(self):
        self.items = self._get_items()
        super(DocMinutesViewlet, self).update()

class WrittenQuestionResponseViewlet(browser.BungeniViewlet):

    mode = "view"
    for_display = True
    form_name = _(u"Response")
    render = ViewPageTemplateFile("templates/written-question-response.pt")

    def __init__(self, context, request, view, manager):
        self.request = request
        self.context = context
        self.manager = manager
        self.question = removeSecurityProxy(context)
        # Check type of question. Only written questions get this viewlet
        if self.question.response_type == "oral":
            self.for_display = False
        else:
            if self.question.response_text in (None, ""):
                self.for_display = False


class OfficesHeldViewlet(browser.BungeniItemsViewlet):

    render = ViewPageTemplateFile("templates/offices-held-viewlet.pt")

    def _get_items(self):
        formatter = self.get_date_formatter("date", "long")
        trusted = removeSecurityProxy(self.context)
        user_id = trusted.user_id
        office_list = []
        if interfaces.IMemberOfParliament.providedBy(self.context):
            parliament_id = trusted.group_id
        else:
            parliament = get_parliament_for_group_id(trusted.group_id)
            if parliament:
                parliament_id = parliament.parliament_id
            else:
                return office_list
        for oh in get_groups_held_for_user_in_parliament(user_id, parliament_id):
            title = {}
            # !+FULL_NAME(mr, oct-2010) this should probably make use of 
            # the GroupDescriptor (combined) listing Field full_name
            title["group"] = "%s - %s" % (_(oh[0]), oh[1] and _(oh[1]) or "")
            title["group_type"] = _(oh[2])
            if oh[3]:
                title["member_title"] = _(oh[3])
            else:
                title["member_title"] = _(u"Member")
            title["start_date"] = None
            if oh[4]:
                title["start_date"] = formatter.format(oh[4])
            elif oh[6]:
                title["start_date"] = formatter.format(oh[6])
            title["end_date"] = None
            if oh[5]:
                title["end_date"] = formatter.format(oh[5])
            elif oh[7]:
                title["end_date"] = formatter.format(oh[7])
            office_list.append(title)
        return office_list

    def update(self):
        self.items = self._get_items()



def _get_public_states_for(*tis):
    ps = set()
    for ti in tis:
        ps.update(ti.workflow.get_state_ids(tagged=["public"]))
    return list(ps)

class MemberItemsViewlet(browser.BungeniItemsViewlet):
    """A tab with bills, motions etc for an MP 
    (the "parliamentary activities" tab of of the "member" view)
    """
    states = _get_public_states_for( *[ ti 
        for (key, ti) in capi.iter_type_info() 
        if ti.custom and issubclass(ti.domain_model, domain.Doc) ] )
    
    render = ViewPageTemplateFile("templates/mp-item-viewlet.pt")

    def __init__(self, context, request, view, manager):
        super(MemberItemsViewlet, self).__init__(
            context, request, view, manager)
        user_id = self.context.user_id
        parliament_id = self.context.group_id
        self.query = Session().query(domain.Doc).filter(
            sql.and_(
                domain.Doc.owner_id == user_id,
                domain.Doc.parliament_id == parliament_id,
                domain.Doc.status.in_(self.states),
            ))
        #self.for_display = (self.query.count() > 0)
        self.formatter = self.get_date_formatter("date", "medium")
    
    def update(self):
        user_id = self.context.user_id
        parliament_id = self.context.group_id
        wf = capi.get_type_info("signatory").workflow
        session = Session()
        # add cosigned items
        signed_pi_ids = [sgn.head_id for sgn in
            session.query(domain.Signatory).filter(
                sql.and_(domain.Signatory.user_id == user_id,
                    domain.Signatory.status.in_(
                        wf.get_state_ids(tagged=["public"])
                    ),
                )
            ).all()
        ]
        if len(signed_pi_ids) > 0:
            self.query = self.query.union(
                session.query(domain.Doc).filter(
                    sql.and_(
                        domain.Doc.parliament_id == parliament_id,
                        domain.Doc.status.in_(self.states),
                        domain.Doc.doc_id.in_(
                            signed_pi_ids
                        )
                    )
                )
            )
        self.query = self.query.order_by(
            domain.Doc.doc_id.desc()
        )
    
    @property
    def items(self):
        for item in self.query.all():
            _url = "/business/%ss/obj-%i" % (item.type,
                item.doc_id)
            yield {"type": item.type,
                "title": item.title,
                "status": misc.get_wf_state(item),
                "submission_date" : item.submission_date,
                "url": _url }


class DisplayViewlet(BungeniAttributeDisplay):
    """Display a target object; if the object is `None`, the user is
    prompted to add it.
    """

    mode = "view"
    for_display = True
    query = None
    factory = None
    has_data = False
    form_fields = form.Fields()

    add_action = form.Actions(
        form.Action(_(u"Add"), success="handle_add"),
    )

    def __init__(self, context, request, view, manager):
        super(DisplayViewlet, self).__init__(
            context, request, view, manager)
        # set add url before we change context
        self.add_url = self.get_add_url()

        target = self.get_target()
        if target is None:
            self.status = _(u"No item has been set")
        else:
            self.context = target
            self.has_data = True
            assert self.factory is not None
            descriptor = utils.get_descriptor(self.factory)
            self.form_fields = descriptor.fields

    def update(self):
        # only if there's data to display do we update using our
        # immediate superclass
        if self.has_data:
            super(DisplayViewlet, self).update()
        else:
            self.setupActions()
            super(form.SubPageDisplayForm, self).update()

    def handle_add(self, action, data):
        self.request.response.redirect(self.add_url)

    def get_add_url(self):
        raise NotImplementedError("Must be implemented by subclass.")

    def get_target(self):
        raise NotImplementedError("Must be implemented by subclass.")

    def set_target(self, target):
        raise NotImplementedError("Must be implemented by subclass.")

    def setupActions(self):
        if self.has_data:
            super(DisplayViewlet, self).setupActions()
        else:
            self.actions = self.add_action.actions

    @property
    def form_name(self):
        descriptor = utils.get_descriptor(self.factory)
        return descriptor.display_name

@register.viewlet(interfaces.IItemSchedule,
    manager=IContentViewManager,
    name="bungeni.viewlet.scheduling-item-discussions",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class SchedulingMinutesViewlet(SubformViewlet):
    sub_attr_name = "discussions"

@register.viewlet(interfaces.IItemSchedule,
    manager=IContentViewManager,
    name="bungeni.viewlet.scheduling-item-votes",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class SchedulingVotesViewlet(SubformViewlet):
    sub_attr_name = "votes"
    form_name = _("vote records")

    @property
    def for_display(self):
        """Only display viewlet for doc types"""
        if not interfaces.IDoc.providedBy(self.context.__parent__):
            return False
        return super(SchedulingVotesViewlet, self).for_display

@register.viewlet(interfaces.ISession,
    manager=IContentViewManager,
    name="bungeni.viewlet.session-sitting-calendar",
    protect=register.PROTECT_VIEWLET_PUBLIC)
class SessionCalendarViewlet(browser.BungeniItemsViewlet):
    """Display a monthly calendar with all sittings for a session.
    """
    weight = 20
    def __init__(self, context, request, view, manager):
        super(SessionCalendarViewlet, self).__init__(
            context, request, view, manager)
        self.query = None
        self.date = None

    view_name = "session_sittings"
    viewlet_id = "session_viewlet_sittings"

    def _get_display_date(self, request):
        display_date = date.getDisplayDate(self.request)
        session = self.context
        if display_date:
            if session.end_date:
                if display_date > session.end_date:
                    display_date = session.end_date
            if session.start_date > display_date:
                display_date = session.start_date
        else:
            display_date = session.end_date
        return display_date

    def current_sittings_query(self, date):
        session = removeSecurityProxy(self.context)
        group_id = session.parliament_id
        start_date = session.start_date
        if start_date.month < date.month:
            start_date = datetime.date(date.year, date.month, 1)
        end_date = session.end_date
        if end_date:
            if end_date.month > date.month:
                end_date = date + relativedelta.relativedelta(day=31)
        else:
            end_date = date + relativedelta.relativedelta(day=31)
        
        s_filter = sql.and_(
            domain.Sitting.group_id == group_id,
            sql.between(domain.Sitting.start_date, start_date, end_date)
        )
        return Session().query(domain.Sitting).filter(s_filter).order_by(
                domain.Sitting.start_date)
    
    def previous(self):
        """Return link to the previous month, 
        if the session start date is prior to the current month
        """
        session = self.context
        if self.date.month == 1:
            month = 12
            year = self.date.year - 1
        else:
            month = self.date.month - 1
            year = self.date.year
        try:
            prevdate = datetime.date(year, month, self.date.day)
        except:
            # in case we try to move to Feb 31st (or so)
            prevdate = datetime.date(year, month, 15)
        if session.start_date < datetime.date(
                self.date.year, self.date.month, 1):
            return """<a href="?date=%s#%s"> &lt;&lt; </a>""" % (
                datetime.date.strftime(prevdate, "%Y-%m-%d"), self.viewlet_id)
        else:
            return ""

    def next(self):
        """Return link to the next month if the end date,
        if the session is after the 1st of the next month
        """
        session = self.context
        if self.date.month == 12:
            month = 1
            year = self.date.year + 1
        else:
            month = self.date.month + 1
            year = self.date.year
        try:
            nextdate = datetime.date(year, month, self.date.day)
        except:
            # if we try to move from 31 of jan to 31 of feb or so
            nextdate = datetime.date(year, month, 15)
        if session:
            if session.end_date:
                if session.end_date < datetime.date(year, month, 1):
                    return ""
        return """<a href="?date=%s#%s"> &gt;&gt; </a>""" % (
            datetime.date.strftime(nextdate, "%Y-%m-%d"), self.viewlet_id)

    def get_sittings_path(self):
        """get the url to the context sittings container"""
        scheduling_context = None
        context = self.context
        while scheduling_context is None:
            scheduling_context = ISchedulingContext(context, None)
            if not scheduling_context:
                context = context.__parent__
        if scheduling_context:
            try:
                ctx = scheduling_context.__parent__
                if hasattr(ctx, "sittings"):
                    sittings_container = ctx.sittings
                else:
                    sittings_container = removeSecurityProxy(ctx).publishTraverse(
                        self.request, "sittings"
                    )
                return url.absoluteURL(sittings_container, self.request)
            except NotFound:
                log.error("Could not determine sittings path for context %s",
                    self.context
                )
        return "../sittings"

    def _get_items(self):
        """Return the data of the query.
        """
        data_list = []
        path = self.get_sittings_path()
        formatter = self.get_date_formatter("time", "short")
        for result in self.query.all():
            data = {}
            data["sittingid"] = ("sid_" + str(result.sitting_id))
            data["sid"] = result.sitting_id
            data["short_name"] = "%s - %s" % (
                formatter.format(result.start_date),
                formatter.format(result.end_date)
            )
            data["start_date"] = result.start_date
            data["end_date"] = result.end_date
            data["start_time"] = result.start_date.time()
            data["end_time"] = result.end_date.time()
            data["day"] = result.start_date.date()
            data["url"] = "/".join([path, stringKey(result)])
            data["did"] = "dlid_%s" % (
                datetime.datetime.strftime(result.start_date, "%Y-%m-%d"))
            data_list.append(data)
        return data_list
    
    def get_td_id(self, date):
        """
        return an Id for that td element:
        consiting of tdid- + date
        like tdid-2008-01-17
        """
        return "tdid-" + datetime.date.strftime(date, "%Y-%m-%d")
    
    def get_day_class(self, Date):
        """Return the class settings for that calendar day.
        """
        css_class = ""
        if self.date.month != Date.month:
            css_class = css_class + "other-month "
        if Date < datetime.date.today():
            css_class = css_class + "past-date "
        if Date == datetime.date.today():
            css_class = css_class + "current-date "
        if Date.weekday() in prefs.getWeekendDays():
            css_class = css_class + "weekend-date "
        query = Session().query(domain.Holiday
            ).filter(domain.Holiday.date == Date)
        results = query.all()
        if results:
            css_class = css_class + "holyday-date "
        return css_class.strip()
    
    def get_week_no(self, Date):
        """Return the weeknumber for a given date.
        """
        return Date.isocalendar()[1]
    
    def get_sittings_for_day(self, Date):
        """Return the sittings for that day.
        """
        day_data = []
        for data in self.items:
            if data["day"] == Date:
                day_data.append(data)
        return day_data
    
    def update(self):
        """Refresh the query.
        """
        self.date = self._get_display_date(self.request)
        if not self.date:
            self.date = datetime.date.today()
        self.query = self.current_sittings_query(self.date)
        self.monthcalendar = calendar.Calendar(prefs.getFirstDayOfWeek()
            ).monthdatescalendar(self.date.year, self.date.month)
        self.monthname = datetime.date.strftime(self.date, "%B %Y")
        self.items = self._get_items()
    
    render = ViewPageTemplateFile("templates/session-calendar-viewlet.pt")

