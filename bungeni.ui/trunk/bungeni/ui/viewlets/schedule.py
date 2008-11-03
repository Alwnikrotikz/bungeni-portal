# encoding: utf-8
# Calendar for scheduling questions
# at the top the questions available for scheduling are displayed,
# below you have a calendar that displays the sittings
# to schedule drag the question to be scheduled to the sitting

import calendar
import datetime
from types import *

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet.manager import WeightOrderedViewletManager
from zope.viewlet import viewlet
import zope.interface
from zope.security import proxy
from zope.formlib import form
from ore.alchemist.container import stringKey
from zc.resourcelibrary import need
from ore.alchemist import Session
from ore.workflow.interfaces import IWorkflowInfo

from interfaces import IScheduleCalendar
from bungeni.ui.utils import getDisplayDate
import bungeni.core.schema as schema
import bungeni.core.domain as domain
from bungeni.ui.browser import container
from bungeni.core.workflows.question import states
import bungeni.core.globalsettings as prefs

import sqlalchemy.sql.expression as sql
import sqlalchemy as rdb
from sqlalchemy.orm import mapper

import simplejson

### debug



#Among the “admissible” questions the Speaker or the Clerk's office will select questions for scheduling for a specific sitting 
#(please note, in many parliaments only a fraction of the approved questions are scheduled to be addressed in a sitting).


#For scheduling purposes, the system will retrieve the “admissible” but not yet scheduled questions 
#according to the sequence they were approved by the Speaker's Office or by other criteria set by each parliament.

#The system should not allow questions to be scheduled:

#      on a day the House is not sitting or;

#      on n days after the week in which the question was presented (with an override option)

#      when a different question from the same MP has been scheduled for that particular House sitting 
#      (exception may apply to this rule).

#The system should also store the following parameters:

#      maximum number of days ‘d' that can elapse between the time a question is sent to the relevant Ministry 
#      and the time the question is placed on the Order Paper has to be parameterised;

#      maximum number of questions ‘n' that can be asked in the House per sitting. 
#     (i.e. appear on the Order Paper) will also be parameterised;

#      maximum number of days that may elapse between the days a Minister receives a question and the day a written response 
#      is submitted to the clerk;

#      maximum number of days that may elapse between the day a question by private notice 
#      (questions that in the opinion of the Speaker are of an urgent nature) is scheduled for reply.

#       All scheduled Questions need to be printed/exported to then be forwarded on paper or electronically 
#       to the various Ministries and the relevant offices informing them also of the day in which they are scheduled.
#       Notifications will be sent to the Speaker and the Clerk listing all questions that have exceeded the limits stated above. 


class ScheduledQuestionItems( object ):
    """
    Questions scheduled for a sitting
    """
_scheduled_questions = rdb.join( schema.questions, schema.items_schedule, 
                                schema.questions.c.question_id == schema.items_schedule.c.item_id )
                                
scheduled_questions = mapper( ScheduledQuestionItems, _scheduled_questions)

class ScheduledMotionItems ( object ):
    """
    Motions scheduled for a sitting
    """
_scheduled_motions = rdb.join( schema.motions, schema.items_schedule, 
                                schema.motions.c.motion_id == schema.items_schedule.c.item_id )
                                
scheduled_questions = mapper( ScheduledMotionItems, _scheduled_motions)

class ScheduledBillItems( object ):
    """
    Bills scheduled for a sitting
    """
_scheduled_bills = rdb.join( schema.bills, schema.items_schedule, 
                                schema.bills.c.bill_id == schema.items_schedule.c.item_id )
                                
scheduled_bills = mapper( ScheduledBillItems, _scheduled_bills)


def getScheduledItemId ( schedule_id ):
    """
    return the item_id for a given schedule_id
    """
    session = Session()
    scheduled_item = session.query(domain.ItemSchedule).get(schedule_id)
    return scheduled_item.item_id


class QuestionJSONValidation( BrowserView ):
    """
    validate if a question can be scheduled for a sitting, 
    """
    
    def sittingBeforeApproval(self, sitting, question ):
        """
        the sitting date is before the question was approved
        so it cannot be scheduled for this sitting
        """
        if sitting.start_date.date() < question.approval_date:
            return "Question cannot be scheduled before it was approved by the clerk"
    
    
    def sittingToEarly(self, sitting, question):
        """
        A question cannot be scheduled on n days after the week in which the question was presented
        """
        noOfDaysBeforeQuestionSchedule = prefs.getNoOfDaysBeforeQuestionSchedule()
        minScheduleDate = question.approval_date + datetime.timedelta(noOfDaysBeforeQuestionSchedule)
        if sitting.start_date.date() < minScheduleDate:
            return "The question may not be scheduled before %s" %( datetime.date.strftime(minScheduleDate,'%Y-%m-%d') )
    
    
    def sittingToManyQuestions(self, question_id, sitting_questions):
        """
        the maximum number of questions in this sitting is exceeded
        """
        maxNoOfQuestions = prefs.getMaxQuestionsPerSitting()
        if question_id in sitting_questions:
            noOfQuestions = len(sitting_questions)
        else:
            noOfQuestions = len(sitting_questions) + 1
        if noOfQuestions >  maxNoOfQuestions:
            return "Maximum number of questions (%s) for this sitting exceeded" % noOfQuestions           
                                    
    def sittingToManyQuestionsByMP(self, question, questions ):
        """
        Maximum number of questions by a certain MP is exceeded
        """      
        maxNoOfQuestions = prefs.getMaxQuestionsByMpPerSitting()   
        noOfQuestions = 0
        memberOfParliament = u""
        session = Session()
        user_id = None
        for q in questions:
            if question.question_id != q.question_id:
                # do not count self
                if question.owner_id == q.owner_id:
                    noOfQuestions = noOfQuestions + 1
                    user_id =  q.owner_id
        if noOfQuestions > maxNoOfQuestions:
            session = Session()
            user = session.query(domain.User).get(user_id)
            username = u"%s %s" %( user.first_name, user.last_name )
            return "%s asked %s questions, a maximum of %s questions is allowed per MP and sitting" % (username, noOfQuestions, maxNoOfQuestions)
        
        
        
    def __call__( self ):
        """
        the sitting, questions in that sitting and the question to be scheduled for that sitting
        are passed as form parameters
        """
        errors = []
        warnings = []        
        form_data = self.request.form
        sitting_questions = []
        if form_data:
            #XXX some more cases to take care of!
            if form_data.has_key( 'sitting_id' ):
                sitting_id = long(form_data['sitting_id'][4:])
            if form_data.has_key( 'question_id'):   
                question_id = long(form_data['question_id'][2:])
            if form_data.has_key('q_id'):
                sq_ids = form_data['q_id']
                for qid in sq_ids:
                    if qid[:2] == 'q_' :
                        sitting_questions.append(long(qid[2:]))
        session = Session()
        questions = session.query(domain.Question).filter(schema.questions.c.question_id.in_(sitting_questions)).distinct().all()
        sitting = session.query(domain.GroupSitting).get(sitting_id)
        question = session.query(domain.Question).get(question_id)                
            
        result = self.sittingBeforeApproval( sitting, question )    
        if result:
            errors.append(result)
        result = self.sittingToEarly( sitting, question)
        if result:
            warnings.append(result)
        result = self.sittingToManyQuestions( question_id, sitting_questions)
        if result:
            warnings.append(result)
        result = self.sittingToManyQuestionsByMP( question, questions )    
        if result:
            warnings.append(result)
       
        #data = {'errors':['to many quesitions','question scheduled to early'], 'warnings': ['more than 1 question by mp...',]}
        data = {'errors': errors, 'warnings': warnings}
        return simplejson.dumps( data )

def start_DateTime( Date ):
    """
    return the start datetime for the query
    i.e. first of month 00:00
    """
    return datetime.datetime(Date.year, Date.month, 1, 0, 0, 0)
    
    
def end_DateTime( Date ):
    """
    return the end datetime for the query
    i.e. last of month 23:59
    """
    if Date.month == 12:
        month = 1
        year = Date.year + 1
    else:
        month = Date.month + 1
        year = Date.year    
    return datetime.datetime(year, month, 1, 0, 0, 0)  - datetime.timedelta(seconds=1)       
    
    
    
             
  
def current_sitting_query(date):
    """
    get the current session and return all sittings for that session.
    """    
    session=Session()
    cdfilter = sql.or_(
        sql.between(date, schema.parliament_sessions.c.start_date, schema.parliament_sessions.c.end_date),
        sql.and_( schema.parliament_sessions.c.start_date <= date, schema.parliament_sessions.c.end_date == None)
        )
    try:    
        query = session.query(domain.ParliamentSession).filter(cdfilter)[0]
    except:
        #No current session
        query = None
    results = query
    if results:
        # we are in a session
        session_id = results.session_id
    else:
        # no current session, get the next one
        try:                    
            query = session.query(domain.ParliamentSession
                            ).filter(
                            schema.parliament_sessions.c.start_date >= date
                            ).order_by(
                            schema.parliament_sessions.c.start_date)[0]
        except:
            #No next session
            query = None
        results = query                              
        if results:
            session_id = results.session_id
            date = results.start_date
        else:
            #no current and no next session so just get the last session
            try:                                
                query = session.query(domain.ParliamentSession
                                ).order_by(
                                schema.parliament_sessions.c.end_date.desc())[0]  
            except:
                #No last Session
                query = None
            results = query                            
            if results:
                session_id = results.session_id
                date = results.start_date
            else:
                # No session found
                date = datetime.date.today()
                session_id = -1 # None is not an option because group sittings (committees) do not have sessions                
    gsfilter = sql.and_(
                schema.sittings.c.start_date.between(start_DateTime( date ), end_DateTime( date )),
                schema.sittings.c.session_id == session_id)                                        
    gsquery =  session.query(domain.GroupSitting).filter(gsfilter).order_by(schema.sittings.c.start_date)      
    return gsquery, date        
            

class Calendar(BrowserView):
    __call__ = ViewPageTemplateFile("templates/schedule.pt")


class ScheduleCalendarViewletManager( WeightOrderedViewletManager ):
    """
    manage the viewlets that make up the calendar view
    """
    zope.interface.implements(IScheduleCalendar) 


class YUIDragDropViewlet( viewlet.ViewletBase ):
    """
    get the javascript for the YUI Drag and Drop
    """    
    approved_question_ids = []
    postponed_question_ids =[]
    scheduled_question_ids = []
    sitting_ids =[]
    
    
    
    def update(self):
        """
        refresh the query
        """
        self.approved_question_ids = []
        self.postponed_question_ids =[]
        self.scheduled_question_ids = []
        self.sitting_ids =[]
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()                
        session = Session()
        approved_questions = session.query(domain.Question).filter(schema.questions.c.status == states.admissible).distinct()
        results = approved_questions.all()
        for result in results:
            self.approved_question_ids.append(result.question_id)
        postponed_questions = session.query(domain.Question).filter(schema.questions.c.status == states.postponed).distinct()
        results = postponed_questions.all()
        for result in results:
            self.postponed_question_ids.append(result.question_id)  
                      
        sittings, self.Date = current_sitting_query(self.Date)    
        results = sittings.all()     
        for result in results:
            self.sitting_ids.append(result.sitting_id)     
        scheduled_question_filter = sql.and_(schema.items_schedule.c.sitting_id.in_(self.sitting_ids), 
                                            schema.questions.c.status == states.scheduled)
                                            #schema.items_schedule.c.status == states.scheduled)        
        scheduled_questions = session.query(ScheduledQuestionItems).filter(scheduled_question_filter).distinct()
        results = scheduled_questions.all()
        for result in results:
            self.scheduled_question_ids.append(result.schedule_id)    
            
    
    def render(self):
        need('yui-dragdrop')
        need('yui-animation')    
        #need('yui-logger')    #debug
        need('yui-json')
        JScript = """
<div id="user_actions">
 
</div>
<b id="list-counter"> 0 </b>
<form name="make_schedule" method="POST" action="" enctype="multipart/form-data">
  <input type="button" id="saveButton" value="Save" />
  <input id="form.actions.cancel" class="context" type="submit" value="Cancel" name="cancel"/>
</form>
        
<script type="text/javascript">
<!--
(function() {

var Dom = YAHOO.util.Dom;
var Event = YAHOO.util.Event;
var DDM = YAHOO.util.DragDropMgr;
var liProxyEl = document.createElement('li');
liProxyEl.id = "li_proxy_id";

//////////////////////////////////////////////////////////////////////////////
// example app
//////////////////////////////////////////////////////////////////////////////
YAHOO.example.DDApp = {
    init: function() {


        %(DDTarget)s
        %(DDList)s     
        
        Event.on("saveButton", "click", this.showOrder);     
        YAHOO.widget.Logger.enableBrowserConsole();   
    },

    showOrder: function() {
        var parseList = function(ul) {
            if (ul != null) {
                var el_option;
                var items = ul.getElementsByTagName("li");
                var el_select = document.createElement('select');
                el_select.multiple = "multiple";  
                el_select.name = ul.id;                                 
                
                for (i=0;i<items.length;i=i+1) {
                   
                    el_option=document.createElement("option");
                    el_option.selected = "selected";
                    el_option.value = items[i].id;
                    el_select.appendChild(el_option);
                }
               
                document.make_schedule.appendChild(el_select)
                return;            
            }
        };

       
        var %(targetList)s;       
         %(parseList)s           
        document.make_schedule.submit("form.actions.save");
    },


};

//////////////////////////////////////////////////////////////////////////////
// custom drag and drop implementation
//////////////////////////////////////////////////////////////////////////////

YAHOO.example.DDList = function(id, sGroup, config) {

    YAHOO.example.DDList.superclass.constructor.call(this, id, sGroup, config);

    this.logger = this.logger || YAHOO;
    var el = this.getDragEl();
    Dom.setStyle(el, "opacity", 0.67); // The proxy is slightly transparent

    this.goingUp = false;
    this.lastY = 0;
    this.originalEl = document.createElement('li');
    this.originalEl.id = "original_proxy_id";
     
    //var originalEl, originalParent;
};

YAHOO.extend(YAHOO.example.DDList, YAHOO.util.DDProxy, {
    
    
     getQuestionValidation: function(url, passData) {
          this.logger.log("data :" + passData);
          if (window.XMLHttpRequest) {              
            AJAX=new XMLHttpRequest();              
          } else {                                  
            AJAX=new ActiveXObject("Microsoft.XMLHTTP");
          }
          if (AJAX) {
            // false for synchronus request!
            //AJAX.open("POST", url, false);
            AJAX.open("GET", url + "?"+passData, false);
            AJAX.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            //AJAX.send(passData);
            AJAX.send(null);
            return AJAX.responseText;                                         
          } else {
             return false;
          }                                             
        },

    
    
    startDrag: function(x, y) {
        this.logger.log(this.id + " startDrag");
        // make the proxy look like the source element
        var dragEl = this.getDragEl();
        var clickEl = this.getEl();
        var parentEl = clickEl.parentNode;          
        // sometimes the proxy for the original element does
        // not get removed properly onDragDrop :(
        if (document.getElementById(this.originalEl.id) != null) {
            var opEl = document.getElementById(this.originalEl.id);
            var p_opEl = opEl.parentNode;
            p_opEl.removeChild(opEl)
            }
        parentEl.insertBefore(this.originalEl, clickEl.nextSibling);         
                         
        Dom.setStyle(clickEl, "visibility", "hidden");

        dragEl.innerHTML = clickEl.innerHTML;
    
        Dom.setStyle(dragEl, "color", Dom.getStyle(clickEl, "color"));
        Dom.setStyle(dragEl, "backgroundColor", Dom.getStyle(clickEl, "backgroundColor"));
        Dom.setStyle(dragEl, "border", "2px solid gray");      
        
    },


//    onMouseUp: function(e) {
//            var srcPEl = this.originalEl.parentNode;
//            srcPEl.removeChild(this.originalEl);
//        },


    onInvalidDrop: function(e) {
        var srcEl = this.getEl();
        var srcPEl = this.originalEl.parentNode;
        srcPEl.insertBefore(srcEl, this.originalEl);                
        srcPEl.removeChild(this.originalEl); 
        },

    endDrag: function(e) {
        var srcEl = this.getEl();
        var proxy = this.getDragEl();
        //var srcPEl = this.originalEl.parentNode;
        // Show the proxy element and animate it to the src element's location
        Dom.setStyle(proxy, "visibility", "");
        var a = new YAHOO.util.Motion( 
            proxy, { 
                points: { 
                    to: Dom.getXY(srcEl)
                }
            }, 
            0.2, 
            YAHOO.util.Easing.easeOut 
        )
        var proxyid = proxy.id;
        var thisid = this.id;      
        // Hide the proxy and show the source element when finished with the animation
        a.onComplete.subscribe(function() {
                Dom.setStyle(proxyid, "visibility", "hidden");
                Dom.setStyle(thisid, "visibility", "");
            });
        a.animate();
        //srcPEl.removeChild(this.originalEl); 
    },

    onDragDrop: function(e, id) {

        // If there is one drop interaction, the li was dropped either on the list,
        // or it was dropped on the current location of the source element.
        if (DDM.interactionInfo.drop.length === 1) {

            // The position of the cursor at the time of the drop (YAHOO.util.Point)
            var pt = DDM.interactionInfo.point; 

            // The region occupied by the source element at the time of the drop
            var region = DDM.interactionInfo.sourceRegion; 

            //
            var srcEl = this.getEl();
            var destEl = Dom.get(id);
            var destDD = DDM.getDDById(id); 
            var srcPEl = this.originalEl.parentNode;
            var valObject = { errors: [], warnings: []};
            var hasErrors = false;
            if (destEl.nodeName.toLowerCase() == "ol") {
                    Dom.removeClass(id, 'dragover');
                    var queryStr="";
                    var items = destEl.getElementsByTagName("li");
                    var sitting = {
                        sitting_id : destEl.id,
                        question_id : srcEl.id,
                        }
                    queryStr="sitting_id=" + destEl.id + "&question_id=" + srcEl.id    
                    var sitting_questions=new Array();
                    for (i=0;i<items.length;i=i+1) {
                        sitting_questions[i] = items[i].id;
                        queryStr = queryStr + "&q_id=" + items[i].id;
                        }
                    sitting.questions = sitting_questions;  
                    var jsonStr = YAHOO.lang.JSON.stringify(sitting);
                    //alert(jsonStr); 
                    var Validation=YAHOO.lang.JSON.parse(this.getQuestionValidation('./@@json_validate_question', queryStr));
                    if (Validation.errors.length >0) {
                        var errors = "" ;
                        for (i=0;i<Validation.errors.length;i=i+1) {
                            errors = errors + "\\n" + Validation.errors[i]
                            }
                        alert (errors);
                        hasErrors = true;
                        }
                    if (!(hasErrors)) {
                        if (Validation.warnings.length >0) {
                            var errors = "" ;
                            for (i=0;i<Validation.warnings.length;i=i+1) {
                                errors = errors + "\\n" + Validation.warnings[i]
                                }
                            errors = errors + "\\n" + "schedule anyway?"    
                            hasErrors = !(confirm (errors));
                            }                      
                        }    
                }
            if (destEl.nodeName.toLowerCase() == "li") {
                var pEl = destEl.parentNode;
                alert( srcEl.id + " -> " + destEl.id);
                if (pEl.nodeName.toLowerCase() == "ol") {                   
                    Dom.removeClass(pEl.id, 'dragover');
                    }
                }
            if (hasErrors) {
                //alert ("invalid target");
                //this.onInvalidDrop(e)
                //this.invalidDropEvent.fire()
                this.logger.log("proxy parent: " + srcPEl.id);
                srcPEl.insertBefore(srcEl, this.originalEl);                
            }
            // Check to see if we are over the source element's location.  We will
            // append to the bottom of the list once we are sure it was a drop in
            // the negative space (the area of the list without any list items)
            else {
            if (!region.intersect(pt)) {               
                destEl.appendChild(srcEl);
                destDD.isEmpty = false;                
            }
            }           
        }
        srcPEl.removeChild(this.originalEl); 
        DDM.refreshCache(); 
    },

    onDrag: function(e) {

        // Keep track of the direction of the drag for use during onDragOver
        var y = Event.getPageY(e);

        if (y < this.lastY) {
            this.goingUp = true;
        } else if (y > this.lastY) {
            this.goingUp = false;
        }

        this.lastY = y;
    },

/////////////////////////////////////////////////
/////////
    setListCounter : function ( destEl ) {
         // count the elements in the list
         return;
         var counterEl = Dom.get("list-counter");
         var itemCount = destEl.getElementsByTagName("li").length;
         counterEl.innerHTML = "- " + itemCount
    },

    onDragEnter: function(e, id) {        
        var destEl = Dom.get(id);
        //Dom.setStyle(liProxyEl.id, "visibility", "");
        if (destEl.nodeName.toLowerCase() == "ol") {
            //this.setListCounter( destEl);
            Dom.addClass(id, 'dragover');
            }            
        if (destEl.nodeName.toLowerCase() == "li") {
            var pEl = destEl.parentNode;
            if (pEl.nodeName.toLowerCase() == "ol") {
                //this.setListCounter(pEl);
                Dom.addClass(pEl.id, 'dragover');
                }
            }
        
    },

   
   
   onDragOut: function(e, id) {        
        var destEl = Dom.get(id);
         //Dom.setStyle(liProxyEl.id, "visibility", "hidden");
         if (destEl.nodeName.toLowerCase() == "ol") {
             Dom.removeClass(id, 'dragover');
            }            
        if (destEl.nodeName.toLowerCase() == "li") {
            var pEl = destEl.parentNode;
            if (pEl.nodeName.toLowerCase() == "ol") {
                 //Dom.removeClass(pEl.id, 'dragover');
                }
            }        
    },

////////////
///////////////////////////////////////////////

    onDragOver: function(e, id) {
        
        var srcEl = this.getEl();
        var destEl = Dom.get(id);
        
        // We are only concerned with list items, we ignore the dragover
        // notifications for the list.
        if (destEl.nodeName.toLowerCase() == "li") {
            var p = destEl.parentNode;

            if (this.goingUp) {
                p.insertBefore(srcEl, destEl); // insert above
            } else {
               p.insertBefore(srcEl, destEl.nextSibling); // insert below
            }

            DDM.refreshCache();
        }
    }
});

Event.onDOMReady(YAHOO.example.DDApp.init, YAHOO.example.DDApp, true);

})();

-->        
</script>         
        """
        DDList = ""
        for qid in self.approved_question_ids:            
            #new YAHOO.example.DDList("li" + i + "_" + j);
            DDList = DDList + 'new YAHOO.example.DDList("q_' + str(qid) +'"); \n'
        for qid in self.postponed_question_ids:
            DDList = DDList + 'new YAHOO.example.DDList("q_' + str(qid) +'"); \n'
        for qid in self.scheduled_question_ids:
            DDList = DDList + 'new YAHOO.example.DDList("isid_' + str(qid) +'"); \n'
        DDTarget = ""    
        for sid in self.sitting_ids:
            #new YAHOO.util.DDTarget("ul"+i);
            DDTarget = DDTarget + 'new YAHOO.util.DDTarget("sid_'  + str(sid) +'"); \n'
        #add the hardcoded targets for postponed and admissable list
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("admissible_questions"); \n'
        DDTarget = DDTarget + 'new YAHOO.util.DDTarget("postponed_questions"); \n'
        t_list = ""
        for sid in self.sitting_ids:
            # var ul1=Dom.get("ul1"), ul2=Dom.get("ul2"); 
            t_list = t_list + ' sid_'+ str(sid) +'=Dom.get("sid_' + str(sid) + '"),'
        t_list = t_list + 'admissible_questions=Dom.get("admissible_questions"),'
        t_list = t_list + 'postponed_questions=Dom.get("postponed_questions")'
        parseList =""
        for sid in self.sitting_ids:
            #parseList(ul1, "List 1") +
            parseList = parseList + 'parseList(sid_'+ str(sid) + '); \n'
        parseList = parseList +  'parseList(admissible_questions); \n'   
        parseList = parseList +  'parseList(postponed_questions);'
        maxQuestionsPerSitting = prefs.getMaxQuestionsPerSitting()
        js_inserts= {
            'DDList':DDList,
            'DDTarget':DDTarget,
            'targetList': t_list,
            'parseList': parseList,
            'maxQuestionsPerSitting': maxQuestionsPerSitting }
        return JScript % js_inserts           
        
        
class QuestionInStateViewlet( viewlet.ViewletBase ):
    name = state = None
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "_questions"    
    def getData(self):
        """
        return the data of the query
        """      
        data_list = []
        results = self.query.all()
        for result in results:            
            data ={}
            data['qid']= ( 'q_' + str(result.question_id) )                         
            data['subject'] = result.subject
            data_list.append(data)            
        return data_list
    
    
    def update(self):
        """
        refresh the query
        """
        session = Session()
        questions = session.query(domain.Question).filter(schema.questions.c.status == self.state)
        self.query = questions        
        
class PostponedQuestionViewlet( QuestionInStateViewlet ):
    """
    display the postponed questions
    """    
    name = state = states.postponed   
    list_id = "postponed_questions"    
    
    
class AdmissibleQuestionViewlet( QuestionInStateViewlet ):
    """
    display the admissible questions
    """    
    name = state = states.admissible
    render = ViewPageTemplateFile ('templates/schedule_question_viewlet.pt')    
    list_id = "admissible_questions"
    
    
    
    
class ScheduleCalendarViewlet( viewlet.ViewletBase, form.FormBase ):
    """
    display a calendar with all sittings in a month
    """
    
    @form.action((u"Save"), condition = None)                     
    def handleSaveAction(self, action, data):
        pdb.set_trace()    
        
    @form.action((u"Cancel"))                     
    def handleSaveAction(self, action, data):
        pdb.set_trace()          
    
    
    
        
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        self.Date=datetime.date.today()
        self.Data = []
        session = Session()
        self.type_query = session.query(domain.SittingType)
        
    def previous(self):
        """
        return link to the previous month 
        if the session start date is prior to the current month
        """            
        return ''
        
    def next(self):
        """
        return link to the next month if the end date
        of the session is after the 1st of the next month
        """        
        return ''


        
    def getData(self):
        """
        return the data of the query
        """
        sit_types ={}
        type_results = self.type_query.all()
        for sit_type in type_results:
            sit_types[sit_type.sitting_type_id] = sit_type.sitting_type
        data_list=[]      
        path = ''       
        results = self.query.all()
        for result in results:            
            data ={}
            data['sittingid']= ('sid_' + str(result.sitting_id) )     
            data['sid'] =  result.sitting_id                   
            data['short_name'] = ( datetime.datetime.strftime(result.start_date,'%H:%M')
                                    + ' (' + sit_types[result.sitting_type] + ')')
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
            data['day'] = int(result.start_date.day)
            data_list.append(data)            
        return data_list

    def getSittingQuestions(self, sitting_id):
        """
        return all questions assigned to that sitting
        """
        session = Session()
        questions = session.query(ScheduledQuestionItems).filter(schema.items_schedule.c.sitting_id == sitting_id)
        data_list=[] 
        results = questions.all()
        for result in results:            
            data ={}
            #data['qid']= ( 'q_' + str(result.question_id) ) 
            data['schedule_id'] = ( 'isid_' + str(result.schedule_id) ) # isid for ItemSchedule ID                        
            data['subject'] = result.subject
            data['status'] = result.status
            data_list.append(data)            
        return data_list



    def GetSittings4Day(self, day):
        """
        return the sittings for that day
        """
        day_data=[]
        for data in self.Data:
            if data['day'] == int(day):
                day_data.append(data)
        return day_data                
       
       
    def schedule_question(self, question_id, sitting_id, sort_id):
        print question_id, sitting_id, sort_id
        session = Session()
        item_schedule = domain.ItemSchedule()
        question = session.query(domain.Question).get(question_id)
        # set the question's parent to the application for security checks
        question.__parent__= self.context
        
        #question.context = self.context    
        #question.request = self.request    
        
        if question:
            if sitting_id:
                sitting = session.query(domain.GroupSitting).get(sitting_id)
            else:
                sitting = None                
            if sitting:
                if question.sitting_id is None:  
                    # our question is either admissible, deferred or postponed  
                    #XXX check_security=True
                    #question.sitting_id = sitting_id
                    item_schedule.sitting_id = sitting_id
                    item_schedule.item_id = question_id
                    item_schedule.order = sort_id
                    session.save(item_schedule)
                    IWorkflowInfo(question).fireTransitionToward(states.scheduled, check_security=True)
                    #if IWorkflowInfo(question).state().getState() == states.admissible:
                    #    IWorkflowInfo(question).fireTransition('schedule', check_security=True)
                    #elif IWorkflowInfo(question).state().getState() == states.deferred:
                    #    IWorkflowInfo(question).fireTransition('schedule-deferred', check_security=True)
                    #elif IWorkflowInfo(question).state().getState() == states.postponed:
                    #    IWorkflowInfo(question).fireTransition('schedule-postponed', check_security=True)
                    #else:
                    #    print "invalid workflow state:", IWorkflowInfo(question).state().getState()
                        
                elif question.sitting_id != sitting_id:  
                    # a question with a sitting id is scheduled
                    assert IWorkflowInfo(question).state().getState() == states.scheduled                  
                    IWorkflowInfo(question).fireTransition('postpone', check_security=True)
                    #assert question.sitting_id is None
                    #question.sitting_id = sitting_id
                    IWorkflowInfo(question).fireTransition('schedule-postponed', check_security=True)
                else:
                    #sitting stays the same - nothing to do
                    #print question.sitting_id == sitting_id
                    pass
            else:
                if question.sitting_id is not None: 
                    #question.sitting_id = sitting_id
                    if IWorkflowInfo(question).state().getState() == states.scheduled:
                        IWorkflowInfo(question).fireTransition('postpone', check_security=True)
                    
    def insert_questions(self, form):
        print form
        for sitting in form.keys():
            if sitting[:4] == 'sid_':
                qids = form[sitting]
                sitting_id = long(sitting[4:])     
                sort_id = 0           
                if type(qids) == ListType:
                    for qid in qids:                        
                        if qid[:2] == 'q_':
                            sort_id = sort_id + 1
                            question_id = long(qid[2:])
                            self.schedule_question(question_id, sitting_id, sort_id)
                        elif (qid[:5] == 'isid_'):
                            #this is a scheduled item
                            sort_id = sort_id + 1
                            schedule_id = long(qid[5:])
                            question_id = getScheduledItemId(schedule_id)
                            self.schedule_question(question_id, sitting_id, sort_id)
                if type(qids) in StringTypes:
                    if qids[:2] == 'q_':
                        question_id = long(qids[2:])
                        self.schedule_question(question_id, sitting_id, 1)  
                    elif (sitting[:5] == 'isid_'):
                        sort_id = sort_id + 1
                        schedule_id = long(qid[5:])
                        question_id = getScheduledItemId(schedule_id)
                        self.schedule_question(question_id, sitting_id, sort_id)
                                          
            elif (sitting == 'admissible_questions') or (sitting == 'postponed_questions'):                
                qids = form[sitting]
                print sitting
                if type(qids) == ListType:            
                    for qid in qids:                            
                        if qid[:2] == 'q_':                            
                            question_id = long(qid[2:])
                            self.schedule_question(question_id, None, 0)
                if type(qids) in StringTypes:
                    if qids[:2] == 'q_':
                        question_id = long(qids[2:])
                        self.schedule_question(question_id, None, 0)
#            elif :
#                qids = form['postponed_questions']
#                if type(qids) == ListType:
#                    for qid in qids:                            
#                        if qid[:2] == 'q_':
#                            sort_id = sort_id + 1
#                            question_id = long(qid[2:])
#                            self.schedule_question(question_id, None, 0)
#                if type(qids) in StringTypes:
#                    if qids[:2] == 'q_':
#                        question_id = long(qids[2:])
#                        self.schedule_question(question_id, None, 0)                        
       
    def update(self):
        """
        refresh the query
        """
    
        if self.request.form:
            if not self.request.form.has_key('cancel'):
                self.insert_questions(self.request.form) 
                
        self.Date = getDisplayDate(self.request)
        if not self.Date:
            self.Date=datetime.date.today()            
                
        self.query, self.Date = current_sitting_query(self.Date)        
        #print str(query)
        self.request.response.setCookie('display_date', datetime.date.strftime(self.Date,'%Y-%m-%d') )
        self.monthcalendar = calendar.monthcalendar(self.Date.year, self.Date.month)
        self.monthname = datetime.date.strftime(self.Date,'%B %Y')
        self.Data = self.getData()
    
    render = ViewPageTemplateFile ('templates/schedule_calendar_viewlet.pt')
    
