"""Convert IRkernel Jupyter Notebooks to R Markdown."""
import os
import argparse
import json
import subprocess

__version__ = "1.0.0"


SETUP_R = """```{r setup, include=FALSE}
library(knitr)
opts_chunk$set(tidy.opts=list(width.cutoff=60),tidy=TRUE)
```

"""


def convert_ipynb_to_rmd(ipynb_file, compile=False):
    """Convert an ipynb file to rmd.

    :param file ipynb_file:
    """
    file_name, original_ext = os.path.splitext(ipynb_file.name)

    if original_ext != ".ipynb":
        raise TypeError("Only ipynb files can be converted")

    file_contents = json.load(ipynb_file)

    rmd_file_name = file_name + ".rmd"

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

    if compile:
        subprocess.call(["r", "-e", "library(rmarkdown); render('%s', 'pdf_document')" % rmd_file_name])


def main(args=None):
    parser = argparse.ArgumentParser(description="Convert an ipynb file to rmd")
    parser.add_argument("-c", "--compile", action="store_true")
    parser.add_argument("ipynb_file", type=argparse.FileType(mode="r"))
    args = parser.parse_args(args)

    return convert_ipynb_to_rmd(args.ipynb_file, args.compile)

if __name__ == "__main__":
    exit(main())
