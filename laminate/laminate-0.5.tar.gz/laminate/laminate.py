# -*- coding: utf-8 -*-
# pylint: disable=R0913, R0201
"""Laminate - Create beatifull yet simple html and pdf documents
from markdown"""
import os
from shutil import copytree, rmtree
from jinja2 import Environment, FileSystemLoader
import markdown
import laminate_default # pylint: disable=E0401

class Laminate():
    """This class parses markdown and combines the result with
    jinja templates and config variables provided by the user.

    Parameters:
        input_file : (str)
            Path to the index markdownfile.

        build_dir : (str)
            Path to output directory. **default: build**

        custom_template : (str)
            Path to custom template directory
    """

    def __init__(self, input_file, build_dir='build',
                 custom_template=None, **config):
        self._input_file = input_file
        self._input_filename = input_file.split('/')[-1]

        self._input_dir = os.path.dirname(os.path.abspath(self._input_file))
        self._input_dirname = self._input_dir.split('/')[-1]

        self._build_dir = os.path.join(build_dir, self._input_dirname)

        self._template = custom_template or os.path.join(
            list(laminate_default.__path__)[0], 'templates')

        self._config = config


    def create_html(self, markdown_parser=None):
        """Create the complete report as an html document

        Returns:
            dict:
                a dictionary (html, assets) contaning, paths to html file
                and assets directory.

        """
        self._clean_up_build_dir()

        output_file = os.path.join(self._build_dir, 'index.html')
        parsed_html = self.parse_jinja(markdown_parser)

        file_paths = {}
        file_paths['html'] = self._write_result(parsed_html, output_file)
        file_paths['assets'] = self._copy_template_assets()
        return file_paths


    def _copy_template_assets(self, asset_dir='assets',
                              source=None, destination=None):
        source = source or os.path.join(self._template, asset_dir)
        destination = destination or os.path.join(self._build_dir, asset_dir)
        # Copy all assets from template
        copytree(source, destination)
        return destination

    def _clean_up_build_dir(self):
        if os.path.exists(self._build_dir):
            rmtree(self._build_dir)

    def _write_result(self, content, output_file):
        output_dir = os.path.dirname(output_file)
        if os.path.exists(output_dir) is False:
            os.makedirs(output_dir)
        with open(output_file, 'wt', encoding="utf-8") as f:
            f.write(content)
        return output_file

    def parse_markdown(self, text=None, extentions=()):
        # pylint: disable=R0201
        """Parse markdown to html

        Parameters:
            text : str
                text to be converted to markdown

            extentions : touple
                A touple of extentions to be added to Python Markdown

        Returns:
            str:
                String containing the parsed mardown as html
        """
        text = text or open(self._input_file, 'r').read()
        # Read more about extentions here:
        # https://pythonhosted.org/Markdown/extensions/index.html
        markdown_extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.headerid',
        ]
        markdown_extensions += list(extentions)
        return markdown.markdown(text, extensions=markdown_extensions)

    def parse_jinja(self, markdown_parser=None):
        # pylint: disable=E1101
        """Combines a string of html with the jinja2 templates.

        Parameters:
            markdown_parser : func
                A custom markdown parser. Can be used to add custom extentions
                or use a different markdown parser. Default: self.parse_markdown

                Note: Since markdown is parsed for each filter. Extensions like
                TOC that creates table of content based on the content, will
                produce a toc for each time the filter is used. This will
                generally not what you want. So avoid the TOC extension for
                Python Markdown.

        Returns:
            str:
                The complete html document parsed by jinja as a string.
        """
        # Initialize the Jinja environment
        loaders = FileSystemLoader([self._template, self._input_dir])
        env = Environment(loader=loaders)

        # A custom markdown filter
        # can be disabled by setting markdown_parser to False
        if markdown_parser is not False:
            env.filters['markdown'] = markdown_parser or self.parse_markdown

        # Get the index markdown file
        template = env.get_template(self._input_filename)
        return template.render(**self._config)
