package org.un.bungeni.translators.odttoakn.configurations;

import java.util.HashMap;

import org.un.bungeni.translators.odttoakn.steps.Step;

/**
 * This is the interface for the configuration reader. A configuration reader has a singleton
 * pattern and is used to read a specific configuration 
 */
public interface ConfigurationReaderInterface 
{
	/**
	 * Get the step of the configuration with the given name
	 * @param aName the name of the step that you want to retreive
	 * @return a Step with the given name
	 */
	public Step getStepByName(String aName);

	/**
	 * Get the step of the configuration with the given href
	 * @param aURI the href of the step that you want to retreive
	 * @return a Step with the given href
	 */
	public Step getStepByHref(String aURI);

	/**
	 * Get the step of the configuration with the given position
	 * @param aPosition the position of the step that you want to retreive
	 * @return a Step with the given position
	 */
	public Step getStepByPosition(Integer aPosition);
	
	/**
	 * Used to get an HashMao containing all the Steps of the configuration with their position 
	 * as key 
	 * @return the HashMap containing all the Steps of the configuration
	 */
	public HashMap<Integer,Step> getSteps();

}
