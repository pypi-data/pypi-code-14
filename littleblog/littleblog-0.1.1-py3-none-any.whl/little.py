import os
import shutil

import importlib.util

from jinja2 import Environment, FileSystemLoader

import markdown


md_extensions = [
    'fenced_code', 
    'codehilite(linenums=True)',
]


class SettingsNotFound(Exception):
    pass


def load_settings(project_name):
    """ Load the settings.py file from the specified project_name directory """
    spec = importlib.util.spec_from_file_location('settings', os.path.join(project_name, 'settings.py'))
    settings = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(settings)
    except FileNotFoundError:
        raise SettingsNotFound("Couldin't find settings for '{}'".format(project_name))
    
    settings.CONTENT_DIR = os.path.join(project_name, settings.CONTENT_DIR) 
    settings.OUTPUT_DIR = os.path.join(project_name, settings.OUTPUT_DIR)
    settings.TEMPLATE_DIR = os.path.join(project_name, settings.TEMPLATE_DIR)
    settings.STATIC_DIR = os.path.join(project_name, settings.STATIC_DIR)

    return settings


def _render_markdown(content):
    return markdown.markdown(content, extensions=md_extensions)


def _render_detail(content, settings):
    env = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIR))
    template = env.get_template('detail.html')
    return template.render(content=content) 

def render(project_name):
    settings = load_settings(project_name)
    
    # Remove the previously generated content
    shutil.rmtree(settings.OUTPUT_DIR, ignore_errors=True)

    shutil.copytree(settings.STATIC_DIR, os.path.join(settings.OUTPUT_DIR, os.path.basename(settings.STATIC_DIR)))

    # Create the new output dir
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    
    for current_directory, sub_directories, files in os.walk(settings.CONTENT_DIR):
        if files:
            out_dir = current_directory.replace(settings.CONTENT_DIR, settings.OUTPUT_DIR, 1)
            os.makedirs(out_dir, exist_ok=True) 
            
            for f in files:
                with open(os.path.join(current_directory, f), 'r') as openf:
                    md = _render_markdown(openf.read())
                html_content = _render_detail(md, settings)
                fn = os.path.splitext(f)[0] + ".html"
                with open(os.path.join(out_dir, fn), 'w') as out:
                    out.write(html_content)   
