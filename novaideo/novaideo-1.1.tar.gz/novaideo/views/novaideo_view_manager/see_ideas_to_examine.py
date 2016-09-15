# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeIdeasToExamine)
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES, merge_with_filter_view, find_entities)


CONTENTS_MESSAGES = {
    '0': _(u"""No idea found"""),
    '1': _(u"""One idea found"""),
    '*': _(u"""${nember} ideas found""")
    }


def sort_ideas(ideas):
    ordered_ideas = [(idea,
                          (len(idea.tokens_support) - \
                           len(idea.tokens_opposition))) \
                         for idea in ideas]
    groups = {}
    for idea in ordered_ideas:
        if groups.get(idea[1], None):
            groups[idea[1]].append(idea)
        else:
            groups[idea[1]] = [idea]

    for group_key in list(groups.keys()):
        sub_ideas = list(groups[group_key])
        groups[group_key] = sorted(sub_ideas,
                    key=lambda idea: len(idea[0].tokens_support),
                    reverse=True)
    groups = sorted(groups.items(), key=lambda value: value[0], reverse=True)
    return [idea[0] for sublist in groups
            for idea in sublist[1]]


@view_config(
    name='seeideastoexamine',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeIdeasToExamineView(BasicView):
    title = _('Ideas to examine')
    name = 'seeideastoexamine'
    behaviors = [SeeIdeasToExamine]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seeideastoexamine'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def _add_filter(self, user):
        def source(**args):
            filters = [
                {'metadata_filter': {
                    'negation': True,
                    'states': ['examined']
                }},
                {'metadata_filter': {
                    'content_types': ['idea'],
                    'states': ['published']
                }}
            ]
            objects = find_entities(
                user=user, include_site=True, filters=filters, **args)
            return objects

        url = self.request.resource_url(self.context, '@@novaideoapi')
        return get_filter(
            self,
            url=url,
            source=source,
            select=[('metadata_filter', ['keywords']),
                    'contribution_filter', ('temporal_filter', ['negation', 'created_date']),
                    'text_filter', 'other_filter'])

    def update(self):
        self.execute(None)
        user = get_current()
        filter_form, filter_data = self._add_filter(user)
        filters = [
            {'metadata_filter': {
                'negation': True,
                'states': ['examined']
            }},
            {'metadata_filter': {
                'content_types': ['idea'],
                'states': ['published']
            }}
        ]
        args = {}
        args = merge_with_filter_view(self, args)
        args['request'] = self.request
        objects = find_entities(user=user,
                                filters=filters,
                                **args)
        if 'idea' in self.request.content_to_support:
            objects = sort_ideas(objects)

        url = self.request.resource_url(self.context, 'seeideastoexamine')
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_contents"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})
        filter_data['filter_message'] = self.title
        filter_body = self.filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
        if filter_form:
            result = merge_dicts(
                {'css_links': filter_form['css_links'],
                'js_links': filter_form['js_links']
                }, result)

        values = {'bodies': result_body,
                  'batch': batch,
                  'filter_body': filter_body}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeIdeasToExamine: SeeIdeasToExamineView})


FILTER_SOURCES.update(
    {SeeIdeasToExamineView.name: SeeIdeasToExamineView})
