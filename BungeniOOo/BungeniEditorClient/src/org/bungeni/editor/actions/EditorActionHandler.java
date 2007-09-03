/*
 * EditorActionHandler.java
 *
 * Created on August 20, 2007, 4:37 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.actions;

import com.sun.star.beans.PropertyValue;
import com.sun.star.text.XText;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextViewCursor;
import javax.swing.JDialog;
import javax.swing.WindowConstants;
import org.apache.log4j.Logger;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.selectors.InitDebateRecord;
import org.bungeni.editor.selectors.InitQuestionBlock;
import org.bungeni.editor.selectors.SelectorDialogModes;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.utils.MessageBox;

/**
 *
 * @author Administrator
 */
public class EditorActionHandler implements IEditorActionEvent {
     private static org.apache.log4j.Logger log = Logger.getLogger(EditorActionHandler.class.getName());
     private OOComponentHelper ooDocument;
    /** Creates a new instance of EditorActionHandler */
    public EditorActionHandler() {
    }

    public void doCommand(OOComponentHelper ooDocument, toolbarAction action) {
        //main action handler class 
        //can be implemented by any class that implements IEditorActionEvent]
        this.ooDocument = ooDocument;
        String cmd = action.action_name();
        if (cmd.equals("makeMastHead"))
            doMakePrayerSection(action);
        else if (cmd.equals ("makePrayerSection")) 
            doMakeSection(action);
        else if (cmd.equals("makeQASection"))
            doMakeSection(action);
        else if (cmd.equals("makePaperSection"))
            doMakeSection(action);
        else if (cmd.equals("makeNoticeOfMotionSection"))
            doMakeSection(action);
        else if (cmd.equals("makeQuestionBlockSection"))
            doMakeQuestionBlockSection(action);
        else if (cmd.equals("makePrayerMarkup"))
            doMarkup(action);
        else if (cmd.equals("makePaperMarkup"))
            doMarkup(action);
        else if (cmd.equals("makePaperDetailsMarkup"))
            doMarkup(action);
        else if (cmd.equals("makeNoticeOfMotionMarkup"))
            doMarkup(action);
        else if (cmd.equals("makeNoticeMarkup"))
            doMarkup(action);
        else if (cmd.equals("makeNoticeDetailsMarkup"))
            doMarkup(action);
        else
            MessageBox.OK("the command action: "+cmd+" has not been implemented!");    
    }
    
     private void doMakePrayerSection(toolbarAction action) {
      
            //section was added now prompt for dialog information
             JDialog initDebaterecord;
             initDebaterecord = new JDialog();
             initDebaterecord.setTitle("Enter Settings for Document");
             initDebaterecord.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
             //initDebaterecord.setPreferredSize(new Dimension(420, 300));
             InitDebateRecord panel = new InitDebateRecord(ooDocument, 
                     initDebaterecord, action);;
             initDebaterecord.getContentPane().add(panel);
             initDebaterecord.pack();
             initDebaterecord.setLocationRelativeTo(null);
             initDebaterecord.setVisible(true);
             initDebaterecord.setAlwaysOnTop(true);
       
     }
     
     private void doMakeQuestionBlockSection(toolbarAction action) {
            //section was added now prompt for dialog information
             JDialog makeQuestionBlock;
             makeQuestionBlock = new JDialog();
             makeQuestionBlock.setTitle("Enter Settings for Document");
             makeQuestionBlock.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
             //initDebaterecord.setPreferredSize(new Dimension(420, 300));
             InitQuestionBlock panel = new InitQuestionBlock(ooDocument, 
                     makeQuestionBlock, action);;
             
              if (ooDocument.isTextSelected())
                panel.setDialogMode(SelectorDialogModes.TEXT_SELECTED);
              else
                panel.setDialogMode(SelectorDialogModes.TEXT_INSERTION);

             makeQuestionBlock.getContentPane().add(panel);
             makeQuestionBlock.pack();
             makeQuestionBlock.setLocationRelativeTo(null);
             makeQuestionBlock.setVisible(true);
             makeQuestionBlock.setAlwaysOnTop(true);   
     }
     private int doMakeSection(toolbarAction action){
           //get the section name and numbering type for the command
           String namingConvention, numberingType;
           String newName = "";
           namingConvention = action.action_naming_convention();
           if (namingConvention.equals("")) {
                log.debug("unable to name section, section mame was blank");
                MessageBox.OK("The command:" + action.action_name()+" does not have a naming convention associated with it");
                return -1;
           }
           numberingType = action.action_numbering_convention();
           
           if (numberingType.equals("single")) {
                newName = namingConvention;
           } else if (numberingType.equals("serial")) {
                //do sequential naming thing....or whatever.....
                newName = namingConvention;
           } else if (numberingType.equals("")) {
               MessageBox.OK("The command: "+ action.action_name()+ " does not have a numbering type associated with it");
               return -1;
           }
           if (this.ooDocument.getTextSections().hasByName(newName)){
                   log.debug("in doc command: section  already exists");
                   MessageBox.OK("The section:  prayers already exists");
                   return 0;
            }
          else {
               log.debug("in doCommand : adding text section prayers");
               addTextSection(newName);
               return 1;
          }
    }
    private void addTextSection(String sectionName){
 
        String sectionClass = "com.sun.star.text.TextSection";
        XTextViewCursor xCursor = ooDocument.getViewCursor();
        XText xText = xCursor.getText();
        XTextContent xSectionContent = ooDocument.createTextSection(sectionName, (short)1);
        try {
            xText.insertTextContent(xCursor, xSectionContent , true);        
        } catch (com.sun.star.lang.IllegalArgumentException ex) {
            log.debug("in addTextSection : "+ex.getLocalizedMessage(), ex);
        }        
        
        
    }
    
      private void doMarkup(toolbarAction action) {
        log.debug("in doMarkup for command: "+action.action_name());
          
           String namingConvention = "", numberingType = "", newName = "";
           namingConvention = action.action_naming_convention();
           numberingType =action.action_numbering_convention();
           log.debug("naming convention = "+ namingConvention);
            if (namingConvention.equals("")) {
                log.debug("unable to name section, section mame was blank");
                MessageBox.OK("The command:" + action.action_name()+" does not have a naming convention associated with it");
                return;
            }
           log.debug("numbering type = " + numberingType);
           if (action.action_type().equals("markup")) {    
              
               PropertyValue[] loadProps = new com.sun.star.beans.PropertyValue[2];
               loadProps[0] = new PropertyValue();
               loadProps[0].Name = new String( "Template");
               loadProps[0].Value = namingConvention;
               loadProps[1] = new PropertyValue();
               loadProps[1].Name = new String( "Family");
               loadProps[1].Value = new Integer(2);
               log.debug("invoking execute dispatch");
               ooDocument.executeDispatch(".uno:StyleApply", loadProps);
           }
    }

}
