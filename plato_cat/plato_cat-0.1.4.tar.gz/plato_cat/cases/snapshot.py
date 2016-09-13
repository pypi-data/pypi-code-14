# from plato_cat.cases import wait_for_job
# from plato_cat.cases import get_resource
# from plato_cat.cases import post_resource


class SnapshotCase():

    def run(self, API, sleep):
        pass
#         snapshots = get_resource(API, 'DescribeSnapshots',
#                                       {}, 'snapshotSet')

#         volumes = get_resource(API, 'DescribeVolumes', {
#             'status': ['active']
#         }, 'volumeSet')

#         volume_ids = [v['volumeId'] for v in volumes]

#         result = API.conn.call('CreateSnapshots', {
#             'name': 'test-snapshot',
#             'volumeId': volume_ids[0],
#         })

#         job_id = result['jobId']

#         wait_for_job(API, job_id, sleep)


class CleanSnapshots():

    def run(self, API, sleep):
        pass
#         snapshots = get_resource(API, 'DescribeSnapshots',{
#             'status': ['active', 'error'],
#         }, 'snapshotSet')

#         snapshot_ids = [i['snapshotId'] for i in snapshots]

#         post_resource(API, 'DeleteSnapshots', snapshot_ids, 'snapshotIds')
