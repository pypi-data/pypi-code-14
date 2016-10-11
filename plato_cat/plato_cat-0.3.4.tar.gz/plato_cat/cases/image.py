from plato_cat.cases import get_resource
from plato_cat.cases import wait_busy_resource
from plato_cat.cases import post_resource


class ImageCase():

    def run(self, API, sleep):
        API.conn.call('DescribeImages')


class CleanImages():

    def run(self, API, sleep):
        wait_busy_resource(API, 'DescribeImages', {
            'status': ['pending'],
            'isPublic': False
        }, sleep)

        images = get_resource(API, 'DescribeImages', {
            'status': ['active', 'error'],
            'isPublic': False
        }, 'imageSet')

        image_ids = [i['imageId'] for i in images]
        post_resource(API, 'DeleteImages', image_ids, 'imageIds')
