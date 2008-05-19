/*
 * documentMetadataPanel.java
 *
 * Created on May 15, 2008, 11:47 AM
 */

package org.bungeni.editor.panels;


import com.sun.star.text.XTextDocument;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.ArrayList;
import java.util.GregorianCalendar;

import java.util.Vector;
import javax.swing.DefaultComboBoxModel;

import javax.swing.DefaultListModel;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JTree;
import javax.swing.ListModel;
import javax.swing.Timer;
import org.bungeni.editor.dialogs.editorTabbedPanel;


import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.ooo.ooDocNoteStructure;
import org.bungeni.ooo.ooDocNotes;
import org.bungeni.ooo.ooQueryInterface;
import org.bungeni.utils.TextSizeFilter;

/**
 *
 * @author  Ashok Hariharan
 */
public class documentNotesPanel extends javax.swing.JPanel implements ITabbedPanel {
    private OOComponentHelper ooDocument;
    private JFrame parentFrame;
    private editorTabbedPanel parentPanel;
    private Timer tList;

    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(documentNotesPanel.class.getName());
    //document notes
    private ooDocNotes m_ooNotes;

   
    /** Creates new form documentMetadataPanel */
    public documentNotesPanel() {
        initComponents();
    }
    
   public documentNotesPanel(OOComponentHelper ooDocument, JFrame parentFrame, JPanel parentPanel){
         this.parentFrame=parentFrame;
         this.parentPanel = (editorTabbedPanel) parentPanel;
         this.ooDocument=ooDocument;
         init();
     }
    
    private void init() {
        initComponents();
       cboListDocuments.addActionListener(new cboListDocumentsActionListener());
       initListDocuments();
       initNotesPanel();
       initTimer();
    }
    
    private void initListDocuments(){
        log.debug("initListDocuments: init");
        String[] listDocuments = parentPanel.getCurrentlyOpenDocuments().keySet().toArray(new String[parentPanel.getCurrentlyOpenDocuments().keySet().size()]);
        cboListDocuments.setModel(new DefaultComboBoxModel(listDocuments));
    }
    
    private void updateListDocuments(){
       /* String strTitle = ooDocument.getFrameTitle(ooDocument.getTextDocument());
        cboListDocuments.setSelectedItem(strTitle);*/
       
          String[] listDocuments = parentPanel.getCurrentlyOpenDocuments().keySet().toArray(new String[parentPanel.getCurrentlyOpenDocuments().keySet().size()]);
          String selectedItem = (String)cboListDocuments.getSelectedItem();
          
          parentPanel.setProgrammaticRefreshOfDocumentListFlag(true);
          cboListDocuments.setModel(new DefaultComboBoxModel(listDocuments));
          
          if (!parentPanel.getCurrentlyOpenDocuments().containsKey(selectedItem))
               cboListDocuments.setSelectedIndex(0);
           else
               cboListDocuments.setSelectedItem(selectedItem);
          parentPanel.setProgrammaticRefreshOfDocumentListFlag(false);
    }
       
    private void initTimer(){
        tList = new Timer(5000, new ActionListener(){
            public void actionPerformed(ActionEvent e) {
                updateListDocuments();
            }
        }   
        );
    }
    private void initNotesPanel() {
        try {
        //restrict editor note text field
        javax.swing.text.Document txtEditorNoteDoc = txtEditorNote.getDocument();
        if (txtEditorNoteDoc instanceof javax.swing.text.AbstractDocument) {
            javax.swing.text.AbstractDocument doc = (javax.swing.text.AbstractDocument)txtEditorNoteDoc;
            doc.setDocumentFilter(new TextSizeFilter(100));
        } else {
            log.debug("initNotesPanel: not an AbstratDocument instance");
        }
        //populate editor notes list
        initEditorNotesList();
        
        } catch (Exception ex) {
            log.error("exception initNotesPanel:"+ ex.getMessage());
            ex.printStackTrace();
        }
    }
    
    private void initEditorNotesList() {
        try {
        m_ooNotes = new ooDocNotes (ooDocument);
        Vector<ooDocNoteStructure> allNotes = new Vector<ooDocNoteStructure>();
        log.debug("after initializing ooDocNotes");
        allNotes = m_ooNotes.readNotes();
        DefaultListModel notesList = new DefaultListModel();
        log.debug("getting default listmodel");
   
        if (allNotes != null) {
            log.debug("allNotes is not null = "+ allNotes.size());
            for (int i=0; i < allNotes.size(); i++ ) {
                ooDocNoteStructure docNote = null;
                docNote = allNotes.elementAt(i);
                notesList.addElement(docNote);
                log.debug("docNote no."+ i + " , value = "+ docNote.getNoteDate());
            }
        } 
        listboxEditorNotes.setModel(notesList);
        log.debug("initEditorNotesList: size = "+ listboxEditorNotes.getModel().getSize());
        listboxEditorNotes.ensureIndexIsVisible(listboxEditorNotes.getModel().getSize());
        listboxEditorNotes.setSelectedIndex(listboxEditorNotes.getModel().getSize());
        } catch (Exception e) {
            log.error("initEditorNotesList: exception : " + e.getMessage());
        }
        
    }
    
    
    /**
 * This action listener updates document handles when switching between documents
 * The listnere does not switch the handle by itself, merely raises an event in the parent
 * panel which switches the openoffice context and switches the other panesl
 * @author  Administrator
 */
    class cboListDocumentsActionListener implements ActionListener {
        Object oldItem;
        public void actionPerformed(ActionEvent e) {
            JComboBox cb = (JComboBox) e.getSource();
            Object newItem = cb.getSelectedItem();
            boolean same = newItem.equals(oldItem);
            oldItem = newItem;
            if ("comboBoxChanged".equals(e.getActionCommand())) {
                parentPanel.updateMain((String)newItem, same);
                /*
                if (same) {
                    if (self().program_refresh_documents == true)
                        return;
                    else
                        //check and see if the doctype property exists before you bring the window front
                     //  if(ooDocument.propertyExists("doctype")){
                            bringEditorWindowToFront();
                      // }
                        
                    //return;
                } else {
                    String key = (String)newItem;
                    componentHandleContainer xComp = editorMap.get(key);
                    if (xComp == null ) {
                        log.debug("XComponent is invalid");
                    }
                   // ooDocument.detachListener();
                    setOODocumentObject(new OOComponentHelper(xComp.getComponent(), ComponentContext));
                 
                    initFields();
                    //initializeValues();
                   
                    // removed call to collapsiblepane function
                    //retrieve the list of dynamic panels from the the dynamicPanelMap and update their component handles
                    //updateCollapsiblePanels();
                    updateFloatingPanels();
                    initNotesPanel();
                    initBodyMetadataPanel();
                    initDialogListeners();
                    //check and see if the doctype property exists before you refresh the metadata table
                    ///if(!ooDocument.propertyExists("doctype")){
                    ///   JOptionPane.showMessageDialog(null,"This is not a bungeni document.","Document Type Error",JOptionPane.ERROR_MESSAGE);
                    ///   
                    ///} 
                    refreshTableDocMetadataModel();
                    
                                                               
                    if (self().program_refresh_documents == false)
                        bringEditorWindowToFront();
                    
                   
                 
                       
                } */
            }
            
        }
        
    }
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        lblEditorNotes = new javax.swing.JLabel();
        txtEditorNote = new javax.swing.JTextArea();
        btnNewEditorNote = new javax.swing.JButton();
        btnSaveEditorNote = new javax.swing.JButton();
        jLabel4 = new javax.swing.JLabel();
        listboxEditorNotes = new javax.swing.JList();
        cboListDocuments = new javax.swing.JComboBox();
        lblOpenDocuments = new javax.swing.JLabel();

        getAccessibleContext().setAccessibleDescription("Document Notes");
        lblEditorNotes.setText("Editor Note");

        txtEditorNote.setColumns(20);
        txtEditorNote.setEditable(false);
        txtEditorNote.setFont(new java.awt.Font("Tahoma", 0, 11));
        txtEditorNote.setLineWrap(true);
        txtEditorNote.setRows(5);
        txtEditorNote.setToolTipText("Type in your editor notes here.");

        btnNewEditorNote.setText("New Note");
        btnNewEditorNote.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnNewEditorNoteActionPerformed(evt);
            }
        });

        btnSaveEditorNote.setText("Save Note");
        btnSaveEditorNote.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnSaveEditorNoteActionPerformed(evt);
            }
        });

        jLabel4.setText("Archived Notes");

        listboxEditorNotes.setModel(new javax.swing.AbstractListModel() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        listboxEditorNotes.addListSelectionListener(new javax.swing.event.ListSelectionListener() {
            public void valueChanged(javax.swing.event.ListSelectionEvent evt) {
                listboxEditorNotesValueChanged(evt);
            }
        });

        lblOpenDocuments.setText("Open Documents");

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, listboxEditorNotes, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 213, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, layout.createSequentialGroup()
                        .add(btnNewEditorNote)
                        .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 47, Short.MAX_VALUE)
                        .add(btnSaveEditorNote))
                    .add(org.jdesktop.layout.GroupLayout.LEADING, txtEditorNote, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 213, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, lblEditorNotes, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 163, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, cboListDocuments, 0, 213, Short.MAX_VALUE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, lblOpenDocuments, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 206, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                    .add(org.jdesktop.layout.GroupLayout.LEADING, jLabel4, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 201, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .add(lblOpenDocuments, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 14, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(cboListDocuments, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(lblEditorNotes)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(txtEditorNote, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 90, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                    .add(btnNewEditorNote)
                    .add(btnSaveEditorNote))
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(jLabel4)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(listboxEditorNotes, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 86, Short.MAX_VALUE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void listboxEditorNotesValueChanged(javax.swing.event.ListSelectionEvent evt) {//GEN-FIRST:event_listboxEditorNotesValueChanged
// TODO add your handling code here:
        JList listbox = (JList)evt.getSource();
        ListModel model = listbox.getModel();
        int index = listbox.getMaxSelectionIndex();
        if (index != -1 ) {
            ooDocNoteStructure ooNote = (ooDocNoteStructure) model.getElementAt(index);
            String noteText = ooNote.getNoteText();
            txtEditorNote.setText(noteText);
        }
    }//GEN-LAST:event_listboxEditorNotesValueChanged

    private void btnSaveEditorNoteActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnSaveEditorNoteActionPerformed
// TODO add your handling code here:
        Date current = new Date();
        GregorianCalendar calendar = new GregorianCalendar();
        calendar.setTime(current);
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String strNoteDate = formatter.format(current);
        String strAuthor= "Ashok";
        String strEditorNote = txtEditorNote.getText();
        log.debug("actionPerformed:saveEditorNote");
        ooDocNoteStructure ooNote = new ooDocNoteStructure(strNoteDate, strAuthor, strEditorNote);
        m_ooNotes.addNote(ooNote);
        initEditorNotesList();
        txtEditorNote.setEditable(false);
    }//GEN-LAST:event_btnSaveEditorNoteActionPerformed

    private void btnNewEditorNoteActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnNewEditorNoteActionPerformed
// TODO add your handling code here:
        txtEditorNote.setText("");
        txtEditorNote.setEditable(true);
    }//GEN-LAST:event_btnNewEditorNoteActionPerformed

    /**
     * Required functions for ITabbedPanel interface
     **/
    public void setOOComponentHandle(OOComponentHelper ooComponent) {
        this.ooDocument = ooComponent;
        this.initEditorNotesList();
    }

    public Component getObjectHandle() {
        return this;
    }

    public void setParentHandles(JFrame c, JPanel containerPanel) {
        this.parentFrame = c;
        this.parentPanel = (editorTabbedPanel) containerPanel;
    }

    public JFrame getParentWindowHandle() {
        return this.parentFrame;
    }

    public JPanel getParentPanelHandle() {
        return this.parentPanel;
    }
    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnNewEditorNote;
    private javax.swing.JButton btnSaveEditorNote;
    private javax.swing.JComboBox cboListDocuments;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel lblEditorNotes;
    private javax.swing.JLabel lblOpenDocuments;
    private javax.swing.JList listboxEditorNotes;
    private javax.swing.JTextArea txtEditorNote;
    // End of variables declaration//GEN-END:variables
    
}
