from ftw.referencewidget.browser.utils import extend_with_batching
from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.browser.utils import get_traversal_types
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import json


class SearchView(BrowserView):

    def __call__(self):
        search_term = self.request.get('term')
        if not search_term:
            return json.dumps([])

        if not search_term.endswith("*"):
            search_term += "*"
        search_types = get_selectable_types(self.context)

        query = {'portal_type': search_types, 'Title': search_term}
        catalog = getToolByName(self.context.context, 'portal_catalog')
        results = catalog(query)
        results, batch_html = extend_with_batching(self.context, results)
        json_prep = {'batching': batch_html, 'items': []}

        traversel_type = get_traversal_types(self.context)

        for item in results:
            contenttype = 'contenttype-' \
                + item.portal_type.replace('.', '-').lower()

            traversable = item.is_folderish and  \
                (item.portal_type in traversel_type)

            label = '{0} ({1})'.format(item.Title, item.getPath())
            json_prep['items'].append({'title': label,
                                       'path': item.getPath(),
                                       'selectable': True,
                                       'content-type': contenttype,
                                       'traversable': traversable
                                       })

        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(json_prep)
