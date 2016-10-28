def load_deps_from_makefile(filename, target=None):
    try:
        deps_list = []
        f = open(filename, "r")
        rule = ""
        for line in f:
            if rule and (rule[-1] == "\\"):
                rule = rule[:-1] + line.strip()
            else:
                rule = line.strip()
            if rule and rule[-1] != "\\":
                if (target is None) or rule.startswith("%s:" % target):
                    if target:
                        deps = rule[len(target) + 1:]
                    else:
                        deps = rule.split(":", 2)[1]
                    deps = deps.strip()
                    deps_list += deps.split(" ")
        f.close()
        return deps_list
    except IOError:
        pass
