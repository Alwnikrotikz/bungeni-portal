import logging
from Products.CMFCore.utils import getToolByName

# The profile id of your package:
PROFILE_ID = 'profile-bungenicms.membershipdirectory:default'


class Empty:
    pass
    

def add_catalog_indexes(context, logger):
    """Method to add our wanted indexes to portal_catalog and uid_catalog
    
    @parameters:

    When called from the setup_various method below, 'context' is the plone site 
    and 'logger' is the portal_setup logger.  But this method can also be used 
    as upgrade step, in which case 'context' will be portal_setup and 'logger' 
    will be None.
    """
    if logger is None:
        logger = logging.getLogger('bungenicms.membershipdirectory')
        
    # Run the catalog.xml step as that may have defined new metadata columns.  
    # We could instead add <depends name="catalog"/> to the registration of our 
    # import step in zcml, but doing it in code makes this method usable as 
    # upgrade step as well.  Note that this silently does nothing when there is 
    # no catalog.xml, so it is quite safe.
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
    
    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    
    # Specify the indexes you want, with ('index_name', 'index_type')
    wanted = (('county', 'FieldIndex'),
              ('constituency', 'FieldIndex'),
              ('priority_number', 'FieldIndex'),              
              ('political_party', 'FieldIndex'),
              ('elected_nominated', 'FieldIndex'),
              ('member_status', 'FieldIndex'),
              ('special_interest', 'FieldIndex'),
              ('other_names', 'FieldIndex'),
              ('member_role', 'FieldIndex'),
              ('member_title', 'FieldIndex'),
              ('body_text', 'FieldIndex'),
              ('member_full_names', 'ZCTextIndex'),
              )

    indexables = []
    for (name, meta_type) in wanted:
        if meta_type and name not in indexes:
            if meta_type == 'ZCTextIndex':
                item_extras = Empty()
                item_extras.doc_attr = name
                item_extras.index_type = 'Okapi BM25 Rank'
                item_extras.lexicon_id = 'plone_lexicon'
                catalog.addIndex(name, meta_type, item_extras)
            else:
                catalog.addIndex(name, meta_type)
            
            indexables.append(name)
            logger.info('Added %s for field %s.', meta_type, name)
    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def setup_various(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('bungenicms.membershipdirectory-reindex.txt') is None:
        return
    logger = context.getLogger('bungenicms.membershipdirectory')
    site = context.getSite()
    add_catalog_indexes(site, logger)
    
