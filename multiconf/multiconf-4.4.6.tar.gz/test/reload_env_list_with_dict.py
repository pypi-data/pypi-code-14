from __future__ import print_function


class _ConfigBase(object):
    named_as = None

    def __setattr__(self, attr_name, value):
        if attr_name[0] == '_':
            object.__setattr__(self, attr_name, value)
            return

        try:
            current_env = self._mc_cr._mc_env
            self._mc_env_configs[self._mc_cr._mc_env_factory.envs.index(current_env)][attr_name] = value
        except KeyError:
            pass

    def setattr(self, attr_name, **env_values):
        if attr_name[0] == '_':
            raise Exception("attribute starting with '_' can't be set with item.setattr. Use assigment.")
        
        try:
            current_env = self._mc_cr._mc_env
            value = env_values[current_env]
            self._mc_env_configs[self._mc_cr._mc_env_factory.envs.index(current_env)][attr_name] = value
        except KeyError:
            # current_env not specified in **env_values
            pass

        try:
            getattr(self, attr_name)
        except AttributeError:
            raise Exception("No value specified for for env '{env}' when setting '{attr}', and no default.".format(
                env=current_env, attr=attr_name))

    def __getattr__(self, attr_name):
        try:
            current_env = self._mc_cr._mc_env
            return self._mc_env_configs[self._mc_cr._mc_env_factory.envs.index(current_env)][attr_name]
        except KeyError:
            return object.__getattribute__(self, attr_name)

    def getattr(self, attr_name, env):
        try:
            return self._mc_env_configs[self._mc_cr._mc_env_factory.envs.index(env)][attr_name]
        except KeyError as ex:
            return object.__getattribute__(self, attr_name)

    def env(self):
        return self._mc_cr._mc_env

    def __str__(self):
        return self._mc_cr._mc_env


class ConfigItem(_ConfigBase):
    named_as = None

    def __new__(cls, cr):
        try:
            return object.__getattribute__(cr, cls.named_as)
        except AttributeError:
            self= super(ConfigItem, cls).__new__(cls)
            self._mc_cr = cr
            self._mc_env_configs = [{} for _ in cr._mc_env_factory.envs]

            # Insert self in root. TODO contained_in
            object.__setattr__(cr, self.named_as, self)
            return self

    def __init__(self, cr):
        pass

    def __enter__(self):
        print('ci1')
        return self

    def __exit__(self, exc_type, value, traceback):
        print('ci2')


class ConfigRoot(_ConfigBase):
    def __init__(self):
        self._mc_cr = self

    def __enter__(self):
        print('r1')
        return self

    def __exit__(self, exc_type, value, traceback):
        print('r2')

    def env_factory(self):
        return self._mc_env_factory


class EnvFactory(object):
    def __init__(self):
        self.envs = ['pp', 'prod']
        self.cr = None

    def config(self, env):
        self.cr._mc_env = env
        return self.cr


def mc_config(env_factory, config_root_cls, allowed_todo=(), allowed_to_current=(), *root_cls_args, **root_cls_kwargs):
    def deco(conf_func):
        # Create root object
        cr = config_root_cls(*root_cls_args, **root_cls_kwargs)
        cr._mc_env_factory = env_factory
        cr._mc_env_configs = [{} for _ in env_factory.envs]
        env_factory.cr = cr

        # Load envs
        for env in env_factory.envs:
            cr._mc_env = env
            conf_func(cr)

    return deco


# --- fw ---

class X(ConfigItem):
    named_as = 'x'

    def __init__(self, cr):
        super(X, self).__init__(cr)
        self.ttt = 1

    def __enter__(self):
        print('x1')
        return self

    def __exit__(self, exc_type, value, traceback):
        print('x2')


ef = EnvFactory()


@mc_config(ef, ConfigRoot)
def config(root):
    with root as cr:
        print("in config method - loading:", cr)
        with X(cr) as x:
            x.setattr('ttt', prod=17)
            x.setattr('a', pp=11, prod=22)
            x.b = 17

        return cr


prod_cfg = ef.config('prod')
print("get me:", prod_cfg, prod_cfg.x.a, prod_cfg.x.b)
print("get other:", prod_cfg, prod_cfg.x.getattr('a', 'pp'), prod_cfg.x.getattr('b', 'pp'))
del prod_cfg

pp_cfg = ef.config('pp')
print("get me:", pp_cfg, pp_cfg.x.a, pp_cfg.x.b)
print("get other:", pp_cfg, pp_cfg.x.getattr('a', 'prod'), pp_cfg.x.getattr('b', 'prod'))
print("get ttt:", pp_cfg, pp_cfg.x.ttt, 'prod:', pp_cfg.x.getattr('ttt', 'prod'))

try:
    pp_cfg.x.q
except Exception as ex:
    print(ex)

try:
    pp_cfg.x.getattr('z', 'prod')
except Exception as ex:
    print(ex)
