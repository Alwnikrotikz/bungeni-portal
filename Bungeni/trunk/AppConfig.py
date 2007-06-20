# Permissions we want globally available
from Products.CMFCore import permissions

# The Plone site should be a membrane/remember site.

# Products that are integrated in Bungeni product. 
DEPENDENCIES = [
        'AddRemoveWidget', 
        'PloneHelpCenter',
        'qRSS2Syndication', # RSS2 feeds
        'AuditTrail', 
        'Relations',
        ]

# Products that we want to use alongside Bungeni
DEPENDENCIES += [
        'iterate', # Installs CMFEditions, CMFDiffTool
        # 'Hornet', # Requires ZMySQLdb
        'TeamSpace',
        'LinguaPlone', # Installs PloneLanguageTool
        'Plone4ArtistsCalendar', # Installs CMFonFive
        ]

# TODO: Move this to the model
ACTIVE_MEMBRANE_STATES = {
        'MemberOfParliament': ['public', 'private'],
        'Clerk': ['public', 'private'],
        'MemberOfPublic': ['public', 'private']
}

# Note that though we need PloneHelpCenter in the Products dir, we don't
# want to install it, as we don't use its content types -- only the ones
# that we derive from it.
