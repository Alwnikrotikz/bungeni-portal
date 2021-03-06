from lxml import etree

from ore import yuiwidget

from zope import schema, component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.formlib import form
#from zope.viewlet import viewlet

from bungeni.alchemist import Session
from alchemist.traversal.interfaces import IManagedContainer
from bungeni.alchemist import catalyst
from bungeni.models import domain, interfaces
from bungeni.core.index import IndexReset
from bungeni.ui import container, search, browser
from bungeni.ui.calendar import utils as calendar_utils
from bungeni.ui.interfaces import IBungeniSkin
from bungeni.utils import register
from bungeni.ui.i18n import _
from bungeni.ui.utils.queries import execute_sql


@register.view(interfaces.IBungeniAdmin, IBungeniSkin, name="settings",
    protect={"zope.ManageSite": dict(attributes=["browserDefault", "__call__"])})
class Settings(catalyst.EditForm):

    form_fields = form.Fields(interfaces.IBungeniSettings)
        
    def update(self):
        settings = component.getUtility(interfaces.IBungeniSettings)()
        self.adapters = {interfaces.IBungeniSettings : settings}
        super(Settings, self).update()


## class FieldEditColumn(column.FieldEditColumn):
##     def renderCell(self, item, formatter):
##         id = self.makeId(item)
##         request = formatter.request
##         field = self.field
##         if self.bind:
##             field = field.bind(item)
##         widget = component.getMultiAdapter((field, request), IInputWidget)
##         widget.setPrefix(self.prefix + "." + id)
##         if self.widget_extra is not None:
##             widget.extra = self.widget_extra
##         if self.widget_class is not None:
##             widget.cssClass = self.widget_class
##         ignoreStickyValues = getattr(formatter, "ignoreStickyValues", False)
##         if ignoreStickyValues or not widget.hasInput():
##             widget.setRenderedValue(self.get(item))
##         return widget()


@register.view(interfaces.IBungeniAdmin, IBungeniSkin, name="email-settings",
    like_class=Settings)
class EmailSettings(catalyst.EditForm):
    
    form_fields = form.Fields(interfaces.IBungeniEmailSettings)
    
    def update(self):
        settings = \
            component.getUtility(interfaces.IBungeniEmailSettings)()
        self.adapters = {interfaces.IBungeniEmailSettings : settings}
        super(EmailSettings, self).update()



@register.view(None, IBungeniSkin, name="user-settings")
class UserSettings(catalyst.EditForm):

    form_fields = form.Fields(interfaces.IBungeniUserSettings, interfaces.IUser)
    form_fields = form_fields.omit("user_id", "login", "date_of_death", "status")
    
    def update(self):
        session = Session()
        query = session.query(domain.User).filter(
            domain.User.login == self.request.principal.id)
        results = query.all()
        if len(results) == 1:
            user = results[0]
        else:
            user = None
        settings = interfaces.IBungeniUserSettings(user, None)
        if settings is None:
            raise SyntaxError("User Settings Only For Database Users")
        self.adapters = {interfaces.IBungeniUserSettings : settings,
                          interfaces.IUser : user}
        super(UserSettings, self).update()


SIMPLE_LIST = "<ul/>"
X_TITLE = "font-weight:bold; padding:5px; color:#fff; display:block; background-color:#%s;"

def add_sub_element(parent, tag, text=None, **kw):
    _element = etree.SubElement(parent, tag, **kw)
    if text: 
        _element.text = str(text)
    return _element

COLOUR_COUNT = 10
COLOURS = calendar_utils.generate_event_colours(COLOUR_COUNT)
GROUP_SITTING_EXTRAS = dict(questions="Question", motions="Motion", 
    tableddocuments="TabledDocument", bills="Bill", agendaitems="AgendaItem"
)
def generate_doc_for(domain_class, title=None, color=0):
    doc = etree.fromstring(SIMPLE_LIST)
    _color = COLOURS[color]
    if color:
        doc.attrib["style"] = "background-color:#%s;" % _color
    if title:
        add_sub_element(doc, "li", title)
    
    proxy_dict = domain_class.__dict__
    class_dict = {}
    class_dict.update(proxy_dict)
    if domain_class is domain.GroupSitting:
        class_dict.update(GROUP_SITTING_EXTRAS)
    sort_key = lambda kv: str(IManagedContainer.providedBy(kv[1]) or kv[0] in GROUP_SITTING_EXTRAS.keys()) + "-" + kv[0]
    class_keys = sorted([ kv for kv in class_dict.iteritems() ],
        key = sort_key
    )
    for (key, value) in class_keys:
        if (not key.startswith("_")) and (not hasattr(value, "__call__")):
            elx = add_sub_element(doc, "li")
            if (key in GROUP_SITTING_EXTRAS.keys() or
                IManagedContainer.providedBy(value)
            ):
                _title = "%s (list)" % key
                color = (color + 1) % COLOUR_COUNT
                next_color = COLOURS[color]
                elx.attrib["style"] = "border-left:1px solid #%s;" % next_color
                add_sub_element(elx, "span", _title, 
                    style=X_TITLE % next_color
                )
                if key in GROUP_SITTING_EXTRAS.keys():
                    container_name = value
                else:
                    container_name = value.container
                cls_name = container_name.split(".").pop().replace("Container", 
                    ""
                )
                the_model = getattr(domain, cls_name)
                elx.append(generate_doc_for(the_model, title, color))
                continue
            elx.text = key
    return doc


@register.view(interfaces.IBungeniAdmin, IBungeniSkin, 
    name="report-documentation", 
    like_class=Settings)
class ReportDocumentation(browser.BungeniBrowserView):
    
    render = ViewPageTemplateFile("templates/report-documentation.pt")
    
    def generateDocumentation(self):
        document = etree.fromstring(SIMPLE_LIST)
        st_tr = add_sub_element(document, "li")
        st_tr.attrib["style"] = "border-left:1px solid #%s;" % COLOURS[0]
        add_sub_element(st_tr, "span", "sittings (list)", 
            style=X_TITLE % COLOURS[0]
        ) 
        st_tr.append(generate_doc_for(domain.GroupSitting, 0))
        return etree.tostring(document)
    
    @property
    def documentation(self):
        return self.generateDocumentation()

    def __call__(self):
        return self.render()


@register.view(interfaces.IBungeniAdmin, IBungeniSkin, name="xapian-settings",
    like_class=Settings)
class XapianSettings(browser.BungeniBrowserView):
    
    render = ViewPageTemplateFile("templates/xapian-settings.pt")
    
    def __init__(self, context, request):
        return super(XapianSettings, self).__init__(context, request)
    
    def __call__(self):
        if self.request.method == "POST":
            IndexReset().start()
        return self.render()
    

@register.view(interfaces.IBungeniAdmin, IBungeniSkin, name="registry-settings",
    like_class=Settings)
class RegistrySettings(catalyst.EditForm):
    
    form_fields = form.Fields(interfaces.IBungeniRegistrySettings)
    
    def update(self):
        if self.request.method == "POST":
            # !+NUMBER_GENERATION (ah, nov-2011) - Reset the number sequence here.
            # Added the 'false' parameter at the end, otherwise setval() automatically
            # increments the sequence when called.
            # NOTE: this is a direct PG call, there is no SQLAlchemy way of resetting
            # a sequence, perhaps they should be dropped and recreated in SQLALchemy
            if self.request.get("form.questions_number") == "on":
                execute_sql("SELECT setval('question_registry_sequence', 1, false);")
            if self.request.get("form.motions_number") == "on":
                execute_sql("SELECT setval('motion_registry_sequence', 1, false);")
            if self.request.get("form.agendaitems_number") == "on":
                execute_sql("SELECT setval('agendaitem_registry_sequence', 1, false);")
            if self.request.get("form.bills_number") == "on":
                execute_sql("SELECT setval('bill_registry_sequence', 1, false);")
            if self.request.get("form.reports_number") == "on":
                execute_sql("SELECT setval('report_registry_sequence', 1, false);")
            if self.request.get("form.tableddocuments_number") == "on":
                execute_sql("SELECT setval('tableddocument_registry_sequence', 1, false);")
            if self.request.get("form.global_number") == "on":
                execute_sql("SELECT setval('registry_number_sequence', 1, false);")

        settings = \
            component.getUtility(interfaces.IBungeniRegistrySettings)()
        self.adapters = {interfaces.IBungeniRegistrySettings : settings}



