from .SMBase import SMBase

""" A collection of builtin server types. """

class Types(SMBase):
    """A class for keeping track of all types supported."""

    # TODO read from files later for types, but for now...
    supported = ["minimal"]

    @classmethod
    def supported(self, stype):
        """Determine if the type given is supported."""
        return stype in self.supported

    @classmethod
    def find_template(self, stype):
        """Find specific templates for types."""
        """template format is: for one server with {NAME}, and
         {description}, {result} for each report item.
         The returned list is [header, name section, result, footer] in html"""
        # TODO use files for templates
        if stype == "minimal":
            return ["<html>", "{NAME}<br/>", "{description}:{result}<br/>", "</html>"]
        else:
            return False

    @classmethod
    def find_reporter(self, stype):
        """Get report items."""
        """ should be list of [descrption, test] items"""
        if stype == "minimal":
            return [["CPU Usage", "mpstat | awk '$12 ~ /[0-9.]+/ { \
                    print 100 - $12\"%\" }'"]]
        else:
            return False
