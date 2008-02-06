"""
$Id: $
"""
from zope import interface, schema

from sqlalchemy import orm
from ore.alchemist import container, Session
from zope.security.proxy import removeSecurityProxy
from z3c.traverser.interfaces import ITraverserPlugin

import domain
import interfaces
# 
# class VersionTraversal( object ):
#     
#     interface.implements( ITraverserPlugin )
# 
#     def __init__( self, context, request ):
#         self.context = context
#         self.request = request
#         
#     def publishTraverse(self, request, name):
#         if name != 'versions':
#             return 
#         return interfaces.IVersioned( self.context )
        
class Versioned( container.PartialContainer ):
    
    interface.implements( interfaces.IVersioned )
    
    def create( self ):
        """
        store the existing state of the adapted context as a new version
        """
        version = self.domain_class()
        for field in schema.getFields( IModelDescriptor( self.domain_class ).domain_interface ).values():
            field.set( version, field.query( self.context ) )
        session = Session()
        session.save( version )
        
    def revert( self, version ):
        """
        revert the current state of the adapted object to the values specified
        in version, and create a new version with reverted state. 
        """
        for field in schema.getFields( IModelDescriptor( self.domain_class ).domain_interface ).values():
            value = field.query( self.context )
            if value:
                field.set( version, value )
                
        self.create()
        
        
def ContextVersioned( ob ):
    versionedFactory = globals()['Versioned%s'%(ob.__class__.__name__)]
    return versionedFactory( ob )

class ContentVersionsFactory( object ):
    
    def __init__( self, pk ):
        self.pk = pk
    
    def __call__( self, context ):
        content_version_class = getattr( domain, context.__class__.__name__ + "Version" )
        versions = Versioned()
        versions._class = content_version_class 
        trusted_ctx = removeSecurityProxy( context )
        mapper = orm.object_mapper( trusted_ctx )
        pk_value = mapper.primary_key_from_instance( removeSecurityProxy(trusted_ctx) )[0]
        versions.setQueryModifier( content_version_class.c[ self.pk ] == pk_value )
        versions.__parent__ = context
        versions.__name__ = 'versions'
        return versions
                
VersionedBill = ContentVersionsFactory( 'bill_id')
VersionedMotion = ContentVersionsFactory( 'motion_id')
VersionedQuestion = ContentVersionsFactory( 'question_id' )
