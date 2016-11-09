# encoding=utf-8
import os
from genericpath import exists
from os.path import join, abspath

html_replace = {
    '\n': '<br>',
    '[b]': '<strong style="color: red">',
    '[/b]': '</strong>',
    # For exception
    'File "': 'File "<font style="color: blue"><i>',
    '", line ': '</i></font>", line <font style="color: green"><b>',
    ', in ': '</b></font>, in ',
    '  ': ' &nbsp; &nbsp; &nbsp;',
}


def format_html(text):
    for field in html_replace:
        text = text.replace(field, html_replace[field])

    return text


class APIError(Exception):
    pass


class ImportModuleError(APIError):
    def __str__(self):
        try:
            user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
        except KeyError:
            user_paths = []

        module_full_path = self.args[0]
        error = self.args[1]
        traceback_text = self.args[2]
        relative_path = module_full_path.replace('.', '/') + ".py"

        real_path = None
        for path in user_paths:
            full_path = join(path, relative_path)
            if exists(full_path):
                real_path = abspath(full_path)
                break

        if real_path:
            return "Import module [b]{0}[/b] failed (file://{1})." \
                   "\n[b]Error when import: {2}." \
                   "[/b]\n----------------------\n{3}".format(
                        module_full_path, real_path,
                        str(error),
                        traceback_text
                    )

        return "Could not find module {0}. PYTHONPATH: {1}".format(
            module_full_path,
            ':'.join(user_paths)
        )


class ImportModuleClassError(APIError):
    def __str__(self):
        module_full_name, actual_module_name = self.args
        return 'Could not find class {0} in {1}'.format(actual_module_name, module_full_name)


class InvalidMethodError(APIError):
    def __str__(self):
        module_name, method_name = self.args
        return "API '{0}' does not have method '{1}'. Maybe it is not added or has a typo".format(module_name, method_name)
