
from zope.viewlet.interfaces import IViewletManager

from ploned.ui.interfaces import IPlonedSkin

class IBungeniSkin( IPlonedSkin ):
    """ skin for bungeni """
    
class IWorkflowViewletManager( IViewletManager ):
    """
    Viewlet manager to display worflow history
    """
class IVersionViewletManager( IViewletManager ):
    """
    Viewletmanager to display the versions
    """

# class IParliamentMemberTaskMenu( interface.Interface ):
#     """ viewlet manager for member of parliament """
# 
# class IMinisterMemberTaskMenu( interface.Interface ):
#     """ viewlet manager for ministry """
