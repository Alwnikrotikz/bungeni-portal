/*
 * holderUIPanel.java
 *
 * Created on July 1, 2008, 3:16 PM
 */

package org.bungeni.editor.panels;

import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.HashMap;
import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JRadioButton;
import javax.swing.JTree;
import javax.swing.Timer;
import javax.swing.ToolTipManager;
import javax.swing.plaf.ComponentUI;
import javax.swing.plaf.basic.BasicTreeUI;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeCellRenderer;
import javax.swing.tree.TreePath;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.db.QueryResults;
import org.bungeni.db.SettingsQueryFactory;
import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.actions.EditorActionFactory;
import org.bungeni.editor.actions.IEditorActionEvent;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.actions.toolbarSubAction;
import org.bungeni.editor.panels.impl.IFloatingPanel;
import org.bungeni.editor.providers.DocumentSectionFriendlyAdapterDefaultTreeModel;
import org.bungeni.editor.providers.DocumentSectionFriendlyTreeModelProvider;
import org.bungeni.editor.providers.DocumentSectionProvider;
import org.bungeni.editor.selectors.SelectorDialogModes;
import org.bungeni.editor.toolbar.BungeniToolbarTargetProcessor;
import org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode;
import org.bungeni.editor.toolbar.BungeniToolbarXMLTreeNodeProcessor;
import org.bungeni.editor.toolbar.conditions.BungeniToolbarConditionProcessor;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.utils.CommonExceptionUtils;
import org.bungeni.utils.BungeniBNode;
import org.bungeni.utils.BungeniBTree;
import org.bungeni.utils.CommonTreeFunctions;
import org.bungeni.utils.NodeDisplayTextSetter;
import org.bungeni.utils.compare.BungeniTreeRefactorTree;

/**
 *
 * @author  undesa
 */
public class holderUIPanel extends javax.swing.JPanel implements IFloatingPanel {
    private OOComponentHelper ooDocument;
    private JFrame parentFrame;
    
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(holderUIPanel.class.getName());
    
    private org.bungeni.editor.toolbar.BungeniToolbarXMLTree toolbarXmlTree ;    
    private BungeniClientDB instance;
    private Timer timerSectionTree;
    /** Creates new form holderUIPanel */
    public holderUIPanel() {
        initComponents();
        instance = new BungeniClientDB (DefaultInstanceFactory.DEFAULT_INSTANCE(), DefaultInstanceFactory.DEFAULT_DB());
       //the below are called from initUI()
        // initToolbarTree();
       // initSectionStructureTree();
    }

    private void initToolbarTree(){
        try{
        toolbarXmlTree = new org.bungeni.editor.toolbar.BungeniToolbarXMLTree(toolbarTree);
        toolbarXmlTree.loadToolbar();
        toolbarTree.addMouseListener(new toolbarTreeMouseListener());
        toolbarTree.setCellRenderer(new toolbarTreeCellRenderer());
        //-tree-deprecated--CommonTreeFunctions.expandAll(toolbarTree, true);
       // toolbarTree.addTreeWillExpandListener(new toolbarTreeWillExpandListener());
        CommonTreeFunctions.expandAll(toolbarTree);
        //using a timer to repaint the tree causes very poor tab switching performnce in some cases
        //investigate using fireTreeNodesChanged
        javax.swing.Timer toolbarTreePaintTimer = new javax.swing.Timer(3000, new toolbarTreePaintTimerListener(toolbarTree));
        toolbarTreePaintTimer.start();
        //for note above about firenodeschanged, this has been implemented but works for model refresh ==> tree update.
        //but does not reflect in case of document cursor changes ==> reflecting back to the tree, as this requires a full iteration 
        //of the tree again. so for now implemented both as a treeTimer and fireNodeschanged event refresh
        ToolTipManager.sharedInstance().registerComponent(toolbarTree);
        } catch (Exception ex) {
            log.error("initTree: "+ ex.getMessage());
        }
    }

    private void initSectionStructureTree(){
         sectionStructureTree.setExpandsSelectedPaths(true);
         ImageIcon minusIcon = CommonTreeFunctions.treeMinusIcon();
         ImageIcon plusIcon = CommonTreeFunctions.treePlusIcon();
         sectionStructureTree.setCellRenderer(new treeViewPrettySectionsTreeCellRenderer());
         sectionStructureTree.setShowsRootHandles(true);
         ComponentUI treeui = sectionStructureTree.getUI();
         if (treeui instanceof BasicTreeUI){
             ((BasicTreeUI)treeui).setExpandedIcon(minusIcon);
             ((BasicTreeUI)treeui).setCollapsedIcon(plusIcon);
         }
        initSectionStructureTreeModel();     
        Action sectionViewRefreshRunner = new AbstractAction() {
                public void actionPerformed (ActionEvent e) {
                    updateSectionTree();
                }
            };
        timerSectionTree = new Timer(3000, sectionViewRefreshRunner);
        timerSectionTree.setInitialDelay(2000);
        timerSectionTree.start();
    }

    private void initSectionStructureTreeModel(){
        try {
        DocumentSectionFriendlyAdapterDefaultTreeModel model = DocumentSectionFriendlyTreeModelProvider.create() ;//_without_subscription();
        this.sectionStructureTree.setModel(model);
        CommonTreeFunctions.expandAll(sectionStructureTree);
        } catch (Exception ex) {
            log.error ("initSectionStructureTreeModel : " + ex.getMessage());
            log.error ("initSectionStructureTreeModel : " + CommonExceptionUtils.getStackTrace(ex));
        }
    }
    
    private holderUIPanel self(){
        return this;
    }
    
    private void initButtonListeners() {
        btnViewDefault.setSelected(true);
        //add action listeners to button
        btnViewDefault.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent arg0) {
                JRadioButton btn = (JRadioButton) arg0.getSource();
                if (btn.isSelected()){
                    scrollToolbarTree.setVisible(true);
                    scrollTreeView.setVisible(true);
                    self().parentFrame.setVisible(true);
                    self().parentFrame.setExtendedState(JFrame.NORMAL);
                }
            }
        });
        btnHideToolbarTree.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent arg0) {
                JRadioButton btn = (JRadioButton) arg0.getSource();
                if (btn.isSelected()){
                    scrollToolbarTree.setVisible(false);
                    scrollTreeView.setVisible(true);
                    //revalidate does 're-layout' of the panel
                    self().revalidate();
                }
            }
        });
        btnHideTreeView.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent arg0) {
                JRadioButton btn = (JRadioButton) arg0.getSource();
                if (btn.isSelected()){
                    scrollToolbarTree.setVisible(true);
                    scrollTreeView.setVisible(false);
                    //revalidate does 're-layout' of the panel
                    self().revalidate();
                }
            }
        });
    }
       
    
    private void initMouseListener(){
        parentFrame.addMouseListener(new MouseListener(){
            public void mouseClicked(MouseEvent arg0) {
            }
            public void mousePressed(MouseEvent arg0) {
            }
            public void mouseReleased(MouseEvent arg0) {
            }
            public void mouseEntered(MouseEvent arg0) {
                log.debug("mouseListener : entered holderUIPanel" );
                parentFrame.requestFocus();
            }
            public void mouseExited(MouseEvent arg0) {
            }
        });
    }
 
    private void updatePanelonComponentChange(){
        updateSectionTree();
    }
    
    private synchronized void updateSectionTree() {
        NodeDisplayTextSetter nsetter = new NodeDisplayTextSetter(ooDocument);
        BungeniBNode.setINodeSetterCallback(nsetter);

        BungeniBTree newTree = DocumentSectionProvider.getNewFriendlyTree();
        log.debug("initList: refreshing tree : " + newTree.toString());
         BungeniBNode newRootNode = newTree.getFirstRoot();

         DocumentSectionFriendlyAdapterDefaultTreeModel model = (DocumentSectionFriendlyAdapterDefaultTreeModel) this.sectionStructureTree.getModel();
         DefaultMutableTreeNode mnode = (DefaultMutableTreeNode) model.getRoot();
         BungeniBNode origNode = (BungeniBNode) mnode.getUserObject();
         BungeniTreeRefactorTree refTree = new BungeniTreeRefactorTree (model, origNode, newRootNode);
         refTree.doMerge();
    }
    
    class treeViewPrettySectionsTreeCellRenderer extends JLabel implements TreeCellRenderer {
        Color bgColor = new java.awt.Color(232, 255, 175);
        Color bgColorSelect = new java.awt.Color(207, 242, 255);
        treeViewPrettySectionsTreeCellRenderer(){
            setOpaque(true);
        }
        
        public Component getTreeCellRendererComponent(JTree tree, Object value, boolean selected, boolean expanded, boolean leaf, int row, boolean hasFocus) {
            setText(value.toString());
            if (value instanceof DefaultMutableTreeNode) {
                  DefaultMutableTreeNode uo = (DefaultMutableTreeNode)value;
                  Object uoObj = uo.getUserObject();
                  if (uoObj.getClass() == org.bungeni.utils.BungeniBNode.class) {
                      BungeniBNode aNode = (BungeniBNode) uoObj;
                      if (aNode.getName().equals(ooDocument.currentSectionName())) {
                          //setBorder(selBorder);
                          setBackground(bgColor);
                      } else if (selected) {
                            setBackground(bgColorSelect);
                      }  else {
                          setBackground(null);
                      }
                  }
            }
            return this;
        }
        
    }
    
    class toolbarTreeMouseListener implements MouseListener {
      
        public void mouseClicked(MouseEvent evt) {
      
        }

       public void mousePressed(MouseEvent evt) {
            //get treepath for currennt mouse click
            TreePath selPath = toolbarTree.getPathForLocation(evt.getX(), evt.getY());
            if (selPath != null ) {
                Object node = selPath.getLastPathComponent();
                if (node == null ) return;
                if (node.getClass() == org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode.class ) {
                    BungeniToolbarXMLAdapterNode toolbarXmlNode = (BungeniToolbarXMLAdapterNode) node;
                    if (toolbarXmlNode.childCount() == 0 && evt.getClickCount() == 2) {
                        processBungeniToolbarXmlAdapterNode(toolbarXmlNode); 
                    }
                }  
            }
       }
       private void processAction(toolbarAction action) {
           log.debug("processAction:" + action.action_name() );

           if (action.isTopLevelAction()) {
               log.info("toolbar: processAction: not processing topLevelAction type");
               return;
           }
          IEditorActionEvent event = getEventClass(action);
          event.doCommand(ooDocument, action, parentFrame);
       }
       
       private void processSubAction(toolbarSubAction action) {
           log.debug("processSubAction:" + action.sub_action_name() );
                   
              IEditorActionEvent event = getEventClass(action);
              event.doCommand(ooDocument, action, parentFrame);
       }
       
       private void processBungeniToolbarXmlAdapterNode (BungeniToolbarXMLAdapterNode adapterNode) {
              try {
              BungeniToolbarXMLTreeNodeProcessor nodeProc = new BungeniToolbarXMLTreeNodeProcessor(adapterNode);
              Object nodeUserObject = adapterNode.getUserObject();
                   //check if node is enabled or disabled
                   if (nodeUserObject != null) {
                       if (nodeUserObject.getClass() == treeGeneralEditorNodeState.class) {
                           treeGeneralEditorNodeState thestate = (treeGeneralEditorNodeState)nodeUserObject;
                           //if disabled, dont process, just return
                           if (thestate == treeGeneralEditorNodeState.DISABLED) {
                               log.debug("treeGeneralEditor, mousclick, node state was disabled ");
                             return;  
                           } 
                       }
                   }
                   //blank target, so nothing to process, return
                   if (nodeProc.getTarget() == null ){
                       log.debug("treeGeneralEditor, mousclick, target was null");
                       return;
                   } 
                   //if node is not visible, nothing to process, return
                   if (nodeProc.getVisible() == null ) {
                       return;
                   }
                   //based on the target information we need to create the action objectr
                   
                   String strTarget = nodeProc.getTarget();
                   log.info("processBungeniToolbarXmlAdapterNode  target = " + strTarget);
                   BungeniToolbarTargetProcessor targetObj = new BungeniToolbarTargetProcessor(strTarget);
                   SelectorDialogModes selectedMode = SelectorDialogModes.valueOf(nodeProc.getMode());
                   toolbarAction tbAction = null;
                   toolbarSubAction tbSubAction = null;
                   switch (targetObj.target_type) {
                       case ACTION:
                          tbAction =  processInsertion(targetObj);
                          tbAction.setSelectorDialogMode(selectedMode);
                          processAction (tbAction);
                          break;
                       case SUB_ACTION:
                          tbSubAction =  processSelection(targetObj); 
                          tbSubAction.setSelectorDialogMode(selectedMode);
                          processSubAction(tbSubAction);
                          break;
                   } 
                } catch (Exception ex) {
                    log.error("processBungeniToolbarXmlAdapterNode:"+ ex.getMessage());
                    log.error("processBungeniToolbarXmlAdapterNode:"+ CommonExceptionUtils.getStackTrace(ex));
                }
           
       }
       

       private toolbarSubAction processSelection(BungeniToolbarTargetProcessor targetObj) {
         
            String documentType = BungeniEditorProperties.getEditorProperty("activeDocumentMode");
            instance.Connect();
            String actionQuery = SettingsQueryFactory.Q_FETCH_SUB_ACTIONS(documentType, targetObj.actionName, targetObj.subActionName);
            log.info("processSelection: "+ actionQuery); 
            QueryResults qr = instance.QueryResults(actionQuery);
             instance.EndConnect();
             if (qr == null ) {
                 log.info("processSelection : queryResults :" + actionQuery + " were null, metadata incorrectly setup");
                 return null;
             }
             if (qr.hasResults()) {
                //this should return only a single toolbarSubAction
                 toolbarSubAction subActionObj =  new toolbarSubAction(qr.theResults().elementAt(0), qr.columnNameMap());
                 subActionObj.setActionValue(targetObj.actionValue);
                 return subActionObj;
             } else {
                  log.info("processSelection : queryResults :" + actionQuery + " were null, metadata incorrectly setup");
                 return null;
             }
       }
       private toolbarAction processInsertion(BungeniToolbarTargetProcessor targetAction) {
          // BungeniToolbarTargetProcessor targetObject = new BungeniToolbarTargetProcessor()
            String documentType = BungeniEditorProperties.getEditorProperty("activeDocumentMode");

           
           instance.Connect();
           String actionQuery = SettingsQueryFactory.Q_FETCH_ACTION_BY_NAME(documentType, targetAction.actionName);
           QueryResults qr = instance.QueryResults(SettingsQueryFactory.Q_FETCH_ACTION_BY_NAME(documentType, targetAction.actionName));
             instance.EndConnect();
             if (qr == null ) {
                 log.info("toolbar: processInsertion: the metadata has been setup incorrectly for action :" + targetAction.actionName);
                 return null;
             }
             if (qr.hasResults()) {
                 return new toolbarAction(qr.theResults().elementAt(0), qr.columnNameMap());
             } else {
                 log.info("toolbar: processInsertion: the metadata has been setup incorrectly for action :" + targetAction.actionName);
                 return null;
             }
       }
       
     
       
        public void mouseReleased(MouseEvent e) {
        }

        public void mouseEntered(MouseEvent e) {
        }

        public void mouseExited(MouseEvent e) {
        }

      
        
    }
    
    class toolbarTreePaintTimerListener implements ActionListener{
        private JTree timedTree;
        
        public toolbarTreePaintTimerListener(JTree timedTree){
            this.timedTree = timedTree;
        }
        
        public void actionPerformed(ActionEvent e) {
            if (timedTree.isShowing()) {
                this.timedTree.repaint();
            }
        }

 
        
    }
        
    /*Static declarations used by toolbar classes */
    static HashMap<String, toolbarIcon> toolbarIconMap = new HashMap<String,toolbarIcon>();
    static int BLOCK_ICON = 0, METADATA_ICON = 1, ACTION_ICON = 2;
    static String[] icons = { "block", "block_action", "metadata", "action"};
       
    class toolbarIcon {
            public String iconName;
            public ImageIcon enabledIcon;
            public ImageIcon disabledIcon;
            public toolbarIcon(String icon, String pathPrefix) {
                   String imgPathEnabled = pathPrefix + icon + "_enabled.png" ;
                   String imgPathDisabled = pathPrefix + icon +"_disabled.png" ;
                   enabledIcon = new ImageIcon(getClass().getResource(imgPathEnabled), "");
                   disabledIcon = new ImageIcon(getClass().getResource(imgPathDisabled), "");
            }
    
    }
         
    enum treeGeneralEditorNodeState {ENABLED, DISABLED};
    /*** caches conditionValue and condition processor for better performance **/
    HashMap<String, BungeniToolbarConditionProcessor> conditionMap = new HashMap<String, BungeniToolbarConditionProcessor>();
    class toolbarTreeCellRenderer extends JLabel implements TreeCellRenderer {

         int SECTION_ICON = 0;
         int SECTION_PLUS_ICON = 1;
         int MARKUP_ICON = 2;
         int TOPLEVEL_ICON=3;
         int DISABLED_ICON=4;
         Font labelFont = new Font("Tahoma", Font.PLAIN, 11);
         public toolbarTreeCellRenderer() {
            if (toolbarIconMap.size() == 0 ) {
                for (int i=0; i < icons.length; i++ ) {
                    toolbarIconMap.put(icons[i], new toolbarIcon(icons[i], "/gui/"));
                }
            }
         }
        private int ACTION_OBJECT=0, SELECTION_OBJECT=1;
        
        public void setToolbarStates() {
            
        }
        
        
        private toolbarIcon getIcon(String elementName ) {
            if (elementName.equals("root")) {
                return toolbarIconMap.get("block");
            } else if (elementName.equals("actionGroup")) {
                return toolbarIconMap.get("block");
            } else if (elementName.equals("blockAction")) {
                return toolbarIconMap.get("block_action");
            } else if (elementName.equals("action")) {
                return toolbarIconMap.get("action");
            } else if (elementName.equals("subaction")) {
                return toolbarIconMap.get("action");
            } else
                return toolbarIconMap.get("block");
        }
        
        
        public Component getTreeCellRendererComponent(JTree tree, Object value, boolean selected, boolean expanded, boolean leaf, int row, boolean hasFocus) {
                int objectType = -1;
                toolbarIcon currentIcon;
                Object userObj;
                if (ooDocument == null) {
                    return this;
                }
                try {
                   if (selected) 
                      setOpaque(true);
                   else
                      setOpaque(false);
                
                    //for selection object the node user object is always a string
                    //if (userObj.getClass() == java.lang.String.class) 
                    //     objectType = this.SELECTION_OBJECT;
                    if (value.getClass() == org.bungeni.editor.toolbar.BungeniToolbarXMLAdapterNode.class) {
                        BungeniToolbarXMLAdapterNode toolbarNode = (BungeniToolbarXMLAdapterNode)value;
                        BungeniToolbarXMLTreeNodeProcessor nodeProc = new BungeniToolbarXMLTreeNodeProcessor(toolbarNode);
                        toolbarIcon theIcon = getIcon(toolbarNode.node.getName());
                        org.jdom.Attribute visibleAttrib = toolbarNode.node.getAttribute("visible");
                        org.jdom.Attribute conditionAttrib = toolbarNode.node.getAttribute("condition");
                        org.jdom.Attribute nameAttrib = toolbarNode.node.getAttribute("name");
                        setFont(labelFont);
                        //if visible = false - disable the action
                        //if visible = true  - check if condition is required
                        //if condition = none - enable the action unconditionallhy
                        //if condition = something - check if the condition is valid
                        //enable the aciton only when the condition is valid
                        if (visibleAttrib == null) {
                           nodeEnabled(theIcon, nodeProc);
                        } else
                        if (visibleAttrib.getValue().equals("false")) {
                            nodeDisabled(theIcon, nodeProc);
                        } else
                        if (visibleAttrib.getValue().equals("true")) {
                            if (conditionAttrib == null ) {
                                //no condition act as if true
                                nodeEnabled(theIcon, nodeProc);
                            } else if (conditionAttrib.getValue().equals("none")) {
                                //no condition act as if true
                                nodeEnabled(theIcon, nodeProc);
                            } else if (conditionAttrib.getValue().length()> 0) {
                                //other condition always evaluates to whether action should be enabeld or disabled
                                boolean bCondition =  processActionCondition(conditionAttrib);
                               if (bCondition) {
                                   nodeEnabled(theIcon, nodeProc);
                               } else {
                                   nodeDisabled(theIcon, nodeProc);
                               }
                            }
                        }                    
                    
                    }
                
                } catch (Exception ex) {
                    log.error("cellRender error: " + ex.getMessage());
                    log.error("cellRender stackTrace: "+ org.bungeni.ooo.utils.CommonExceptionUtils.getStackTrace(ex));
                } finally {
                return this;
                }
        }

        void nodeEnabled(toolbarIcon theIcon, BungeniToolbarXMLTreeNodeProcessor nodeProc) {
            nodeProc.getAdapterNode().setUserObject(treeGeneralEditorNodeState.ENABLED);
            String ttText = nodeProc.getToolTip();
            if (ttText != null) {
               setToolTipText(ttText.replace('\n','-'));
            }
            setForeground(new java.awt.Color(0x00, 0x00,0x00));
      
            setIcon(theIcon.enabledIcon);
            setText(nodeProc.getTitle());
           // treeGeneralEditor.getModel().valueForPathChanged()
            //this.repaint();
            //tree.repaint();
        }
        
        
        void nodeDisabled(toolbarIcon theIcon, BungeniToolbarXMLTreeNodeProcessor nodeProc) {
            nodeProc.getAdapterNode().setUserObject(treeGeneralEditorNodeState.DISABLED);
            String ttText = nodeProc.getToolTip();
            if (ttText != null) {
                setToolTipText(ttText.replace('\n','-'));
            }
            setForeground(new java.awt.Color(0xFF, 0xCC,0xFF));
            setIcon(theIcon.disabledIcon);
            setText(nodeProc.getTitle());
                //this.repaint();
            //tree.repaint();
        }
       
         boolean processActionCondition(org.jdom.Attribute conditionAttrib) {
            boolean bAction = true;

            String conditionValue =  conditionAttrib.getValue().trim();
            if (conditionMap.containsKey(conditionValue)) {
                //already has conditionprocessor object, get cached object and reset...
                conditionMap.get(conditionValue).setOOComponentHandle(ooDocument);
            } else {
                BungeniToolbarConditionProcessor condProc = new BungeniToolbarConditionProcessor(ooDocument, conditionValue);
                conditionMap.put(conditionValue, condProc);
            }
             bAction = conditionMap.get(conditionValue).evaluate();

            return bAction;
        }


       }        
       
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        btnGroupSwitchView = new javax.swing.ButtonGroup();
        scrollToolbarTree = new javax.swing.JScrollPane();
        toolbarTree = new javax.swing.JTree();
        scrollTreeView = new javax.swing.JScrollPane();
        sectionStructureTree = new javax.swing.JTree();
        cboChangeStructure = new javax.swing.JComboBox();
        btnHideToolbarTree = new javax.swing.JRadioButton();
        btnHideTreeView = new javax.swing.JRadioButton();
        btnViewDefault = new javax.swing.JRadioButton();

        scrollToolbarTree.setViewportView(toolbarTree);

        scrollTreeView.setViewportView(sectionStructureTree);

        cboChangeStructure.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Item 1", "Item 2", "Item 3", "Item 4" }));

        btnGroupSwitchView.add(btnHideToolbarTree);
        btnHideToolbarTree.setText("Hide Toolbar Panel");

        btnGroupSwitchView.add(btnHideTreeView);
        btnHideTreeView.setText("Hide Section View Panel");

        btnGroupSwitchView.add(btnViewDefault);
        btnViewDefault.setText("Switch to Default View");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(scrollTreeView, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, 221, Short.MAX_VALUE)
            .addComponent(scrollToolbarTree, javax.swing.GroupLayout.DEFAULT_SIZE, 221, Short.MAX_VALUE)
            .addComponent(cboChangeStructure, 0, 221, Short.MAX_VALUE)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(btnHideToolbarTree)
                .addContainerGap(69, Short.MAX_VALUE))
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(btnViewDefault)
                .addContainerGap(49, Short.MAX_VALUE))
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(btnHideTreeView)
                .addContainerGap(37, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addComponent(scrollToolbarTree, javax.swing.GroupLayout.DEFAULT_SIZE, 253, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(scrollTreeView, javax.swing.GroupLayout.DEFAULT_SIZE, 253, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(cboChangeStructure, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(btnHideToolbarTree)
                .addGap(5, 5, 5)
                .addComponent(btnHideTreeView)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(btnViewDefault))
        );
    }// </editor-fold>//GEN-END:initComponents


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.ButtonGroup btnGroupSwitchView;
    private javax.swing.JRadioButton btnHideToolbarTree;
    private javax.swing.JRadioButton btnHideTreeView;
    private javax.swing.JRadioButton btnViewDefault;
    private javax.swing.JComboBox cboChangeStructure;
    private javax.swing.JScrollPane scrollToolbarTree;
    private javax.swing.JScrollPane scrollTreeView;
    private javax.swing.JTree sectionStructureTree;
    private javax.swing.JTree toolbarTree;
    // End of variables declaration//GEN-END:variables

    public static void main (String[] args){
             javax.swing.JFrame floatingFrame = new javax.swing.JFrame();
             holderUIPanel floatingPanel = new holderUIPanel();
             floatingFrame.add(floatingPanel);
             floatingFrame.setSize(221, 551);
             floatingFrame.setAlwaysOnTop(true);
             floatingFrame.setVisible(true);
            //position frame
            Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
            Dimension windowSize = floatingFrame.getSize();
            
            int windowX = screenSize.width - floatingFrame.getWidth() - 2;
            int windowY = (screenSize.height - floatingFrame.getHeight())/2;
            floatingFrame.setLocation(windowX, windowY);  // Don't use "f." inside constructor.
            floatingFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
    }

    public void setOOComponentHandle(OOComponentHelper ooComponent) {
            if (ooDocument != null ) {
                synchronized (ooDocument) {
                    this.ooDocument = ooComponent;
                    updatePanelonComponentChange();
                }
            } else {
                this.ooDocument = ooComponent;
            }
    }

    public Component getObjectHandle() {
        return this;
    }

    public IEditorActionEvent getEventClass(toolbarSubAction subAction) {
       IEditorActionEvent event = EditorActionFactory.getEventClass(subAction);
        return event;
    }
    
    public IEditorActionEvent getEventClass(toolbarAction action) {
       IEditorActionEvent event = EditorActionFactory.getEventClass(action);
        return event;
    }
    
    public void setParentWindowHandle(JFrame c) {
        this.parentFrame = c;
    }

    public JFrame getParentWindowHandle() {
        return this.parentFrame;
    }

    public void initUI() {
        this.initToolbarTree();
        this.initSectionStructureTree();
        this.initButtonListeners();
        this.initMouseListener();
    }
}
