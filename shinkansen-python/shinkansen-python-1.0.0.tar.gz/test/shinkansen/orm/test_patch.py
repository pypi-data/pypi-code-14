import __builtin__

import mox

from shinkansen.orm import patch


class TestPatch(mox.MoxTestBase):
    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx

    def test_apply_patches(self):
        redis = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(patch.db, 'redis_conn')
        patch.db.redis_conn().AndReturn(self.context(redis))
        self.mox.StubOutWithMock(patch.orm, 'get_lock')
        patch.orm.get_lock('key.LOCK', redis).AndReturn(self.context())
        self.mox.StubOutWithMock(patch, '_apply_patches')
        patch._apply_patches(redis, 'key', 'dir', 'mod')
        self.mox.ReplayAll()
        patch.apply_patches('key', 'dir', 'mod')

    def test__apply_patches_no_patches(self):
        redis = self.mox.CreateMockAnything()
        redis.smembers('key').AndReturn([])
        self.mox.StubOutWithMock(patch.glob, 'glob')
        patch.glob.glob(mox.IgnoreArg()).AndReturn([])
        self.mox.ReplayAll()
        patch._apply_patches(redis, 'key', 'dir', 'mod')

    def test__apply_patches(self):
        redis = self.mox.CreateMockAnything()
        redis.smembers('key').AndReturn(['a'])
        self.mox.StubOutWithMock(patch.glob, 'glob')
        patch.glob.glob(mox.IgnoreArg()).AndReturn(['c', 'a', 'b'])
        self.mox.StubOutWithMock(__builtin__, '__import__')
        b = self.mox.CreateMockAnything()
        __builtin__.__import__('mod.b', fromlist=['mod.b']).AndReturn(b)
        b.main()
        redis.sadd('key', 'b')
        c = self.mox.CreateMockAnything()
        __builtin__.__import__('mod.c', fromlist=['mod.c']).AndReturn(c)
        c.main()
        redis.sadd('key', 'c')
        self.mox.ReplayAll()
        patch._apply_patches(redis, 'key', 'dir', 'mod')
