"""
$Id: $
"""

from ore.alchemist.vocabulary import DatabaseSource, ObjectSource
from bungeni import core
 
#ModelTypeSource = ObjectSource( model.DataModelType, 'short_name', 'id')
#SecurityLevelSource = DatabaseSource( model.SecurityLevel, 'short_name', 'id' )

ParliamentMembers = ObjectSource( core.ParliamentMember, 'name', 'id' )
PoliticalParties  = ObjectSource( core.PoliticalParty, 'full_name', "id")


                             
                      
        
        
        
