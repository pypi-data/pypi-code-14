from rest_framework import serializers

from django.conf import settings

from bulbs.sections.models import Section


class GlanceContentSerializer(serializers.Serializer):

    type = serializers.IntegerField(required=True, allow_null=False)
    id = serializers.CharField()
    title = serializers.CharField()
    url = serializers.URLField()
    modified = serializers.DateTimeField()
    published = serializers.DateTimeField()
    campaign_id = serializers.IntegerField()
    description = serializers.CharField()
    feature_type = serializers.CharField()
    images = serializers.ListField(
        child=serializers.URLField()
    )
    videos = serializers.ListField(
        child=serializers.URLField()
    )
    authors = serializers.ListField(
        child=serializers.DictField()
    )
    sections = serializers.ListField(
        child=serializers.DictField()
    )
    tags = serializers.ListField(
        child=serializers.DictField()
    )

    def to_representation(self, obj):

        # TODO: Move into common code?
        sections = Section.objects.filter(
            pk__in=[s.rpartition('.')[-1] for s in obj.percolate_sections()]
        ).order_by('name').all()

        default_author = getattr(settings, 'GLANCE_FEED_AUTHOR', None)
        if default_author:
            authors = [{
                'id': 0,
                'label': default_author,
            }]
        else:
            authors = [
                {'id': author.id,
                 'label': author.get_full_name()}
                for author in obj.authors.all()
            ]

        # Note: Currently only sets "article" and "video". Type "graphic" not set.
        content_type = 'article'

        # Simple way to look for videos. Does not check for embeds.
        videos = []
        if hasattr(obj, 'videohub_ref'):
            content_type = 'video'
            videos = [obj.videohub_ref.get_hub_url()]

        return {
            'type': content_type,
            'id': obj.id,
            'title': obj.title,
            'modified': obj.last_modified.isoformat(),
            'published': obj.published.isoformat(),
            # Note: Could also check if part of special coverage
            'campaign_id': obj.tunic_campaign_id,
            'description': obj.description,
            'feature_type': (obj.feature_type.name if obj.feature_type else None),
            'images': [
                obj.thumbnail.get_crop_url(ratio='16x9'),
            ],
            'url': self.context['request'].build_absolute_uri(obj.get_absolute_url()),
            'body': getattr(obj, 'body', ''),
            'authors': authors,
            'sections': [
                {'id': section.id,
                 'label': section.name,
                 }
                for section in sections
            ],
            'tags': [
                {'id': tag.id,
                 'label': tag.name,
                 }
                for tag in obj.ordered_tags()
            ],
            'videos': videos,
        }
