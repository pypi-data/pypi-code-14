import os


def package_path():
    from path_helpers import path

    return path(__file__).parent


def get_lib_directory():
    r"""
    Return directory containing the Arduino library headers.
    """ 
    return package_path().joinpath('Arduino', 'TimerOne')



def get_includes():
    r"""
    Return the directory that contains the `arduino_timer_one` Cython *.hpp and
    *.pxd header files.

    Extension modules that need to compile against `arduino_timer_one` should use
    this function to locate the appropriate include directory.

    Notes
    -----
    When using ``distutils``, for example in ``setup.py``.
    ::

        import arduino_timer_one
        ...
        Extension('extension_name', ...
                  include_dirs=[...] + arduino_timer_one.get_includes())
        ...

    """
    return [get_lib_directory()]


def get_sources():
    r"""
    Return Arduino source file paths.  This includes any supplementary source
    files that are not contained in Arduino libraries.
    """
    return get_lib_directory().files('*.c*')
