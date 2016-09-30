import json
import datetime
import pytz
from .settings import DEFAULT_TIMEZONE


def is_date_value(value):
    return isinstance(value, (datetime.datetime, datetime.date))


def get_date_string(value):
    """
    Properly converts date to datetime, time zone to UTC and formats according to spec
    """
    dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'
    if not isinstance(value, (datetime.datetime, datetime.date)):
        raise TypeError("'get_date_string' requires a datetime or date object.")
    if isinstance(value, datetime.date):
        value = datetime.datetime.fromordinal(value.toordinal())
    if value.tzinfo is None:
        tz = pytz.timezone(DEFAULT_TIMEZONE)
        value = value.replace(tzinfo=tz)
    utc = pytz.timezone('UTC')
    utc_value = value.astimezone(utc)
    return utc_value.strftime(dateformat)


def parse_date_string(value):
    """
    Converts a string to datetime with the default timezone set
    """
    dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'
    utc = pytz.timezone('UTC')
    utc_value = datetime.datetime.strptime(value, dateformat)
    utc_value.replace(tzinfo=utc)
    tz = pytz.timezone(DEFAULT_TIMEZONE)
    return value.replace(tzinfo=tz)


class ContentItem(object):
    """
    The basic definition of a content item with shortcuts
    """
    attributes = [
        'contentItemId',
        'name',
        'url',
        'text',
        'headline',
        'description',
        'keywords',
        'learningResourceType',
        'thumbnail',
        'image',
        'squareImage',
        'video',
        'dateCreated',
        'dateModified',
        'datePublished',
        'provider',
        'publisher',
    ]

    required_attributes = ['name', 'url', 'text', ]

    def __init__(self, **kwargs):
        from .registration import registry

        self._keywords = set()
        self._thumbnail = {'contentUrl': None}
        self._image = {'contentUrl': None}
        self._squareImage = {'contentUrl': None}
        self._video = {'embedUrl': None}
        self._provider = {'name': None}
        self._publisher = {'name': None}

        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            self.adapter = registry.adapter_for_instance(self.instance)
        else:
            self.instance = None
            self.adapter = None

        for attr in self.attributes:
            if attr in kwargs:
                setattr(self, attr, kwargs.get(attr))
            elif self.adapter is not None:
                setattr(self, attr, getattr(self.adapter, attr))

    def as_json(self):
        obj = {}
        for attr in self.attributes:
            obj[attr] = getattr(self, attr, '')

        if is_date_value(obj['dateCreated']):
            obj['dateCreated'] = get_date_string(obj['dateCreated'])
        if is_date_value(obj['dateModified']):
            obj['dateModified'] = get_date_string(obj['dateModified'])
        if is_date_value(obj['datePublished']):
            obj['datePublished'] = get_date_string(obj['datePublished'])

        # For creating objects, there won't be a contentItemId, so delete it
        # from the object if it is blank to avoid API confusion
        if not obj['contentItemId']:
            del obj['contentItemId']

        return json.dumps(obj)

    def from_json(self, json_string):
        obj = json.loads(json_string)
        if obj['dateCreated']:
            obj['dateCreated'] = parse_date_string(obj['dateCreated'])
        if obj['dateModified']:
            obj['dateModified'] = parse_date_string(obj['dateModified'])
        if obj['datePublished']:
            obj['datePublished'] = parse_date_string(obj['datePublished'])

        return obj

    @property
    def keywords(self):
        """
        Makes sure the keywords are managed as a set, but return a list
        """
        return list(self._keywords)

    @keywords.setter
    def keywords(self, keywords):
        if isinstance(keywords, (list, tuple, )):
            self._keywords.update(set(keywords))
        else:
            self._keywords.add(keywords)

    @property
    def thumbnail(self):
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value):
        self._thumbnail['contentUrl'] = value

    @thumbnail.deleter
    def thumbnail(self):
        self._thumbnail['contentUrl'] = None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image['contentUrl'] = value

    @image.deleter
    def image(self):
        self._image['contentUrl'] = None

    @property
    def squareImage(self):  # NOQA
        return self._squareImage

    @squareImage.setter
    def squareImage(self, value):  # NOQA
        self._squareImage['contentUrl'] = value

    @squareImage.deleter
    def squareImage(self):  # NOQA
        self._squareImage['contentUrl'] = None

    @property
    def video(self):
        return self._video

    @video.setter
    def video(self, value):
        self._video['embedUrl'] = value

    @video.deleter
    def video(self):
        self._video['embedUrl'] = None

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, value):
        self._provider['name'] = value

    @provider.deleter
    def provider(self):
        self._provider['name'] = None

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, value):
        self._publisher['name'] = value

    @publisher.deleter
    def publisher(self):
        self._publisher['name'] = None

    def __getattr__(self, name):
        """
        If the attribute hasn't been set, but is one of the known attributes,
        return an empty string
        """
        if name in self.attributes:
            return ''
