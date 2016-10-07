
import yappi
import _yappi
import utils
import time
from threading import Thread

class PerThreadTests(utils.YappiUnitTestCase):

    def test_basic_perthread(self):
        self.call_count = 0

        class Thread1(Thread): pass
        class Thread2(Thread): pass
        def b(): pass
        def a():
            time.sleep(0.1)
            self.call_count += 1
            if self.call_count == 2:
                b()

        yappi.set_clock_type("wall")
        yappi.start()
        t1 = Thread1(target=a)
        t1.start()
        t1.join()
        t2 = Thread2(target=a)
        t2.start()
        t2.join()
        fstats = yappi.get_func_stats()
        tstats = yappi.get_thread_stats()
        
        self.assertTrue(len(tstats) == 3)
        maint = utils.find_stat_by_id(tstats, 0)
        t1 = utils.find_stat_by_id(tstats, 1)
        t2 = utils.find_stat_by_id(tstats, 2)
        t1stats = yappi.get_func_stats(filter={"ctx_id":t1.id})
        t2stats = yappi.get_func_stats(filter={"ctx_id":t2.id})
        maintstats = yappi.get_func_stats(filter={"ctx_id":maint.id})
        sa = utils.find_stat_by_name(t1stats, "a")
        self.assertTrue(len(sa.children) == 0)
        self.assertEqual(sa.ncall, 1)
        self.assertTrue(sa.ttot < 1.4)
        sa = utils.find_stat_by_name(t2stats, "a")
        self.assertTrue(len(sa.children) == 1)
        self.assertEqual(sa.ncall, 1)
        self.assertTrue(sa.ttot < 1.4)
        sa = utils.find_stat_by_name(maintstats, "a")
        self.assertEqual(sa, None)

        sa = utils.find_stat_by_name(t2stats, "b")
        self.assertNotEqual(sa, None)
        sa = utils.find_stat_by_name(t1stats, "b")
        self.assertEqual(sa, None)

    def test_pause_resume(self):
        class Thread1(Thread): pass
        def a():pass
        def b():pass
        def c():pass
        yappi.start()
        t1 = Thread1(target=b)
        t1.start()
        t1.join()
        a()
        yappi.stop()
        a()
        yappi.start()
        a()
        t1 = Thread1(target=c)
        t1.start()
        t1.join()
        fstats = yappi.get_func_stats()
        fsa = utils.find_stat_by_name(fstats, "a")
        fsb = utils.find_stat_by_name(fstats, "b")
        self.assertEqual(fsa.ncall, 2)
        self.assertEqual(fsb.ncall, 1)
        tstats = yappi.get_thread_stats()
        self.assertEqual(len(tstats), 3)
        maint = utils.find_stat_by_id(tstats, 0)
        t1 = utils.find_stat_by_id(tstats, 1)
        t2 = utils.find_stat_by_id(tstats, 2)
        t1stats = yappi.get_func_stats(filter={"ctx_id":t1.id})
        t2stats = yappi.get_func_stats(filter={"ctx_id":t2.id})
        maintstats = yappi.get_func_stats(filter={"ctx_id":maint.id})
        sa = utils.find_stat_by_name(t1stats, "b")
        self.assertNotEqual(sa, None)
        sa = utils.find_stat_by_name(t2stats, "c")
        self.assertNotEqual(sa, None)


    def test_clear_stats(self):
        def a(): pass
        yappi.start()
        a()
        yappi.clear_stats()
        a()
        fsa = yappi.get_func_stats(filter={"name":"a"})
        self.assertNotEqual(fsa, None)
        fsb = yappi.get_func_stats(filter={"name":"b"})
        self.assertEqual(fsb.empty(), True)

    def test_ctx_callback_with_timings(self):
        self.ctx_id = 0
        def cbk():
            return self.ctx_id
        
        def b(): pass
        def a(): 
            b()

        _timings = {"a_1":15,"b_1":12,"a_2":9,"b_2":7}
        _yappi._set_test_timings(_timings)
        yappi.set_context_id_callback(cbk)
        yappi.start()
        a() # ctx-id=0
        self.ctx_id = 1
        a() # ctx-id=1

        yappi.stop()
        fstats = yappi.get_func_stats(filter={"ctx_id":0})
        fsa = utils.find_stat_by_name(fstats, "a")
        fsb = utils.find_stat_by_name(fstats, "b")
        self.assertEqual(fsa.ttot, 15)
        self.assertEqual(fsa.tsub, 3)
        self.assertEqual(fsb.ttot, 12)
        self.assertEqual(fsb.tsub, 12)
        fstats = yappi.get_func_stats(filter={"ctx_id":1})
        fsa = utils.find_stat_by_name(fstats, "a")
        fsb = utils.find_stat_by_name(fstats, "b")
        self.assertEqual(fsa.ttot, 15)
        self.assertEqual(fsa.tsub, 3)
        self.assertEqual(fsb.ttot, 12)
        self.assertEqual(fsb.tsub, 12)

        # save/load test
        fstats.save("pts.ystat", )
        stats = yappi.YFuncStats().add("pts.ystat")
        fsa = utils.find_stat_by_name(stats, "a")
        fsb = utils.find_stat_by_name(stats, "b")
        self.assertEqual(fsa.ttot, 15)
        self.assertEqual(fsa.tsub, 3)
        self.assertEqual(fsa.ncall, 1)
        self.assertEqual(fsb.ttot, 12)
        self.assertEqual(fsb.tsub, 12)
        self.assertEqual(fsb.ncall, 1)
