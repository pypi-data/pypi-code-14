# Generated from sdpl.g4 by ANTLR 4.5.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .sdplParser import sdplParser
else:
    from sdplParser import sdplParser

# This class defines a complete listener for a parse tree produced by sdplParser.
class sdplListener(ParseTreeListener):

    # Enter a parse tree produced by sdplParser#startrule.
    def enterStartrule(self, ctx:sdplParser.StartruleContext):
        pass

    # Exit a parse tree produced by sdplParser#startrule.
    def exitStartrule(self, ctx:sdplParser.StartruleContext):
        pass


    # Enter a parse tree produced by sdplParser#libDecl.
    def enterLibDecl(self, ctx:sdplParser.LibDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#libDecl.
    def exitLibDecl(self, ctx:sdplParser.LibDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#relationDecl.
    def enterRelationDecl(self, ctx:sdplParser.RelationDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#relationDecl.
    def exitRelationDecl(self, ctx:sdplParser.RelationDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#projectionDecl.
    def enterProjectionDecl(self, ctx:sdplParser.ProjectionDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#projectionDecl.
    def exitProjectionDecl(self, ctx:sdplParser.ProjectionDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#schemaFields.
    def enterSchemaFields(self, ctx:sdplParser.SchemaFieldsContext):
        pass

    # Exit a parse tree produced by sdplParser#schemaFields.
    def exitSchemaFields(self, ctx:sdplParser.SchemaFieldsContext):
        pass


    # Enter a parse tree produced by sdplParser#schemaField.
    def enterSchemaField(self, ctx:sdplParser.SchemaFieldContext):
        pass

    # Exit a parse tree produced by sdplParser#schemaField.
    def exitSchemaField(self, ctx:sdplParser.SchemaFieldContext):
        pass


    # Enter a parse tree produced by sdplParser#expandSchema.
    def enterExpandSchema(self, ctx:sdplParser.ExpandSchemaContext):
        pass

    # Exit a parse tree produced by sdplParser#expandSchema.
    def exitExpandSchema(self, ctx:sdplParser.ExpandSchemaContext):
        pass


    # Enter a parse tree produced by sdplParser#storeDecl.
    def enterStoreDecl(self, ctx:sdplParser.StoreDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#storeDecl.
    def exitStoreDecl(self, ctx:sdplParser.StoreDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#storeSchemaDecl.
    def enterStoreSchemaDecl(self, ctx:sdplParser.StoreSchemaDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#storeSchemaDecl.
    def exitStoreSchemaDecl(self, ctx:sdplParser.StoreSchemaDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#joinDecl.
    def enterJoinDecl(self, ctx:sdplParser.JoinDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#joinDecl.
    def exitJoinDecl(self, ctx:sdplParser.JoinDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#joinElement.
    def enterJoinElement(self, ctx:sdplParser.JoinElementContext):
        pass

    # Exit a parse tree produced by sdplParser#joinElement.
    def exitJoinElement(self, ctx:sdplParser.JoinElementContext):
        pass


    # Enter a parse tree produced by sdplParser#relationColumns.
    def enterRelationColumns(self, ctx:sdplParser.RelationColumnsContext):
        pass

    # Exit a parse tree produced by sdplParser#relationColumns.
    def exitRelationColumns(self, ctx:sdplParser.RelationColumnsContext):
        pass


    # Enter a parse tree produced by sdplParser#relationColumn.
    def enterRelationColumn(self, ctx:sdplParser.RelationColumnContext):
        pass

    # Exit a parse tree produced by sdplParser#relationColumn.
    def exitRelationColumn(self, ctx:sdplParser.RelationColumnContext):
        pass


    # Enter a parse tree produced by sdplParser#filterDecl.
    def enterFilterDecl(self, ctx:sdplParser.FilterDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#filterDecl.
    def exitFilterDecl(self, ctx:sdplParser.FilterDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#filterExpression.
    def enterFilterExpression(self, ctx:sdplParser.FilterExpressionContext):
        pass

    # Exit a parse tree produced by sdplParser#filterExpression.
    def exitFilterExpression(self, ctx:sdplParser.FilterExpressionContext):
        pass


    # Enter a parse tree produced by sdplParser#filterOperation.
    def enterFilterOperation(self, ctx:sdplParser.FilterOperationContext):
        pass

    # Exit a parse tree produced by sdplParser#filterOperation.
    def exitFilterOperation(self, ctx:sdplParser.FilterOperationContext):
        pass


    # Enter a parse tree produced by sdplParser#filterOperand.
    def enterFilterOperand(self, ctx:sdplParser.FilterOperandContext):
        pass

    # Exit a parse tree produced by sdplParser#filterOperand.
    def exitFilterOperand(self, ctx:sdplParser.FilterOperandContext):
        pass


    # Enter a parse tree produced by sdplParser#orderByDecl.
    def enterOrderByDecl(self, ctx:sdplParser.OrderByDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#orderByDecl.
    def exitOrderByDecl(self, ctx:sdplParser.OrderByDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#groupByDecl.
    def enterGroupByDecl(self, ctx:sdplParser.GroupByDeclContext):
        pass

    # Exit a parse tree produced by sdplParser#groupByDecl.
    def exitGroupByDecl(self, ctx:sdplParser.GroupByDeclContext):
        pass


    # Enter a parse tree produced by sdplParser#quotedString.
    def enterQuotedString(self, ctx:sdplParser.QuotedStringContext):
        pass

    # Exit a parse tree produced by sdplParser#quotedString.
    def exitQuotedString(self, ctx:sdplParser.QuotedStringContext):
        pass


    # Enter a parse tree produced by sdplParser#quotedCode.
    def enterQuotedCode(self, ctx:sdplParser.QuotedCodeContext):
        pass

    # Exit a parse tree produced by sdplParser#quotedCode.
    def exitQuotedCode(self, ctx:sdplParser.QuotedCodeContext):
        pass


    # Enter a parse tree produced by sdplParser#compOperator.
    def enterCompOperator(self, ctx:sdplParser.CompOperatorContext):
        pass

    # Exit a parse tree produced by sdplParser#compOperator.
    def exitCompOperator(self, ctx:sdplParser.CompOperatorContext):
        pass


