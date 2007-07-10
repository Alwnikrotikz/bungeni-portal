python = '/home/jean/zope/Python-2.4.4/bin/python'
zope_version = '2.9.7'

# For use on development machines, set this to True.
# WARNING: in no case set this to True on a live site!
# When False (the default), the products marked as 'develop' will not
# be installed.  When True, all products will be installed.
#     development_machine = False
development_machine = True

# Data for creating the instance
#     user = 'test'
#     password = 'test'
#     port = '8080'
#     ftp_port = '8021'
#     ftp_port = None
port = '8045'
ftp_port = None

symlink_basedir_template = '%(user_dir)s/repos/'
symlink_sources = [
        # Bungeni products
        {'source': 'svn/googlecode.com/bungeni-portal/AuditTrail/trunk', 'productname': 'AuditTrail'},
        {'source': 'svn/googlecode.com/bungeni-portal/Bungeni/trunk', 'productname': 'Bungeni'},
        {'source': 'svn/googlecode.com/bungeni-portal/BungeniDefaultContent/trunk', 'productname': 'BungeniDefaultContent'},
        {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkin/trunk', 'productname': 'BungeniSkin'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinAO/trunk', 'productname': 'BungeniSkinAO'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinCM/trunk', 'productname': 'BungeniSkinCM'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinGH/trunk', 'productname': 'BungeniSkinGH'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinKE/trunk', 'productname': 'BungeniSkinKE'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinMZ/trunk', 'productname': 'BungeniSkinMZ'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinNG/trunk', 'productname': 'BungeniSkinNG'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinPanafrica/trunk', 'productname': 'BungeniSkinPanafrica'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinRW/trunk', 'productname': 'BungeniSkinRW'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinTZ/trunk', 'productname': 'BungeniSkinTZ'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinUG/trunk', 'productname': 'BungeniSkinUG'},
        # {'source': 'svn/googlecode.com/bungeni-portal/BungeniSkinZA/trunk', 'productname': 'BungeniSkinZA'},
        {'source': 'svn/googlecode.com/bungeni-portal/Marginalia/trunk', 'productname': 'Marginalia'},
        {'source': 'svn/googlecode.com/bungeni-portal/DCWorkflow', 'productname': 'DCWorkflow'},

        # Plone
        {'source': 'svn/svn.plone.org/MoreFieldsAndWidgets/AddRemoveWidget/trunk', 'productname': 'AddRemoveWidget'},
        # installed into site-packages somewhere, gmf ..
        # {'source': 'svn/svn.plone.org/gsxml-trunk/inquant', 'productname': 'inquant', 'pylib': True},
        {'source': 'svn/svn.plone.org/SecureMaildropHost-trunk', 'productname': 'SecureMaildropHost'},
        {'source': 'svn/svn.plone.org/membrane-trunk', 'productname': 'membrane'},
        {'source': 'svn/svn.plone.org/PloneHelpCenter/trunk', 'productname': 'PloneHelpCenter'},
        {'source': 'svk/PloneStickies-trunk', 'productname': 'PloneStickies'},
        {'source': 'svn/svn.plone.org/Relations-trunk', 'productname': 'Relations'},
        {'source': 'svn/svn.plone.org/remember-trunk', 'productname': 'remember'},

        # While debugging
        {'source': 'svn/svn.plone.org/PDBDebugMode-trunk', 'productname': 'PDBDebugMode', 'develop': True},
        {'source': '/home/jean/repos/svk/zdb-trunk', 'productname': 'zdb', 'develop': True},
        ]

symlinkbundle_basedir_template = '%(user_dir)s/repos/'
symlinkbundle_sources = [
        {'source': 'svn/plone4artists.org/Plone4ArtistsCalendar-bundle', 'droplist': ('EXTERNALS.txt', )
            },
        {'source': 'svn/svn.objectrealms.net/iterate__bundles__0.3-plone-2.1-2.5',
            'droplist': ('CMFDiffTool', 'CMFEditions', 'ZopeVersionControl', 'externals.txt')
            },
        {'source': 'svn/svn.plone.org/CMFEditions__bundles__plone-2.5-zope-2.9',
            'droplist': ('iterate', 'EXTERNALS.txt', 'getZopeVersionControl.sh')},
        ]

use_svn_export = False

archive_basedir_template = '%(user_dir)s/download/code/plone/products/'
archive_sources = [
        # 'gsxml-bungeni.tar.gz',
        'MaildropHost-1.20.tgz',
        'PlonePopoll-2.5.1.tgz',
        'qRSS2Syndication-0.5.1.tar.gz',
        'TeamSpace-1.5.tar.gz',
        # Using svn
        # 'membrane-1.0.tar.gz',
        # 'remember-1.0b1.tar.gz',
        ]

archivebundle_basedir_template = '%(user_dir)s/download/code/plone/'
archivebundle_sources = [
        {'source': 'distro/Plone-2.5.3-final.tar.gz', 'droplist': ('DCWorkflow', 'Marshall')
            },
        {'source': 'products/LinguaPlone-0.9.tgz', 'droplist': 'PloneLanguageTool'
            },
        ]

#     main_products = []
main_products = ['Bungeni']

# Extension profiles for adapting the plone config with GenericSetup.
# See self.ploneSite.portal_setup.listContextInfos() for possible ids.
# Two examples are: 'profile-CMFPlone:plone' and
# u'profile-Products.CMFQuickInstallerTool:CMFQuickInstallerTool'.

#     generic_setup_profiles= []
generic_setup_profiles= [
        'profile-membrane:default',
        'profile-remember:default',
        ]

