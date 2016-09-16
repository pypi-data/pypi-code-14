# -*- coding: utf-8 -*-
from .cfg import SettingsLoadStrategyCfg
from .json_file import SettingsLoadStrategyJson
from .python import SettingsLoadStrategyPython

yaml_strategy = None
try:
    from .yaml_file import SettingsLoadStrategyYaml
    yaml_strategy = SettingsLoadStrategyYaml
except ImportError:  # pragma: no cover
    pass


strategies = (
    SettingsLoadStrategyPython,
    SettingsLoadStrategyCfg,
    SettingsLoadStrategyJson
)

if yaml_strategy:
    strategies += (yaml_strategy,)
