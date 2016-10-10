"""This module provides the index function."""

import confipy.reader
import confipy.converter
import confipy.parser


def load(path_or_fp, read_engine="auto", parsers=("include", "substitute"),
         notation="dot", **kwargs):
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
    notation: {"dot", "dict"}, optional
        Define output type of config data. By default, config data provided in
        dot notation.

    Returns
    -------
    converted_cfg: {DotNotation, dict}

    """

    read_cfg = confipy.reader.read_config(path_or_fp, read_engine=read_engine)

    flatten_cfg = confipy.converter._flat_dict(read_cfg, notation=notation)

    parsed_cfg = confipy.parser.parsing_handler(parsers,
                                                flatten_cfg,
                                                source_path=path_or_fp,
                                                **kwargs)

    converted_cfg = confipy.converter._unflat_dict(parsed_cfg,
                                                   notation=notation)

    return converted_cfg
