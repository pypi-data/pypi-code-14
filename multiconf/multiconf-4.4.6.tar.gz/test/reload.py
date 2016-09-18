from __future__ import print_function


class EnvAttr(object):
    "Give property access to env specific values"

    def __init__(self, env, value):
        self.frozen = False
        self._mc_env_values = {}
        self._mc_env_values[env] = value

    def __get__(self, obj, objtype=None):
        if obj is None:
            print('__get__, obj == None')
            return self

        print('__get__')
        try:
            return self._mc_env_values[obj._mc_cr._mc_env]
        except KeyError:
            print('__get__, trying default')
            return self.default

    def __set__(self, obj, value):
        print('__set__')
        if self.frozen:
            raise AttributeError("can't set frozen mc attribute")
        self._mc_env_values[obj._mc_cr._mc_env] = value

    def __delete__(self, obj):
        raise AttributeError("can't delete mc attribute")

    def get_other_env(self, env):
        print('get_other_env', env)
        try:
            return self._mc_env_values[env]
        except KeyError:
            print('get_other_env, trying default')
            return self.default


class _ConfigBase(object):
    named_as = None

    def __setattr__(self, attr_name, value):
        print('_ConfigBase, __setattr__', attr_name, type(value))
        # Not called if attr already exists and is an EnvAttr
        if attr_name[0] != '_':
            value = EnvAttr(self._mc_cr._mc_env, value)
            try:
                value.default = getattr(self, attr_name)
            except AttributeError:
                pass

        object.__setattr__(self, attr_name, value)

    def setattr(self, attr_name, **env_values):
        if attr_name[0] == '_':
            raise Exception("attribute starting with '_' can't be set with item.setattr. Use assigment.")

        current_env = self._mc_cr._mc_env
        try:
            value = env_values[current_env]
            setattr(self, attr_name, value)
        except KeyError:
            # current_env not specified in **env_values
            pass

        try:
            getattr(self, attr_name)
        except AttributeError:
            raise Exception("No value specified for for env '{env}' when setting '{attr}', and no default.".format(
                env=current_env, attr=attr_name))

    def getattr(self, attr_name, env):
        try:
            attr = self.__dict__['attr_name']
            return attr._mc_env_values[env]
        except (KeyError, AttributeError) as ex:
            return getattr(self, attr_name)

    def __getattribute__(self, attr_name):
        attr = object.__getattribute__(self, attr_name)
        return attr.__get__(self, _ConfigBase) if hasattr(attr, '__get__') else attr

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

# class Root(object):
#     _mc_env = 'pp'
# 
# class Ttt(object):
#     _mc_cr = Root()
#     x = EnvAttr('pp', 1)
# 
# ttt = Ttt()
# print(ttt.x)
