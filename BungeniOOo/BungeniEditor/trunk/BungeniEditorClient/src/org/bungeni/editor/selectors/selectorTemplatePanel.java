/*
 * selectorTemplatePanel.java
 *
 * Created on September 19, 2007, 11:34 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors;

import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JRootPane;
import javax.swing.JScrollPane;
import javax.swing.JSpinner;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.BungeniRegistryFactory;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.utils.MessageBox;
import org.jdesktop.swingx.JXDatePicker;

/**
 *
 * @author Administrator
 */
public class selectorTemplatePanel extends javax.swing.JPanel 
                implements IDialogSelector {
   
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(selectorTemplatePanel.class.getName());
 
    protected OOComponentHelper ooDocument;
    protected JDialog parent;
    protected toolbarAction theAction;
    protected toolbarSubAction theSubAction = null;

    protected SelectorDialogModes theMode;
    protected BungeniClientDB dbInstance=null;
    protected BungeniClientDB dbSettings = null;
    protected HashMap<String,String> theSerializationMap = new HashMap<String,String>();
    protected HashMap<String,String> theMetadataMap = new HashMap<String,String>();
    protected HashMap<String,Component> theControlMap = new HashMap<String,Component>();
    protected HashMap<String, Object> theControlDataMap = new HashMap<String, Object>();
    protected String windowTitle;
    
   //for selection mode apis 
   protected ArrayList<String> enabledControls = new ArrayList<String>(); 
 
    
    class dlgBackgrounds {
        Color background;
        String windowTitle = "";
        dlgBackgrounds(SelectorDialogModes mode) {
            if (mode == SelectorDialogModes.TEXT_SELECTED_INSERT) {
                  background = new Color(255, 255, 153);
                  windowTitle = "Selection Mode Insert";
              } else 
            if (mode == SelectorDialogModes.TEXT_SELECTED_EDIT) {
                  background = new Color(255, 255, 153);
                  windowTitle = "Selection Mode Edit";
              } else 
            if (mode == SelectorDialogModes.TEXT_INSERTION){
                  background = new Color(204, 255, 153);
                  windowTitle = "Insertion Mode";
            } else 
            if (mode == SelectorDialogModes.TEXT_EDIT){
                  background = new Color(150, 255, 153);
                  windowTitle = "Edit Mode";
            } else {
                background = new Color (100, 255, 153);
                windowTitle = "Mode not Selected";
            }
        }
        
        Color getBackground() {
            return background;
        }
        String getTitle() {
            return windowTitle;
        }
        }
    
    
    /** Creates a new instance of selectorTemplatePanel */
    public selectorTemplatePanel() {
    }
    
    public selectorTemplatePanel (OOComponentHelper ooDocument, 
            JDialog parentDlg, 
            toolbarAction theAction) {
            initVariables(ooDocument, parentDlg, theAction);
    }

    public selectorTemplatePanel(OOComponentHelper ooDocument, JDialog parentDlg, toolbarAction theAction, toolbarSubAction theSubAction) {
            initVariables(ooDocument, parentDlg, theAction, theSubAction);
    }
    
    protected void initVariables (OOComponentHelper ooDocument, JDialog parentDlg, toolbarAction theAction, toolbarSubAction theSubAction) {
       initVariables(ooDocument, parentDlg, theAction);
       this.theSubAction = theSubAction;
    }
    
    protected void initVariables (OOComponentHelper ooDocument, JDialog parentDlg, toolbarAction theAction) {
        this.ooDocument = ooDocument;
        this.parent = parentDlg;
        this.theAction = theAction;
        this.theMode = theAction.getSelectorDialogMode();
        dlgBackgrounds bg = new dlgBackgrounds(theMode);
        this.setBackground(bg.getBackground());
        this.windowTitle = bg.getTitle(); 
        HashMap<String,String> registryMap = BungeniRegistryFactory.fullConnectionString();  
        this.dbInstance = new BungeniClientDB(registryMap);
        this.dbSettings = new BungeniClientDB(DefaultInstanceFactory.DEFAULT_INSTANCE(), DefaultInstanceFactory.DEFAULT_DB());
        this.theSubAction = null;
    }
    
    public void setDialogMode(SelectorDialogModes mode) {
        this.theMode = mode;
    }

    public SelectorDialogModes getDialogMode() {
        return this.theMode;
    }

    public String getWindowTitle() {
        return windowTitle;
    }
    public void setOOComponentHelper(OOComponentHelper ooComp) {
        this.ooDocument=ooComp;
    }

    public void setToolbarAction(toolbarAction action) {
        this.theAction = action;
    }

    public void setParentDialog(JDialog dlg) {
        this.parent = dlg;
    }
    
    public void setSectionMetadataForAction(String sectionName, toolbarAction action) {
      
        HashMap<String,String> sectionMeta = new HashMap<String,String>();
        sectionMeta.put("BungeniSectionType", theAction.action_section_type());
        ooDocument.setSectionMetadataAttributes(sectionName, sectionMeta);
      
    }
    
    public void setSectionMetadataSectionType (String sectionName, String sectionType) {
      
        HashMap<String,String> sectionMeta = new HashMap<String,String>();
        sectionMeta.put("BungeniSectionType",sectionType);
        ooDocument.setSectionMetadataAttributes(sectionName, sectionMeta);
        
    }
       
    public HashMap<String,String> getSectionMetadataForAction(String sectionName) {
        HashMap<String,String> sectionMeta = new HashMap<String,String>();
        return ooDocument.getSectionMetadataAttributes(sectionName);
    }    
 
    public void buildComponentsArray() {
        getComponentsWithNames(this);
    }
    
   private void getComponentsWithNames(Container container) {
        
        for (Component component: container.getComponents()){
           String strName = null;
           if (component.getClass() == javax.swing.JList.class) {
               System.out.println("this is a jlist");
           }
           strName = component.getName();
           if (strName != null) {
               theControlMap.put(strName.trim(), component);
           }
     
           if (component instanceof JRootPane) {    
              JRootPane nestedJRootPane = (JRootPane)component;
              getComponentsWithNames(nestedJRootPane.getContentPane());
            }

           if (component instanceof JPanel) {
              // JPanel found. Recursing into this panel.
              JPanel nestedJPanel = (JPanel)component;
              getComponentsWithNames(nestedJPanel);
            }
           
           if (component instanceof JScrollPane) {
               JScrollPane nestedJScroller = (JScrollPane) component;
               getComponentsWithNames(nestedJScroller.getViewport());
           }
   
        }
        
    }
   
   //selection mode api
   
     //move to base class implementation
    protected ArrayList<String> checkFieldsMessages = new ArrayList<String>(0);
    
    protected boolean checkFields() {
        boolean fieldCheck = true;
        Iterator<String> enabledFields = enabledControls.iterator();
        while (enabledFields.hasNext()) {
            String fieldName = enabledFields.next();
            boolean tmpCheck = checkField(fieldName);
            //if any of the fields fails the checks, record it as a global failure
            if (tmpCheck == false) fieldCheck = false;
        }
        return fieldCheck;
    }
    
    protected void displayFieldErrors () {
        MessageBox.OK(parent, checkFieldsMessages.toArray());
        checkFieldsMessages.clear();
    }
    //move to base class implementation
    private boolean checkField (String fieldName) {
        Component componentField = theControlMap.get(fieldName);
        if (isValidationRequired(componentField)) {
            Object fieldValue =  getFieldValue(componentField);
            if (fieldValue == null ) {
                checkFieldsMessages.add("Field :"+ fieldName+ " cannot be blank!");
                return false;
            }
            boolean validationCheck = validateFieldValue(componentField, fieldValue);
            return validationCheck;
        } else 
            return true;
    }

   ///move to base class
    private Object getFieldValue (Component field) {
        if (field.getClass() == org.jdesktop.swingx.JXDatePicker.class ){
           JXDatePicker dateField = (JXDatePicker)field;
           Date fieldValue = dateField.getDate();
           return fieldValue;
        } else if (field.getClass() == javax.swing.JTextField.class) {
            JTextField textField = (JTextField) field;
            String fieldValue = textField.getText();
            return fieldValue ;
        } else if (field.getClass() == javax.swing.JList.class) {
            JList listField = (JList) field;
            Object fieldValue = listField.getSelectedValue();
            return fieldValue;
        } else if (field.getClass() == javax.swing.JComboBox.class)  {
            JComboBox comboField = (JComboBox) field;
            Object fieldValue = comboField.getSelectedItem();
            return fieldValue;
        } else if (field.getClass() == javax.swing.JTextArea.class) {
            JTextArea textareaField = (JTextArea) field;
            Object fieldValue = textareaField.getText();
            return fieldValue;
        } else if (field.getClass() == javax.swing.JSpinner.class ) {
            JSpinner spinnerField = (JSpinner) field;
            Object fieldValue = spinnerField.getValue();
            return fieldValue;
        } else {
            log.debug("getFieldValue: "+ field.getClass().getName()+ " field type not supported!");
            return null;
        }
        
    }
     
    protected boolean validateFieldValue(Component field, Object fieldValue) {
        return true;
    }
    
    protected ArrayList<String> getEnabledControls() {
          return this.enabledControls;
      }
 //move to base class
    private boolean isValidationRequired(Component c) {
        //add additional field types if required...
        if (c.getClass() == org.jdesktop.swingx.JXDatePicker.class ){
            return true;
        } else if (c.getClass() == javax.swing.JTextField.class) {
            return true;
        } else if (c.getClass() == javax.swing.JList.class) {
            return true;
        } else if (c.getClass() == javax.swing.JComboBox.class)  {
            return true;
        } else if (c.getClass() == javax.swing.JTextArea.class) {
            return true;
        } else {
            return false;
        }
    }

 public void selectionControlModes() {
        //set selection mode control modes
         getEnabledControlList();
         if (theControlMap.keySet().size() > 0 ) {
             Iterator<String> iterCtlNames = theControlMap.keySet().iterator();
             while (iterCtlNames.hasNext()) {
                 String controlname =   iterCtlNames.next();
                 if (!enabledControls.contains(controlname)) {
                     //disable all these controls
                     if (theControlMap.containsKey(controlname)) {
                         theControlMap.get(controlname).setVisible(false);
                     }
                 }
             }
         } else {
             log.debug("selectionControlModes: no controls with names were found");
         }
      }    

 protected void getEnabledControlList() {
         String actionFields = theSubAction.action_fields().trim();
         if (actionFields.indexOf(";") != -1) {
            String[] enabledFields =  actionFields.split(";");
            for (int i=0; i < enabledFields.length; i++ ) {
                enabledControlNameFromAction(enabledFields[i]);
            }
         } else {
            enabledControlNameFromAction(actionFields);
         }
         //add elements from ignore list
         /*
         for (int i=0; i < this.controls_ignore_list.length ; i++ ) {
             enabledControls.add(controls_ignore_list[i]);
         }
          */
      } 
     
    private void enabledControlNameFromAction (String actionField) {
                 String[] control_and_name = actionField.split(":");
                 String controlName = control_and_name[0].trim()+"_"+control_and_name[1].trim();
                 this.enabledControls.add(controlName);
                 String labelName = "lbl_" + control_and_name[1];
                 this.enabledControls.add(labelName);
      }
 
    
    //full insert events
    
    /*
     *Event that traps full insert events....
     *You dont have to override this, as this takes care of routing
     *..unless of course you want to override the routing
     *over-ride the pre/process/post insert functions in the dialog classes
     */
     protected void applyFullInsert() {
       log.debug("in applyFullInsert()");
       if (checkFields() == false) {
            if (!checkFieldsMessages.isEmpty()) {
                displayFieldErrors();   
                return;
            }
        }
       if (preFullInsert() == false) {
            //activities needed to be done before a full insert
            if (!checkFieldsMessages.isEmpty()) {
                displayFieldErrors();   
                return;
            }  
       }   
       if (processFullInsert() == false) {
            //activities needed to be done during a full insert 
           if (!checkFieldsMessages.isEmpty()) {
                displayFieldErrors();   
                return;
            }   
       }   
       if (postFullInsert() == false) {
            //activities to be done after a full insert  
            if (!checkFieldsMessages.isEmpty()) {
                displayFieldErrors();   
                return;
            }  
       }   else {
           parent.dispose();
       }
    }
     
    /*
     *All these functions are overriden in the dialog classes
     */ 
    protected boolean preFullInsert(){
        return true;
    }
    
    protected boolean postFullInsert(){
        return true;
    }
    
    protected boolean processFullInsert(){
        return true;
    }
  
     protected void applySelectEdit() {
        log.debug("applySelectEdit: not implemented yet");
     }
     
     protected void applySelectInsert() {
        log.debug("applySelectInsert: not implemented yet");
     }
     
    protected void formApply() {
      switch (getDialogMode()) {
        case TEXT_SELECTED_EDIT :
            applySelectEdit();
            break;
        case TEXT_SELECTED_INSERT :
            applySelectInsert();
            break;
        case TEXT_EDIT:
            applyFullEdit();
            break;
        case TEXT_INSERTION:
            log.debug("formApply: calling apllyFullInsert()");
            applyFullInsert();
            break;
        default:
            break;
    }
    }
    
    /*
     *Event that traps full insert events....
     *You dont have to override this, as this takes care of routing
     *..unless of course you want to override the routing
     *over-ride the pre/process/post insert functions in the dialog classes
     */
     protected void applyFullEdit() {
       if (checkFields() == false) {
            if (!checkFieldsMessages.isEmpty()) {
                displayFieldErrors();   
                return;
            }
        }
       if (preFullEdit() == false) {
            //activities needed to be done before a full insert
            if (!checkFieldsMessages.isEmpty()) {
                displayFieldErrors();   
                return;
            }  
       }   
       if (processFullEdit() == false) {
            //activities needed to be done during a full insert 
           if (!checkFieldsMessages.isEmpty()) {
                displayFieldErrors();   
                return;
            }   
       }   
       if (postFullEdit() == false) {
            //activities to be done after a full insert  
            if (!checkFieldsMessages.isEmpty()) {
                displayFieldErrors();   
                return;
            }  
       }   else {
           parent.dispose();
       }
    }
     
     
    /*
     *All these functions are overriden in the dialog classes
     */ 
    protected boolean preFullEdit(){
        return true;
    }
    
    protected boolean postFullEdit(){
        return true;
    }
    
    protected boolean processFullEdit(){
        return true;
    }
  
    
}


