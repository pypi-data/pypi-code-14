# ----------------------------------------------------------------------------
# Copyright 2015 Nervana Systems Inc.
# ----------------------------------------------------------------------------
"""
Subcommands for launching and managing interactive environments.
"""
import logging
from functools import partial

from ncloud.commands.command import Command, build_subparser
from ncloud.commands.command import START, STOP, LS
from ncloud.util.api_call import api_call_json
from ncloud.config import INTERACT
from ncloud.formatting.output import print_table

logger = logging.getLogger()


class Start(Command):
    """
    Launch an interactive ipython notebook environment.
    """
    @classmethod
    def parser(cls, subparser):
        interact = subparser.add_parser(START.name, aliases=START.aliases,
                                        description=Start.__doc__,
                                        help=Start.__doc__)
        interact.add_argument("-d", "--dataset-id",
                              help="ID of dataset to mount in notebook.")
        interact.add_argument("-f", "--framework-version",
                              help="Neon tag, branch or commit to use.")
        interact.add_argument("-i", "--resume-model-id",
                              help="Start training a new model using the state"
                                   " parameters of a previous one.")
        interact.add_argument("-g", "--gpus", default=1,
                              help="Number of GPUs to train this model with.")
        interact.add_argument("-u", "--custom-code-url",
                              help="URL for codebase containing custom neon "
                                   "scripts and extensions.")
        interact.add_argument("-c", "--custom-code-commit", default="master",
                              help="Commit ID or branch specifier for custom "
                                   "code repo.")
        interact.add_argument("-n", "--name",
                              help="Name of this interactive ipython "
                                   "notebook. If not supplied, one will be "
                                   "provided for you.")

        interact.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, gpus=1, dataset_id=None, framework_version=None,
             custom_code_url=None, resume_model_id=None,
             custom_code_commit=None, name=None):

        vals = {"gpus": gpus}
        if framework_version:
            vals["framework_version"] = framework_version

        if dataset_id:
            vals["dataset_id"] = dataset_id

        if resume_model_id:
            vals["resume_model_id"] = resume_model_id

        if custom_code_url:
            vals["custom_code_url"] = custom_code_url

        if custom_code_commit:
            vals["custom_code_commit"] = custom_code_commit

        if name:
            vals["name"] = name

        return api_call_json(config, INTERACT, method="POST", data=vals)

    @staticmethod
    def display_after(config, args, res):
        if 'uuid' in res:
            res['url'] = config.get_default_host() \
                               .rstrip('/') + '/interact/' + res['uuid']
            del res['uuid']

            print_table(res)


class Stop(Command):
    """
    Stop an interactive environment.
    """
    @classmethod
    def parser(cls, subparser):
        interact = subparser.add_parser(STOP.name, aliases=STOP.aliases,
                                        help=Stop.__doc__,
                                        description=Stop.__doc__)
        interact.add_argument("id", nargs="+",
                              help="id or list of IDs of sessions to stop")
        interact.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, id):

        res = []
        for stop in id:
            try:
                res.append(api_call_json(config, INTERACT+"/{}"
                           .format(stop), method="Delete"))
            except Exception:
                pass

        return res


class List(Command):
    """
    List interactive sessions.
    """
    @classmethod
    def parser(cls, subparser):
        interact = subparser.add_parser(LS.name, aliases=LS.aliases,
                                        help=List.__doc__,
                                        description=List.__doc__)
        interact.add_argument('-a', "--all", action="store_true",
                              help="Show sessions in all states.")
        interact.add_argument("-n", "--count", type=int, default='10',
                              help="Show up to n most recent sessions. "
                                   "For unlimited set n=0.")
        interact.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, all=False, count=10):
        vals = {"count": count}
        if not all:
            vals["filter"] = ["Ready", "Launching"]

        res = api_call_json(config, INTERACT, method="Get", params=vals)

        if 'sessions' in res:
            # adjust content for display, show full URL rather than uuid
            res = res['sessions']
            for r in res:
                r['url'] = config.get_default_host().rstrip('/') + \
                           '/interact/' + r['uuid']
                del r['uuid']

        return res


parser = partial(
    build_subparser, 'interact', ['i'], __doc__, (Start, List, Stop)
)
