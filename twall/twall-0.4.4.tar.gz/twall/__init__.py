from .web import create_app as create_web_app
from .console import run_console as run_in_terminal

__all__ = ['create_web_app', 'run_in_terminal']