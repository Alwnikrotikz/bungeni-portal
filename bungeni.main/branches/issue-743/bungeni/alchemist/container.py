# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Bungeni Alchemist container - [
    ore.alchemist.container
    alchemist.ui.container
]

$Id$
"""
log = __import__("logging").getLogger("bungeni.alchemist")


# used directly in bungeni
__all__ = [
    "valueKey",             # alias -> ore.alchemist.container
    "stringKey",            # redefn -> ore.alchemist.container
    "contained",            # redefn -> ore.alchemist.container
    "AlchemistContainer",   # redefn -> ore.alchemist.container
    "PartialContainer",     # redefn -> ore.alchemist.container
    
    "ContainerListing",     # alias -> alchemist.ui.container
    "getFields",            # redefn -> alchemist.ui.container
]


from bungeni.alchemist import Session, model, interfaces

#

from zope import interface
from zope.security import proxy
from zope.proxy import sameProxiedObjects
from zope.location.interfaces import ILocation
from zope.app.container.contained import Contained, ContainedProxy
from zope.app.container.interfaces import IContained
from zope.configuration.name import resolve
from persistent import Persistent

from sqlalchemy import orm, exceptions


# ore.alchemist.container

from ore.alchemist.container import valueKey

def stringKey(obj):
    """Replacement of ore.alchemist.container.stringKey
    
    The difference is that here the primary_key is not determined by 
    sqlalchemy.orm.mapper.primary_key_from_instance(obj) but by doing the 
    logically equivalent (but a little more laborious) 
    [ getattr(instance, c.name) for c in mapper.primary_key ].
    
    This is because, in some hard-to-debug cases, the previous was returning 
    None to all pk values e.g. for objects on which checkPermission() has not
    been called. Using this version, the primary_key is correctly determined
    irrespective of whether checkPermission() had previously been called on
    the object.
    """
    unproxied = proxy.removeSecurityProxy(obj)
    mapper = orm.object_mapper(unproxied)
    #primary_key = mapper.primary_key_from_instance(unproxied)
    identity_values = [ getattr(unproxied, c.name) for c in mapper.primary_key ]
    identity_key = "-".join(map(str, identity_values))
    return "obj-%s" % (identity_key)


# alchemist.ui.container

from alchemist.ui.container import ContainerListing

def getFields(context, interface=None, annotation=None):
    """Generator of all [zope.schema] fields that will be displayed in a 
    container listing.
    
    Redefines alchemist.ui.container.getFields, making use of the 
    @listing_columns property of the ModelDescriptor class.
    """
    if interface is None:
        domain_model = proxy.removeSecurityProxy(context.domain_model)
        interface = model.queryModelInterface(domain_model)
    if annotation is None:
        annotation = model.queryModelDescriptor(interface)
    for field_name in annotation.listing_columns:
        yield interface[field_name]


# ore.alchemist.container

def contained(obj, parent, name=None):
    """An implementation of zope.app.container.contained.contained
    that doesn't generate events, for internal use.

    copied from SQLOS / z3c.zalchemy (via ore.alchemist.container)
    """
    if (parent is None):
        raise TypeError("Must provide a parent")
    
    if not IContained.providedBy(obj):
        if ILocation.providedBy(obj):
            interface.directlyProvides(obj, IContained,
                interface.directlyProvidedBy(obj))
        else:
            obj = ContainedProxy(obj)
    
    oldparent = obj.__parent__
    oldname = obj.__name__
    
    if ((oldparent is None) or 
            not (oldparent is parent or sameProxiedObjects(oldparent, parent))
        ):
        obj.__parent__ = parent
    
    if oldname != name and name is not None:
        obj.__name__ = name
    
    return obj


class AlchemistContainer(Persistent, Contained):
    """A persistent container with contents from an rdbms.
    """
    _class_name = ""
    _class = None
    
    interface.implements(interfaces.IAlchemistContainer)

    def setClassName(self, name):
        self._class_name = name
        self._class = resolve(name)

    def getClassName(self):
        return self._class_name
    
    class_name = property(getClassName, setClassName)
    
    @property
    def domain_model(self):
        return self._class

    def batch(self, order_by=(), offset=0, limit=20, filter=None):
        """This method pulls a subset/batch of values for paging through a 
        container.
        """      
        query = self._query  
        if filter:
            query = query.filter(filter)
        if order_by:
            query = query.order_by(order_by)
        #limit and offset must be applied after filter and order_by            
        query = query.limit(limit).offset(offset)            
        for ob in query:
            ob = contained(ob, self, stringKey(ob))
            yield ob

    def query(self, **kw):
        return list(self._query.filter_by(**kw))

    @property
    def _query(self):
        session = Session()
        query = session.query(self._class)
        return query
        
    #################################
    # Container Interface
    #################################
    
    def keys(self):
        for name, obj in self.items():
            yield name
    
    def values(self):
        for name, obj in self.items():
            yield obj
    
    def items(self):
        for obj in self._query:
            name = stringKey(obj)
            yield (name, contained(obj, self, name))
    
    def get(self, name, default=None):
        try:
            key = valueKey(name)
        except KeyError:
            return default
        #value = self._query.get(key)
        # sqlalchemy 0.5.x does thow an exception instead of a warning as in .4.x:
        # InvalidRequestError: Query.get() being called on a Query with existing criterion.
        session = Session()
        value = session.query(self.domain_model).get(key)
        if value is None:
            return default
        value = contained(value, self, stringKey(value))
        return value
    
    def __iter__(self):
        return iter(self.keys())
    
    def __getitem__(self, name):
        value = self.get(name)
        if value is None:
            raise KeyError(name)
        return value
    
    def __setitem__(self, name, item):
        session = Session()
        session.add(item)
    
    def __delitem__(self, name):
        instance = self[ name ]
        session = Session()
        session.delete(instance)
    
    def __contains__(self, name):
        return self.get(name) is not None
    
    def __len__(self):
        try:
            return self._query.count()
        except exceptions.SQLError:
            return 0


class PartialContainer(AlchemistContainer):
    """An alchemist container that matches against an arbitrary subset,
    via definition of a query modification function. contents added to this
    container, may there fore not nesc. be accessible from it, unless they 
    also match the query. the alchemist ui views provide add views which can 
    maintain the constraint.
    """
    _subset_query = None
    
    def setQueryModifier(self, query):
        self._subset_query = query
    
    def getQueryModifier(self):
        return self._subset_query
    
    subset_query = property(getQueryModifier, setQueryModifier)
    
    @property
    def _query(self):
        query = super(PartialContainer, self)._query 
        return query.filter(self._subset_query)

