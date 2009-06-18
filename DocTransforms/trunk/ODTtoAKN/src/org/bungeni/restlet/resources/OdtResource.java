package org.bungeni.restlet.resources;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.HashMap;

import org.bungeni.plugins.translator.OdtTranslate;
import org.bungeni.restlet.server.TransformerServer;
import org.restlet.Context;
import org.restlet.data.Form;
import org.restlet.data.MediaType;
import org.restlet.data.Request;
import org.restlet.data.Response;
import org.restlet.resource.FileRepresentation;
import org.restlet.resource.Representation;
import org.restlet.resource.Variant;

/**
 *Accepts ODT submissions - processes the ODT file and returns a response
 * @author Ashok Hariharan
 */
public class OdtResource  extends org.restlet.resource.Resource  {

    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(OdtResource.class.getName());

    /**
     * Add return Application xml as a variant
     * @param context
     * @param request
     * @param response
     */
    public OdtResource(Context context, Request request,
			Response response) {
		super(context, request, response);
        getVariants().add(new Variant(MediaType.APPLICATION_XML));
        
	}

    /**
     * Allow post for this resource
     * @return
     */
	@Override
	public boolean allowPost() {
		return true;
	}
	
	private String getOdtFolderPath(){
		
		String folderPath = TransformerServer.getTempFileFolder() + File.separator + "odt";
	     File fFolder = new File(folderPath);
	     if (!fFolder.exists()) fFolder.mkdirs();
        
	     return folderPath;
        
	}
	
	private String getXmlFolderPath() {
		String folderPath = TransformerServer.getTempFileFolder() + File.separator + "xml";
	    File fFolder = new File(folderPath);
	    if (!fFolder.exists()) fFolder.mkdirs();
	    return folderPath;
	}
	
	private String getOutputXmlFile(String fileName){
	     int nIndex = fileName.indexOf(".");
         String xmlFile = fileName.substring(0, nIndex) + ".xml";
         String outputFile = getXmlFolderPath() + File.separator + xmlFile;
         return outputFile;
	}
	
	/**
	 * Accept the posted odt file
	 * @param fileName
	 * @param entity
	 */
	private String recieveOdtFile(String fileName, Representation entity) {
		FileOutputStream odtFile = null;
		
		String folderPath = getOdtFolderPath();
		
		File file = new File(folderPath + File.separator + fileName);
         try {
             //overwrite the existing file
        	 odtFile = new FileOutputStream(file, false);
			entity.write(odtFile);
		} catch (FileNotFoundException e) {
			log.error("recieveOdtFile:" , e);
		} catch (IOException e) {
			log.error("recieveOdtFile:" , e);
		} finally {
			return file.getPath();
		}
 	}

	/**
	 * Recieve an ODT file to transform
	 * -- transform the ODT to xml
	 * -- return the result xml back in an Xml envelop
	 * 
	 */
	@Override
	public void acceptRepresentation(Representation entity) {
		log.debug("acceptRepresentation :  media type = " + entity.getMediaType());
            try {
                //get the submission headers, for the name of the input file
                Form requestHeaders = (Form) getRequest().getAttributes().get("org.restlet.http.headers");
                log.debug("output form headers = " + requestHeaders);
                String fileName = requestHeaders.getFirstValue("X-Odt-File");
                //write the file to a folder path on the server
                final String odfFile = recieveOdtFile(fileName, entity);
                //get the path and name of the output xml file
                final String outputXmlFile = getOutputXmlFile(fileName);
                //Now start the transform
                OdtTranslate transInstance = OdtTranslate.getInstance();
                HashMap paramMap = new HashMap(){{
                	put("OdfFileURL", odfFile);
                    put("OutputFilePath",outputXmlFile);
                }};
                transInstance.updateParams(paramMap);
                //TODO call the transform here
                System.out.println("trans map = " + transInstance.getParams());
                transInstance.exec();
                //transform end
                //for now return a dummy response
               File outputXml = new File (outputXmlFile);
               Representation returnResponse = new FileRepresentation(outputXml,
            		   MediaType.APPLICATION_XML, 0);
               getResponse().setEntity(returnResponse);

            } catch (Exception e) {
                log.error("acceptRepresentation : ", e);
                
            } finally {
             
            }
    }
}
