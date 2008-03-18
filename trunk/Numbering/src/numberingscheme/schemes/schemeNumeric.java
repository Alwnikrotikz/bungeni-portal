/*
 * newNumbersToAlphabet.java
 *
 * Created on March 18, 2008, 12:52 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package numberingscheme.schemes;

import java.util.ArrayList;
import java.util.Iterator;
import numberingscheme.impl.BaseNumberingScheme;
import numberingscheme.impl.IGeneralNumberingScheme;

/**
 *
 * @author Administrator
 */
public class schemeNumeric extends BaseNumberingScheme implements IGeneralNumberingScheme {
    
    /** Creates a new instance of newNumbersToAlphabet */
    public schemeNumeric(){
        super();
      }
    
    public schemeNumeric(long s, long e) {
        super(s, e);
    }

    public void generateSequence() {
        //seed base sequence first
        super.generateSequence();
        //now generate the class sequence
        Iterator<Long> baseIterator = baseSequence.iterator();
        while (baseIterator.hasNext()) {
            Long baseNumber = baseIterator.next();
            generatedSequence.add(baseNumber.toString());
        }
    }
   
    
    public static void main(String[] args) {
        schemeNumeric numObj = new schemeNumeric((long)12, (long) 33);
        numObj.generateSequence();
        ArrayList<String> seq = numObj.getGeneratedSequence();
        Iterator<String> iter = seq.iterator();
        while (iter.hasNext()) {
            String elem = iter.next();
            System.out.println(elem);
        }
            
    }

}
