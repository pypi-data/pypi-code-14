# -*- coding: utf-8 -*-

from . import logger
from Products.CMFCore.interfaces import IPropertiesTool
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from paste.auth import auth_tkt
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.portlets.portlets import base
from rer.al.mcorevideoportlet import al_mcorevideoportletMessageFactory as _
from rer.al.mcorevideoportlet.config import DEFAULT_TIMEOUT
from zope import schema
from zope.site.hooks import getSite
from zope.component._api import getUtility
from zope.formlib import form
from zope.interface import implements, Interface
import base64
import cjson
import urllib2
import urlparse


class IMediacoreVideoPortlet(Interface):

    """
    Marker interface for Mediacore video portlet
    with field definition
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    video_url = schema.TextLine(
        title=_(u"Video url"),
        description=_(u"The video url"),
        required=True)

    video_security = schema.Bool(
        title=_(u"Video with security"),
        description=_(
            u"Tick this box if you want to render a video with security check"),
        required=True,
        default=False)

    text = schema.Text(
        title=_(u"Text"),
        description=_(u"The text to render"),
        required=False)

    video_width = schema.Int(
        title=_(u"Video width"),
        description=_(u"The video width"),
        required=True,
        default=200,)

    video_height = schema.Int(
        title=_(u"Video height"),
        description=_(u"The video height"),
        required=True,
        default=152,)


class Assignment(base.Assignment):
    implements(IMediacoreVideoPortlet)

    header = ''
    video_url = ''
    text = ''
    video_security = False
    video_height = 0
    video_width = 0
    portlet_id = ''

    def __init__(self, header='', video_url='', text='', video_security=False,
                 video_height=0, video_width=0):
        new_portlet_id = getSite().generateUniqueId('MediacoreVideoPortlet')
        self.header = header
        self.video_url = video_url
        self.text = text
        self.video_security = video_security
        self.video_height = video_height
        self.video_width = video_width
        self.portlet_id = new_portlet_id.replace('-', '').replace('.', '')

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
           "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):

    """Portlet renderer.
       This is registered in configure.zcml. The referenced page template is
       rendered, and the implicit variable 'view' will refer to an instance
       of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('video_portlet.pt')

    def get_portlet_id(self):
        """
        get the portlet id to identify correctly all the video in the page
        """
        return self.data.portlet_id

    def get_variables(self):
        """
        get the variables that allow to configure the video
        """
        meta = self.get_media_metadata()
        if meta:
            meta['portlet_id'] = self.get_portlet_id()
            meta['width'] = self.data.video_width or '200'
            meta['height'] = self.data.video_height or '200'
            VARIABLES = """
            var %(portlet_id)s_jw_file = '%(file_remoteurl)s';
            var %(portlet_id)s_jw_image = '%(image_url)s';
            var %(portlet_id)s_jw_h = '%(height)spx';
            var %(portlet_id)s_jw_w = '%(width)spx';
            """
            return VARIABLES % meta

    def getVideoLink(self, video_remoteurl, file_id, SECRET):
        """
        calculate the video link basing on SECRET
        """
        if SECRET:
            ticket = auth_tkt.AuthTicket(SECRET,
                                         userid='anonymous',
                                         ip='0.0.0.0',
                                         tokens=[str(file_id), ],
                                         user_data='',
                                         secure=False)
            return "%s?token=%s:%s" % (video_remoteurl, file_id,
                                       base64.urlsafe_b64encode(ticket.cookie_value()))
        else:
            return "%s" % (video_remoteurl)

    def get_media_metadata(self):
        """
        get the media metadata from remote
        """
        pprop = getUtility(IPropertiesTool)
        mediacore_prop = getattr(pprop, 'mediacore_properties', None)
        SERVE_VIDEO = (
            mediacore_prop
            and mediacore_prop.base_uri
            or '/file_url/media_unique_id?slug=%s'
        )
        if self.data.video_security:
            SECRET = mediacore_prop and mediacore_prop.secret or ''
        else:
            SECRET = ''
        remoteurl = self.data.video_url
        url = list(urlparse.urlparse(remoteurl)[:2])
        url.extend(4 * ['', ])
        url = urlparse.urlunparse(url)
        media_slug = remoteurl.split('/')[-1]
        try:
            data = urllib2.urlopen(url + SERVE_VIDEO % media_slug,
                                   timeout=DEFAULT_TIMEOUT).read()
        except:
            logger.exception('Error getting data')
            data = None
        if data:
            data = cjson.decode(data)
            video_remoteurl = '%s/files/%s' % (url, data['unique_id'])
            data['file_remoteurl'] = self.getVideoLink(video_remoteurl,
                                                       data['file_id'],
                                                       SECRET)
            return data

    def get_player_setup(self):
        return """
            if (typeof %(portlet_id)s_jw_file === 'undefined') {
                jq('div p#%(portlet_id)s_jw_message').text('Impossibile caricare il video');
            }
            else {
                jwplayer("%(portlet_id)s_jw_container").setup({
                    flashplayer: "++resource++collective.rtvideo.mediacore.jwplayer/player.swf",
                    height: %(portlet_id)s_jw_h,
                    width: %(portlet_id)s_jw_w,
                    provider: 'http',
                    controlbar: 'bottom',
                    file: %(portlet_id)s_jw_file,
                    image: %(portlet_id)s_jw_image,
                });
            }
        """ % {'portlet_id': self.get_portlet_id()}

    def get_player_navigation(self):
        return """
            <li class='jwplayerplay' style="display:inline">
                <a href="#" onclick="jwplayer('%(portlet_id)s_jw_container').play();return false;">Play</a>
            </li>
            <li class='jwplayerpausa' style="display:inline">
                <a href="#" onclick="jwplayer('%(portlet_id)s_jw_container').pause();return false;">Pausa</a>
            </li>
            <li class='jwplayerstop' style="display:inline">
                <a href="#" onclick="jwplayer('%(portlet_id)s_jw_container').stop();return false;">Stop</a>
            </li>
            <li class='jwplayeraudio' style="display:inline">
                <a href="#" onclick="jwplayer('%(portlet_id)s_jw_container').setMute();return false;">Audio</a>
            </li>
        """ % {'portlet_id': self.get_portlet_id()}


class AddForm(base.AddForm):

    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IMediacoreVideoPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _(u"title_add_mediacore_video_portlet",
              default=u"Add Mediacore video portlet here")
    description = _(u"description_add_mediacore_video_portlet",
                    default=u"A portlet which show a mediacore video")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IMediacoreVideoPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _(u"title_edit_mediacore_video_portlet",
              default=u"Edit Mediacore video portlet")
    description = _(u"description_edit_mediacore_video_portlet",
                    default=u"A portlet which show a mediacore video")
