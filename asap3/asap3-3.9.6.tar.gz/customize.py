"""User provided customizations.

This files defines system specific options etc for compiling Asap.

To adapt Asap to a new system type, please add code to this file
to identify it, and contribute the modified file back to the 
Asap project.

Alternatively, make a file called customize-local.py, and put
your customizations there.  

Here are all the lists that can be modified:
    
* libraries
* library_dirs
* include_dirs
* extra_link_args
* extra_compile_args
* runtime_library_dirs
* extra_objects
* define_macros
* mpi_libraries
* mpi_library_dirs
* mpi_include_dirs
* mpi_runtime_library_dirs
* mpi_define_macros

To override use the form:
    
    libraries = ['somelib', 'otherlib']

To append use the form

    libraries += ['somelib', 'otherlib']

You can access all variable from the setup.py script.  Useful ones are
* systemname  (for example 'Linux')
* hostname    (may or may not be fully qualified)
* machinename  (The CPU architechture, e.g. x86_64)
* processorname   (May contain more infor than machinename)

"""


if systemname == 'Linux' and machinename == 'x86_64':
    # For performance on 64-bit Linux.
    #
    # WARNING: -march=native is not appropriate to build
    #   binary packages that will run on another machine.
    
    extra_compile_args += ['-ffast-math', 
                           '-march=native', 
                           '-Wno-sign-compare']


# On the new CAMD Niflheim cluster (version 7), the readline library is not 
# linked when building the executable.  It looks like a bug in the Python
# installation.  It is presently unknown if it is site specific, or
# relevant for other similar installations.  Until that has been determined,
# the bug fix is only enabled when compiling on sylg.fysik.dtu.dk.
#
# Note: The symptom of this problem is that linking fails with missing
# symbols.  The names of many symbols begin with rl_

if hostname == 'sylg.fysik.dtu.dk':
    libraries += ['readline']
