# encoding: utf-8
#
# dislay the current parliament/government with its subitems
# at a given date (defaults to current date)

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet, interfaces

import zc.resourcelibrary

import zope.interface
import datetime

from bungeni.ui.i18n import MessageFactory as _
import bungeni.core.domain as domain

from ore.alchemist import Session

from interfaces import ICurrent, ICurrentGovernment
from bungeni.ui.utils import getDisplayDate, getFilter


import pdb


def getDateFilter(request):
    displayDate = getDisplayDate(request) 
    if not displayDate:
        displayDate = datetime.date.today()       
    if displayDate:
        filter_by='?date=' + datetime.date.strftime(displayDate,'%Y-%m-%d')
    else:
        filter_by = ''
    return filter_by        

class Current(BrowserView):
    __call__ = ViewPageTemplateFile("current.pt")

class Government( BrowserView ):
    __call__ = ViewPageTemplateFile("current-gov.pt")

class CurrentViewletManager( WeightOrderedViewletManager ):
    """Current viewlet manager."""
    zope.interface.implements(ICurrent) 

class DateChooserViewletManager( interfaces.IViewletManager ):
    """ Viewlet manager for Date chooser """
    #zope.interface.implements(IDateChooser)
 
class CurrentGovernmentViewletManager( WeightOrderedViewletManager ):
    """Current viewlet manager."""
    zope.interface.implements(ICurrentGovernment)           
    
    
def getOrder( request, context_class ):
    """
    get the sort order
    """    
    order_list = []
    order_by = request.get('order_by', None)
    
    return order_list
    
class DateChooserViewlet( viewlet.ViewletBase ):
    """
    display a calendar to choose the date which to display the information for
    """    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager       
        self.Date=datetime.date.today()
        self.error = None
        self.error_message = None
        
    def _getDateConstraints(self):
        """
        get the start, end date of the parent
        """     
        if self.context.__parent__ is not None:
            parent = self.context.__parent__
            start_date = getattr( parent, 'start_date', None)   
            if type(start_date) == datetime.datetime:
                start_date = start_date.date()         
            end_date = getattr( parent, 'end_date', None)
            if type(end_date) == datetime.datetime:
                end_date = end_date.date()
            #pdb.set_trace()
            return start_date, end_date
        else:
            return None, None


    def checkDateInConstraints(self):
        """
        check if the date is in the constraints of the parent
        """
        if self.Date:
            start_date, end_date = self._getDateConstraints()
            if start_date:
                if self.Date < start_date:
                    return start_date
            if end_date:
                if self.Date > end_date:
                    return end_date                    
        return None
            

    
    def update(self):
        """
        refresh the query
        """       
        zc.resourcelibrary.need("yui-calendar")
        zc.resourcelibrary.need("yui-container")
        zc.resourcelibrary.need("yui-button")
        
        self.Date = getDisplayDate(self.request)
        if self.Date:
            self.DateStr=datetime.date.strftime(self.Date,'%Y-%m-%d')
        else:
            self.DateStr='all'
            self.request.response.setCookie('display_date','all')
        minmaxdate= self.checkDateInConstraints()
        if minmaxdate:                    
            self.error = 'error' 
            self.error_message = _("""
                The date you requested (%(current)s) is not in the current restrictions. <br />
                Either select <a href="?date=%(minmax)s"> %(minmax)s </a> 
                or browse the data <a href="?date=all">for all dates</a>.
                """) % ({'current': self.DateStr , 'minmax': minmaxdate})           
            
    render = ViewPageTemplateFile ('date_chooser_viewlet.pt')    
            
            
class AllParliamentsViewlet( viewlet.ViewletBase ):
    """
    display all parliaments
    """            
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.current_query = None
        self.Date=datetime.date.today()
        
    def update(self):
        """
        refresh the query
        """
        session = Session()
        self.query = session.query(domain.Parliament)
        self.Date = getDisplayDate(self.request) 
        #current
        if not self.Date:
            self.Date = datetime.date.today()
            self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.current_query = session.query(domain.Parliament).filter(getFilter(self.Date))    

    def getData(self):
        """
        return the data of the query
        """        
        data_list=[]
        curlpf=getDateFilter(self.request)  
        current_results = self.current_query.all()      
        results = self.query.all()
        for result in results:            
            data ={}
            if result.start_date and result.end_date:
                #diff = result.end_date - result.start_date
                #mid = result.start_date + diff/2
                urlpf = '?date=' + datetime.date.strftime(result.end_date,'%Y-%m-%d')
            else:
                urlpf ='?date=' + datetime.date.strftime(datetime.date.today(),'%Y-%m-%d')            
            data['url']= '/parliament/' +urlpf
            data['short_name'] = result.short_name
            data['election_date'] = result.election_date
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['mpurl']= '/parliament/obj-' + str(result.parliament_id) + '/parliamentmembers' + urlpf
            if result in current_results:
                data['current'] = 'even'
                data['selector'] = '-->>'
                data['mpurl']= '/parliament/obj-' + str(result.parliament_id) + '/parliamentmembers' + curlpf
                data['url']= '/parliament/' + curlpf
            else:
                data['current'] = 'odd' 
                data['selector'] = ''               
            data_list.append(data)
        return data_list
                    
    render = ViewPageTemplateFile ('current_parliament_viewlet.pt')


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
        if not self.Date:
            self.Date = datetime.date.today()
            self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.query = session.query(domain.Parliament).filter(getFilter(self.Date))        
        
    
    def getData(self):
        """
        return the data of the query
        """
        data_list=[]
        urlpf=getDateFilter(self.request)        
        results = self.query.all()
        for result in results:            
            data ={}
            data['url']= '/parliament/obj-' + str(result.parliament_id) + urlpf
            data['short_name'] = result.short_name
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['mpurl']= '/parliament/obj-' + str(result.parliament_id) + '/parliamentmembers' + urlpf
            data['current'] = 'odd'
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
        if not self.Date:
            self.Date = datetime.date.today()
        self.query = session.query(domain.Government).filter(getFilter(self.Date))
        


    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        urlpf=getDateFilter(self.request)
        results = self.query.all()
        for result in results:            
            data ={}
            data['url']= ('/parliament/obj-' + str(result.parliament_id) +
                          '/governments/obj-' + str(result.government_id) + urlpf)
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
        if not self.Date:
            self.Date = datetime.date.today()
        self.query = session.query(domain.Ministry).filter(getFilter(self.Date))
        


    def getData(self):
        """
        return the data of the query
        """   
        session = Session()   
        urlpf=getDateFilter(self.request)                  
        data_list=[]        
        results = self.query.all()
        if results:
            m_id= results[0].ministry_id
            mpg_query = session.query(domain.MinistryInParliament).filter(domain.MinistryInParliament.c.ministry_id == m_id)
            mpg_result = mpg_query.first()
                    

        for result in results:            
            data ={}
            data['url']= ('/parliament/obj-' + str(mpg_result.parliament_id) +
                          '/governments/obj-' + str(mpg_result.government_id) + 
                          '/ministries/obj-' + str(result.ministry_id) + urlpf)
            data['minister_url']= ('/parliament/obj-' + str(mpg_result.parliament_id) +
                          '/governments/obj-' + str(mpg_result.government_id) + 
                          '/ministries/obj-' + str(result.ministry_id) + 
                          '/ministers' + urlpf)
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
        if not self.Date:
            self.Date = datetime.date.today()
        self.query = session.query(domain.Committee).filter(getFilter(self.Date))
        


    def getData(self):
        """
        return the data of the query
        """
        data_list=[]        
        urlpf=getDateFilter(self.request)
        results = self.query.all()
        for result in results:            
            data ={}
            data['url']= ('/parliament/obj-' + str(result.parliament_id) +
                          '/committees/obj-' + str(result.committee_id) + urlpf)
            data['short_name'] = result.short_name
            data['full_name'] = result.full_name            
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data_list.append(data)
        return data_list
        
        
    render = ViewPageTemplateFile ('current_committees_viewlet.pt')    
    
class CurrentSitting( viewlet.ViewletBase ):
    """
    the current sittings are those closest to the given date.
    """        
    
    
