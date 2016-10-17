from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName


def runProfile(portal, profileName):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profileName)


def install(portal):
    """Run the GS profile to install this package"""
    out = StringIO()
    runProfile(portal, 'profile-sixfeetup.customfolderalert:default')
    print >> out, "Installed sixfeetup.customfolderalert"
    return out.getvalue()


def uninstall(portal, reinstall=False):
    """Run the GS profile to install this package"""
    out = StringIO()
    if not reinstall:
        runProfile(portal, 'profile-sixfeetup.customfolderalert:uninstall')
        print >> out, "Uninstalled sixfeetup.customfolderalert"
    return out.getvalue()

