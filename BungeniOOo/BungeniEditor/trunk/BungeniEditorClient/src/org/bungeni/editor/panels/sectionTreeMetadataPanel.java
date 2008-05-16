/*
 * documentMetadataPanel.java
 *
 * Created on May 15, 2008, 11:47 AM
 */

package org.bungeni.editor.panels;

import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertySet;
import com.sun.star.container.NoSuchElementException;
import com.sun.star.container.XNamed;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.text.XTextSection;
import java.awt.Color;
import java.awt.Component;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.Enumeration;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTree;
import javax.swing.Timer;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeCellRenderer;
import javax.swing.tree.TreePath;
import org.bungeni.editor.BungeniEditorProperties;
import org.bungeni.editor.BungeniEditorPropertiesHelper;
import org.bungeni.editor.dialogs.metadatapanel.SectionMetadataLoad;
import org.bungeni.editor.dialogs.treetable.DocMetadataTreeTableModel;
import org.bungeni.editor.dialogs.treetable.sectionHive;
import org.bungeni.editor.metadata.DocumentMetadataTableModel;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.utils.CommonTreeFunctions;
import org.jdesktop.swingx.JXTreeTable;

/**
 *
 * @author  Administrator
 */
public class sectionTreeMetadataPanel extends javax.swing.JPanel {
    private OOComponentHelper ooDocument;
    private JFrame parentFrame;
    private DefaultMutableTreeNode sectionRootNode = null;
    private boolean emptyRootNode= false;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(sectionTreeMetadataPanel.class.getName());
    private static final String ROOT_SECTION = BungeniEditorPropertiesHelper.getDocumentRoot();

    private Timer sectionMetadataRefreshTimer;
    /** Creates new form documentMetadataPanel */
    public sectionTreeMetadataPanel() {
        initComponents();
    }
    
   public sectionTreeMetadataPanel(OOComponentHelper ooDocument, JFrame parentFrame){
         this.parentFrame=parentFrame;
         this.ooDocument=ooDocument;
         init();
     }
    
    private void init() {
        initComponents();
        initTableDocumentMetadata();    
        initTimer();
    }
    
    private void initTableDocumentMetadata() {
         initSectionsArray();   
         this.treeSectionTreeMetadata.setModel(new DefaultTreeModel(sectionRootNode));
         this.treeSectionTreeMetadata.addMouseListener(new treeDocStructureTreeMouseListener());
         updateTableMetadataModel(ROOT_SECTION);
         //-tree-deprecated--CommonTreeFunctions.expandAll(treeSectionStructure, true);
         CommonTreeFunctions.expandAll(treeSectionTreeMetadata);
    }
    
      private void initSectionsArray() {
        final OOComponentHelper ooDoc;
        synchronized(ooDocument) {
            ooDoc  = ooDocument;
        }
        try {
            if (!ooDoc.isXComponentValid()) return;
            if (!ooDoc.getTextSections().hasByName(ROOT_SECTION)) {
                log.debug("no root section found");
                return;
            }
            Object rootSection = ooDoc.getTextSections().getByName(ROOT_SECTION);
            XTextSection theSection = ooQueryInterface.XTextSection(rootSection);
            if (theSection.getChildSections().length == 0) {
                //root is empty and has no children. 
                //set empty status 
                this.emptyRootNode = true;
            }
            sectionRootNode = new DefaultMutableTreeNode(new String(ROOT_SECTION));
            recurseSections (theSection, sectionRootNode);
        } catch (NoSuchElementException ex) {
            log.error("recurseSections :" + ex.getMessage());
        } catch (WrappedTargetException ex) {
            log.error("recurseSections :" + ex.getMessage());
        }
    }
    
    
    private void recurseSections (XTextSection theSection, DefaultMutableTreeNode node ) {
        //recurse children
        XTextSection[] sections = theSection.getChildSections();
        if (sections != null ) {
            if (sections.length > 0 ) {
                //start from last index and go to first
                for (int nSection = sections.length - 1 ; nSection >=0 ; nSection--) {
                    log.debug ("section name = "+sections[nSection] );
                    //get the name for the section and add it to the root node.
                    XPropertySet childSet = ooQueryInterface.XPropertySet(sections[nSection]);
                    XNamed xNamedSection = ooQueryInterface.XNamed(sections[nSection]);
                    String childSectionName = xNamedSection.getName();
                    DefaultMutableTreeNode newNode = new DefaultMutableTreeNode(childSectionName);
                    node.add(newNode);
                    recurseSections (sections[nSection], newNode);
                }
            } else 
                return;
        } else 
            return;

    }
    
    private synchronized void initTimer(){
          sectionMetadataRefreshTimer= new Timer(4000, new ActionListener() {
              public void actionPerformed(ActionEvent e) {
                //refreshSectionMetadataTreeTable();
                  refreshTree();
              }
           });
           sectionMetadataRefreshTimer.start();
    }

   private void refreshTree(){
       TreePath[] selections = this.treeSectionTreeMetadata.getSelectionPaths();
       Enumeration expandedNodes = this.treeSectionTreeMetadata.getExpandedDescendants(new TreePath(this.treeSectionTreeMetadata.getModel().getRoot()));
       refreshTreeModel();
       if (expandedNodes != null  ) {
           log.debug("refreshTree: expandedNodes was NOT null");
           while (expandedNodes.hasMoreElements()) {
               this.treeSectionTreeMetadata.expandPath((TreePath)expandedNodes.nextElement());
           }
       } else
           log.debug("refreshTree: expandedNodes was null");
       if (selections != null)  {
             this.treeSectionTreeMetadata.setSelectionPaths(selections);
            log.debug("refreshTree: selections was NOT null");
       }  else
            log.debug("refreshTree: selections was null");
         CommonTreeFunctions.expandAll(treeSectionTreeMetadata);    
   }

   private void refreshTreeModel(){
         initSectionsArray();   
         ((DefaultTreeModel)this.treeSectionTreeMetadata.getModel()).setRoot(sectionRootNode);
         this.treeSectionTreeMetadata.setModel(this.treeSectionTreeMetadata.getModel());
         //this.treeSectionTreeMetadata.setModel(new DefaultTreeModel(sectionRootNode));
   }

   public void updateTableMetadataModel(String sectionName){
          SectionMetadataLoad sectionMetadataTableModel = new SectionMetadataLoad(ooDocument,sectionName);
          this.tblSectionViewMetadata.setModel(sectionMetadataTableModel);
          this.tblSectionViewMetadata.setFont(new Font("Tahoma", Font.PLAIN, 11));   
   }
   
   private String m_selectedSection = "";
   
  class treeDocStructureTreeMouseListener implements MouseListener {
       treeDocStructureTreeMouseListener() {
        }
        
        public void mouseClicked(MouseEvent e) {
        }     
        
         public void mousePressed(MouseEvent evt) {
              int selRow = treeSectionTreeMetadata.getRowForLocation(evt.getX(), evt.getY());
                    TreePath selPath = treeSectionTreeMetadata.getPathForLocation(evt.getX(), evt.getY());
                     if (selRow != -1 ) {
                             DefaultMutableTreeNode node = (DefaultMutableTreeNode) selPath.getLastPathComponent();
                             String m_selectedSection = (String)node.getUserObject();
                             updateTableMetadataModel(m_selectedSection);
                          return;
                     }
        }
        public void mouseReleased(MouseEvent e) {
        }

        public void mouseEntered(MouseEvent e) {
        }

        public void mouseExited(MouseEvent e) {
        }
  }    
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        lblSectionMetadata = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        treeSectionTreeMetadata = new javax.swing.JTree();
        jScrollPane2 = new javax.swing.JScrollPane();
        tblSectionViewMetadata = new javax.swing.JTable();
        lblSectionTreeMetadataView = new javax.swing.JLabel();

        getAccessibleContext().setAccessibleDescription("Section Metadata");
        lblSectionMetadata.setText("Section Metadata");

        jScrollPane1.setViewportView(treeSectionTreeMetadata);

        tblSectionViewMetadata.setModel(new javax.swing.table.DefaultTableModel(
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
        jScrollPane2.setViewportView(tblSectionViewMetadata);

        lblSectionTreeMetadataView.setText("Click on a section to view its Metadata");

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(lblSectionTreeMetadataView)
                    .add(lblSectionMetadata, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 196, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(jScrollPane1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 213, Short.MAX_VALUE)
                    .add(jScrollPane2, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 213, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .add(lblSectionTreeMetadataView)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jScrollPane1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 134, Short.MAX_VALUE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblSectionMetadata)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jScrollPane2, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 117, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents
    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JLabel lblSectionMetadata;
    private javax.swing.JLabel lblSectionTreeMetadataView;
    private javax.swing.JTable tblSectionViewMetadata;
    private javax.swing.JTree treeSectionTreeMetadata;
    // End of variables declaration//GEN-END:variables
    
}
