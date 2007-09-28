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
import java.util.HashMap;
import javax.swing.JDialog;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.BungeniRegistryFactory;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class selectorTemplatePanel extends javax.swing.JPanel 
                implements IDialogSelector {
    protected OOComponentHelper ooDocument;
    protected JDialog parent;
    protected toolbarAction theAction;
    protected SelectorDialogModes theMode;
    protected BungeniClientDB dbInstance=null;
    protected BungeniClientDB dbSettings = null;
    class dlgBackgrounds {
        Color background;
        
        dlgBackgrounds(SelectorDialogModes mode) {
            if (mode == SelectorDialogModes.TEXT_SELECTED) {
                  background = new Color(255, 255, 153);
              } else 
            if (mode == SelectorDialogModes.TEXT_INSERTION){
                  background = new Color(204, 255, 153);
            } else 
            if (mode == SelectorDialogModes.TEXT_EDIT){
                  background = new Color(150, 255, 153);
            } else {
                background = new Color (100, 255, 153);
            }
        }
        
        Color getBackground() {
            return background;
        }
        }
    
    
    /** Creates a new instance of selectorTemplatePanel */
    public selectorTemplatePanel() {
    }
    
    public selectorTemplatePanel (OOComponentHelper ooDocument, 
            JDialog parentDlg, 
            toolbarAction theAction) {
        this.ooDocument = ooDocument;
        this.parent = parentDlg;
        this.theAction = theAction;
        this.theMode = theAction.getSelectorDialogMode();
        dlgBackgrounds bg = new dlgBackgrounds(theMode);
        this.setBackground(bg.getBackground());
        HashMap<String,String> registryMap = BungeniRegistryFactory.fullConnectionString();  
        dbInstance = new BungeniClientDB(registryMap);
        dbSettings = new BungeniClientDB(DefaultInstanceFactory.DEFAULT_INSTANCE(), DefaultInstanceFactory.DEFAULT_DB());
    }

    public void setDialogMode(SelectorDialogModes mode) {
        this.theMode = mode;
    }

    public SelectorDialogModes getDialogMode() {
        return this.theMode;
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
    
    
}
