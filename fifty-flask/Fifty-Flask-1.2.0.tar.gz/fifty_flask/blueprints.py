from flask import Blueprint as DefaultBlueprint


class Blueprint(DefaultBlueprint):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('static_folder', 'static')
        kwargs.setdefault('template_folder', 'templates')
        super(Blueprint, self).__init__(*args, **kwargs)
