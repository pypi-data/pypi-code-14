import apt
import argparse

class DepFinder(object):

    def __init__(self, pkg_list):
        self.dep_set = set()
        self.apt_cache = apt.cache.Cache()
        self.apt_cache.open()
        for item in pkg_list:
            p = self.apt_cache[item]
            self.deps_recurse(self.dep_set, p)
        self.apt_cache.close()

    def __call__(self, pkg_list):
        self.dep_set.clear()
        self.apt_cache.open()
        for item in pkg_list:
            p = self.apt_cache[item]
            self.deps_recurse(self.dep_set, p)
        self.apt_cache.close()

    def deps_recurse(self, s, p):
      deps = p.candidate.get_dependencies('Depends')
      for i in deps:
        dp = i.installed_target_versions
        if len(dp) > 0:
          if not dp[0].package.name in s:
            s.add(dp[0].package.name)
            self.deps_recurse(s, dp[0].package)

def main():
    parser = argparse.ArgumentParser(
        description='Find recursive dependencies of installed package.')
    parser.add_argument('pkgs', metavar='PACKAGES', nargs='+',
                    help='package(s) to resolve dependencies')
    args = parser.parse_args()
    df = DepFinder(args.pkgs)
    deps = df.dep_set
    for i in deps:
      print(i)

if __name__ == '__main__':
    main()
