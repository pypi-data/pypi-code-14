import os


def build_cxx_source(ctx, source):
    if isinstance(source, list):
        return
    output_file_name = os.path.join(ctx.build_dir, os.path.basename(source) + ".o")
    compiler = ctx.get_param("CXX_COMPILER")
    assert compiler, "CXX_COMPILER not defined"
    flags = ctx.get_param("CXX_FLAGS[]")
    flags += " -MMD -MP -MF \"%s\"" % (output_file_name + ".deps")
    command = "\"%s\" -c %s -o \"%s\" \"%s\"" % (compiler, flags, output_file_name, source)
    inputs = ctx.load_package("platform/tools/makefile").load_deps_from_makefile(output_file_name + ".deps",
                                                                                 output_file_name)
    inputs = inputs if inputs else [source]
    ctx.run_command(command, inputs, output_file_name)
    return output_file_name


def load_to_context(ctx, config):
    ctx.add_rule(r".*\.cpp$", build_cxx_source)
