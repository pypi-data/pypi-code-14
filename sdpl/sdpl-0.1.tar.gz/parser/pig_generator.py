__author__ = 'Bohdan Mushkevych'

from io import TextIOWrapper
from antlr4 import *

import schema.io
from grammar.sdplListener import sdplListener
from grammar.sdplParser import sdplParser
from parser.relation import Relation
from parser.data_source import DataSource
from parser.data_sink import DataSink
from parser.projection import RelationProjection
from parser.decorator import print_comments
from parser.pig_schema import parse_datasink, parse_datasource, parse_schema


class PigGenerator(sdplListener):
    def __init__(self, token_stream: CommonTokenStream, output_stream: TextIOWrapper):
        super().__init__()
        self.token_stream = token_stream
        self.output_stream = output_stream

        # format: {name: Relation}
        self.relations = dict()

    def _out(self, text):
        self.output_stream.write(text)
        self.output_stream.write('\n')

    def _out_bypass_parser(self, ctx: ParserRuleContext):
        """ prints user input *as-is*: retaining all formatting, spaces, special symbols, etc """
        start_index = ctx.start.tokenIndex
        stop_index = ctx.stop.tokenIndex
        user_text = self.token_stream.getText(interval=(start_index, stop_index))
        self._out(user_text)

    @print_comments('--')
    def exitLibDecl(self, ctx: sdplParser.LibDeclContext):
        # REGISTER quotedString (AS ID )? ;
        # 0        1             2  3
        path_child = ctx.getChild(1)      # library path: QuotedStringContext

        if ctx.getChildCount() > 3:
            # read out the AS ID part
            library_alias = ctx.getChild(3)
            self._out('REGISTER {0} AS {1};'.format(path_child.getText(), library_alias.getText()))
        else:
            self._out('REGISTER {0};'.format(path_child.getText()))

    @print_comments('--')
    def exitRelationDecl(self, ctx: sdplParser.RelationDeclContext):
        relation_name = ctx.getChild(0).getText()
        if ctx.getChild(3).getText() == 'TABLE':
            # ID = LOAD TABLE ... FROM ... WITH SCHEMA ... VERSION ... ;
            # 0  1 2    3     4   5    6   7    8      9   10      11
            table_name = ctx.getChild(4).getText()
            repo_path = ctx.getChild(6).getText()
            schema_path = ctx.getChild(9).getText()
            version = ctx.getChild(11).getText()
            relation = Relation(relation_name, schema_path, version)
            self.relations[relation_name] = relation

            # NOTICE: all LOAD specifics are handled by `DataSource` instance
            data_source = DataSource(table_name, repo_path, relation)
            self._out("{0} = {1};".format(relation_name, parse_datasource(data_source)))
        elif ctx.getChild(3).getText() == 'SCHEMA':
            # ID = LOAD SCHEMA ... VERSION ... ;
            # 0  1 2    3      4   5       6
            schema_path = ctx.getChild(4).getText()
            version = ctx.getChild(6).getText()
            self.relations[relation_name] = Relation(relation_name, schema_path, version)
        else:
            ctx_children = [ctx.getChild(i).getText() for i in range(4)]
            clause = ' '.join(ctx_children)
            raise UserWarning('Unknown clause {0}. Expecting either LOAD SCHEMA ... or LOAD TABLE ...'
                              .format(clause))

    def parse_schema_projection(self, relation_name, schema_fields: list)->RelationProjection:
        """ method is the heart of the Schema Projection functionality:
            it reads the input, produces projected `Relation`
            and enlists it into the `self.relations` - list of known relations """
        projection = RelationProjection(self.relations)
        for ctx_schema_field in schema_fields:
            assert isinstance(ctx_schema_field, sdplParser.SchemaFieldContext)
            if ctx_schema_field.getChildCount() <= 4:
                # `B.bbb` or `-B.bbb` format
                schema_field = ctx_schema_field.getText()
                schema_name, field_name = schema_field.split('.')
                as_field_name = field_name
            else:
                # `B.bbb AS ccc` format
                schema_field = ''.join(f.getText() for f in ctx_schema_field.children[:-2])
                schema_name, field_name = schema_field.split('.')
                as_field_name = ctx_schema_field.children[-1].getText()  # last list element carries new field name

            do_subtract = schema_field.startswith('-')
            schema_name = schema_name.lstrip('-')

            if field_name == '*':
                if do_subtract:
                    # `B.*` format
                    projection.remove_all(schema_name)
                else:
                    # `-B.*` format
                    projection.add_all(schema_name)
            else:
                if do_subtract:
                    projection.remove(schema_name, field_name)
                else:
                    projection.add(schema_name, field_name, as_field_name)

        self.relations[relation_name] = projection.finalize_relation(relation_name)
        return projection

    @print_comments('--')
    def exitProjectionDecl(self, ctx: sdplParser.ProjectionDeclContext):
        # ID = SCHEMA PROJECTION ( schemaFields ) ;
        # schemaFields:  schemaField (',' schemaField)* ;
        # schemaField :  ('-')? ID '.' ( ID | '*') ('AS' ID)? ;
        relation_name = ctx.getChild(0).getText()
        ctx_schema_fields = ctx.getTypedRuleContexts(sdplParser.SchemaFieldsContext)
        ctx_schema_fields = ctx_schema_fields[0]    # only one block of schema fields is expected

        schema_fields = ctx_schema_fields.getTypedRuleContexts(sdplParser.SchemaFieldContext)
        self.parse_schema_projection(relation_name, schema_fields)

    @print_comments('--')
    def exitExpandSchema(self, ctx:sdplParser.ExpandSchemaContext):
        # EXPAND SCHEMA ID ;
        # 0      1      2
        relation_name = ctx.getChild(2).getText()
        referenced_schema = self.relations[relation_name].schema
        self._out('-- autocode: expanding relation {0} schema'.format(relation_name))
        self._out(parse_schema(referenced_schema))

    @print_comments('--')
    def exitStoreDecl(self, ctx: sdplParser.StoreDeclContext):
        # STORE ID INTO TABLE quotedString FROM quotedString ;
        # 0     1  2    3     4            5    6
        relation_name = ctx.getChild(1).getText()
        table_name = ctx.getChild(4).getText()
        repo_path = ctx.getChild(6).getText()
        relation = self.relations[relation_name]
        data_sink = DataSink(table_name, repo_path, relation)
        self._out(parse_datasink(data_sink))

    @print_comments('--')
    def exitStoreSchemaDecl(self, ctx: sdplParser.StoreSchemaDeclContext):
        # STORE SCHEMA ID INTO quotedString;
        # 0     1      2  3    4
        relation_name = ctx.getChild(2).getText()
        schema_path = ctx.getChild(4).getText()
        referenced_schema = self.relations[relation_name].schema
        schema.io.store(referenced_schema, schema_path)

    @print_comments('--')
    def exitJoinDecl(self, ctx: sdplParser.JoinDeclContext):
        # ID = JOIN joinElement (, joinElement)+ WITH SCHEMA PROJECTION ( schemaFields );
        # 0  1 2    3            4+
        # joinElement     :  ID 'BY' (relationColumn | relationColumns) ;
        # relationColumns :  '(' relationColumn (',' relationColumn)* ')' ;
        # relationColumn  :  ID ('.' ID) ;

        # step 1: Generate JOIN as JOIN_SA_SB_..._SZ
        relation_name = ctx.getChild(0).getText()
        ctx_join_elements = ctx.getTypedRuleContexts(sdplParser.JoinElementContext)

        join_name = 'JOIN'
        join_body = ''
        for ctx_join_element in ctx_join_elements:
            assert isinstance(ctx_join_element, sdplParser.JoinElementContext)
            element_id = ctx_join_element.getChild(0).getText()
            join_name += '_' + element_id.upper()

            if not join_body:
                # this is the first cycle of the loop
                join_body = 'JOIN {0} BY '.format(element_id)
            else:
                join_body += ', {0} BY '.format(element_id)

            ctx_columns = ctx_join_element.getTypedRuleContexts(sdplParser.RelationColumnsContext)
            ctx_columns = ctx_columns[0]  # only one block of relation columns is expected
            join_body += ctx_columns.getText()

        self._out('{0} = {1} ;'.format(join_name, join_body))

        # step 2: perform schema projection
        ctx_schema_fields = ctx.getTypedRuleContexts(sdplParser.SchemaFieldsContext)
        ctx_schema_fields = ctx_schema_fields[0]    # only one block of schema fields is expected

        schema_fields = ctx_schema_fields.getTypedRuleContexts(sdplParser.SchemaFieldContext)
        projection = self.parse_schema_projection(relation_name, schema_fields)

        # step 3: expand schema with FOREACH ... GENERATE
        self._out('{0} = FOREACH {1} GENERATE'.format(relation_name, join_name))
        output = ',\n    '.join([str(f) for f in projection.fields])
        self._out('    ' + output)
        self._out(';')

    @print_comments('--')
    def exitFilterDecl(self, ctx: sdplParser.FilterDeclContext):
        # ID = FILTER ID BY filterExpression ;
        # 0  1 2      3  4  5
        relation_name = ctx.getChild(0).getText()
        source_relation_name = ctx.getChild(3).getText()
        self.relations[relation_name] = self.relations[source_relation_name]
        self._out_bypass_parser(ctx)

    @print_comments('--')
    def exitOrderByDecl(self, ctx: sdplParser.OrderByDeclContext):
        # ID = ORDER ID BY relationColumn (, relationColumn)* ;
        # 0  1 2     3  4  5               6+
        relation_name = ctx.getChild(0).getText()
        source_relation_name = ctx.getChild(3).getText()
        self.relations[relation_name] = self.relations[source_relation_name]
        self._out_bypass_parser(ctx)

    @print_comments('--')
    def exitGroupByDecl(self, ctx: sdplParser.GroupByDeclContext):
        # ID = GROUP ID BY relationColumn (, relationColumn)* ;
        # 0  1 2     3  4  5               6+
        relation_name = ctx.getChild(0).getText()
        source_relation_name = ctx.getChild(3).getText()
        self.relations[relation_name] = self.relations[source_relation_name]
        self._out_bypass_parser(ctx)

    @print_comments('--')
    def exitQuotedCode(self, ctx:sdplParser.QuotedCodeContext):
        # QUOTE_DELIM .*? QUOTE_DELIM ;
        ctx.start = ctx.children[1].symbol  # skipping starting QUOTE_DELIM
        ctx.stop = ctx.children[-2].symbol  # skipping closing QUOTE_DELIM
        self._out('-- quoted source code: start')
        self._out_bypass_parser(ctx)
        self._out('-- quoted source code: finish')
