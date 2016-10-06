"""Convert IRkernel Jupyter Notebooks to R Markdown."""
import os
import argparse
import json
import subprocess

__version__ = "2.0.0"


SETUP_R = """```{r setup, include=FALSE}
library(knitr)
opts_chunk$set(tidy.opts=list(width.cutoff=60),tidy=TRUE,cache=TRUE)
```

"""


def compile_rmarkdown(file_name, output_type):
    """Compile the rmarkdown file.

    :param str file_name: Name of file to compile
    :param str output_type: Type of output to generate
    """
    subprocess.call(["r", "-e", "library(rmarkdown); render('%s', '%s')" % (file_name, output_type)])


def convert_to_rmd(target_file, output_type, run_compile=False):
    """Convert a file to rmd.

    Note: If you pass an .rmd file to this function we will just compile it

    :param file target_file: Input file
    :param str output_type: Type of output to generate
    :param bool run_compile: If True, also compile the code
    """
    file_name, original_ext = os.path.splitext(target_file.name)
    rmd_file_name = file_name + ".rmd"

    if compile_rmarkdown and original_ext == ".rmd":
        compile_rmarkdown(rmd_file_name, output_type)
        return

    if original_ext != ".ipynb":
        raise TypeError("Only ipynb files can be converted")

    file_contents = json.load(target_file)

    with open(rmd_file_name, "w") as rmd:
        # Write initial source
        rmd.write(SETUP_R)

        for cell in file_contents["cells"]:
            cell_type = cell["cell_type"]

            if cell_type in ["markdown", "raw"]:
                rmd.write(''.join(cell["source"]))
            elif cell_type == "code":
                code = cell["source"]

                # Get chunk options
                if code[0].startswith("#r ") or code[0].startswith("# r "):
                    chunk_opts = code[0][1:].strip()
                    code = code[1:]
                else:
                    chunk_opts = "r"

                rmd.write("```{%s}\n%s\n```\n" % (chunk_opts, ''.join(code)))

            rmd.write("\n\n")

    if run_compile:
        compile_rmarkdown(rmd_file_name, output_type)


def main(args=None):
    parser = argparse.ArgumentParser(description="Convert an ipynb file to rmd")
    parser.add_argument("-c", "--compile", action="store_true")
    parser.add_argument("-o", "--output", default="pdf_document")
    parser.add_argument("target_file", type=argparse.FileType(mode="r"))
    args = parser.parse_args(args)

    return convert_to_rmd(args.target_file, args.output, args.compile)

if __name__ == "__main__":
    exit(main())
