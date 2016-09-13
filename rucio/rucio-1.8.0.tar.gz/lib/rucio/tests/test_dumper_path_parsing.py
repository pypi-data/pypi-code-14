# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Fernando Lopez, <felopez@cern.ch>, 2015

import nose.tools
from rucio.common.dumper.path_parsing import remove_prefix
from rucio.common.dumper.path_parsing import components


class TestPathParsing(object):
    def test_remove_prefix(self):
        prefix = ['a', 'b', 'c', 'd']

        full = ['a', 'b', 'c', 'd', 'e', 'f']  # -> e,f
        relative = ['c', 'd', 'e', 'f']  # -> e,f
        exclusive = ['e', 'f', 'g']  # -> e,f,g
        mixed = ['c', 'a', 'e', 'f']  # -> c,a,e,f
        mixed2 = ['d', 'a', 'e']  # -> a,e

        nose.tools.eq_(remove_prefix(prefix, full), ['e', 'f'])
        nose.tools.eq_(remove_prefix(prefix, relative), ['e', 'f'])
        nose.tools.eq_(remove_prefix(prefix, exclusive), ['e', 'f', 'g'])
        nose.tools.eq_(remove_prefix(prefix, mixed), ['c', 'a', 'e', 'f'])
        nose.tools.eq_(remove_prefix(prefix, mixed2), ['a', 'e'])
        nose.tools.eq_(remove_prefix(prefix, prefix), [])
        nose.tools.eq_(remove_prefix([], relative), relative)
        nose.tools.eq_(remove_prefix(prefix, []), [])

    def test_real_sample(self):
        prefix = components('/pnfs/grid.sara.nl/data/atlas/atlasscratchdisk/')
        path_regular = components('/pnfs/grid.sara.nl/data/atlas/atlasscratchdisk/rucio/group10/perf-jets/02/1a/group10.perf-jets.data12_8TeV.periodI.physics_HadDelayed.jmr.2015.01.29.v01.log.4770484.000565.log.tgz')
        path_user = components('/pnfs/grid.sara.nl/data/atlas/atlasscratchdisk/rucio/user/zxi/fd/73/user.zxi.361100.PowhegPythia8EvtGen.DAOD_TOPQ1.e3601_s2576_s2132_r6630_r6264_p2363.08-12-15.log.6249615.000015.log.tgz')
        path_group = components('/pnfs/grid.sara.nl/data/atlas/atlasscratchdisk/rucio/group/det-ibl/00/5d/group.det-ibl.6044653.BTAGSTREAM._000014.root')
        path_sam = components('/pnfs/grid.sara.nl/data/atlas/atlasscratchdisk/SAM/testfile17-GET-ATLASSCRATCHDISK')

        nose.tools.eq_(
            '/'.join(remove_prefix(prefix, path_regular)),
            'rucio/group10/perf-jets/02/1a/group10.perf-jets.data12_8TeV.periodI.physics_HadDelayed.jmr.2015.01.29.v01.log.4770484.000565.log.tgz',
            'Normal path inside directory rucio/',
        )
        nose.tools.eq_(
            '/'.join(remove_prefix(prefix, path_user)),
            'rucio/user/zxi/fd/73/user.zxi.361100.PowhegPythia8EvtGen.DAOD_TOPQ1.e3601_s2576_s2132_r6630_r6264_p2363.08-12-15.log.6249615.000015.log.tgz',
            'User path inside rucio/',
        )
        nose.tools.eq_(
            '/'.join(remove_prefix(prefix, path_group)),
            'rucio/group/det-ibl/00/5d/group.det-ibl.6044653.BTAGSTREAM._000014.root',
            'Group path inside rucio/',
        )
        nose.tools.eq_(
            '/'.join(remove_prefix(prefix, path_sam)),
            'SAM/testfile17-GET-ATLASSCRATCHDISK',
            'SAM path (outside rucio/)',
        )
