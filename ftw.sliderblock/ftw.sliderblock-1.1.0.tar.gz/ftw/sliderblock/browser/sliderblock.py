from Acquisition._Acquisition import aq_inner
from ftw.simplelayout.browser.blocks.base import BaseBlock
from ftw.slider.browser.slider import SliderView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SliderBlockView(BaseBlock, SliderView):
    template = ViewPageTemplateFile('templates/sliderblock.pt')

    def can_add(self):
        context = aq_inner(self.context)
        mtool = getToolByName(context, 'portal_membership')
        permission = mtool.checkPermission('ftw.sliderblock: Add SliderBlock',
                                           context)
        return bool(permission)
