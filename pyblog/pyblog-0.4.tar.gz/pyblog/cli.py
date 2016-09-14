import pyblog
import sys

def pyblog_init():
    if len(sys.argv) != 2:
        sys.exit('usage: %s <directory>' % sys.argv[0])
    try:
        print 'creating blog structure...'
        pyblog.Blog.dir_init(sys.argv[1])
        print 'done'
    except Exception as e:
        sys.exit('error: %r' % e)

def pyblog_build():
    if len(sys.argv) != 3:
        sys.exit('usage: %s <input_dir> <output_dir>' % sys.argv[0])
    try:
        print 'compiling blog'
        pyblog.Blog.compile(sys.argv[1], sys.argv[2])
        print 'done'
    except Exception as e:
        sys.exit('error: %r' % e)
