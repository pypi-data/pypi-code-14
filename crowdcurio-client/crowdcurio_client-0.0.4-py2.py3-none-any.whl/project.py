import datetime
import requests
import time

from crowdcurio_client.crowdcurio import (
    CrowdCurioAPIException, CrowdCurioObject
)

class Project(CrowdCurioObject):
    _api_slug = 'project'
    _link_slug = 'project'
    _edit_attributes = (
        'slug',
        'name',
        'short_description',
        'description',
        'avatar',
        'is_active',
        'is_featured',
        'is_external',
        'redirect_url',
    )

    @classmethod
    def find(cls, id='', slug=None):
        if not id and not slug:
            return None
        return cls.where(id=id, slug=slug).next()

    def get_export(
        self,
        export_type,
        generate=False,
        wait=False,
        wait_timeout=60
    ):

        if generate:
            self.generate_export(export_type)

        if generate or wait:
            export = self.wait_export(export_type, wait_timeout)
        else:
            export = self.describe_export(export_type)

        return requests.get(media_url, stream=True)

    def wait_export(self, export_type, timeout=60):
        success = False
        end_time = datetime.datetime.now() + datetime.timedelta(
            seconds=timeout
        )

        while datetime.datetime.now() < end_time:
            export_description = self.describe_export(export_type)

            if export_type in TALK_EXPORT_TYPES:
                export_metadata = export_description['data_requests'][0]
            else:
                export_metadata = export_description['media'][0]['metadata']

            if export_metadata.get('state', '') in ('ready', 'finished'):
                success = True
                break

            time.sleep(2)

        if not success:
            raise CurioAPIException(
                '{}_export not ready within {} seconds'.format(
                    export_type,
                    timeout
                )
            )

        return export_description

    def generate_export(self, export_type):
        if export_type in TALK_EXPORT_TYPES:
            return talk.post_data_request(
                'project-{}'.format(self.id),
                export_type.replace('talk_', '')
            )

        return Project.post(
            self._export_path(export_type),
            json = {"media":{"content_type":"text/csv"}}
        )[0]

    def describe_export(self, export_type):
        if export_type in TALK_EXPORT_TYPES:
            return talk.get_data_request(
                'project-{}'.format(self.id),
                export_type.replace('talk_', '')
            )[0]

        return Project.get(self._export_path(export_type))[0]

    def _export_path(self, export_type):
        return '{}/{}_export'.format(self.id, export_type)

