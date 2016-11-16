import mox

from scripts import shinkansen_trim_crate_data
from shinkansen import db


class TestShinkansenTrimCrateData(mox.MoxTestBase):
    def setUp(self):
        super(TestShinkansenTrimCrateData, self).setUp()

    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx

    def test_get_count(self):
        cur = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(db, 'cursor')
        db.cursor(None).AndReturn(self.context(cur))
        cur.execute(mox.IgnoreArg())
        cur.fetchone().AndReturn((42,))
        self.mox.ReplayAll()
        self.assertEqual(42, shinkansen_trim_crate_data.get_count(None, ''))
