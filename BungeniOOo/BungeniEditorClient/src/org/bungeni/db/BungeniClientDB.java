/*
 * BungeniClientDB.java
 *
 * Created on August 17, 2007, 12:47 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.db;
import java.sql.*;
import java.util.Vector;
import org.apache.log4j.Logger;
/**
 * Database connector class fro settings database
 * @author Administrator
 */
public class BungeniClientDB {
    
    private static org.apache.log4j.Logger log = Logger.getLogger(BungeniClientDB.class.getName());
  
    private static String DRIVER = "org.h2.Driver";
    private static String JDBC_PREFIX = "jdbc:h2:";
    private static String DEFAULT_DB = "settings.db";
    private static String USER_NAME = "sa";
    private static String PASS_WORD = "";
    
    private String current_database;
    private String path_to_database;
    private Connection db_connection;
    private String connection_string;
    
    /**
     * Creates a new instance of BungeniClientDB
     * @param pathToDb 
     * @param dbName 
     */
    public BungeniClientDB(String pathToDb, String dbName) {
        if (dbName.equals(""))
            current_database = DEFAULT_DB;
        else
            current_database = dbName;
        path_to_database = pathToDb;
        connection_string = JDBC_PREFIX + path_to_database + current_database;
        System.out.println("connection string = "+ connection_string);
    }
    
    public boolean Connect() {
      boolean bState = true;
      try {
             Class.forName(DRIVER);
             db_connection = DriverManager.getConnection(connection_string, USER_NAME, PASS_WORD); 
        } catch (SQLException ex) {
            log.debug("Connect:"+ ex.getMessage());
            bState = false;
        }  catch (ClassNotFoundException ex) {
            log.debug("Connect:"+ ex.getMessage());
            bState = false;
        }  finally {
            return bState;
        }
    }
    /*
    public void Query (String expression) {
       try {
        Statement st;
        ResultSet rs;
    
        st = db_connection.createStatement();         
               
        // statement objects can be reused with
        // repeated calls to execute but we
        // choose to make a new one each time
        rs = st.executeQuery(expression);    // run the query
        ResultSetMetaData meta   = rs.getMetaData();
        int               colmax = meta.getColumnCount();
        int               i;
        Object            o = null;

        // the result set is a cursor into the data.  You can only
        // point to one row at a time
        // assume we are pointing to BEFORE the first row
        // rs.next() points to next row and returns true
        // or false if there is no next row, which breaks the loop
        for (; rs.next(); ) {
            for (i = 0; i < colmax; ++i) {
                o = rs.getObject(i + 1);    // Is SQL the first column is indexed

                // with 1 not 0
                System.out.print(o.toString() + " ");
            }
        }
            System.out.println(" ");
            st.close();
          } catch (SQLException ex) {
            System.out.println("Query : "+ ex.getMessage());
        }    
    }
    */
     
    public synchronized Vector<Vector> Query(String expression) {
            Statement st = null;
            ResultSet rs = null;
            Vector<Vector> results = new Vector<Vector>();
        
            try {

                st = db_connection.createStatement();         // statement objects can be reused with
                // repeated calls to execute but we
                // choose to make a new one each time
                rs = st.executeQuery(expression);    // run the query

                //process result set metadata
                ResultSetMetaData meta   = rs.getMetaData();
                int               colmax = meta.getColumnCount();
                int               i;
                Object            o = null;
                Vector<String> columnsMeta = new Vector<String>();
                for (int iMeta = 0; iMeta < colmax; ++iMeta) {
                    //System.out.println("column no."+(iMeta+1)+" = "+meta.getColumnName(iMeta+1));
                    columnsMeta.addElement( meta.getColumnName(iMeta+1));
                 }
                results.addElement(columnsMeta);
                
                for (   ;rs.next() ; ) {
                    Vector<String> resultsRow = new Vector<String>();
                    for (i = 0; i < colmax; ++i) {
                        o = rs.getObject(i + 1);    // Is SQL the first column is indexed
                                                    // with 1 not 0
                        resultsRow.addElement(o.toString());
                        //System.out.print(o.toString() + " | ");
                    }    
                    //System.out.println(" ");
                    results.addElement(resultsRow);
                }
                log.debug ("Query Results = "+ results.size());
                st.close();    // NOTE!! if you close a statement the associated ResultSet is

        } catch (SQLException ex) {
            System.out.println("query:"+ ex.getLocalizedMessage());
        } finally {
            return results;
        }   
    }
 
          
       
    public void EndConnect() {
        Statement st;
        try {
              st = db_connection.createStatement();
              st.execute("SHUTDOWN");
              st.close();
           } catch (SQLException ex) {
            log.debug("EndConnect:"+ ex.getMessage());
        }
    }
    
   
}
