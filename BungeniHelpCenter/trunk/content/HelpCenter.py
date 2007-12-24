# -*- coding: utf-8 -*-
try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions

from Products.BungeniHelpCenter.config import *
from Products.PloneHelpCenter.content.PHCContent import PHCContent
from Products.ATContentTypes.content.document import ATDocument

from Products.PloneHelpCenter.content import ReferenceManual,\
    Tutorial, TutorialPage, ReferenceManualPage
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin, fti_meta_type
from Products.CMFCore.permissions import View
from AccessControl import ClassSecurityInfo
from Products.CMFPlone.browser.navtree import NavtreeStrategyBase, buildFolderTree
from Products.PloneHelpCenter.config import DEFAULT_CONTENT_TYPES, REFERENCEABLE_TYPES, IMAGE_SIZES
from Products.BungeniHelpCenter.config import BUNGENI_REFERENCEABLE_TYPES

try:
    from Products.CMFDynamicViewFTI.interfaces import ISelectableBrowserDefault
    HAS_ISBD = True
except ImportError:
    HAS_ISBD = False
try:
    from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
    PHCReferenceWidget = ReferenceBrowserWidget
except ImportError:
    PHCReferenceWidget = ReferenceWidget
from Products.PortalTaxonomy.fields import AttributeField, CategoryField

BodyField =  TextField(
        'body',
        searchable=1,
        widget=RichWidget(
                description = "The body text.",
                description_msgid = "phc_desc_body_referencemanual",
                label = "Body text",
                label_msgid = "phc_label_body_referencemanual",
                rows = 25,
                i18n_domain = "plonehelpcenter"
                ),
        **DEFAULT_CONTENT_TYPES
        )

DefinitionField =  TextField(
        'description',
        searchable=1,
        widget=RichWidget(
                description = "An explanation of the term.",
                description_msgid = "phc_desc_definition",
                label = "Definition",
                label_msgid = "phc_label_definition",
                rows = 25,
                i18n_domain = "plonehelpcenter"
                ),
        **DEFAULT_CONTENT_TYPES
        )

IdentityField = ImageField(
        'identity',
        required=0,
        sizes=IMAGE_SIZES,
        widget=ImageWidget(
            label='Identity Image',
            label_msgid='phc_label_identity_image',
            description='Add an identity image',
            description_msgid='phc_help_identity_image',
            i18n_domain='plonehelpcenter',
            ),
        )

IdentityPosition =  StringField('identity_position',
                                accessor = 'getIdentityPosition',
                                mutator = 'setIdentityPosition',
                                vocabulary = DisplayList((
                                            ('right', 'Top Right'),
                                            ('left', 'Top Left'),)),
                                searchable=0,
                                default= ('right'),
                                widget=
                                SelectionWidget(label='Identity Logo Position',
                                                label_msgid="label_identity_position",
                                                description="Select the positioning of the Identity Logo.",
                                                description_msgid="help_identity_position",
                                                i18n_domain="plone"
                                                ),
                                )

TocType =  StringField('toc_type',
                       accessor = 'getTocType',
                       mutator = 'setTocType',
                       vocabulary = DisplayList((
                                   ('drop', 'Drop Down'),
                                   ('box', 'Box'),)),
                       searchable=0,
                       default= ('drop'),
                       widget=
                       SelectionWidget(label='TOC Display Type',
                                       label_msgid="label_toc_type",
                                       description="Select the TOC display type.",
                                       description_msgid="help_toc_type",
                                       i18n_domain="plone"
                                       ),
                       )

ContributorsField =  LinesField(
        'contributors',
        accessor="Contributors",
        languageIndependent=1,
        widget=LinesWidget(
                label='Contributors',
                label_msgid="label_contributors",
                description="Enter additional names (no need to include the current owner) for those who have contributed to this entry, one per line.",
                description_msgid="help_contributors",
                i18n_domain="plone",
                ),
        )

RightsField =  TextField(
         'rights',
         accessor="Rights",
         widget=TextAreaWidget(
                 label='Copyright',
                 description="Copyright info for all content in the helpcenter.",
                 label_msgid="phc_label_copyrights_referencemanual",
                 description_msgid="phc_copyrights_referencemanual",
                 i18n_domain="plonehelpcenter"
                 ),
         )

PositionField =  StringField('navbar_position',
                             accessor = 'getNavBarPosition',
                             mutator = 'setNavBarPosition',
                             vocabulary = '_navbar',
                             searchable=0,
                             default= ('both'),
                             widget= SelectionWidget(label='Navigation Bar',
                                                     label_msgid="label_navigation_bar",
                                                     description="Select the positioning of the Navigation Bar.",
                                                     description_msgid="help_nav_bar",
                                                     i18n_domain="plone"
                                                     ),
                             )


TaxCategoryField = CategoryField('categories')

TaxAttributesField = AttributeField('attribs')

RelatedItemsField =  ReferenceField(
        'relatedItems',
        relationship='PloneHelpCenter',
        allowed_types=BUNGENI_REFERENCEABLE_TYPES,
        required = 0,
        multiValued=1,
        languageIndependent=1,
        widget=PHCReferenceWidget (
                label="Referenced Items",
                description="Set one or more references to HelpCenter items.",
                description_msgid = "phc_reference",
                label_msgid = "phc_label_reference",
                i18n_domain="plonehelpcenter"
                ),
    )

HelpCenterReferenceManual = ReferenceManual.HelpCenterReferenceManual

HelpCenterReferenceManualSchema = HelpCenterReferenceManual.schema + Schema((BodyField, IdentityField, IdentityPosition, RightsField,\
 PositionField, TocType, TaxCategoryField, TaxAttributesField),)

HelpCenterReferenceManualSchema['description'].required = 0
HelpCenterReferenceManualSchema.moveField('relatedItems', pos='bottom')
HelpCenterReferenceManualSchema.moveField('sections', pos='bottom')
HelpCenterReferenceManualSchema.moveField('audiences', pos='bottom')
HelpCenterReferenceManualSchema.moveField('contributors', pos='bottom')
HelpCenterReferenceManualSchema.moveField('startHere', pos='bottom')
HelpCenterReferenceManualSchema.moveField('subject', pos='bottom')
HelpCenterReferenceManualSchema.moveField('relatedItems', pos='bottom')
HelpCenterReferenceManualSchema.moveField('rights', pos='bottom')
HelpCenterReferenceManualSchema.moveField('categories', pos='bottom')
HelpCenterReferenceManualSchema.moveField('attribs', pos='bottom')

class BungeniHelpCenterReferenceManual(BrowserDefaultMixin,  HelpCenterReferenceManual):
    """A reference manual containing ReferenceManualPages,
    ReferenceManualSections, Files and Images.
    """

    __implements__ =(PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,)

    archetype_name = 'Reference Manual'
    meta_type='HelpCenterReferenceManual'
    content_icon = 'referencemanual_icon.gif'
    schema = HelpCenterReferenceManualSchema

    global_allow = 0
    filter_content_types = 1
    allowed_content_types =('BungeniHelpCenterReferenceManualPage', 
                             'HelpCenterReferenceManualSection', 
                             'Image', 'File')
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Reference Manual can contain Reference Manual Pages and Sections, Images and Files. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_referencemanual'

    default_view = 'referencemanual_view'
    suppl_views = ('referencemanual_view_roman', 'referencemanual_view_letter',)

    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}',
         'permissions' : (CMFCorePermissions.View,)
         },
        {'id'          : 'edit',
         'name'        : 'Edit',
         'action'      : 'string:${object_url}/edit',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'metadata',
         'name'        : 'Properties',
         'action'      : 'string:${object_url}/properties',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'local_roles',
         'name'        : 'Sharing',
         'action'      : 'string:${object_url}/sharing',
         'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        )

    aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'stats'      : 'phc_stats',
        'gethtml'    : '',
        'mkdir'      : '',
        }

    security = ClassSecurityInfo()

    def _navbar(self):
        """Used to display the position of the navigation bar."""
        return DisplayList((
                ('both', 'Both'),
                ('top', 'Top'),
                ('bottom', 'Bottom'),
                ))

    security.declareProtected(CMFCorePermissions.View, 'getTOC')
    def getTOC(self, current=None, root=None):
        """Get the table-of-contents of this manual. 
        
        The parameter 'current' gives the object that is the current page or
        section being viewed. 
        
        The parameter 'root' gives the root of the manual - if not given, this
        ReferenceManual object is used, but you can pass in a 
        ReferenceManualSection instead to root the TOC at this element. The 
        root element itself is not included in the table-of-contents.
        
        The return value is a list of dicts, recursively representing the 
        table-of-contents of this manual. Each element dict contains:
        
            item        -- a catalog brain for the item (a section or page)
            numbering   -- The dotted numbering of this item, e.g. 1.3.2
            depth       -- The depth of the item (0 == top-level item)
            currentItem -- True if this item corresponds to the object 'current'
            children    -- A list of dicts
            
        The list 'children' recursively contains the equivalent dicts for
        children of each section. If the parameter 'current' is not given, no
        element will have current == True.
        """

        if not root:
            root = self

        class Strategy(NavtreeStrategyBase):
            
            rootPath = '/'.join(root.getPhysicalPath())
            showAllParents = False
                
        strategy = Strategy()
        query=  {'path'        : '/'.join(root.getPhysicalPath()),
                 'portal_type' : ('HelpCenterReferenceManualSection',
                                   'BungeniHelpCenterReferenceManualPage',),
                 'sort_on'     : 'getObjPositionInParent'}
                
        toc = buildFolderTree(self, current, query, strategy)['children']
        
        def buildNumbering(nodes, base=""):
            idx = 1
            for n in nodes:
                numbering = "%s%d." % (base, idx,)
                n['numbering'] = numbering
                buildNumbering(n['children'], numbering)
                idx += 1
                
        buildNumbering(toc)
        return toc

    def toRoman(self, num):
        """Convert to roman numerials"""
        str = ''
        for number in num.split('.'):
            if number.isdigit():
                str=str+"."+roman.toRoman(int(number))
        if str:
            return str[1:]

    def toAlpha(self, num):
        """Convert to alpha"""
        str = ''
        for number in num.split('.'):
            if number.isdigit():
                str=str+"."+roman.toAlpha(int(number))
        if str:
            return str[1:]

registerType(BungeniHelpCenterReferenceManual, PROJECTNAME)

HelpCenterTutorial = Tutorial.HelpCenterTutorial

HelpCenterTutorialSchema = HelpCenterTutorial.schema +\
    Schema((BodyField, PositionField, TocType, TaxCategoryField, TaxAttributesField),)

HelpCenterTutorialSchema['description'].required = 0
HelpCenterTutorialSchema.moveField('body', pos='top')
HelpCenterTutorialSchema.moveField('description', pos='top')
HelpCenterTutorialSchema.moveField('title', pos='top')

class BungeniHelpCenterTutorial(BrowserDefaultMixin, HelpCenterTutorial):
    """A tutorial containing TutorialPages, Files and Images."""

    __implements__ = (PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,)

    archetype_name = 'Tutorial'
    meta_type = portal_type = 'HelpCenterTutorial'
    content_icon = 'tutorial_icon.gif'
    schema = HelpCenterTutorialSchema
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('BungeniHelpCenterTutorialPage', 'Image', 'File')
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Tutorial can contain Tutorial Pages, Images and Files. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_tutorial'

    default_view = 'tutorial_view'
    suppl_views = ('tutorial_view_roman', 'tutorial_view_letter',)

    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}',
         'permissions' : (CMFCorePermissions.View,)
         },
        {'id'          : 'edit',
         'name'        : 'Edit',
         'action'      : 'string:${object_url}/edit',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'metadata',
         'name'        : 'Properties',
         'action'      : 'string:${object_url}/properties',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'local_roles',
         'name'        : 'Sharing',
         'action'      : 'string:${object_url}/sharing',
         'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        )

    aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'stats'      : 'phc_stats',
        'gethtml'    : '',
        'mkdir'      : '',
        }

    security = ClassSecurityInfo()

    def _navbar(self):
        """Used to display the position of the navigation bar."""
        return DisplayList((
                ('both', 'Both'),
                ('top', 'Top'),
                ('bottom', 'Bottom'),
                ))

    security.declareProtected(CMFCorePermissions.View, 'getPages')
    def getPages(self, states=[]):
        """Get items"""
        criteria = contentFilter = {'portal_type' : 'BungeniHelpCenterTutorialPage'}
        if states:
            criteria['review_state'] = states
        return self.getFolderContents(contentFilter = criteria)

registerType(BungeniHelpCenterTutorial, PROJECTNAME)

HelpCenterTutorialPage = TutorialPage.HelpCenterTutorialPage

HelpCenterTutorialPage.schema['description'].required = 0

ContributorsField =  LinesField(
        'contributors',
        accessor="Contributors",
        languageIndependent=1,
        widget=LinesWidget(
                label='Contributors',
                label_msgid="label_contributors",
                description="Enter additional names (no need to include the current owner) for those who have contributed to this entry, one per line.",
                description_msgid="help_contributors",
                i18n_domain="plone",
                ),
        )

HelpCenterTutorialPage.schema = HelpCenterTutorialPage.schema +\
    Schema((ContributorsField, RelatedItemsField),)

#if HelpCenterTutorialPage.schema.has_key('relatedItems'):
#    del HelpCenterTutorialPage.schema['relatedItems']
HelpCenterTutorialPage.schema.moveField('contributors', pos='bottom')

class BungeniHelpCenterTutorialPage(BrowserDefaultMixin, OrderedBaseFolder, HelpCenterTutorialPage):
    """A tutorial containing TutorialPages, Files and Images."""

    __implements__ = (PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,)

    archetype_name = 'Page'
    meta_type='BungeniHelpCenterTutorialPage'
    content_icon = 'document_icon.gif'
    schema = HelpCenterTutorialPage.schema
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('TabbedSubpages',)
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Tutorial can contain Tutorial Pages, Images and Files. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_tutorial'

    default_view = 'tutorialpage_view'
    suppl_views = ('tutorialpage_horizontal_tabs', 'tutorialpage_vertical_tabs',)

    security = ClassSecurityInfo()

    security.declareProtected(View, 'getTargetObjectLayout')
    def getTargetObjectLayout(self, target):
        """
        Returns target object 'view' action page template
        """
        
        if HAS_ISBD and ISelectableBrowserDefault.isImplementedBy(target):
            return target.getLayout()
        else:
            view = target.getTypeInfo().getActionById('view') or 'base_view'
            
            # If view action is view, try to guess correct template
            if view == 'view':
                view = target.portal_type.lower() + '_view'
                
            return view
            
    def SearchableText(self):
        """Append references' searchable fields."""
        
        data = [HelpCenterTutorialPage.SearchableText(self),]
        
        subpages = self.objectValues(['TabbedSubpages',])
        for subpage in subpages:
            data.append(subpage.SearchableText())
            
        data = ' '.join(data)
        
        return data


    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}',
         'permissions' : (CMFCorePermissions.View,)
         },
        {'id'          : 'edit',
         'name'        : 'Edit',
         'action'      : 'string:${object_url}/edit',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'metadata',
         'name'        : 'Properties',
         'action'      : 'string:${object_url}/properties',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'local_roles',
         'name'        : 'Sharing',
         'action'      : 'string:${object_url}/sharing',
         'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        )

    aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'stats'      : 'phc_stats',
        'gethtml'    : '',
        'mkdir'      : '',
        }

registerType(BungeniHelpCenterTutorialPage, PROJECTNAME)

HelpCenterReferenceManualPage = ReferenceManualPage.HelpCenterReferenceManualPage

HelpCenterReferenceManualPage.schema['description'].required = 0

HelpCenterReferenceManualPage.schema = \
    HelpCenterReferenceManualPage.schema + Schema((RelatedItemsField),)

class BungeniHelpCenterReferenceManualPage(BrowserDefaultMixin, OrderedBaseFolder, HelpCenterReferenceManualPage):
    """A tutorial containing TutorialPages, Files and Images."""

    __implements__ = (PHCContent.__implements__,
                      OrderedBaseFolder.__implements__,)

    archetype_name = 'Page'
    meta_type='BungeniHelpCenterReferenceManualPage'
    content_icon = 'document_icon.gif'
    schema = HelpCenterTutorialPage.schema
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('TabbedSubpages',)
    # allow_discussion = IS_DISCUSSABLE

    typeDescription= 'A Tutorial can contain Tutorial Pages, Images and Files. Index order is decided by the folder order, use the normal up/down arrow in the folder content view to rearrange content.'
    typeDescMsgId  = 'description_edit_tutorial'

    default_view = 'referencemanualpage_view'
    suppl_views = ('referencemanualpage_horizontal_tabs', 'referencemanualpage_vertical_tabs',)

    security = ClassSecurityInfo()

    security.declareProtected(View, 'getTargetObjectLayout')
    def getTargetObjectLayout(self, target):
        """
        Returns target object 'view' action page template
        """
        
        if HAS_ISBD and ISelectableBrowserDefault.isImplementedBy(target):
            return target.getLayout()
        else:
            view = target.getTypeInfo().getActionById('view') or 'base_view'
            
            # If view action is view, try to guess correct template
            if view == 'view':
                view = target.portal_type.lower() + '_view'
                
            return view
            
    def SearchableText(self):
        """Append references' searchable fields."""
        
        data = [HelpCenterReferenceManualPage.SearchableText(self),]
        
        subpages = self.objectValues(['TabbedSubpages',])
        for subpage in subpages:
            data.append(subpage.SearchableText())
            
        data = ' '.join(data)
        
        return data


    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}',
         'permissions' : (CMFCorePermissions.View,)
         },
        {'id'          : 'edit',
         'name'        : 'Edit',
         'action'      : 'string:${object_url}/edit',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'metadata',
         'name'        : 'Properties',
         'action'      : 'string:${object_url}/properties',
         'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        {'id'          : 'local_roles',
         'name'        : 'Sharing',
         'action'      : 'string:${object_url}/sharing',
         'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        )

    aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '',
        'edit'       : 'base_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'stats'      : 'phc_stats',
        'gethtml'    : '',
        'mkdir'      : '',
        }

registerType(BungeniHelpCenterReferenceManualPage, PROJECTNAME)
