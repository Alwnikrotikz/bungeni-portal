/*
 * DocumentSectionTreeModelProvider.java
 *
 * Created on May 18, 2008, 1:39 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.providers;

import java.util.Iterator;
import java.util.TreeMap;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import org.bungeni.utils.BungeniBNode;

/**
 *
 * @author Administrator
 */
public class DocumentSectionTreeModelProvider {
    
    /** Creates a new instance of DocumentSectionTreeModelProvider */
    public static DocumentSectionAdapterDefaultTreeModel theSectionTreeModel = null;
    
    /**
     * Returns a static instance of the section TreeModel
     */
    public static DocumentSectionAdapterDefaultTreeModel create_static(){
        if (theSectionTreeModel == null ) {
            BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
            DefaultMutableTreeNode dmtRootNode = provideRootNode(bRootNode);
            theSectionTreeModel = new DocumentSectionAdapterDefaultTreeModel(dmtRootNode);
            DocumentSectionProvider.subscribeModel(theSectionTreeModel);
            }
        return theSectionTreeModel;    
    }
    
    /**
     * returns a non-static instance of the section TreeModel which is updated directly by the documentsectionProvider
     */
    public static DocumentSectionAdapterDefaultTreeModel create(){
        BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
        DefaultMutableTreeNode dmtRootNode = provideRootNode(bRootNode);
        DocumentSectionAdapterDefaultTreeModel model = new DocumentSectionAdapterDefaultTreeModel(dmtRootNode);
        DocumentSectionProvider.subscribeModel(model);
        return model;
    }
    
    /**
     * creates a non-static section tree model which is not updated by the documentsectionprovider
     */
    public static DocumentSectionAdapterDefaultTreeModel create_without_subscription(){
        BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
        DefaultMutableTreeNode dmtRootNode = provideRootNode(bRootNode);
        DocumentSectionAdapterDefaultTreeModel model = new DocumentSectionAdapterDefaultTreeModel(dmtRootNode);
        //DocumentSectionProvider.subscribeModel(model);
        return model;
    }
    
    public static DocumentSectionAdapterDefaultTreeModel create_non_refreshing_treemodel(){
        BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
        DefaultMutableTreeNode dmtRootNode = provideRootNode(bRootNode);
        DocumentSectionAdapterDefaultTreeModel model = new DocumentSectionAdapterDefaultTreeModel(dmtRootNode, false);
        //DocumentSectionProvider.subscribeModel(model);
        return model;
    }
    
    /**
     * generates a newrootnode for the section model
     */
    public static DefaultMutableTreeNode newRootNode(){
        BungeniBNode bRootNode = DocumentSectionProvider.getTreeRoot();
        return provideRootNode(bRootNode);
    }
    
    private static DefaultMutableTreeNode provideRootNode(BungeniBNode rootNode) {
        //walk nodes and build tree
        DefaultMutableTreeNode theRootNode = new DefaultMutableTreeNode(rootNode);
        recurseNodes(theRootNode);
        return theRootNode;
    }
    
    private static void recurseNodes(DefaultMutableTreeNode theNode) {
        BungeniBNode theBNode = (BungeniBNode) theNode.getUserObject();
        if (theBNode.hasChildren()) {
            TreeMap<Integer, BungeniBNode> children = theBNode.getChildrenByOrder();
            Iterator<Integer> childIterator = children.keySet().iterator();
            while (childIterator.hasNext()) {
                Integer nodeKey = childIterator.next();
                DefaultMutableTreeNode dmtChildNode = new DefaultMutableTreeNode( children.get(nodeKey));
                recurseNodes(dmtChildNode);
                theNode.add(dmtChildNode );
            }
        }
    }
}
