from rest_framework import serializers

from cms.common import mixins
from .models import NavModule, NavModuleItem


class NavModuleItemSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='get_name')
    route = serializers.ReadOnlyField()

    class Meta:
        model = NavModuleItem
        fields = ('name', 'route', 'scroll_to_element', 'link',
                  'link_open_in_new_tab')

    def to_representation(self, obj):
        data = super(NavModuleItemSerializer, self).to_representation(obj)
        if not obj.route:
            data.pop('route')
        if not obj.scroll_to_element:
            data.pop('scroll_to_element')
        if not obj.link:
            data.pop('link')
        if not obj.link_open_in_new_tab:
            data.pop('link_open_in_new_tab')
        return data


class NavModuleSerializer(mixins.ModuleSerializer):
    items = NavModuleItemSerializer(many=True, source='get_items')

    class Meta:
        model = NavModule
        fields = ('pk', 'name', 'module_name_header_level', 'html_class',
                  'items')
