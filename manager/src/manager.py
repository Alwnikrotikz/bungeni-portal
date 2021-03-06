__author__="Ashok Hariharan"
__date__ ="$May 20, 2011 19:35:01 AM$"

"""
Defines application logic and views
"""


"""
System imports
"""
from ui import *
from org.dom4j import QName
from net.miginfocom.swing import MigLayout

"""
Application Imports
"""
from xml import UIXML, WorkflowXML


    
class FieldPanel(Panel): 
    """
    Extended Panel class for containing field controls
    """
  
    class ShowHideListener(MultiSelectListListener):
        """
        Listener for show hide list 
        """
        
        def __roles_element_for__(self, src_list):
            """
            Returns a roles_list corresponding to the modes list
            """
            if src_list.getName() == "show":
                return self.outer_self.roles_show
            else:
                return self.outer_self.roles_hide

        
        def value_changed(self, lsevt, src_list):
            """
            Event handler for list item change
            """
            if src_list.ignore_selection_event == False:
                ### first disable list selection listeners in the assoc_list
                # We first get the selected values in the source list
                # then we get the selected values in the associated list
                # then we un-select the values in the associated list that
                # have been selected in the source list 
                
                src_selected_values =  src_list.get_selected_values()#[str(sel) for sel in src_list.getSelectedValues()]
                assoc_selected_values = src_list.assoc_list.get_selected_values() #[str(sel) for sel in src_list.assoc_list.getSelectedValues()]
                list_items = self.outer_self.__get_items_in_list__(src_list.assoc_list)
                roles_show_hide = self.__roles_element_for__(src_list)
                if len(src_selected_values) == 0:
                    """
                    If no modes are selected, disable the corresponding roles element
                    """
                    roles_show_hide.setEnabled(False)
                else:
                    """
                    Otherwise we enable the corresponding roles selector - and sync
                    the modes list with the associated list.
                    """
                    roles_show_hide.setEnabled(True)
                    for src_selected in src_selected_values:
                        if src_selected in assoc_selected_values:
                            assoc_index = list_items.index(src_selected)
                            src_list.assoc_list.removeSelectionInterval(assoc_index, assoc_index)


    
    def __init__(self, title, index):
        Panel.__init__(self, title)
        from javax.swing.border import TitledBorder
        border = BorderFactory.createTitledBorder(None, title, 
                                                  TitledBorder.DEFAULT_JUSTIFICATION, 
                                                  TitledBorder.DEFAULT_POSITION,
                                                  Font("Courier", Font.BOLD, 19),
                                                  Color.MAGENTA.brighter())
        self.setName(title)
        self.setBorder(border)
        self.up_action = None
        self.down_action = None
        self.list_show = None
        self.list_hide = None
        self.roles_show = None
        self.roles_hide = None
        self.localizable = []
        """
        This is the original order of the field
        """
        self.order = index



class UIXMLPanel(Panel):
    """
    
    holder panel for all the ui.xml form access functionality
    
    This obeys the rules described here :
    
    http://code.google.com/p/bungeni-portal/wiki/HowTo_Customize_Forms_and_Listings
    
    * This WILL NOT generate empty <show /> <hide /> elements , 
    you must select modes , at least one mode is mandatory!
    
    * This WILL NOT generate <show>,<hide>  without modes -- 
    i.e. <show roles="x" /> will not be generated by this application
    
    """


    __ui_xml_title__ = "Forms"
    
    """
    Worker classes
    """
    class SaveXmlWorker(SwingWorker):
        """
        Saves the xml document in a background thread, and 
        refreshes the UI
        """
        
        def __init__(self, outer_self):
            self.outer_self = outer_self
            SwingWorker.__init__(self)
        
        def doInBackground(self):
            self.form_name = self.outer_self.forms_list.getSelectedItem()
            for field in self.outer_self.form_holder_panel.fields:
                # get the field node
                if len(field.localizable) > 0 :
                    # ignore fields which are not localizable
                    field_node = self.outer_self.uixml.get_form_field(self.form_name, field.title)
                    # get selected mode values in show, hide
                    show_modes_selected = field.list_show.get_selected_values()
                    print "show selected" , show_modes_selected
                    
                    self.outer_self.__save_visib_node__(field_node, 
                                             field.list_show.get_selected_values(), 
                                             field.roles_show.get_selected_values(), 
                                             "show")
                    self.outer_self.__save_visib_node__(field_node,
                                             field.list_hide.get_selected_values(), 
                                             field.roles_hide.get_selected_values(), 
                                             "hide")
                    self.outer_self.uixml.save_xml()
        
        def done(self):
            from java.util.concurrent import ExecutionException
            try:
                self.get()
                # reload the form holder panel after saving
                self.outer_self.load_form(self.form_name)
                self.outer_self.save_bn.setEnabled(True)
            except ExecutionException, e:
                print "Error while saving", e

    """
    Listener classes
    """
    from java.awt.event import ActionListener
    class FormsListListener(ActionListener):
        """
        ActionListener class for forms_list combo selection change
        """
        
        def __init__(self, parent_self):
            self.outer_self = parent_self
        
        def actionPerformed(self, evt):
            obj_selected = self.outer_self.forms_list.getSelectedItem()
            self.outer_self.load_form(obj_selected)


    from java.awt.event import ContainerAdapter
    class AddFieldPanelListener(ContainerAdapter):
        """
        Container listener for listening to add component events
        on form holder panel.
        We use this to enable or disable move up / move down buttons
        """
        def __init__(self, parent_self):
            self.outer_self = parent_self
        
        def componentAdded(self, container_event):
            added_container = container_event.getChild()
            if isinstance(added_container, FieldPanel):
                no_of_field_panels = len(self.outer_self.form_holder_panel.fields)
                for index,field_panel in enumerate(self.outer_self.form_holder_panel.fields):
                    if index == 0:
                        field_panel.up_action.setEnabled(False)
                        field_panel.down_action.setEnabled(True)
                    if index == no_of_field_panels -1 and index <> 0 :
                        field_panel.up_action.setEnabled(True)
                        field_panel.down_action.setEnabled(False)
                    if index > 0 and index < no_of_field_panels -1 :
                        field_panel.up_action.setEnabled(True)
                        field_panel.down_action.setEnabled(True)

                 
    class UpAction(TitledAction):
        """
        Action tied to the up button
        """
        
        def __init__(self, form_holder_panel, outer_self):
            TitledAction.__init__(self, name = "up", 
                                  display_title = "<html>&#8593; Move Up</html>")
            self.form_holder_panel = form_holder_panel
            self.outer_self = outer_self
            
        def actionPerformed(self, evt):
            # first remove the current component
            up_bn = evt.getSource()
            field_panel = up_bn.getParent()
            if isinstance(field_panel, FieldPanel):
                cur_index = self.form_holder_panel.field_index(field_panel)
                self.form_holder_panel.remove_field_panel(field_panel)
                self.form_holder_panel.add_field_panel_at_index(cur_index -1, field_panel)
                ### move field in xml
                form_fields = self.outer_self.uixml.get_form_by_name(self.form_holder_panel.title).elements()
                removed_field =form_fields.remove(cur_index)
                form_fields.add(cur_index -1, removed_field)
                ### move field in xml
                self.form_holder_panel.validate()
            
    class DownAction(TitledAction):
        """
        Action tied to the down button
        """
        
        def __init__(self, form_holder_panel, outer_self):
            TitledAction.__init__(self, name = "down", 
                                  display_title = "<html>&#8595; Move Down</html>")
            self.form_holder_panel = form_holder_panel
            self.outer_self = outer_self
            
        def actionPerformed(self, evt):
            down_bn = evt.getSource()
            field_panel = down_bn.getParent()
            if isinstance(field_panel, FieldPanel):
                cur_index = self.form_holder_panel.field_index(field_panel)
                self.form_holder_panel.remove_field_panel(field_panel)
                self.form_holder_panel.add_field_panel_at_index(cur_index + 1, field_panel)
                ### move field in xml
                form_fields = self.outer_self.uixml.get_form_by_name(self.form_holder_panel.title).elements()
                removed_field =form_fields.remove(cur_index)
                form_fields.add(cur_index + 1, removed_field)
                ### move field in xml
                self.form_holder_panel.validate()
    
    class ResetModesAction(TitledAction):
       
        def __init__(self, form_panel, field_panel):
            TitledAction.__init__(self, name="reset_mode",
                             display_title = "Reset Mode")
            self.form_panel = form_panel
            self.field_panel = field_panel
 
        def __multi_attrs_as_list__(self, element, attribute):
            attr_val = element.attributeValue(attribute)
            list_attr = [] if attr_val is None else attr_val.split(" ")
            return list_attr
 
        def actionPerformed(self, evt):
            uixml = UIXML(__uixml__())
            
            #self.field_panel.list_show.ignore_selection_event = True
            #self.field_panel.list_hide.ignore_selection_event = True
            
            elems_show = uixml.get_form_field_show(self.form_panel.title, 
                                                   self.field_panel.title)
            self.field_panel.list_show.clearSelection()
            self.field_panel.roles_show.clearSelection()
            if elems_show is not None:
                self.field_panel.list_show.set_selected_values(self.__multi_attrs_as_list__(elems_show, "modes"))
                self.field_panel.roles_show.set_selected_values(self.__multi_attrs_as_list__(elems_show, "roles"))
            else:
                print "elems show was none", elems_show
                        
            elems_hide = uixml.get_form_field_hide(self.form_panel.title, 
                                                   self.field_panel.title)
            self.field_panel.list_hide.clearSelection()
            self.field_panel.roles_hide.clearSelection()
            if elems_hide is not None:
                self.field_panel.list_hide.set_selected_values(self.__multi_attrs_as_list__(elems_hide, "modes"))
                self.field_panel.roles_hide.set_selected_values(self.__multi_attrs_as_list__(elems_hide, "roles"))
            else:
                print "elems hide was none", elems_hide

            #self.field_panel.list_show.ignore_selection_event = False
            #self.field_panel.list_hide.ignore_selection_event = False
 
    def load_form(self, form_name):
        """
        Loads a descriptor into the UI
        """
        uixml = UIXML(__uixml__())
        form_fields = uixml.get_form_fields(form_name)
        # update form_holder_panel (FormPanel)
        self.form_holder_panel.title = form_name
        # reinitialize the fields
        self.form_holder_panel.remove_field_panels()
        for index, form_field in enumerate(form_fields):
            self.add_field_to_holder_panel(index, form_field)
        self.form_holder_scroll.validate()
    
    def reset_field_order(self, evt):
        self.form_holder_panel.restore_original_order()

    def __add_visib_node_attrs__(self, visib_node, modes, roles):
        if len(modes) > 0 :
            # modes were selected
            attr_modes = " ".join(modes)
            visib_node.addAttribute(QName("modes"), attr_modes)
        else:
            # modes were not selected , we remove any existing modes
            visib_node.addAttribute(QName("modes"), None)
        if len(roles) > 0 :
            # roles were selected
            attr_roles = " ".join(roles)
            visib_node.addAttribute(QName("roles"), attr_roles)
        else:
            visib_node.addAttribute(QName("roles"), None)

        
    def __save_visib_node__(self, node, modes, roles, show_or_hide = "show"):
        visib_node = node.element(QName(show_or_hide))
        if visib_node is None and modes is not None and (len(modes) > 0 or len(roles) > 0):
            # if there is no show/hide node create it only if 
            # some modes and roles have been selected
            visib_node = node.addElement(QName(show_or_hide))
        if visib_node is not None:
            if modes is None or len(modes) == 0:
                visib_node.detach()
            else:
                #if the show/hide node exists add the attributes to it
                self.__add_visib_node_attrs__(visib_node, modes, roles)
        # if visib_node has no atttributes remove it
        if visib_node is not None and visib_node.attributeCount() == 0:
            visib_node.detach()       
        
    def save_xml(self, evt):
        self.save_bn.setEnabled(False)
        for field in self.form_holder_panel.fields:
            print "Before invoking background thread " , field.list_show
        self.SaveXmlWorker(self).execute()    
        
        
    def __init__(self):
        """
        Initializes the Panel
        
        We use the following structure 
        
        tabPanel (UIXMLPanel) 
             |
             |
             =====ScrollPane
                     |
                     == Form Panel
                         |
                         |
                         ==== Field panel
                         |
                         ==== Field panel 
                     .....
        
        """
        
        Panel.__init__(self, self.__ui_xml_title__)
        self.setLayout(MigLayout("wrap 2"))
        self.uixml = UIXML(__uixml__())
        self.forms_list = JComboBox(self.uixml.get_form_names(), 
                                    actionListener = self.FormsListListener(self))
        self.add(self.forms_list, "growx")
        self.save_bn = Button("Save", 
                              "Saves the customizations to the ui.xml file", 
                              actionPerformed=self.save_xml)
        self.add(self.save_bn)
        actionPanel = Panel("for actions")
        actionPanel.setLayout(MigLayout("wrap 2"))
        self.add(Button("Reset Order", 
                        "Restores the order represented by the un-saved XML file", 
                        actionPerformed=self.reset_field_order))
        self.add(JButton("Reset All"))
        self.add(actionPanel, "span 2")
        #self.add(JButton("Reset Order", actionPerformed=self.reset_field_order))
        #self.add(JButton("Reset All"))
        # create the form holder panel and add a container listener to it 
        # to listen to add component events
        self.form_holder_panel = FormPanel("form panel", 0)
        self.form_holder_panel.addContainerListener(self.AddFieldPanelListener(self))
        
        self.form_holder_panel.setLayout(MigLayout("wrap 1"))
        # We let MigLayout() figure out the preferred size
        #self.form_holder_panel.panel.setPreferredSize(Dimension(440,700))
        self.form_holder_scroll = JScrollPane(self.form_holder_panel)
        # We let MigLayout() figure out the preferred size
        #form_holder_scroll.setPreferredSize(Dimension(440,300))
        self.add(self.form_holder_scroll, "span 2, grow, push")
    
    def __add_show_hide_list__(self, field_panel, list_data, show_or_hide = "show"):
        lbl_field = GreenLabel(show_or_hide) if show_or_hide == "show" else RedLabel(show_or_hide)
        field_panel.add(lbl_field)
        list_field = MultiSelectList(list_data)
        list_field.setName(show_or_hide)
        list_field.setVisibleRowCount(4)
        sp_list_field = JScrollPane(list_field)
        from java.awt import Dimension
        sp_list_field.setMinimumSize(Dimension(200, 40))
        field_panel.add(sp_list_field)
        return list_field
    
    def add_field_to_holder_panel(self, index, field_node):
        """
        parses a <field> element adds corresponding swing controls
        for the element's attributes and adds them as controls to a
        FieldPanel
        """
        field_name = field_node.attributeValue("name")
        
        # create the field panel
        field_panel = FieldPanel(field_name, index)
        field_panel.setLayout(MigLayout("wrap 4"))
        #field_panel.setPreferredSize(Dimension(440,200))
        # add the show, hide list selectors, these are the only editable fields
        
        show_element = field_node.element(QName("show"))
        hide_element = field_node.element(QName("hide"))
        
        if field_node.attribute("localizable") is not None:
  
            lbl_localizable = BlackLabel("localizable")
            field_panel.add(lbl_localizable, "span 2")
            
            lbl_localizable_text = BlueLabel(field_node.attributeValue("localizable"))
            field_panel.add(lbl_localizable_text, "span 2")
            
            list_data = field_node.attributeValue("localizable").split(" ")
            field_panel.localizable = list_data
            
            field_panel.list_show = self.__add_show_hide_list__(field_panel, list_data, "show")
            field_panel.add(GreenLabel("for roles"))
            field_panel.roles_show = MultiSelectList(self.uixml.get_roles())
            field_panel.roles_show.setName("show")
            field_panel.add(field_panel.roles_show)
         
            field_panel.list_hide = self.__add_show_hide_list__(field_panel, list_data, "hide")
            field_panel.add(RedLabel("for roles"))
            field_panel.roles_hide = MultiSelectList(self.uixml.get_roles())
            field_panel.roles_hide.setName("hide")
            field_panel.add(field_panel.roles_hide)
            # link the 2 lists so they can invoke each others events
            field_panel.list_show.set_assoc_list(field_panel.list_hide)
            field_panel.list_hide.set_assoc_list(field_panel.list_show)
            field_panel.roles_show.set_assoc_list(field_panel.roles_hide)
            field_panel.roles_hide.set_assoc_list(field_panel.roles_show)
            
            if show_element is not None:
                """
                set the selections in the show element
                """
                modes = show_element.attributeValue("modes")
                if modes is not None and len(modes.strip()) > 0:
                    field_panel.list_show.set_selected_values(modes.split(" "))
                
                roles = show_element.attributeValue("roles")
                if roles is not None and len(roles.strip()) > 0 :
                    field_panel.roles_show.set_selected_values(roles.split(" "))
            else:
                """
                If <show> is not present - disable roles selection
                """
                field_panel.roles_show.setEnabled(False)
                    
            if hide_element is not None:
                """
                set the selections in the hide element
                """
                modes = hide_element.attributeValue("modes")
                if modes is not None and len(modes.strip()) > 0 :
                    field_panel.list_hide.set_selected_values(modes.split(" "))
                 
                roles = hide_element.attributeValue("roles")
                if roles is not None and len(roles.strip()) > 0 :
                    field_panel.roles_hide.set_selected_values(roles.split(" "))
            else:
                field_panel.roles_hide.setEnabled(False)
            
            field_panel.list_show.addListSelectionListener(field_panel.ShowHideListener(field_panel))
            field_panel.list_hide.addListSelectionListener(field_panel.ShowHideListener(field_panel))
            
            field_panel.add(JButton(self.ResetModesAction(self.form_holder_panel, field_panel)),
                             "span 2")
        else:
            field_panel.add(RedLabel("NOT LOCALIZABLE"), "span 2")
        
        # add up and down buttons 
        field_panel.up_action = self.UpAction(self.form_holder_panel, self)
        field_panel.down_action = self.DownAction(self.form_holder_panel, self)   
       
        field_panel.add(BlackLabel("ORIGINAL ORDER :"))
        field_panel.add(BlueLabel(str(field_panel.order + 1)))
        field_panel.add(JButton(field_panel.up_action), "span 1")
        field_panel.add(JButton(field_panel.down_action),"span 1")    
        
        # add the field panel to the form and validate
        self.form_holder_panel.add_field_panel(field_panel)
        self.form_holder_panel.validate()
               


class WorkflowXMLPanel(Panel):
    """
    Container panel for  a workflow.
    
    It uses the following structure
    
    WorkflowXMLPanel
        |
        --wfs_list combo selector for workflows
        |
        --forms_scroll (scroll pane)
            |
            -- forms panel (FormPanel) (for 1 workflow)
                |
                --- StatePanel (per workflow state)
                |
                --- StatePanel (per workflow state)
        
    """
  
    __panel_title__ = "Workflows"
    WF_list = []
  
    def __init__(self):
        """
        """
        Panel.__init__(self, self.__panel_title__)
        self.setLayout(MigLayout("wrap 2"))
        self.__build_wf_list__()
        self.wfs_list = JComboBox(self.WF_list, actionListener=self.WFListListener(self))
        self.add(self.wfs_list, "span 2, growx")
        # Now add the form_panel container
        self.form_panel = FormPanel("Workflow", 0)
        self.form_panel.addContainerListener(self.AddStatesPanelListener(self))
        self.form_panel.setLayout(MigLayout("wrap 1"))
        # We let MigLayout() figure out the preferred size
        self.form_scroll = JScrollPane(self.form_panel)    
        self.add(self.form_scroll, "span 2, grow, push")

    
    def get_WF_list(self):
        return [str(WF) for WF in self.WF_list]
    
    def __build_wf_list__(self):
        for wf in __wfxmls__():
            wfxml = WorkflowXML(wf)
            self.WF_list.append(self.WF(wfxml.get_title(), wf))

    def load_wf(self, wf):
        """
        Loads a descriptor into the UI
        """
        WFxml = WorkflowXML(wf.file)
        self.__load_wf_xml(WFxml)
        
    
    def __load_wf_xml(self, WFxml):
        self.form_panel.remove_field_panels()
        for state in WFxml.get_states():
            self.load_state(WFxml,state)

            
    def load_state(self, WFxml, state):
        self.form_panel.add_field_panel(self.StatePanel(self, WFxml, state))
        self.form_scroll.validate()
        
    def reload_wf(self):
        wf = self.wfs_list.getSelectedItem()
        from java.awt import Cursor
        self.setCursor(Cursor(Cursor.WAIT_CURSOR))
        self.load_wf(wf)
        self.setCursor(Cursor(Cursor.DEFAULT_CURSOR))
        
    """
    All contained classes here
    """

    """
    General use classes
    """

    class WF:
        """
        Object that groups workflow title and source file
        Used by wfs_list selector 
        """
        def __init__(self, title, file):
            self.title = title
            self.file = file
        
        def __repr__(self):
            """
            The list iterator uses the __repr__ to represent the 
            list objects
            """
            return self.title


    """
    Listener classes
    """
    from java.awt.event import ActionListener
    class WFListListener(ActionListener):
        """
        ActionListener class for forms_list combo selection change
        """
        
        def __init__(self, outer_self):
            self.outer_self = outer_self
        
        def actionPerformed(self, evt):
            wf = self.outer_self.wfs_list.getSelectedItem()
            from java.awt import Cursor
            self.outer_self.setCursor(Cursor(Cursor.WAIT_CURSOR))
            self.outer_self.load_wf(wf)
  

    from java.awt.event import ContainerAdapter
    class AddStatesPanelListener(ContainerAdapter):
        """
        This is invoked whenever a state panel is added
        to the form panel
        """
        def __init__(self, parent_self):
            self.outer_self = parent_self
        
        def componentAdded(self, container_event):
            added_container = container_event.getChild()
            pass


    """
    Contained Panel classes
    """
        
    class StatePanel(Panel):
        """
        Every state in the workflow is rendered in a panel - StatePanel
        """
        
        """
        This is the state node
        """
        state = None
    
                    
        def __init__(self, outer_self, WFxml, state):
            self.outer_self = outer_self
            self.WFxml = WFxml
            self.state = state
            self.state_id = state.attributeValue("id")
            Panel.__init__(self, self.state_id)
            self.setLayout(MigLayout("wrap 2"))
            from javax.swing.border import TitledBorder
            border = BorderFactory.createTitledBorder(None, 
                                                  state.attributeValue("title"), 
                                                  TitledBorder.DEFAULT_JUSTIFICATION, 
                                                  TitledBorder.DEFAULT_POSITION,
                                                  Font("Courier", Font.BOLD, 19),
                                                  Color.MAGENTA.brighter())
            self.setName(self.title)
            self.setBorder(border)
            self.__setup_widgets__()
        
        def __setup_widgets__(self):
            self.StateTableLoader(self, self.state_id).execute()
            pass
          
        def __load_table__(self, table_model):
            self.grants_table  = JTable(table_model)
            self.grants_scroll = JScrollPane(self.grants_table)
            from java.awt import Dimension
            self.grants_scroll.setPreferredSize(Dimension(300, 100))
            self.add(self.grants_scroll, "span 2, growx,push")
            #self.save_bn = Button("Save State","Save the grants for this state", actionPerformed=self.save_state_grants )
            #self.add(self.save_bn)
            self.validateTree()
            
        """
        All Contained classes in StatePanel
        """

        """
        Listener classes and functions
        """
        
        def __lookdown_assignment_and_act(self, grant_or_deny = False, assignment = None):
            """
             If the state appears as a like_state for another state - we need to go all 
             the way down the hierarchy to grant/deny in all the inheriting states
            """
            child_states = self.WFxml.get_child_states(self.state_id)
            for child_state in child_states:
                child_assignments = self.WFxml.get_applicable_state_assignments(child_state.attributeValue("id"))
                for child_assignment in child_assignments:
                    if child_assignment.inherited == False and grant_or_deny == child_assignment.grant:
                        child_assignment.state_grant.detach()
                            
                #if child_assignment.inherited == False:
                #    if assignment == child_assignment:
                #        child_assignment.state_grant.detach()
        
        def __lookup_assignment_and_act(self, grant_or_deny = False, assignment = None):
            
            """
             We check the applicable assignment of the like_state
             if there is no like_state, we grant/deny appropriately for the permission+role
             if there is a like_state
                We get the applicable assignments of the like_state
                if the permission+role combination exists for the like_state ;
                     -- and it matches the action (grant or deny), we delete the 
                     grant in the current state
            """ 
            name = "grant" if grant_or_deny==True else "deny"
            like_state = assignment.state_node.attributeValue("like_state")
     
            if like_state is None:
                assignment.state_grant.setName(name)
                self.__lookdown_assignment_and_act(grant_or_deny, assignment)
            else:
                ###
                # !-(LIKE_STATE) query the likeness and if the applicable assignment in the like
                # is a grant then delete the current element #
                pg_list = self.WFxml.get_applicable_state_assignments(like_state)
                if assignment in pg_list:
                    idx = pg_list.index(assignment)
                    if pg_list[idx].grant == grant_or_deny:
                        assignment.state_grant.detach()
       

        def save_state_grants(self, evt):
            self.save_state()                

        def save_state(self):
            """
            Saves a state
            """
            do_save = False
            table_model = self.grants_table.getModel()
            table_assignments = table_model.assignments
            for assignment in table_assignments:
                if assignment.edited:
                    ## if it has been edited save it
                    if assignment.grant:
                        """
                        if it is granted, confirm with QName
                        """
                        if assignment.state_grant.getQName().getName() == "grant":
                            """
                            Nothing to do 
                            If its granting the permission and the node is already a 'grant' node
                            """
                            pass
                        else:
                            if assignment.inherited:
                                print "Inherited assignment was changed ! add a grant node here "
                                self.WFxml.add_grant_to_state(assignment.state_node, 
                                                         assignment.state_grant.attributeValue("permission"), 
                                                         assignment.state_grant.attributeValue("role"))
                                print "Checking down the hierarchy"
                                #self.__lookdown_assignment_and_act(True, assignment)
                            else:
                                # Here we check up the like_state tree to see if a the same
                                # permission + role grant exists.
                                # if it exists 
                                #    We check it is also a grant, 
                                #    if it is a grant
                                #        we delete the current grant since its anyway inherited
                                self.__lookup_assignment_and_act(grant_or_deny = True, assignment = assignment)
                            do_save = True
                    else:
                        if assignment.state_grant.getQName().getName() == "deny":
                            """
                            Nothing to do 
                            If its denying the permission and the node is already a 'deny' node
                            """
                            pass
                        else:
                            ## rename to deny
                            if assignment.inherited:
                                print "Inherited assignment was changed ! add a deny node here"
                                self.WFxml.add_deny_to_state(assignment.state_node, 
                                                             assignment.state_grant.attributeValue("permission"), 
                                                             assignment.state_grant.attributeValue("role"))
                            else:
                                self.__lookup_assignment_and_act(grant_or_deny=False, assignment=assignment)
                            do_save = True
                else:
                    print "nothing to save"
            
            if do_save:
                print "saving xml"
                self.WFxml.save_xml()
        
        def reload_wf(self):
            self.outer_self.reload_wf()
                    
        """
        JTable related classes
        """
        
        from javax.swing.table import DefaultTableModel
        class StateTableModel(DefaultTableModel):
            """
            This class describes the Model for the table used
            to present the grant, deny for a state
            """
            
            column_names = ["Grant", "Permission", "Role"]
            
            """
            Presents a state node as a table model
            """
            def __init__(self, outer_self, state_id):
                self.outer_self = outer_self
                self.assignments = outer_self.WFxml.get_applicable_state_assignments(state_id)
                
            def getColumnName(self, col):
                return self.column_names[col] 
            
            def getColumnCount(self):
                return len(self.column_names)   
            
            def getRowCount(self):
                return len(self.assignments)
            
            def getValueAt(self, row, col):
                if col == 0:
                    return self.assignments[row].grant
                if col == 1:
                    return self.assignments[row].permission
                if col == 2:
                    return self.assignments[row].role
            
            def getColumnClass(self, index):
                from java.lang import Boolean,String,Object
                if index == 0:
                    return Object.getClass(Boolean.TRUE)
                else:
                    return Object.getClass(String(""))
            
            def isCellEditable(self, row, col):
                if col == 0:
                    return True
                else:
                    return False
                
            def setValueAt(self, value, row, col):
                if col == 0:
                    print "setting value for ", self.assignments[row], "edited = true"
                    self.assignments[row].grant = value
                    self.assignments[row].edited = True
                    self.outer_self.save_state()
                    self.outer_self.reload_wf()
                    #self.assignments[row].edited = False
                else:
                    pass
            
            def __update_assignment__(self, row, grant_value):
                self.assignments[row].grant = grant_value
                self.assignments[row].edited = True
            
                    
        class StateTableLoader(SwingWorker):
            
            def __init__(self, outer_self, state_id):
                self.outer_self = outer_self
                self.state_id  = state_id
                
            def doInBackground(self):
                table_model = self.outer_self.StateTableModel(self.outer_self, self.state_id)
                return table_model
            
            def done(self):
                from java.util.concurrent import ExecutionException
                try:
                    table_model = self.get()
                    self.outer_self.__load_table__(table_model)
                    from java.awt import Cursor
                    self.outer_self.outer_self.setCursor(Cursor(Cursor.DEFAULT_CURSOR))
                except ExecutionException, e:
                    print "Error while loading table", e


        class StateTableSaver(SwingWorker):
            pass


class Manager:
    """
    Entry point class for the application
    """

    def __init__(self):
        """
        Blank constructor , just to initialize the global manage
        """
        pass
    
    
    """
    Main class that glues the panels with the frame and launches the frame
    """

    def init(self, bungeni_path):
        from inst import Bungeni
        self.BUNGENI = Bungeni(bungeni_path)
        self.FRAME = Frame("Admin UI", (500,600), MigLayout("wrap 1"))
        tabPane = TabPane()
        # panel 1
        panel1 = UIXMLPanel()
        # add panels to tabs
        tabPane.add_tab(panel1)
        panel2 = WorkflowXMLPanel()
        #panel3 = Panel("Workflows")
        tabPane.add_tab(panel2)
        #tabPane.add_tab(panel3)
        # add to frame
        self.FRAME.add(tabPane.tab, "grow, push")
        self.FRAME.show()


"""
Manager is declared via a global variable
"""
global manage        
manage = Manager()

"""
Access APIs for global manage
"""
def __uixml__():
    global manage
    return manage.BUNGENI.ui_xml()

def __wfxml__(name):
    global manage
    return manage.BUNGENI.workflow(name)

def __wfxmls__():
    global manage
    return manage.BUNGENI.workflows()


def __manager_init__(path):
    global manage
    manage.init(path)

if __name__ == '__main__':
    import sys
    print sys.argv
    if len(sys.argv) == 2:
        print "bungeni running in ", sys.argv[1]
        __manager_init__(sys.argv[1])
    else:
        print "you need to pass the bungeni installation directory as a parameter"