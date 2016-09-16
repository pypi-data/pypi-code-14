def remove(tag, db):
    from src import utils
    assert isinstance(db, utils.DB)

    job = db.get_job_by_tag(tag)

    if job.container:
        print('Stopping and removing the running container')
        from .lib.docker import docker_rm
        docker_rm(job.using_host, job.remote_path, job.container, job.docker)
        job.container = None
        db.save()

    # remove job
    print('Removing the tag: {} from DB'.format(tag))
    db.remove_job(job)
    print('Done')

