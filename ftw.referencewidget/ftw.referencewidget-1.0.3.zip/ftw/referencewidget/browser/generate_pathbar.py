from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five import BrowserView
import json


class GeneratePathbar(BrowserView):

    def __call__(self):
        widget = self.context
        mtool = getToolByName(widget.context, 'portal_membership')

        originpoint = self.request.get('origin', None)
        if not originpoint:
            originpoint = widget.get_start_path()

        if isinstance(originpoint, unicode):
            originpoint = originpoint.encode('utf-8')

        obj = widget.context.unrestrictedTraverse(originpoint)
        results = []

        while True:
            clickable = mtool.checkPermission('View', obj)
            results.insert(0, {'title': obj.Title(),
                               'path': '/'.join(obj.getPhysicalPath()),
                               'clickable': bool(clickable)})
            if IPloneSiteRoot.providedBy(obj):
                break
            else:
                obj = aq_parent(obj)
        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(results)
