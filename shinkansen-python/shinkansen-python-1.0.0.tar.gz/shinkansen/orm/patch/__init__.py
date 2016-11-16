import glob
import logging
import os

from shinkansen import db, orm


log = logging.getLogger(__name__)


DB_PATCHES_KEY = 'shinkansen.orm.patches.applied'


def apply_patches(db_patches_key=None, directory=None, module_base=None):
    if directory is None:
        directory = os.path.dirname(__file__)
    if db_patches_key is None:
        db_patches_key = DB_PATCHES_KEY
    if module_base is None:
        module_base = 'shinkansen.orm.patch'
    with db.redis_conn() as redis:
        with orm.get_lock(db_patches_key + '.LOCK', redis):
            _apply_patches(redis, db_patches_key, directory, module_base)


def _apply_patches(redis, db_patches_key=None, directory=None, module_base=None):
    applied_patches = set(redis.smembers(db_patches_key))
    patches = glob.glob(os.path.join(directory, '[0-9]*.py'))
    patches.sort()
    for patch_path in patches:
        patch_file = os.path.basename(patch_path)
        if patch_file in applied_patches:
            log.debug('Patch %s already applied', patch_file)
            continue
        log.info('Applying patch %s', patch_file)
        patch_module_name = '%s.%s' % (module_base, os.path.splitext(patch_file)[0])
        patch_module = __import__(patch_module_name, fromlist=[patch_module_name])
        patch_module.main()
        log.info('Patch %s applied', patch_file)
        redis.sadd(db_patches_key, patch_file)
