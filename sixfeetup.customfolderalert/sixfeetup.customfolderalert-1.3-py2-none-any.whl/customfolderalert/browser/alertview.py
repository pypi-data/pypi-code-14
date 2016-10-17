import os
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.memoize.view import memoize_contextless


class AlertView(BrowserView):
    """View class for alerts methods"""

    def is_alert_disabled(self):
        """Is the custom folder alert disabled?"""
        truisms = ['yes', 'y', 'true', 'on']
        disabled = os.environ.get("DISABLE_CUSTOMFOLDER_ALERT", None)
        return disabled is not None and disabled.lower() in truisms

    @memoize_contextless
    def check_for_evil(self):
        """Check to see if any non filesystem directories have
        any items.
        """
        items_found = 0
        skins_tool = getToolByName(self.context, 'portal_skins')
        # TODO: Verify that this works even when using something
        #       like themetweaker.themeswitcher
        default_skin = skins_tool.getDefaultSkin()
        skin_path = skins_tool.getSkinPath(default_skin).split(',')
        # loop through all the skins dirs
        for path in skin_path:
            folder = skins_tool.get(path, None)
            if folder is None:
                continue
            # only return true if it's not a fs dir and has something in it
            zope_folder = folder.meta_type != 'Filesystem Directory View'
            folder_contents = folder.objectIds()
            if zope_folder and folder_contents:
                items_found += len(folder_contents)
        return items_found
