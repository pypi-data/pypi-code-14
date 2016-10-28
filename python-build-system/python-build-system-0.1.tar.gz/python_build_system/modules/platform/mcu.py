import os
from mcu_info_util.toolchain import Toolchain


def convert_to_hex(ctx, source):
    if isinstance(source, list):
        return
    output_file_name = os.path.join(ctx.build_dir, os.path.splitext(os.path.basename(source))[0] + ".hex")
    objcopy = "%sobjcopy" % ctx.get_param("TOOLCHAIN_PREFIX")
    if not os.path.isfile(objcopy):
        objcopy += ".exe"
        if not os.path.isfile(objcopy):
            return
    command = "\"%s\" -Obinary \"%s\" \"%s\"" % (objcopy, source, output_file_name)
    ctx.run_command(command, source, output_file_name)
    return output_file_name


def convert_to_bin(ctx, source):
    if isinstance(source, list):
        return
    output_file_name = os.path.join(ctx.build_dir, os.path.splitext(os.path.basename(source))[0] + ".bin")
    objcopy = "%sobjcopy" % ctx.get_param("TOOLCHAIN_PREFIX")
    if not os.path.isfile(objcopy):
        objcopy += ".exe"
        if not os.path.isfile(objcopy):
            return
    command = "\"%s\" -Obinary \"%s\" \"%s\"" % (objcopy, source, output_file_name)
    ctx.run_command(command, source, output_file_name)
    return output_file_name


def display_elf_size(ctx, source):
    if isinstance(source, list):
        return
    size = "%ssize" % ctx.get_param("TOOLCHAIN_PREFIX")
    if not os.path.isfile(size):
        size += ".exe"
        if not os.path.isfile(size):
            return
    command = "\"%s\" \"%s\"" % (size, source)
    ctx.run_command(command, source, [])


def load_to_context(ctx, config):
    toolchain = Toolchain.find_toolchain(config)
    if toolchain is None:
        raise Exception("Failed to detect toolchain for MCU %s" % config)
    compiler = toolchain.find_compiler()
    if not compiler:
        raise Exception("Toolchain for MCU %s not installed" % config)
    prefix = toolchain.find_prefix()
    ctx.add_param("TOOLCHAIN_PREFIX", prefix)
    ctx.add_param("C_COMPILER", compiler)
    ctx.add_param("CXX_COMPILER", compiler)
    ctx.add_param("LINKER", compiler)
    ctx.add_param("EXECUTABLE_SUFFIX", ".elf")
    flags = toolchain.get_flags(config)
    flags_str = " ".join(flags)
    flags_str += " -ffunction-sections -fdata-sections -fno-common -Wl,-gc-sections"
    ctx.add_param("C_FLAGS[]", flags_str)
    ctx.add_param("CXX_FLAGS[]", flags_str)
    ctx.add_param("CXX_FLAGS[]", "-fno-exceptions -fno-rtti")
    ctx.add_param("LINK_FLAGS[]", flags_str)
    f_cpu = ctx.get_param("F_CPU")
    if f_cpu:
        ctx.add_param("C_FLAGS[]", "-DF_CPU=%s" % f_cpu)
        ctx.add_param("CXX_FLAGS[]", "-DF_CPU=%s" % f_cpu)
        ctx.remove_param("F_CPU")

    def generate_files(ctx):
        if not ctx.simulation:
            if toolchain.generate_linker_script(config, os.path.join(ctx.build_dir, "script.ld")):
                ctx.add_source(os.path.join(ctx.build_dir, "script.ld"))
            if toolchain.generate_header(config, os.path.join(ctx.build_dir, "mcudefs.h")):
                ctx.add_source(os.path.join(ctx.build_dir, "mcudefs.h"))
                ctx.add_param("C_FLAGS[]", "-I\"%s\"" % ctx.build_dir)
                ctx.add_param("CXX_FLAGS[]", "-I\"%s\"" % ctx.build_dir)

    ctx.add_prebuild_step(generate_files)
    ctx.add_package("platform/tools/c_compiler")
    ctx.add_package("platform/tools/cxx_compiler")
    ctx.add_package("platform/tools/linker")
    ctx.add_rule(r".*\.elf$", convert_to_hex)
    ctx.add_rule(r".*\.elf$", convert_to_bin)
    ctx.add_rule(r".*\.elf$", display_elf_size)
