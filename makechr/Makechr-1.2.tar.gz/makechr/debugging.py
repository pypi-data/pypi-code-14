    #############################
    print '========================================'
    print '-dot profile manifest-------------------'
    for dot_profile, did in self._dot_manifest._dict.items():
      print '%s = %r [%s]' % (did, dot_profile, len(dot_profile))
    print '========================================'
    print '-color needs manifest-------------------'
    for color_needs, cid in self._color_manifest._dict.items():
      print '%s = %r [%s]' % (cid, color_needs, len(color_needs))
    print '========================================'
    print '-palette--------------------------------'
    print pal
    import sys
    print '========================================'
    print '-artifacts color_needs------------------'
    for y in xrange(30):
      for x in xrange(32):
        sys.stdout.write('%s ' % (self._artifacts[y][x][0],))
      sys.stdout.write('\n')
    print '========================================'
    print '-artifacts dot_profile------------------'
    for y in xrange(30):
      for x in xrange(32):
        sys.stdout.write('%s ' % (self._artifacts[y][x][1],))
      sys.stdout.write('\n')
    print '========================================'
    print '-artifacts vert_needs-------------------'
    for y in xrange(30):
      for x in xrange(32):
        sys.stdout.write('%s ' % (self._artifacts[y][x][2],))
      sys.stdout.write('\n')
    print '========================================'
    print '-colorization---------------------------'
    for y in xrange(30):
      for x in xrange(32):
        sys.stdout.write('%s ' % (self._ppu_memory.gfx_0.colorization[y][x]))
      sys.stdout.write('\n')
    print '========================================'
    print '-traverse artifacts---------------------'

    #############################

