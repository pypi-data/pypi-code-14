import platform


def run_executable(ctx):
    command = "\"%s\"" % ctx.get_param("EXECUTABLE_NAME")
    ctx.run_command(command, [], [])


def load_to_context(ctx, config):
    if (platform.system() == "Windows") or (platform.system().startswith("CYGWIN")):
        ctx.add_param("EXECUTABLE_SUFFIX", ".exe")
    c_compiler = "gcc"
    cxx_compiler = "g++"
    ctx.add_param("C_COMPILER", c_compiler)
    ctx.add_param("CXX_COMPILER", cxx_compiler)
    ctx.add_param("LINKER", cxx_compiler)
    flags_str = "-ffunction-sections -fdata-sections -fno-common -Wl,-gc-sections"
    ctx.add_param("C_FLAGS[]", flags_str)
    ctx.add_param("CXX_FLAGS[]", flags_str)
    ctx.add_param("LINK_FLAGS[]", flags_str)
    ctx.add_package("platform/tools/c_compiler")
    ctx.add_package("platform/tools/cxx_compiler")
    ctx.add_package("platform/tools/linker")
    ctx.add_target("run", run_executable)
