package org.un.bungeni.translators.odttoakn.steps;

/**
 * This is the map step object
 * A map step object is an object used to store each element of the mapping files
 */
public class MapStep implements MapStepInterface
{
	//the id of the step 
	private Integer stepId;
	
	//the type attribute of the step
	private String stepType;
	
	//the name attribute of the step
	private String stepName;
	
	//the bungeniSectionType attribute of the step 
	private String stepBungeniSectionType;
	
	//the result attribute of the step 
	private String stepResult;
	
	//the string that contains all the operation to be done on the attributes of the element regarding this step 
	private String stepAttributes;
	
	
	/**
	 * Create a new step setting its type, name, bungeniSectionType and result to the given values
	 * @param aStepType the type attribute of the step 
	 * @param aStepName the name attribute of the step
	 * @param aStepBungeniSectionType the bungeniSectionType attribute of the step 
	 * @param aStepResult the result attribute of the step 
	 * @param anAttributesList the string that contains all the operation to be done on the attributes of a particular element
	 */
	public MapStep(Integer aStepId, String aStepType, String aStepName, String aStepBungeniSectionType, String aStepResult, String anAttributesList)
	{
		//set the id attribute of the step
		this.stepId = aStepId;
		
		//set the type attribute of the step 
		this.stepType = aStepType;
		
		//set the name attribute of the step
		this.stepName = aStepName;
		
		//set the bungeniSectionType attribute of the step
		this.stepBungeniSectionType = aStepBungeniSectionType;
		
		//set the result attribute of the step 
		this.stepResult = aStepResult;
		
		//set the attributes list of this map step 
		this.stepAttributes = anAttributesList;
	}
	
	/**
	 * This method is used to get the id attribute of a map Step
	 * @return the id attribute of a map Step
	 */
	public Integer getId()
	{
		//copy the value of the type attribute and return it
		Integer aId = this.stepId;
		return aId;
	}
	/**
	 * This method is used to get the type attribute of a map Step
	 * @return the type attribute of a map Step
	 */
	public String getType()
	{
		//copy the value of the type attribute and return it
		String aType = this.stepType;
		return aType;
	}
	/**
	 * This method is used to get the name attribute of a map Step
	 * @return the name attribute of a map Step
	 */
	public String getName()
	{
		//copy the value of the name attribute and return it
		String aName = this.stepName;
		return aName;
	}
	/**
	 * This method is used to get the bungeniSectionType attribute of a map Step
	 * @return the bungeniSectionType attribute of a map Step
	 */
	public String getBungeniSectionType()
	{
		//copy the value of the bungeniSectionType attribute and return it
		String aBungeniSectionType = this.stepBungeniSectionType;
		return aBungeniSectionType;
	}
	/**
	 * This method is used to get the result attribute of a map Step
	 * @return the result attribute of a map Step
	 */
	public String getResult()
	{
		//copy the value of the result attribute and return it
		String aResult = this.stepResult;
		return aResult;
	}
	
	/**
	 * This method is used to get the  attribute operations  of a map Step
	 * @return the result attribute of a map Step
	 */
	public String getAttributes()
	{
		//copy the value of the result attribute and return it
		String aStepAttributes = this.stepAttributes;
		return aStepAttributes;
	}

	/**
	 * Set the id attribute of a step to the given type. 
	 * @param aStepId the new id of the step 
	 */
	public void setId(Integer aStepId)
	{
		//write the type of the step 
		this.stepId = aStepId;
	}
	/**
	 * Set the type attribute of a step to the given type. 
	 * @param aStepType the new type of the step 
	 */
	public void setType(String aStepType)
	{
		//write the type of the step 
		this.stepType = aStepType;
	}
	/**
	 * Set the name attribute of a step to the given name. 
	 * @param aStepType the new name of the step 
	 */
	public void setName(String aStepName)
	{
		//write the name of the step 
		this.stepName = aStepName;
	}
	/**
	 * Set the bungeniSectionTypeAttribute of the step to the given bungeniSectionType
	 * @param aStepBungeniSectionType the new bungeniSectionType of the step 
	 */
	public void setBungeniSectionType(String aStepBungeniSectionType)
	{
		//write the bungeniSectionType of the step 
		this.stepBungeniSectionType = aStepBungeniSectionType;
	}
	/**
	 * Set the result of the step to the given result
	 * @param aStepResult the new result of the step 
	 */
	public void setResult(String aStepResult)
	{
		//write the result of the step
		this.stepResult = aStepResult;
	}
	
	/**
	 * Set the operation that will be done on the attributes
	 * @param aStepAttributes the string that contains all the operation to be done on the attributes of a particular element 
	 */
	public void setAttributes(String aStepAttributes)
	{
		//write the attributes of the step
		this.stepAttributes = aStepAttributes;
	}
}
