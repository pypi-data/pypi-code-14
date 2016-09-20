VARS = (
    (  'NAME'      ,  'DEFVAL' ,  'FORMAT'  ),

    (  'var_string',  "calgary",  "%s"      ),
    (  'var_float' ,  19.88    ,  "%.2f"    ),
    (  'var_int'   ,  46       ,  "%d"      ),
)

def _rotate_dict( tupl, dict_name ):
    globals()[ dict_name ] = dict()
    for var_name in tupl[ 0 ]:
        globals()[ dict_name ][ var_name ] = []
    for vals in tupl[ 1: ]:
        for i, var_name in enumerate( tupl[ 0 ]):
            globals()[ dict_name ][ var_name ].append( vals[ i ])

_rotate_dict( VARS, 'VAR' )
print repr(VAR)

for i, name in enumerate( VAR[ 'NAME' ]):
    globals()[ name ] = VAR[ 'DEFVAL' ][ i ]

if __name__ == '__main__':
    for i, name in enumerate( VAR[ 'NAME' ]):
        print ( "%s = " + VAR[ 'FORMAT' ][ i ]) % ( name, globals()[ name ])

    var_string = "montreal"
    var_float = 19.76
