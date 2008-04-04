/*
 * schemeAlphabetical.java
 *
 * Created on March 18, 2008, 12:52 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package numberingscheme.schemes;

import java.util.ArrayList;
import java.util.Iterator;
import net.sf.saxon.number.Numberer;
import numberingscheme.impl.BaseNumberingScheme;
import numberingscheme.impl.GeneralNumberer;
import numberingscheme.impl.IGeneralNumberingScheme;

/**
 *
 * @author Administrator
 */
public class schemeAlphabetical extends BaseNumberingScheme implements IGeneralNumberingScheme {
   
    
    class NumToAlpha extends GeneralNumberer {
        public String toAlpha(long number){
            return toAlphaSequence(number, "ABCDEFGHIJKLMOPQRSTUVWXYZ" );
        }
    } ;
    
    NumToAlpha numberer ;
    
    /** Creates a new instance of newNumbersToAlphabet */
    /**default constructor required**/
    public schemeAlphabetical(){
        super();
        numberer = new NumToAlpha();
    }
    /**parametered constructor**/
    public schemeAlphabetical(long s, long e) {
        super(s, e);
        numberer = new NumToAlpha();
    }


    public void generateSequence() {
        //seed base sequence first
        super.generateSequence();
        Iterator<Long> baseIterator = baseSequence.iterator();
        while (baseIterator.hasNext()) {
            Long baseNumber = baseIterator.next();
            addNumberToSequence(numberer.toAlpha(baseNumber));
        }
    }
   

    
    public static void main(String[] args) {
        schemeAlphabetical numObj = new schemeAlphabetical((long)12, (long) 33);
        numObj.setParentPrefix("1.1");
        numObj.generateSequence();
        ArrayList<String> seq = numObj.getGeneratedSequence();
        Iterator<String> iter = seq.iterator();
        while (iter.hasNext()) {
            String elem = iter.next();
            System.out.println(elem);
        }
            
    }
}
