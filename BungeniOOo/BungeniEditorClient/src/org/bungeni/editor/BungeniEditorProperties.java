/*
 * BungeniEditorProperties.java
 *
 * Created on August 24, 2007, 6:44 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor;

import java.util.HashMap;
import java.util.Vector;
import org.apache.log4j.Logger;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.db.QueryResults;
import org.bungeni.db.SettingsQueryFactory;

/**
 *
 * @author Administrator
 */
public class BungeniEditorProperties {
    private static HashMap<String,String> propertiesMap = new HashMap();
    private static org.apache.log4j.Logger log = Logger.getLogger(BungeniEditorProperties.class.getName());
    
    /** Creates a new instance of BungeniEditorProperties */
    public BungeniEditorProperties() {
    }

    private static int PROPERTY_NAME_COLUMN=0;
    private static int PROPERTY_VALUE_COLUMN=1;
    public static String getEditorProperty(String propertyName) {
        String propertyValue = "";
        if (propertiesMap.containsKey(propertyName) ) {
           log.debug("getEditorProperty : property found in map");
           return (String) propertiesMap.get(propertyName);
        } else {
            log.debug("getEditorProperty: property not cached, querying");
        }
        
        String settingsInstance = DefaultInstanceFactory.DEFAULT_INSTANCE();
        BungeniClientDB db = new BungeniClientDB(settingsInstance, "");
        db.Connect();
        HashMap resultsMap = db.Query(SettingsQueryFactory.Q_FETCH_EDITOR_PROPERTY(propertyName));
        db.EndConnect();
        QueryResults results = new QueryResults(resultsMap);
        if (results.hasResults() ) {
           Vector<Vector> resultRows  = new Vector<Vector>();
           resultRows = results.theResults();
           //it should always return a single row.... 
           //so we process the first row and brea
           Vector<java.lang.String> tableRow = new Vector<java.lang.String>();
  
               for (int i = 0 ; i < resultRows.size(); i++ ) {
                   //get the results row by row into a string vector
                   tableRow = resultRows.elementAt(i);
                   break;
               }
           if (tableRow.size() > 0) {
            propertyValue = tableRow.elementAt(PROPERTY_VALUE_COLUMN);    
            propertiesMap.put(propertyName, propertyValue);
        
           }
        } 
         return propertyValue;
    }
    
}
