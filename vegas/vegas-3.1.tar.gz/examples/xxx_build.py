from cffi import FFI
ffi = FFI()

ffi.set_source("_xxx",
    """ // passed to the real C compiler
        #include <sys/types.h>
        #include <pwd.h>
    """,
    libraries=[])   # or a list of libraries to link with
    # (more arguments like setup.py's Extension class:
    # include_dirs=[..], extra_objects=[..], and so on)

ffi.cdef("""     // some declarations from the man page
    struct passwd {
        char *pw_name;
        ...;     // literally dot-dot-dot
    };
    struct passwd *getpwuid(int uid);
""")

if __name__ == "__main__":
    ffi.compile()
