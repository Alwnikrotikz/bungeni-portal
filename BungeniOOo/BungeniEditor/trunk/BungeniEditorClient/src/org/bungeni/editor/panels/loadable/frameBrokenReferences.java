/*
 * frameBrokenReferences.java
 *
 * Created on May 25, 2008, 10:25 AM
 */

package org.bungeni.editor.panels.loadable;

import com.sun.star.beans.PropertyVetoException;
import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertySet;
import com.sun.star.container.XNameAccess;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextDocument;
import com.sun.star.text.XTextField;
import com.sun.star.text.XTextRange;
import com.sun.star.text.XTextSection;
import com.sun.star.text.XTextViewCursor;
import com.sun.star.uno.AnyConverter;
import com.sun.star.util.XRefreshable;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.TreeMap;
import javax.swing.BorderFactory;
import javax.swing.Icon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTree;
import javax.swing.ListSelectionModel;
import javax.swing.Renderer;
import javax.swing.border.Border;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.table.AbstractTableModel;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeCellRenderer;
import javax.swing.tree.TreeModel;
import javax.swing.tree.TreePath;
import org.bungeni.editor.numbering.ooo.OOoNumberingHelper;
import org.bungeni.editor.providers.DocumentSectionProvider;
import org.bungeni.editor.providers.DocumentSectionTreeModelProvider;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.utils.BungeniBNode;
import org.bungeni.utils.CommonTreeFunctions;
import org.bungeni.utils.MessageBox;

/**
 *
 * @author  Administrator
 */
public class frameBrokenReferences extends javax.swing.JFrame {
    private OOComponentHelper ooDocument;
    private ArrayList<XTextField> orphanedReferences;
    private JFrame parentFrame;
    private boolean launchedState = false;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(frameBrokenReferences.class.getName());

    /** Creates new form frameBrokenReferences */
    public frameBrokenReferences() {
        initComponents();
    }
    
    public frameBrokenReferences(OOComponentHelper ooDoc, JFrame parentFrame, ArrayList<XTextField> brokenReferences){
        setOOComponentHelper(ooDoc);
        setOrphanedReferences(brokenReferences);
        setParentFrame(parentFrame);
        init();
    }
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        taskpaneBrokenReferences = new com.l2fprod.common.swing.JTaskPane();
        taskpaneGrpFindBrokenReferences = new com.l2fprod.common.swing.JTaskPaneGroup();
        panelBrowseBrokenReferences = new javax.swing.JPanel();
        scrollBrowseBrokenReferences = new javax.swing.JScrollPane();
        tblBrowseBrokenReferences = new javax.swing.JTable();
        scrollMessageArea = new javax.swing.JScrollPane();
        txtMessageArea = new javax.swing.JTextArea();
        btnFindBroken = new javax.swing.JButton();
        btnFixBroken = new javax.swing.JButton();
        btnClose1 = new javax.swing.JButton();
        taskpaneGrpFixBrokenReferences = new com.l2fprod.common.swing.JTaskPaneGroup();
        panelFixBrokenReferences = new javax.swing.JPanel();
        scrollFixBrokenReferences = new javax.swing.JScrollPane();
        treeFixBrokenReferences = new javax.swing.JTree();
        btnFixBrokenReferences = new javax.swing.JButton();
        btnCloseFrame = new javax.swing.JButton();
        btnClose2 = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.DO_NOTHING_ON_CLOSE);
        setResizable(false);

        taskpaneGrpFindBrokenReferences.setCollapsable(false);
        taskpaneGrpFindBrokenReferences.setTitle("Find Broken References");
        tblBrowseBrokenReferences.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null}
            },
            new String [] {
                "Title 1", "Title 2", "Title 3", "Title 4"
            }
        ));
        scrollBrowseBrokenReferences.setViewportView(tblBrowseBrokenReferences);

        txtMessageArea.setColumns(20);
        txtMessageArea.setLineWrap(true);
        txtMessageArea.setRows(5);
        scrollMessageArea.setViewportView(txtMessageArea);

        btnFindBroken.setText("Find Broken");
        btnFindBroken.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnFindBrokenActionPerformed(evt);
            }
        });

        btnFixBroken.setText("Fix References");
        btnFixBroken.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnFixBrokenActionPerformed(evt);
            }
        });

        btnClose1.setText("Close");

        org.jdesktop.layout.GroupLayout panelBrowseBrokenReferencesLayout = new org.jdesktop.layout.GroupLayout(panelBrowseBrokenReferences);
        panelBrowseBrokenReferences.setLayout(panelBrowseBrokenReferencesLayout);
        panelBrowseBrokenReferencesLayout.setHorizontalGroup(
            panelBrowseBrokenReferencesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelBrowseBrokenReferencesLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelBrowseBrokenReferencesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(scrollMessageArea, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 407, Short.MAX_VALUE)
                    .add(panelBrowseBrokenReferencesLayout.createSequentialGroup()
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(btnFindBroken, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 138, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(btnFixBroken, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 123, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(btnClose1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 134, Short.MAX_VALUE))
                    .add(scrollBrowseBrokenReferences, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 407, Short.MAX_VALUE))
                .add(15, 15, 15))
        );
        panelBrowseBrokenReferencesLayout.setVerticalGroup(
            panelBrowseBrokenReferencesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelBrowseBrokenReferencesLayout.createSequentialGroup()
                .add(scrollMessageArea, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 64, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(scrollBrowseBrokenReferences, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 112, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(14, 14, 14)
                .add(panelBrowseBrokenReferencesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnFindBroken)
                    .add(btnFixBroken)
                    .add(btnClose1))
                .addContainerGap())
        );
        taskpaneGrpFindBrokenReferences.getContentPane().add(panelBrowseBrokenReferences);

        taskpaneBrokenReferences.add(taskpaneGrpFindBrokenReferences);

        taskpaneGrpFixBrokenReferences.setTitle("Fix Broken References");
        scrollFixBrokenReferences.setViewportView(treeFixBrokenReferences);

        btnFixBrokenReferences.setText("Insert Cross Ref");
        btnFixBrokenReferences.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnFixBrokenReferencesActionPerformed(evt);
            }
        });

        btnCloseFrame.setText("Browse Broken ");
        btnCloseFrame.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnCloseFrameActionPerformed(evt);
            }
        });

        btnClose2.setText("Close");

        org.jdesktop.layout.GroupLayout panelFixBrokenReferencesLayout = new org.jdesktop.layout.GroupLayout(panelFixBrokenReferences);
        panelFixBrokenReferences.setLayout(panelFixBrokenReferencesLayout);
        panelFixBrokenReferencesLayout.setHorizontalGroup(
            panelFixBrokenReferencesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(panelFixBrokenReferencesLayout.createSequentialGroup()
                .addContainerGap()
                .add(panelFixBrokenReferencesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(panelFixBrokenReferencesLayout.createSequentialGroup()
                        .add(btnFixBrokenReferences, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 138, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(btnCloseFrame, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 129, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                        .add(btnClose2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 133, Short.MAX_VALUE))
                    .add(scrollFixBrokenReferences, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 412, Short.MAX_VALUE))
                .addContainerGap())
        );
        panelFixBrokenReferencesLayout.setVerticalGroup(
            panelFixBrokenReferencesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(org.jdesktop.layout.GroupLayout.TRAILING, panelFixBrokenReferencesLayout.createSequentialGroup()
                .addContainerGap()
                .add(scrollFixBrokenReferences, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 161, Short.MAX_VALUE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(panelFixBrokenReferencesLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnFixBrokenReferences)
                    .add(btnClose2)
                    .add(btnCloseFrame))
                .addContainerGap())
        );
        taskpaneGrpFixBrokenReferences.getContentPane().add(panelFixBrokenReferences);

        taskpaneBrokenReferences.add(taskpaneGrpFixBrokenReferences);

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(taskpaneBrokenReferences, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 474, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .add(taskpaneBrokenReferences, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 576, Short.MAX_VALUE)
                .addContainerGap())
        );
        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void btnFindBrokenActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnFindBrokenActionPerformed
// TODO add your handling code here:
            int nSelectedIndex = this.tblBrowseBrokenReferences.getSelectedRow();
            if (nSelectedIndex != -1 ) {
                XTextField field = this.orphanedReferences.get(nSelectedIndex);
                XTextRange theRange = field.getAnchor();
                XTextViewCursor viewCursor = ooDocument.getViewCursor();
                viewCursor.gotoRange(theRange, false);
            } else {
                MessageBox.OK(this, "Please select a reference from the table !");
            }
    }//GEN-LAST:event_btnFindBrokenActionPerformed

    private void btnFixBrokenReferencesActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnFixBrokenReferencesActionPerformed
// TODO add your handling code here:
        applyInsertCrossReference();
    }//GEN-LAST:event_btnFixBrokenReferencesActionPerformed

    private void btnCloseFrameActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnCloseFrameActionPerformed
// TODO add your handling code here:
        this.taskpaneGrpFixBrokenReferences.setExpanded(false);
        this.taskpaneGrpFixBrokenReferences.setVisible(false);
        this.taskpaneGrpFindBrokenReferences.setExpanded(true);
        this.taskpaneGrpFindBrokenReferences.setVisible(true);
        
    }//GEN-LAST:event_btnCloseFrameActionPerformed

    private void btnFixBrokenActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnFixBrokenActionPerformed
// TODO add your handling code here:
        this.taskpaneGrpFindBrokenReferences.setExpanded(false);
        this.taskpaneGrpFindBrokenReferences.setVisible(false);
        this.taskpaneGrpFixBrokenReferences.setExpanded(true);
        this.taskpaneGrpFixBrokenReferences.setVisible(true);
    }//GEN-LAST:event_btnFixBrokenActionPerformed
    
    public void findBrokenFrameSetExpanded (boolean bState) {
        this.taskpaneGrpFindBrokenReferences.setVisible(bState);
        this.taskpaneGrpFindBrokenReferences.setExpanded(bState);
        this.taskpaneGrpFixBrokenReferences.setVisible(!bState);
        this.taskpaneGrpFixBrokenReferences.setExpanded(!bState);
    }
    
    public void fixBrokenFrameSetExpanded (boolean bState) {
           this.taskpaneGrpFixBrokenReferences.setVisible(bState);
           this.taskpaneGrpFixBrokenReferences.setExpanded(bState);
           this.taskpaneGrpFindBrokenReferences.setVisible(!bState);
           this.taskpaneGrpFindBrokenReferences.setExpanded(!bState);
    }
    
    public enum LaunchMode {BrowseBroken, CrossReferences};
   
    /*
    public static frameBrokenReferences Launch(OOComponentHelper ooDoc, JFrame parentFrame, ArrayList<XTextField> brokenReferences){
                frameBrokenReferences f = new frameBrokenReferences( ooDoc,  parentFrame,  brokenReferences);
                f.setAlwaysOnTop(true);
                f.setSize(new Dimension(498, 380));
                f.setVisible(true);
                return f;
    }
      */  
    
    private static final String FRAME_TITLE = "References Manager";
    public static frameBrokenReferences Launch(OOComponentHelper ooDoc, JFrame parentFrame, ArrayList<XTextField> brokenReferences, LaunchMode mode){
                frameBrokenReferences f = new frameBrokenReferences( ooDoc,  parentFrame,  brokenReferences);
                f.setAlwaysOnTop(true);
                f.setTitle(FRAME_TITLE);
                f.setSize(new Dimension(498, 340));
                if (mode == LaunchMode.BrowseBroken) {
                    f.findBrokenFrameSetExpanded(true);    
                } else {
                    f.fixBrokenFrameSetExpanded(true);    
                }
                f.setVisible(true);
                return f;
    }
    
    private void applyInsertCrossReference(){
        TreePath selectedPath = this.treeFixBrokenReferences.getSelectionPath();
        if (selectedPath != null) {
            DefaultMutableTreeNode selectedNode = (DefaultMutableTreeNode) selectedPath.getLastPathComponent();
            numberedHeadingsNode thenode = (numberedHeadingsNode) selectedNode.getUserObject();
            if (!thenode.numberedHeading) {
                //no it is not a numbered heading
                MessageBox.OK(this, "Please select a referenced heading ! (highlighted in green) ");
                return;
            } 
            XTextSection selectedSection = ooDocument.getSection(thenode.sectionName);
            //get the complete reference chain
            ArrayList<String> referenceSourceChain = getReferenceSourceChain(selectedSection);
            insertCrossRef(referenceSourceChain);
            MessageBox.OK(this, "The reference was successfully inserted!");
            
        } else {
            MessageBox.OK(this, "Please select a section in the tree to insert a cross reference to it");
            return;
        }
    }
    
    
    /*
     *
     *The reference chain works like this:
     *Article1
     *  <article 1 numbered heading section>
     *  Clause1
     *      <clause 1 numbered heading section>
     *
     *To get the reference chain for clause 1, we go up 2 levels from clause -> article,
     *and then back down one level to <article 1 numbered section>
     *
     *
     */
    private ArrayList<String> getReferenceSourceChain(XTextSection refSection){
        //refSection has the insertable reference, we go up the chain to insert all parent references
        ArrayList<String> numberReferencesList = new ArrayList<String>(0);
        while (refSection != null ) {
            String refSource = getNumberedReferenceSource(refSection);
            if (refSource != null ) {
                //found a number reference add it to our list
                numberReferencesList.add(refSource);
            }   //go up 2 levles and see if the grand parent is valid and has a numbered child container
            refSection = getParentNumberedSection(refSection);
         }
         return numberReferencesList;
    }
    
    private XTextSection getParentNumberedSection(XTextSection aChild){
            XTextSection aGrandParent = getGrandParentSection(aChild);
            XTextSection aNumberedSection = ooDocument.getChildSectionByType(aGrandParent, "NumberedContainer");
            return aNumberedSection;
    }
    
    private XTextSection getGrandParentSection(XTextSection aSection) {
        XTextSection aParent = aSection.getParentSection();
        if (aParent == null ) return null;
        XTextSection aGrandParent = aParent.getParentSection();
        return aGrandParent;
    }
    
    private String getNumberedReferenceSource(XTextSection refSection) {
        HashMap<String,String> refMeta = ooDocument.getSectionMetadataAttributes(refSection);
        if (refMeta.containsKey("BungeniSectionUUID")) {
            String uuidStr = refMeta.get("BungeniSectionUUID");
            String referenceName = OOoNumberingHelper.HEADING_REF_PREFIX+uuidStr;
            if (ooDocument.getReferenceMarks().hasByName(referenceName)) {
                return referenceName;
            }
        }
        return null;
    }
    
    private final static String REFERENCE_SEPARATOR = " , ";
    private boolean insertCrossRef(ArrayList<String> referenceChain) {
          final int lastIndex = referenceChain.size() - 1;  
          boolean bState = false;
          XTextViewCursor viewCursor = ooDocument.getViewCursor();
          XTextDocument xDoc = ooDocument.getTextDocument();

          try {
              for (int i = lastIndex ; i >= 0 ; i--) {
                  Object oRefField=ooDocument.createInstance("com.sun.star.text.TextField.GetReference");
                  XPropertySet refFieldProps = ooQueryInterface.XPropertySet(oRefField);
                    refFieldProps.setPropertyValue("ReferenceFieldSource", com.sun.star.text.ReferenceFieldSource.REFERENCE_MARK);
                    refFieldProps.setPropertyValue("SourceName", referenceChain.get(i));
                    refFieldProps.setPropertyValue("ReferenceFieldPart", com.sun.star.text.ReferenceFieldPart.TEXT);
                    XTextContent fieldContent = ooQueryInterface.XTextContent(oRefField);  
                    xDoc.getText().insertTextContent(viewCursor, fieldContent, true);
                    if (i > 0 ) { //no comma for 
                        xDoc.getText().insertString(viewCursor, REFERENCE_SEPARATOR, false);
                    }
              }

              XRefreshable xRefresh = ooQueryInterface.XRefreshable(xDoc);
              xRefresh.refresh();
              bState = true;
            } catch (PropertyVetoException ex) {
                log.error("insertCrossRef ("+ex.getClass().getName() +") " + ex.getMessage());
            } catch (WrappedTargetException ex) {
                log.error("insertCrossRef ("+ex.getClass().getName() +") " + ex.getMessage());
            } catch (UnknownPropertyException ex) {
                log.error("insertCrossRef ("+ex.getClass().getName() +") " + ex.getMessage());
            } catch (com.sun.star.lang.IllegalArgumentException ex) {
                log.error("insertCrossRef ("+ex.getClass().getName() +") " + ex.getMessage());
            } finally {
                return bState;
            }
    }
    /*
    private void insertCrossReference(String sourceName){
      int i=0;
    
       try { 
       
         XTextDocument xDoc = ooDocument.getTextDocument();
            
         XTextViewCursor xViewCursor=ooDocument.getViewCursor();
         Object oRefField=ooDocument.createInstance("com.sun.star.text.TextField.GetReference");
         
         XReferenceMarksSupplier xRefSupplier = (XReferenceMarksSupplier) UnoRuntime.queryInterface(
             XReferenceMarksSupplier.class, xDoc);
         
         // Get an XNameAccess which refers to all inserted reference marks
         XNameAccess xMarks = (XNameAccess) UnoRuntime.queryInterface(XNameAccess.class,
             xRefSupplier.getReferenceMarks());
         
        String[] aNames = xMarks.getElementNames();
        XPropertySet oFieldSet = ooQueryInterface.XPropertySet(oRefField);
     
           
            
        
             oFieldSet.setPropertyValue("ReferenceFieldSource",com.sun.star.text.ReferenceFieldSource.REFERENCE_MARK); 
            
         oFieldSet.setPropertyValue("SourceName", sourceName);
             oFieldSet.setPropertyValue("ReferenceFieldPart",com.sun.star.text.ReferenceFieldPart.TEXT);


             XTextContent xRefContent = (XTextContent) UnoRuntime.queryInterface(
                     XTextContent.class, oFieldSet);
             
              xDoc.getText().insertTextContent(xViewCursor , xRefContent, true);
               xDoc.getText().insertString(xViewCursor , " , ", false);
            
            
              XRefreshable xRefresh = (XRefreshable) UnoRuntime.queryInterface(
                 XRefreshable.class, xDoc);
            xRefresh.refresh();   
            
         
          
        
          } catch (UnknownPropertyException ex) {
                ex.printStackTrace();
            } catch (WrappedTargetException ex) {
                ex.printStackTrace();
            } catch (PropertyVetoException ex) {
                ex.printStackTrace();
            } catch (com.sun.star.lang.IllegalArgumentException ex) {
                ex.printStackTrace();
            } 
         
        
   
    }*/
    
    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                frameBrokenReferences f = new frameBrokenReferences();
                f.setSize(new Dimension(498, 380));
                f.setVisible(true);
            }
        });
    }

    public void setOOComponentHelper(OOComponentHelper ooDoc) {
        this.ooDocument = ooDoc;
    }

    public void setOrphanedReferences(ArrayList<XTextField> brokenReferences) {
        this.orphanedReferences = brokenReferences;
    }

    public void setParentFrame(JFrame parentFrame) {
        this.parentFrame = parentFrame;
    }

    public boolean getLaunchedState(){
        return launchedState;
    }
    
    private String m_selectedReference = "";
    private void init() {
        initComponents();
        launchedState = true;
        this.txtMessageArea.setText("Broken references are listed below, double clicking on a reference will take you " +
                "to the point in the the document where the broken reference appears, Use the 'fix reference' option to repair the reference ");
        BrokenReferencesTableModel model = new BrokenReferencesTableModel(this.ooDocument, this.orphanedReferences);
        this.tblBrowseBrokenReferences.setModel(model);
        this.tblBrowseBrokenReferences.setRowSelectionAllowed(true);
        this.tblBrowseBrokenReferences.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        this.tblBrowseBrokenReferences.getSelectionModel().addListSelectionListener(new ListSelectionListener(){
            public void valueChanged(ListSelectionEvent e) {
                        if (e.getValueIsAdjusting()) {      
                                return;
                        }
                        m_selectedReference = (String) tblBrowseBrokenReferences.getValueAt(tblBrowseBrokenReferences.getSelectedRow(), 0);
            }
            
        });

        
        
        
        
        DefaultTreeModel treeFixBrokenModel = new DefaultTreeModel(buildTreeModel());
        this.treeFixBrokenReferences.setModel(treeFixBrokenModel);
        DefaultTreeCellRenderer renderTree = new DefaultTreeCellRenderer();
        this.treeFixBrokenReferences.setCellRenderer(
                                         new treeBrokenReferencesCellRenderer(
                                            renderTree.getOpenIcon(), 
                                            renderTree.getClosedIcon(),
                                            renderTree.getLeafIcon()));
        CommonTreeFunctions.expandAll(treeFixBrokenReferences);
        
        this.btnClose1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e) {
              shutdownFrame();
            }
            
        });
        this.btnClose2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e) {
               shutdownFrame();
            }
            
        });
    }
    
    class treeBrokenReferencesCellRenderer extends JLabel implements TreeCellRenderer {
        Icon openIcon,  closedIcon, leafIcon;
        Color thisBackGround = Color.WHITE;
        Color numberedBackGround = Color.GREEN;
        Color thisforeGround = Color.BLACK;
        Border selectionBorder = BorderFactory.createLineBorder(Color.MAGENTA, 2);
        treeBrokenReferencesCellRenderer(Icon openIcon, Icon closedIcon, Icon leafIcon){
            this.openIcon = openIcon;
            this.closedIcon = closedIcon;
            this.leafIcon = leafIcon;
           // this.setForeground(thisforeGround);
        }
        
        public Component getTreeCellRendererComponent(JTree tree, Object value, boolean selected, boolean expanded, boolean leaf, int row, boolean hasFocus) {
                if (selected) {
                   setOpaque(true);
                } else {
                   setOpaque(false); 
                }

            if (value instanceof DefaultMutableTreeNode) {
                DefaultMutableTreeNode node  = (DefaultMutableTreeNode)value;
                numberedHeadingsNode numberedNode = (numberedHeadingsNode)node.getUserObject();
                if (numberedNode.numberedHeading) {
                    setForeground(new java.awt.Color(0xFF, 0xCC,0xFF));
                } else {
                    setForeground(new java.awt.Color(0x00, 0x00,0x00));
                }
                if (expanded) {
                    setIcon(openIcon);
                } else if (leaf) {
                    setIcon(leafIcon);
                } else {
                    setIcon(closedIcon);
                }
            }

            setText(value.toString());
            return this;
        }
        
    }
    
    /*
     *
     *DefaultMutableTreeNode member that hides node name, and shows content for numbered headings
     *
     */
    class numberedHeadingsNode {
            public String nodeName;
            public String sectionName;
            public boolean numberedHeading = false;
            numberedHeadingsNode (OOComponentHelper ooDoc, BungeniBNode aNode) {
                XTextSection aSection = ooDoc.getSection(aNode.getName());
                this.sectionName = aNode.getName();
                HashMap<String,String> sectionMeta  = ooDoc.getSectionMetadataAttributes(aSection);
                if (sectionMeta.containsKey("BungeniSectionType")){
                    String sectionType = sectionMeta.get("BungeniSectionType");
                    if (sectionType.equals("NumberedContainer")) {
                        numberedHeading = true;
                        nodeName = aSection.getAnchor().getString();
                    } else {
                        nodeName = aNode.getName();
                    }
                } else {
                  nodeName = aNode.getName();  
                }
            }
            public String toString(){
                return nodeName;
            }
    }

    private DefaultMutableTreeNode buildTreeModel(){
       BungeniBNode bRootNode =  DocumentSectionProvider.getTreeRoot();
       numberedHeadingsNode brf = new numberedHeadingsNode (ooDocument, bRootNode);
       DefaultMutableTreeNode aNode = new DefaultMutableTreeNode(brf); 
       recurseTreeNodes (aNode, bRootNode);
       return aNode;
    }
    
        
    private void recurseTreeNodes(DefaultMutableTreeNode theNode, BungeniBNode theBNode) {
       // BungeniBNode theBNode = (BungeniBNode) theNode.getUserObject();
        if (theBNode.hasChildren()) {
            TreeMap<Integer, BungeniBNode> children = theBNode.getChildrenByOrder();
            Iterator<Integer> childIterator = children.keySet().iterator();
            while (childIterator.hasNext()) {
                Integer nodeKey = childIterator.next();
                BungeniBNode newBNode = children.get(nodeKey);
                numberedHeadingsNode brf = new numberedHeadingsNode(ooDocument, newBNode);
                DefaultMutableTreeNode dmtChildNode = new DefaultMutableTreeNode(brf);
                recurseTreeNodes(dmtChildNode, newBNode);
                theNode.add(dmtChildNode );
            }
        }
    }
    
    private void shutdownFrame() {
        launchedState = false;
        dispose();
    }
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnClose1;
    private javax.swing.JButton btnClose2;
    private javax.swing.JButton btnCloseFrame;
    private javax.swing.JButton btnFindBroken;
    private javax.swing.JButton btnFixBroken;
    private javax.swing.JButton btnFixBrokenReferences;
    private javax.swing.JPanel panelBrowseBrokenReferences;
    private javax.swing.JPanel panelFixBrokenReferences;
    private javax.swing.JScrollPane scrollBrowseBrokenReferences;
    private javax.swing.JScrollPane scrollFixBrokenReferences;
    private javax.swing.JScrollPane scrollMessageArea;
    private com.l2fprod.common.swing.JTaskPane taskpaneBrokenReferences;
    private com.l2fprod.common.swing.JTaskPaneGroup taskpaneGrpFindBrokenReferences;
    private com.l2fprod.common.swing.JTaskPaneGroup taskpaneGrpFixBrokenReferences;
    private javax.swing.JTable tblBrowseBrokenReferences;
    private javax.swing.JTree treeFixBrokenReferences;
    private javax.swing.JTextArea txtMessageArea;
    // End of variables declaration//GEN-END:variables
    
    
    class BrokenReferencesTableModel extends AbstractTableModel {
        private String[] column_names = {"Source", "Current Text" };
        private OOComponentHelper ooDocument;
        private ArrayList<XTextField> orphanedReferences = new ArrayList<XTextField>();
        
        BrokenReferencesTableModel(OOComponentHelper ooDoc, ArrayList<XTextField> orphaned){
            this.ooDocument=ooDoc;
            this.orphanedReferences = orphaned;
        }

        public int getRowCount() {
            return orphanedReferences.size();
        }

        public int getColumnCount() {
            return this.column_names.length;
        }

         public String getColumnName(int column) {
                return this.column_names[column];
         }
         
         public Class getColumnClass(int col) { 
                return String.class;
         }
         
         private String getPropertyOfField (XTextField aField, String propName) {
             String propValue = "";
            try {
                propValue = AnyConverter.toString(this.ooDocument.getObjectPropertySet(aField).getPropertyValue(propName));
            } catch (UnknownPropertyException ex) {
                    log.error("exception: " + ex.getClass().getName() + " : " + ex.getMessage());
            } catch (WrappedTargetException ex) {
                    log.error("exception: " + ex.getClass().getName() + " : " + ex.getMessage());
            } catch (com.sun.star.lang.IllegalArgumentException ex) {
                    log.error("exception: " + ex.getClass().getName() + " : " + ex.getMessage());
            } finally {
             return propValue;
            }
         }
        public Object getValueAt(int rowIndex, int columnIndex) {
            XTextField mField = this.orphanedReferences.get(rowIndex);
            switch (columnIndex) {
                case 0:
                    return mField.getPresentation(true);
                    
                case 1:
                   
                    return mField.getPresentation(false);

                default:
                    return new String("unknown column");
            }
        }
        
    }
}
