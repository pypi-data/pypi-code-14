from cement.core.controller import CementBaseController, expose

VERSION = '0.0.1'

BANNER = """
Python Digital Ocean tool v%s
""" % VERSION


class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "iMoney DigitalOcean tool"

        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER))
        ]

    @expose(hide=True)
    def default(self):
        print self._help_text
