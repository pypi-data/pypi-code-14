import re
from HTML.Auto import Tag

__version__='0.0.1'

class Table:

    def __init__( self, *args ):
        self.params = args

    def portrait(   self, *args ): return self.generate( self._args(*args), 'theta', 0 )
    def landscape(  self, *args ): return self.generate( self._args(*args), { 'theta': -270, 'tgroups': 0 } )
    def north(      self, *args ): return self.generate( self._args(*args), { 'theta': 0 } )
    def west(       self, *args ): return self.generate( self._args(*args), { 'theta': -270, 'tgroups': 0 } )
    def east(       self, *args ): return self.generate( self._args(*args), { 'theta':   90, 'tgroups': 0, 'pinhead': 1 } )
    def south(      self, *args ): return self.generate( self._args(*args), { 'theta': -180, 'tgroups': 0, 'pinhead': 1 } )

    def generate( self, *args ):
        params = self._process( *args )

        if 'theta' in params and 'flip' in params and int( params['flip'] ):
            params['theta'] = -1 * int( params['theta'] )

        if not 'theta' in params:     # north
            if 'flip' in params:
                params['data'] = list( map( lambda r: r[::-1], params['data'] ) )

        elif params['theta'] == 90:   # east
            params['data'] = list( map( lambda r: list(r), zip( *params['data'] ) ) )
            if 'pinhead' in params and not 'headless' in params:
                for r in params['data']:
                    r.append( r.pop(0) )
            else:
                params['data'] = list( map( lambda r: r[::-1], params['data'] ) )

        elif params['theta'] == -90:
            params['data'] = list( map( lambda r: list(r), zip( *params['data'] ) ) )
            params['data'] = list( reversed( params['data'] ) )
            if 'pinhead' in params and not 'headless' in params:
                for r in params['data']:
                    r.append( r.pop(0) )
            else:
                params['data'] = list( map( lambda r: r[::-1], params['data'] ) )

        elif params['theta'] == 180:
            if 'pinhead' in params and not 'headless' in params:
                params['data'].append( params['data'].pop(0) )
                params['data'] = list( map( lambda r: r[::-1], params['data'] ) )
            else:
                params['data'] = list( map( lambda r: r[::-1], reversed( params['data'] ) ) )

        elif params['theta'] == -180: # south
            if 'pinhead' in params and not 'headless' in params:
                params['data'].append( params['data'].pop(0) )
            else:
                params['data'] = list( reversed( params['data'] ) )

        elif params['theta'] == 270:
            params['data'] = reversed( list( map( lambda r: list(r), zip( *params['data'] ) ) ) )

        elif params['theta'] == -270: # west
            params['data'] = list( map( lambda r: list(r), zip( *params['data'] ) ) )

        return self._make_table( params )

    def _make_table( self, params ):
        cdata   = []
        tr_attr = params['tr'] if 'tr' in params else {}
        tb_attr = params['table'] if 'table' in params else {}

        if 'caption' in params:
            cdata.append( self._tag( 'caption', params['caption'] ) )

        if 'colgroup' in params or 'col' in params:
            for c in self._colgroup( params):
                cdata.append( c )

        if 'tgroups' in params and params['tgroups'] > 0:
            body = list( params['data'] )
            matrix = params.get( 'matrix', 0 )
            head = body.pop(0) if not matrix and len( params['data'] ) > 2 else None
            foot = body.pop()  if not matrix and params['tgroups'] > 1 and len( params['data'] ) > 2 else None

            body_rows = []
            for r in body:
                body_rows.append( { 'tag': 'tr', 'attr': tr_attr, 'cdata': r } )
            if head:
                thead_tr_attr = params['thead.tr'] if 'thead.tr' in params else {}
                thead_attr    = params['thead'] if 'thead' in params else {}
                head_row = { 'tag': 'tr', 'attr': thead_tr_attr, 'cdata': head }
                cdata.append( { 'tag': 'thead', 'attr': thead_attr, 'cdata': head_row } )
            if foot:
                tfoot_tr_attr = params['tfoot.tr'] if 'tfoot.tr' in params else {}
                tfoot_attr    = params['tfoot'] if 'tfoot' in params else {}
                foot_row = { 'tag': 'tr', 'attr': tfoot_tr_attr, 'cdata': foot }
                cdata.append( { 'tag': 'tfoot', 'attr': tfoot_attr, 'cdata': foot_row } )

            tbody_attr = params['tbody'] if 'tbody' in params else {}
            cdata.append( { 'tag': 'tbody', 'attr': tbody_attr, 'cdata': body_rows } )

        else:
            for c in params['data']:
                cdata.append( { 'tag': 'tr', 'attr': tr_attr, 'cdata': c } )

        return params['auto'].tag( { 'tag': 'table', 'attr': tb_attr, 'cdata': cdata } )

    def _process( self, *args ):
        params = self._args( *args )

        if 'headings' in params:
            params['-r0'] = params['headings']

        index = {}
        if len( params['data'][0] ):
            for i in range( len( params['data'][0] ) ):
                key = params['data'][0][i] if params['data'][0][i] else ''
                index[ '-{}'.format(key) ] = i

            for key in list( params.keys() ):
                if key in index:
                    params[ '-c{}'.format(index[key]) ] = params[key]

        empty = params['empty'] if 'empty' in params else '&nbsp;'
        tag   = 'td' if params.get( 'matrix' ) or params.get( 'headless' ) else 'th'

        for r in range( params['_max_rows'] ):

            if not '_layout' in params:
                try:
                    params['data'][r]
                except IndexError:
                    params['data'].append( [] )

                for i in range( params['_max_cols'] - len( params['data'][r] ) ):
                    params['data'][r].append( '' )  # pad
                for i in range( len( params['data'][r] ) - params['_max_cols'] ):
                    params['data'][r].pop()         # truncate

            row = []
            for c in range( params['_max_cols'] ):
                attr  = params[tag] if tag in params else {}
                cdata = str( params['data'][r][c] )

                for dyna_param in [ tag, '-c{}'.format(c), '-r{}'.format(r), '-r{}c{}'.format(r,c) ]:
                    if dyna_param in params:
                        ( cdata, attr ) = self._extrapolate( cdata, attr, params[dyna_param] )

                # encoding here

                regex = re.compile(r"^\s*$")
                if regex.match( cdata ):
                    cdata = empty

                row.append( { 'tag': tag, 'attr': attr, 'cdata': cdata } )

            params['data'][r] = row
            tag = 'td'

        if 'headless' in params:
            params['data'].pop(0)

        return params

    def _args( self, *thingy ):
        data = []
        params = {}

        things = list( self.params ) + list( thingy )
        while things:
            thing = things.pop(0)
            if type( thing ) is list:
                if type( thing[0] ) is list:
                    data = thing
                else:
                    data.append( thing )
            elif type(thing) is dict:
                data = thing['data'] if 'data' in thing else data
                params.update( thing )
            else:
                if thing is 'data':
                    data = things.pop(0)
                else:
                    params[thing] = things.pop(0)

        params['data'] = list( data ) if data else [ [ '' ] ]

        params['_max_rows'] = len( params['data'] )
        params['_max_cols'] = len( params['data'][0] )

        if 'fill' in params and params['fill']:
            (row,col,*junk) = re.split( r'\D', params['fill'] )
            if row and int(row) > 0 and col and int(col) > 0:
                if int(row) > params['_max_rows']:
                    params['_max_rows'] = int(row)
                if int(col) > params['_max_cols']:
                    params['_max_cols'] = int(col)

        tag_params = {
            'level': params.get( 'level', 0 ),
            'sort': params.get( 'attr_sort', 0 )
        }
        if 'indent' in params:
            tag_params['indent'] = params['indent']
        params['auto'] = Tag( tag_params )

        return params

    def _colgroup( self, params ):
        colgroup = []
        if 'col' in params and type( params['col'] ) is dict:
            params['col'] = [ params['col'] ]

        if 'col' in params and type( params['col'] ) is list:
            if type( params['colgroup'] ) is list:
                colgroup = list( map( lambda cg: {
                    'tag': 'colgroup',
                    'attr': cg,
                    'cdata': list( map( lambda a: { 'tag': 'col', 'attr': a }, params['col'] ) )
                }, params['colgroup'] ) )
            else:
                attr = params['colgroup'] if params['colgroup'] else {}
                colgroup = {
                    'tag':   'colgroup',
                    'attr':  attr,
                    'cdata': list( map( lambda a: { 'tag': 'col', 'attr': a }, params['col'] ) )
                }

        else:
            if type( params['colgroup'] ) is dict:
                params['colgroup'] = [ params['colgroup'] ]

            if type( params['colgroup'] ) is list:
                colgroup = list( map( lambda a: { 'tag': 'colgroup', 'attr': a }, params['colgroup'] ) )

        if type( colgroup ) is dict:
            colgroup = [ colgroup ]

        return colgroup

    def _tag( self, tag, cdata ):
        tag = { 'tag': tag, 'cdata': cdata }
        if type( cdata ) is dict:
            keys = list( cdata.keys() )
            tag['cdata'] = keys[0]
            tag['attr']  = cdata[ keys[0] ]
        return tag

    def _extrapolate( self, cdata, orig_attr, thingy ):
        attr     = {}
        new_attr = {}
        thingy   = [ thingy ] if not type( thingy ) is list else thingy

        for t in thingy:
            if type( t ) is dict:
                new_attr = t
            else:
                cdata = t( cdata )

        if type( orig_attr ) is dict:
            for k in orig_attr:
                attr[k] = orig_attr[k]

        for k in new_attr:
            attr[k] = new_attr[k]

        return [ cdata, attr ]
