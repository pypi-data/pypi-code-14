from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class IndexDashboard(Dashboard):
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.ModelList(
            _('Content'),
            column=1,
            collapsible=False,
            models=(
                'cms.content.models.Article',
                'cms.content.models.Category'
            )
        ))
        self.children.append(modules.ModelList(
            _('Pages'),
            column=1,
            collapsible=False,
            models=(
                'cms.pages.models.Page',
            )
        ))
        self.children.append(modules.ModelList(
            _('Modules'),
            column=1,
            collapsible=False,
            models=(
                'cms.nav.models.NavModule',
                'cms.content.models.ContentModule',
                'cms.content.models.ArticlesModule'
            )
        ))
        self.children.append(modules.ModelList(
            _('Emails'),
            column=1,
            collapsible=False,
            models=(
                'cms.emails.models.Message',
            )
        ))
        self.children.append(modules.ModelList(
            _('Settings'),
            column=1,
            collapsible=False,
            models=(
                'cms.settings.models.Settings',
            )
        ))
        self.children.append(modules.ModelList(
            _('Users'),
            column=1,
            collapsible=False,
            models=(
                'django.contrib.auth.models.User',
                'cms.accounts.models.Account',
                'django.contrib.auth.models.Group'
            )
        ))
        self.children.append(modules.LinkList(
            _('Files'),
            column=2,
            collapsible=False,
            children=[
                {
                    'title': _('Manage files'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False
                }
            ]
        ))
