import zope.securitypolicy.interfaces
from bungeni.core.workflows import utils
from bungeni.core.workflows import dbutils
from bungeni.models.utils import get_principal_id

class conditions:
    @staticmethod
    def is_scheduled(info, context):
        return dbutils.isItemScheduled(context.bill_id)

class actions:
    @staticmethod
    def create(info, context):
        utils.setBillSubmissionDate( info, context )
        utils.setParliamentId(info, context)
        user_id = get_principal_id()
        if not user_id:
            user_id ='-'
        zope.securitypolicy.interfaces.IPrincipalRoleMap(context
                        ).assignRoleToPrincipal(u'bungeni.Owner', user_id)
        utils.setParliamentId(info, context)
        owner_id = utils.getOwnerId(context)
        if owner_id and (owner_id != user_id):
            zope.securitypolicy.interfaces.IPrincipalRoleMap( context 
                ).assignRoleToPrincipal( u'bungeni.Owner', owner_id)

    @staticmethod
    def submit(info, context):
        utils.setBillPublicationDate( info, context )
        utils.setSubmissionDate(info, context)


    @staticmethod
    def withdraw(info, context):
        pass

    @staticmethod
    def schedule_first(info, context):
        pass

    @staticmethod
    def postpone_first(info, context):
        pass


    @staticmethod
    def schedule_second(info, context):
        utils.createVersion(info, context)



