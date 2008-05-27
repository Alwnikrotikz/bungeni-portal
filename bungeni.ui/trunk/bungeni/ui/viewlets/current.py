# encoding: utf-8
#
# dislay the current parliament/government with its subitems
# at a given date (defaults to current date)

from zope import component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet
import zope.interface
import datetime

from bungeni.ui.i18n import MessageFactory as _
import bungeni.core.domain as domain

from ore.alchemist import Session

from interfaces import ICurrent

import pdb
class Current(BrowserView):
    __call__ = ViewPageTemplateFile("current.pt")


class CurrentViewletManager( WeightOrderedViewletManager ):
    """Current viewlet manager."""
    zope.interface.implements(ICurrent) 

       
def getDisplayDate(request):   
    """
    get the date for which to display the data.
    #SQL WHERE:
    # displayDate BETWEEN start_date and end_date
    # OR
    # displayDate > start_date and end_date IS NULL   
    """ 
    filter_by = ''
    DisplayDate = request.get('date', None)
    if DisplayDate:
        try:
            y, m, d = (int(x) for x in DisplayDate.split('-'))
            displayDate = datetime.date(y,m,d)
        except:
            displayDate = datetime.date.today()              
    else:
        displayDate = datetime.date.today() 
        
    return displayDate

def getFilter(displayDate):                   
    if displayDate:
        filter_by = """
        '%(displayDate)s' BETWEEN start_date AND end_date
        OR
        '%(displayDate)s' > start_date AND end_date IS NULL
        """ % ({ 'displayDate' : displayDate})        
    else:
        filter_by = ""            
    return filter_by        
    
def getOrder( request, context_class ):
    """
    get the sort order
    """    
    order_list = []
    order_by = request.get('order_by', None)
    
    return order_list

class CurrentParliamentViewlet( viewlet.ViewletBase ):
    """
    display the current parliament.   
    """
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()
        
    def update(self):
        """
        refresh the query
        """
        session = Session()
        self.Date = getDisplayDate(self.request)
        self.query = session.query(domain.Parliament).filter(getFilter(self.Date))
        #.order_by( self.request, domain.Parliament )
        
    
    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        results = self.query.all()
        for result in results:            
            data ={}
            data['short_name'] = result.short_name
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)
        return data_list
                    
    render = ViewPageTemplateFile ('current_parliament_viewlet.pt')
        
        
class CurrentGovernmentViewlet( viewlet.ViewletBase ):         
    """
    display the current Government
    """
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()                       
        
    def update(self):        
        session = Session()
        self.Date = getDisplayDate(self.request)
        self.query = session.query(domain.Government).filter(getFilter(self.Date))
        


    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        results = self.query.all()
        for result in results:            
            data ={}
            data['short_name'] = result.short_name
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)
        return data_list
        
        
    render = ViewPageTemplateFile ('current_government_viewlet.pt')

class CurrentMinistriesViewlet( viewlet.ViewletBase ):
    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()                       
        
    def update(self):        
        session = Session()
        self.Date = getDisplayDate(self.request)
        self.query = session.query(domain.Ministry).filter(getFilter(self.Date))
        


    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        results = self.query.all()
        for result in results:            
            data ={}
            data['short_name'] = result.short_name
            data['full_name'] = result.full_name            
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)
        return data_list
        
        
    render = ViewPageTemplateFile ('current_ministries_viewlet.pt')    
    
class CurrentCommitteesViewlet( viewlet.ViewletBase ):
    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()                       
        
    def update(self):        
        session = Session()
        self.Date = getDisplayDate(self.request)
        self.query = session.query(domain.Committee).filter(getFilter(self.Date))
        


    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        results = self.query.all()
        for result in results:            
            data ={}
            data['short_name'] = result.short_name
            data['full_name'] = result.full_name            
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)
        return data_list
        
        
    render = ViewPageTemplateFile ('current_committees_viewlet.pt')        
