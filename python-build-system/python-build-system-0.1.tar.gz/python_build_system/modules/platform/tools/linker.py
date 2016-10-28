import os


def link_executable(ctx, sources):
    if (not isinstance(sources, list)) or (len(sources) == 0):
        return
    output_file_name = os.path.join(ctx.build_dir, ctx.get_param("PROJECT_NAME") + ctx.get_param("EXECUTABLE_SUFFIX"))
    linker = ctx.get_param("LINKER")
    assert linker, "LINKER not defined"
    flags = ctx.get_param("LINK_FLAGS[]")
    sources_str = ""
    for source in sources:
        if source.endswith(".ld"):
            flags += " -T \"%s\"" % source
        else:
            sources_str += "\"" + source + "\" "
    command = "\"%s\" %s -o \"%s\" %s" % (linker, sources_str, output_file_name, flags)
    ctx.run_command(command, sources, output_file_name)
    ctx.add_param("EXECUTABLE_NAME", output_file_name)
    return output_file_name


def load_to_context(ctx, config):
    ctx.add_rule(r".*\.(o|ld)$", link_executable)
