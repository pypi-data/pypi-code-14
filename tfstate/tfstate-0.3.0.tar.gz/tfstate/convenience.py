from .loader import TerraformLoader
from . import constants


def get(state_uri, cache_dir=constants.DEFAULT_CACHE_DIR,
        cache_max_seconds=60, module=None):
    """Get the terraform output related to the state_uri"""
    loader = TerraformLoader.initialize(
        cache_dir=cache_dir,
        state_uri=state_uri,
        cache_max_seconds=cache_max_seconds,
    )
    return loader.load_state(module=module)
