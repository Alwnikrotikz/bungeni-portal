"""
$Id: $
"""
from zope import interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema import vocabulary
from zope.security.proxy import removeSecurityProxy

from ore.alchemist.vocabulary import DatabaseSource, ObjectSource, Session
from sqlalchemy.orm import mapper, relation, column_property
from sqlalchemy.sql import text

import sqlalchemy as rdb
import schema, domain
import pdb



#ModelTypeSource = ObjectSource( model.DataModelType, 'short_name', 'id')
#SecurityLevelSource = DatabaseSource( model.SecurityLevel, 'short_name', 'id' )

#Constituency = ObjectSource( )
ParliamentMembers = ObjectSource( domain.ParliamentMember, 'name', 'member_id' )
PoliticalParties  = ObjectSource( domain.PoliticalParty, 'full_name', "id")
ParliamentSessions = ObjectSource( domain.ParliamentSession, 'short_name', 'session_id')
QuestionType = vocabulary.SimpleVocabulary.fromItems( [("(O)rdinary", "O"), ("(P)rivate Notice", "P")] )
Constituencies = ObjectSource( domain.Constituency, 'name', 'constituency_id')
Parliaments = ObjectSource( domain.Parliament, 'identifier', 'parliament_id')


SittingTypes = DatabaseSource( domain.SittingType, 'sitting_type', 'sitting_type_id' )   

class mps_sitting( object ):
    """ returns the mps for a sitting """
    
_mp_sitting = rdb.join(schema.sittings, schema.parliament_sessions,
                        schema.sittings.c.session_id == schema.parliament_sessions.c.session_id).join(
                            schema.user_group_memberships,
                            schema.parliament_sessions.c.parliament_id == schema.user_group_memberships.c.group_id).join(
                                schema.users,
                                schema.user_group_memberships.c.user_id == schema.users.c.user_id)
                                                                
mapper( mps_sitting, _mp_sitting,
          properties={
           'fullname' : column_property(
                             (schema.users.c.first_name + u" " + 
                             schema.users.c.middle_name + u" " + 
                             schema.users.c.last_name).label('fullname')
                                           )
                    },)
 



class SQLQuerySource ( object ):
    """ call with a SQL Statement and the rows which make up the vocabulary
    """
    
    def __init__( self, sql_statement, token_field, value_field, title_field=None ):
        self.sql_statement = sql_statement
        self.token_field = token_field
        self.value_field = value_field
        self.title_field = title_field
        
    def constructQuery( self, context ):
        session = Session()        
        query = session.query( text(self.sql_statement) )
        return query
        
    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()
        
        terms = []
        title_field = self.title_field or self.token_field
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, self.value_field), 
                    token = getattr( ob, self.token_field),
                    title = getattr( ob, title_field) ,
                    ))
                    
        return vocabulary.SimpleVocabulary( terms )


                      
        
        
        
