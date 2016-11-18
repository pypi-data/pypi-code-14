# -*- coding: utf-8 -*-
import re
from pygments.lexers.sql import RegexLexer
from pygments.token import Name, Keyword, Text, Comment, Operator, Number, String, Punctuation


class CCL_Lexer(RegexLexer):
    """
    Lexer for Cerner Command Language.
    """
    name = 'CCL'
    aliases = ['ccl']
    filenames = ['*.ccl']

    flags = re.IGNORECASE
    tokens = {
        'root': [
            (r'\s+', Text),
            (r'--.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'('
             r'ABORT|ABS|ABSOLUTE|ACCESS|ADA|ADD|ADMIN|AFTER|AGGREGATE|'
             r'ALIAS|ALL|ALLOCATE|ALTER|ANALYSE|ANALYZE|AND|ANY|ARE|AS|'
             r'ASC|ASENSITIVE|ASSERTION|ASSIGNMENT|ASYMMETRIC|AT|ATOMIC|'
             r'AUTHORIZATION|AVG|BACKWARD|BEFORE|BEGIN|BETWEEN|BITVAR|'
             r'BIT_LENGTH|BOTH|BREADTH|BY|C|CACHE|CALL|CALLED|CARDINALITY|'
             r'CASCADE|CASCADED|CASE|CAST|CATALOG|CATALOG_NAME|CHAIN|'
             r'CHARACTERISTICS|CHARACTER_LENGTH|CHARACTER_SET_CATALOG|'
             r'CHARACTER_SET_NAME|CHARACTER_SET_SCHEMA|CHAR_LENGTH|CHECK|'
             r'CHECKED|CHECKPOINT|CLASS|CLASS_ORIGIN|CLOB|CLOSE|CLUSTER|'
             r'COALSECE|COBOL|COLLATE|COLLATION|COLLATION_CATALOG|'
             r'COLLATION_NAME|COLLATION_SCHEMA|COLUMN|COLUMN_NAME|'
             r'COMMAND_FUNCTION|COMMAND_FUNCTION_CODE|COMMENT|COMMIT|'
             r'COMMITTED|COMPLETION|CONDITION_NUMBER|CONNECT|CONNECTION|'
             r'CONNECTION_NAME|CONSTRAINT|CONSTRAINTS|CONSTRAINT_CATALOG|'
             r'CONSTRAINT_NAME|CONSTRAINT_SCHEMA|CONSTRUCTOR|CONTAINS|'
             r'CONTINUE|CONVERSION|CONVERT|COPY|CORRESPONTING|COUNT|'
             r'CREATE|CREATEDB|CREATEUSER|CROSS|CUBE|CURRENT|CURRENT_DATE|'
             r'CURRENT_PATH|CURRENT_ROLE|CURRENT_TIME|CURRENT_TIMESTAMP|'
             r'CURRENT_USER|CURSOR|CURSOR_NAME|CYCLE|DATA|DATABASE|'
             r'DATETIME_INTERVAL_CODE|DATETIME_INTERVAL_PRECISION|DAY|'
             r'DEALLOCATE|DECLARE|DEFAULT|DEFAULTS|DEFERRABLE|DEFERRED|'
             r'DEFINED|DEFINER|DELETE|DELIMITER|DELIMITERS|DEREF|DESC|'
             r'DESCRIBE|DESCRIPTOR|DESTROY|DESTRUCTOR|DETERMINISTIC|'
             r'DIAGNOSTICS|DICTIONARY|DISCONNECT|DISPATCH|DISTINCT|DO|'
             r'DOMAIN|DROP|DYNAMIC|DYNAMIC_FUNCTION|DYNAMIC_FUNCTION_CODE|'
             r'EACH|ELSE|ENCODING|ENCRYPTED|END|END-EXEC|EQUALS|ESCAPE|EVERY|'
             r'EXCEPT|ESCEPTION|EXCLUDING|EXCLUSIVE|EXEC|EXECUTE|EXISTING|'
             r'EXISTS|EXPLAIN|EXTERNAL|EXTRACT|FALSE|FETCH|FINAL|FIRST|FOR|'
             r'FORCE|FOREIGN|FORTRAN|FORWARD|FOUND|FREE|FREEZE|FROM|FULL|'
             r'FUNCTION|G|GENERAL|GENERATED|GET|GLOBAL|GO|GOTO|GRANT|GRANTED|'
             r'GROUP|GROUPING|HANDLER|HAVING|HIERARCHY|HOLD|HOST|IDENTITY|'
             r'IGNORE|ILIKE|IMMEDIATE|IMMUTABLE|IMPLEMENTATION|IMPLICIT|IN|'
             r'INCLUDING|INCREMENT|INDEX|INDITCATOR|INFIX|INHERITS|INITIALIZE|'
             r'INITIALLY|INNER|INOUT|INPUT|INSENSITIVE|INSERT|INSTANTIABLE|'
             r'INSTEAD|INTERSECT|INTO|INVOKER|IS|ISNULL|ISOLATION|ITERATE|JOIN|'
             r'KEY|KEY_MEMBER|KEY_TYPE|LANCOMPILER|LANGUAGE|LARGE|LAST|'
             r'LATERAL|LEADING|LEFT|LENGTH|LESS|LEVEL|LIKE|LIMIT|LISTEN|LOAD|'
             r'LOCAL|LOCALTIME|LOCALTIMESTAMP|LOCATION|LOCATOR|LOCK|LOWER|'
             r'MAP|MATCH|MAX|MAXVALUE|MESSAGE_LENGTH|MESSAGE_OCTET_LENGTH|'
             r'MESSAGE_TEXT|METHOD|MIN|MINUTE|MINVALUE|MOD|MODE|MODIFIES|'
             r'MODIFY|MONTH|MORE|MOVE|MUMPS|NAMES|NATIONAL|NATURAL|NCHAR|'
             r'NCLOB|NEW|NEXT|NO|NOCREATEDB|NOCREATEUSER|NONE|NOT|NOTHING|'
             r'NOTIFY|NOTNULL|NULL|NULLABLE|NULLIF|OBJECT|OCTET_LENGTH|OF|OFF|'
             r'OFFSET|OIDS|OLD|ON|ONLY|OPEN|OPERATION|OPERATOR|OPTION|OPTIONS|'
             r'OR|ORDER|ORDINALITY|OUT|OUTER|OUTPUT|OVERLAPS|OVERLAY|OVERRIDING|'
             r'OWNER|PAD|PARAMETER|PARAMETERS|PARAMETER_MODE|PARAMATER_NAME|'
             r'PARAMATER_ORDINAL_POSITION|PARAMETER_SPECIFIC_CATALOG|'
             r'PARAMETER_SPECIFIC_NAME|PARAMATER_SPECIFIC_SCHEMA|PARTIAL|'
             r'PASCAL|PENDANT|PLACING|PLI|POSITION|POSTFIX|PRECISION|PREFIX|'
             r'PREORDER|PREPARE|PRESERVE|PRIMARY|PRIOR|PRIVILEGES|PROCEDURAL|'
             r'PROCEDURE|PUBLIC|READ|READS|RECHECK|RECURSIVE|REF|REFERENCES|'
             r'REFERENCING|REINDEX|RELATIVE|RENAME|REPEATABLE|REPLACE|RESET|'
             r'RESTART|RESTRICT|RETURN|RETURNED_LENGTH|'
             r'RETURNED_OCTET_LENGTH|RETURNED_SQLSTATE|RETURNS|REVOKE|RIGHT|'
             r'ROLE|ROLLBACK|ROLLUP|ROUTINE|ROUTINE_CATALOG|ROUTINE_NAME|'
             r'ROUTINE_SCHEMA|ROW|ROWS|ROW_COUNT|RULE|SAVE_POINT|SCALE|SCHEMA|'
             r'SCHEMA_NAME|SCOPE|SCROLL|SEARCH|SECOND|SECURITY|SELECT|SELF|'
             r'SENSITIVE|SERIALIZABLE|SERVER_NAME|SESSION|SESSION_USER|SET|'
             r'SETOF|SETS|SHARE|SHOW|SIMILAR|SIMPLE|SIZE|SOME|SOURCE|SPACE|'
             r'SPECIFIC|SPECIFICTYPE|SPECIFIC_NAME|SQL|SQLCODE|SQLERROR|'
             r'SQLEXCEPTION|SQLSTATE|SQLWARNINIG|STABLE|START|STATE|STATEMENT|'
             r'STATIC|STATISTICS|STDIN|STDOUT|STORAGE|STRICT|STRUCTURE|STYPE|'
             r'SUBCLASS_ORIGIN|SUBLIST|SUBSTRING|SUM|SYMMETRIC|SYSID|SYSTEM|'
             r'SYSTEM_USER|TABLE|TABLE_NAME| TEMP|TEMPLATE|TEMPORARY|TERMINATE|'
             r'THAN|THEN|TIMESTAMP|TIMEZONE_HOUR|TIMEZONE_MINUTE|TO|TOAST|'
             r'TRAILING|TRANSATION|TRANSACTIONS_COMMITTED|'
             r'TRANSACTIONS_ROLLED_BACK|TRANSATION_ACTIVE|TRANSFORM|'
             r'TRANSFORMS|TRANSLATE|TRANSLATION|TREAT|TRIGGER|TRIGGER_CATALOG|'
             r'TRIGGER_NAME|TRIGGER_SCHEMA|TRIM|TRUE|TRUNCATE|TRUSTED|TYPE|'
             r'UNCOMMITTED|UNDER|UNENCRYPTED|UNION|UNIQUE|UNKNOWN|UNLISTEN|'
             r'UNNAMED|UNNEST|UNTIL|UPDATE|UPPER|USAGE|USER|'
             r'USER_DEFINED_TYPE_CATALOG|USER_DEFINED_TYPE_NAME|'
             r'USER_DEFINED_TYPE_SCHEMA|USING|VACUUM|VALID|VALIDATOR|VALUES|'
             r'VARIABLE|VERBOSE|VERSION|VIEW|VOLATILE|WHEN|WHENEVER|WHERE|'
             r'WITH|WITHOUT|WORK|WRITE|YEAR|ZONE|'
             r'abort|abs|absolute|access|ada|add|admin|after|aggregate|'
             r'alias|all|allocate|alter|analyse|analyze|and|any|are|as|'
             r'asc|asensitive|assertion|assignment|asymmetric|at|atomic|'
             r'authorization|avg|backward|before|begin|between|bitvar|'
             r'bit_length|both|breadth|by|c|cache|call|called|cardinality|'
             r'cascade|cascaded|case|cast|catalog|catalog_name|chain|'
             r'characteristics|character_length|character_set_catalog|'
             r'character_set_name|character_set_schema|char_length|check|'
             r'checked|checkpoint|class|class_origin|clob|close|cluster|'
             r'coalsece|cobol|collate|collation|collation_catalog|'
             r'collation_name|collation_schema|column|column_name|'
             r'command_function|command_function_code|comment|commit|'
             r'committed|completion|condition_number|connect|connection|'
             r'connection_name|constraint|constraints|constraint_catalog|'
             r'constraint_name|constraint_schema|constructor|contains|'
             r'continue|conversion|convert|copy|corresponting|count|'
             r'create|createdb|createuser|cross|cube|current|current_date|'
             r'current_path|current_role|current_time|current_timestamp|'
             r'current_user|cursor|cursor_name|cycle|data|database|'
             r'datetime_interval_code|datetime_interval_precision|day|'
             r'deallocate|declare|default|defaults|deferrable|deferred|'
             r'defined|definer|delete|delimiter|delimiters|deref|desc|'
             r'describe|descriptor|destroy|destructor|deterministic|'
             r'diagnostics|dictionary|disconnect|dispatch|distinct|do|'
             r'domain|drop|dynamic|dynamic_function|dynamic_function_code|'
             r'each|else|encoding|encrypted|end|end-exec|equals|escape|every|'
             r'except|esception|excluding|exclusive|exec|execute|existing|'
             r'exists|explain|external|extract|false|fetch|final|first|for|'
             r'force|foreign|fortran|forward|found|free|freeze|from|full|'
             r'function|g|general|generated|get|global|go|goto|grant|granted|'
             r'group|grouping|handler|having|hierarchy|hold|host|identity|'
             r'ignore|ilike|immediate|immutable|implementation|implicit|in|'
             r'including|increment|index|inditcator|infix|inherits|initialize|'
             r'initially|inner|inout|input|insensitive|insert|instantiable|'
             r'instead|intersect|into|invoker|is|isnull|isolation|iterate|join|'
             r'key|key_member|key_type|lancompiler|language|large|last|'
             r'lateral|leading|left|length|less|level|like|limit|listen|load|'
             r'local|localtime|localtimestamp|location|locator|lock|lower|'
             r'map|match|max|maxvalue|message_length|message_octet_length|'
             r'message_text|method|min|minute|minvalue|mod|mode|modifies|'
             r'modify|month|more|move|mumps|names|national|natural|nchar|'
             r'nclob|new|next|no|nocreatedb|nocreateuser|none|not|nothing|'
             r'notify|notnull|null|nullable|nullif|object|octet_length|of|off|'
             r'offset|oids|old|on|only|open|operation|operator|option|options|'
             r'or|order|ordinality|out|outer|output|overlaps|overlay|overriding|'
             r'owner|pad|parameter|parameters|parameter_mode|paramater_name|'
             r'paramater_ordinal_position|parameter_specific_catalog|'
             r'parameter_specific_name|paramater_specific_schema|partial|'
             r'pascal|pendant|placing|pli|position|postfix|precision|prefix|'
             r'preorder|prepare|preserve|primary|prior|privileges|procedural|'
             r'procedure|public|read|reads|recheck|recursive|ref|references|'
             r'referencing|reindex|relative|rename|repeatable|replace|reset|'
             r'restart|restrict|return|returned_length|'
             r'returned_octet_length|returned_sqlstate|returns|revoke|right|'
             r'role|rollback|rollup|routine|routine_catalog|routine_name|'
             r'routine_schema|row|rows|row_count|rule|save_point|scale|schema|'
             r'schema_name|scope|scroll|search|second|security|select|self|'
             r'sensitive|serializable|server_name|session|session_user|set|'
             r'setof|sets|share|show|similar|simple|size|some|source|space|'
             r'specific|specifictype|specific_name|sql|sqlcode|sqlerror|'
             r'sqlexception|sqlstate|sqlwarninig|stable|start|state|statement|'
             r'static|statistics|stdin|stdout|storage|strict|structure|stype|'
             r'subclass_origin|sublist|substring|sum|symmetric|sysid|system|'
             r'system_user|table|table_name| temp|template|temporary|terminate|'
             r'than|then|timestamp|timezone_hour|timezone_minute|to|toast|'
             r'trailing|transation|transactions_committed|'
             r'transactions_rolled_back|transation_active|transform|'
             r'transforms|translate|translation|treat|trigger|trigger_catalog|'
             r'trigger_name|trigger_schema|trim|true|truncate|trusted|type|'
             r'uncommitted|under|unencrypted|union|unique|unknown|unlisten|'
             r'unnamed|unnest|until|update|upper|usage|user|'
             r'user_defined_type_catalog|user_defined_type_name|'
             r'user_defined_type_schema|using|vacuum|valid|validator|values|'
             r'variable|verbose|version|view|volatile|when|whenever|where|'
             r'with|without|work|write|year|zone|'
             r')\b', Keyword),

            (r'('
             r'ARRAY|BIGINT|BINARY|BIT|BLOB|BOOLEAN|CHAR|CHARACTER|DATE|'
             r'DEC|DECIMAL|FLOAT|INT|INTEGER|INTERVAL|NUMBER|NUMERIC|REAL|'
             r'SERIAL|SMALLINT|VARCHAR|VARYING|INT8|SERIAL8|TEXT|'
             r'array|bigint|binary|bit|blob|boolean|char|character|date|'
             r'dec|decimal|float|int|integer|interval|number|numeric|real|'
             r'serial|smallint|varchar|varying|int8|serial8|text|'
             r')\b',Name.Builtin),
            (r'[+*/<>=~!@#%^&|`?-]', Operator),
            (r'[0-9]+', Number.Integer),
            # TODO: Backslash escapes?
            (r"'(''|[^'])*'", String.Single),
            (r'"(""|[^"])*"', String.Symbol), # not a real string literal in ANSI SQL
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),
            (r'[;:()\[\],\.]', Punctuation)
        ],
        'multiline-comments': [
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^/\*]+', Comment.Multiline),
            (r'[/*]', Comment.Multiline)
        ]
    }


