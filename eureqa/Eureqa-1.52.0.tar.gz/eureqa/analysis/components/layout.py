from eureqa.analysis.components.base import _Component
from eureqa.utils.jsonrest import _JsonREST


class Layout(_Component):
    """Generic layout within an Analysis

    A generic grid layout composed of rows and columns sized by
    fractions (`1`, `1/2`, `1/4`, etc). Layouts can be nested within
    other layouts to create any type of grid needed.

    For example::

       layout = Layout()
       layout = Layout(borders=True)                                       # create a layout where borders are displayed
       layout.add_component(HtmlBlock(html="<h1>Hybrid Performance</h1>")) # add an item that is an entire row
       layout.add_row()                                                    # start a new row. newly added components will be placed into the new row.
       layout.add_component(MagnitudeBar(value=-0.22), "1/3")              # add a magnutide bar on the left 1/3 of the screen
       layout.add_component(MagnitudeBar(value=-0.22), "1/3", True)        # add a magnutide bar with dark background enabled
       layout.add_component(HtmlBlock(html="Variables...."), "1/2")        # add a text panel in the next 1/2 of the screen
       analysis.create_card(layout)                                        # Add this Layout to an Analysis

    :param list rows: (optional) List of :class:`~eureqa.analysis.components.Layout.Row` objects to add to this class initially

    """

    class _GridItem(object):
        """ Internal implementation class """
        def __init__(self, component=None, grid_unit="1", dark_background=False, analysis=None):
            self.grid_unit = grid_unit
            self.dark_background = dark_background
            self.component = component
            if component is not None and hasattr(component, "_component_id"):
                self._component_id = component._component_id
            self._analysis = analysis

        def _to_json(self):
            return {
                "grid_unit": self.grid_unit,
                "dark_background": self.dark_background,
                "component_id": self.component._component_id
            }

        def _from_json(self, body):
            if "grid_unit" in body:
                self.grid_unit = body["grid_unit"]
            if "dark_background" in body:
                self.dark_background = body["dark_background"]
            if "component_id" in body:
                self._component_id = body["component_id"]
                if self._analysis is not None:
                    self.component = _Component(_analysis=self._analysis, _component_id=body["component_id"])._get_self()

        def _associate(self, analysis):
            if self.component is None:
                self.component = _Component(_analysis=analysis, _component_id=getattr(self, "_component_id", None))._get_self()
            self.component._associate(analysis)

        def _associate_with_table(self, analysis):
            if self.component is None:
                self.component = _Component(_analysis=analysis, _component_id=getattr(self, "_component_id", None))._get_self()
            return self.component._associate_with_table(analysis)

    class _Row(object):
        """ Internal implementation class """
        def __init__(self, analysis=None, grid_items=None, ):
            self.grid_items = grid_items if grid_items else []
            self._analysis = analysis

        def create_card(self, component, grid_unit="1", dark_background=False):
            self.grid_items.append(Layout._GridItem(component, grid_unit, dark_background, self._analysis))
            return self.grid_items[-1]

        def _to_json(self):
            return [item._to_json() for item in self.grid_items]

        def _from_json(self, val):
            self.grid_items = []
            for item_json in val:
                item = Layout._GridItem(analysis=self._analysis)
                item._from_json(item_json)
                self.grid_items.append(item)

        def _associate(self, analysis):
            for item in self.grid_items:
                item._associate(analysis)

        def _associate_with_table(self, analysis):
            return [item._associate_with_table(analysis) for item in self.grid_items]

    _component_type_str = 'GENERIC_LAYOUT'

    def __init__(self, rows=None, borders=False, _analysis=None, _component_id=None, _component_type=None):
        if rows is not None:
            self.rows = rows
        else:
            self.rows = []
        self._borders = borders

        super(Layout, self).__init__(_analysis=_analysis, _component_id=_component_id, _component_type=_component_type)

    @property
    def _current_row(self):
        # Break with convention:
        # 'self.rows' is not a property that points to 'self._rows
        if len(self.rows) == 0:
            self.rows = [ Layout._Row(analysis=getattr(self, "_analysis", None)) ]

        return self.rows[-1]

    @property
    def borders(self):
        return self._borders

    def add_row(self):
        self.rows.append(Layout._Row(analysis=getattr(self, "_analysis", None)))
        return self.rows[-1]

    def add_component(self, component, grid_unit="1", dark_background=False):
        return self._current_row.create_card(component, grid_unit, dark_background)

    def delete(self):
        for row in self.rows:
            for item in row.grid_items:
                item.component.delete()
        super(Layout, self).delete()

    def _to_json(self):
        ret = super(Layout, self)._to_json()
        ret["rows"] = [row._to_json() for row in self.rows]
        return ret

    def _from_json(self, body):
        super(Layout, self)._from_json(body)
        self.rows = []
        for row_json in body.get("rows", []):
            row = Layout._Row(analysis=getattr(self, "_analysis", None))
            row._from_json(row_json)
            self.rows.append(row)

    def _associate(self, analysis):
        super(Layout, self)._associate(analysis)
        for row in self.rows:
            row._associate(analysis)

    def _fields(self):
        # 'rows' is handled in _to_json
        return super(Layout, self)._fields() + [ "borders" ]

    def _associate(self, analysis):
        for row in self.rows:
            row._associate(analysis)
        super(Layout, self)._associate(analysis)

    def _associate_with_table(self, analysis):
        components_json = []
        for row in self.rows:
            components_json += row._associate_with_table(analysis)
        return super(Layout, self)._associate_with_table(analysis) + components_json
