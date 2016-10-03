"""This module provides the index function."""

import confipy.reader
import confipy.converter
import confipy.parser

converter_opts = {"dot": confipy.converter.DotNotation,
                  "dict": dict}


def load(path_or_fp, read_engine="auto", parsers=("include", "substitute"),
         converter="dot", **kwargs):
    """Main function to initiate reading, parsing and conversion.

    Parameters
    ----------
    path_or_fp: str, file-like
        Path to config file to be read.
    read_engine: {"auto", "yaml", "json", "configparser"}, optional
        Define the read engine to open the config file. By default, the file
        type is used to infer the correct read engine.
    parsers: iterable, optional
        Define parsers to be run on raw config data. Be aware, order matters.
    converter: {"dot", "dict"}, optional
        Define output type of config data. By default, config data provided in
        dot notation.

    Returns
    -------
    converted_cfg: {confipy.converter.DotNotation, dict}

    """

    read_cfg = confipy.reader.read_config(path_or_fp, read_engine=read_engine)
    parsed_cfg = confipy.parser.parsing_handler(parsers, read_cfg,
                                                source_path=path_or_fp,
                                                **kwargs)

    conv_type = converter_opts[converter]
    converted_cfg = confipy.converter._unflat_dict(parsed_cfg,
                                                   default_type=conv_type)

    return converted_cfg
