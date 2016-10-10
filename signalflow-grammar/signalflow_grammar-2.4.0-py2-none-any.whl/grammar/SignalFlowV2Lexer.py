# Generated from grammar/SignalFlowV2Lexer.g4 by ANTLR 4.5.2
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO


import re
from SignalFlowV2Parser import SignalFlowV2Parser
from antlr4.Token import CommonToken


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2")
        buf.write(u"-\u0147\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4")
        buf.write(u"\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r")
        buf.write(u"\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22")
        buf.write(u"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4")
        buf.write(u"\30\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35")
        buf.write(u"\t\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4")
        buf.write(u"$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t")
        buf.write(u",\4-\t-\4.\t.\4/\t/\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3")
        buf.write(u"\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3")
        buf.write(u"\5\3\5\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3")
        buf.write(u"\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3")
        buf.write(u"\n\3\n\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\r\6\r\u009a")
        buf.write(u"\n\r\r\r\16\r\u009b\3\16\7\16\u009f\n\16\f\16\16\16\u00a2")
        buf.write(u"\13\16\3\16\5\16\u00a5\n\16\3\16\6\16\u00a8\n\16\r\16")
        buf.write(u"\16\16\u00a9\3\16\3\16\5\16\u00ae\n\16\3\16\6\16\u00b1")
        buf.write(u"\n\16\r\16\16\16\u00b2\5\16\u00b5\n\16\3\17\3\17\3\17")
        buf.write(u"\7\17\u00ba\n\17\f\17\16\17\u00bd\13\17\3\17\3\17\3\17")
        buf.write(u"\3\17\7\17\u00c3\n\17\f\17\16\17\u00c6\13\17\3\17\5\17")
        buf.write(u"\u00c9\n\17\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\5")
        buf.write(u"\20\u00d3\n\20\3\21\3\21\3\21\3\22\3\22\3\22\3\23\3\23")
        buf.write(u"\3\23\3\24\3\24\3\24\3\25\3\25\3\26\3\26\3\27\3\27\3")
        buf.write(u"\27\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\31\3\32\3\32")
        buf.write(u"\7\32\u00f2\n\32\f\32\16\32\u00f5\13\32\3\33\3\33\3\33")
        buf.write(u"\3\34\3\34\3\34\3\35\3\35\3\36\3\36\3\37\3\37\3 \3 \3")
        buf.write(u"!\3!\3\"\3\"\3#\3#\3$\3$\3%\3%\3&\3&\3\'\3\'\3(\3(\3")
        buf.write(u"(\3)\3)\3*\3*\3+\3+\3+\5+\u011d\n+\3+\3+\5+\u0121\n+")
        buf.write(u"\3+\5+\u0124\n+\5+\u0126\n+\3+\3+\3,\6,\u012b\n,\r,\16")
        buf.write(u",\u012c\3-\3-\3-\5-\u0132\n-\3-\3-\3.\3.\7.\u0138\n.")
        buf.write(u"\f.\16.\u013b\13.\3/\3/\5/\u013f\n/\3/\5/\u0142\n/\3")
        buf.write(u"/\3/\5/\u0146\n/\2\2\60\3\3\5\4\7\5\t\6\13\7\r\b\17\t")
        buf.write(u"\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\2!\21#\22")
        buf.write(u"%\23\'\24)\25+\26-\27/\30\61\31\63\32\65\33\67\349\35")
        buf.write(u";\36=\37? A!C\"E#G$I%K&M\'O(Q)S*U+W\2Y,[-]\2\3\2\16\3")
        buf.write(u"\2\62;\4\2GGgg\4\2--//\6\2\f\f\17\17))^^\6\2\f\f\17\17")
        buf.write(u"$$^^\n\2$$))^^ddhhppttvv\3\2\62\65\3\2\629\5\2C\\aac")
        buf.write(u"|\6\2\62;C\\aac|\4\2\13\13\"\"\4\2\f\f\17\17\u015e\2")
        buf.write(u"\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3")
        buf.write(u"\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2")
        buf.write(u"\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write(u"\2\2\2\35\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write(u"\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2")
        buf.write(u"\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2")
        buf.write(u"\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2")
        buf.write(u"\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3")
        buf.write(u"\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2")
        buf.write(u"U\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\3_\3\2\2\2\5c\3\2\2\2")
        buf.write(u"\7j\3\2\2\2\to\3\2\2\2\13v\3\2\2\2\ry\3\2\2\2\17\u0080")
        buf.write(u"\3\2\2\2\21\u0085\3\2\2\2\23\u008a\3\2\2\2\25\u0090\3")
        buf.write(u"\2\2\2\27\u0093\3\2\2\2\31\u0099\3\2\2\2\33\u00a0\3\2")
        buf.write(u"\2\2\35\u00c8\3\2\2\2\37\u00ca\3\2\2\2!\u00d4\3\2\2\2")
        buf.write(u"#\u00d7\3\2\2\2%\u00da\3\2\2\2\'\u00dd\3\2\2\2)\u00e0")
        buf.write(u"\3\2\2\2+\u00e2\3\2\2\2-\u00e4\3\2\2\2/\u00e7\3\2\2\2")
        buf.write(u"\61\u00eb\3\2\2\2\63\u00ef\3\2\2\2\65\u00f6\3\2\2\2\67")
        buf.write(u"\u00f9\3\2\2\29\u00fc\3\2\2\2;\u00fe\3\2\2\2=\u0100\3")
        buf.write(u"\2\2\2?\u0102\3\2\2\2A\u0104\3\2\2\2C\u0106\3\2\2\2E")
        buf.write(u"\u0108\3\2\2\2G\u010a\3\2\2\2I\u010c\3\2\2\2K\u010e\3")
        buf.write(u"\2\2\2M\u0110\3\2\2\2O\u0112\3\2\2\2Q\u0115\3\2\2\2S")
        buf.write(u"\u0117\3\2\2\2U\u0125\3\2\2\2W\u012a\3\2\2\2Y\u0131\3")
        buf.write(u"\2\2\2[\u0135\3\2\2\2]\u013c\3\2\2\2_`\7f\2\2`a\7g\2")
        buf.write(u"\2ab\7h\2\2b\4\3\2\2\2cd\7t\2\2de\7g\2\2ef\7v\2\2fg\7")
        buf.write(u"w\2\2gh\7t\2\2hi\7p\2\2i\6\3\2\2\2jk\7h\2\2kl\7t\2\2")
        buf.write(u"lm\7q\2\2mn\7o\2\2n\b\3\2\2\2op\7k\2\2pq\7o\2\2qr\7r")
        buf.write(u"\2\2rs\7q\2\2st\7t\2\2tu\7v\2\2u\n\3\2\2\2vw\7c\2\2w")
        buf.write(u"x\7u\2\2x\f\3\2\2\2yz\7n\2\2z{\7c\2\2{|\7o\2\2|}\7d\2")
        buf.write(u"\2}~\7f\2\2~\177\7c\2\2\177\16\3\2\2\2\u0080\u0081\7")
        buf.write(u"P\2\2\u0081\u0082\7q\2\2\u0082\u0083\7p\2\2\u0083\u0084")
        buf.write(u"\7g\2\2\u0084\20\3\2\2\2\u0085\u0086\7V\2\2\u0086\u0087")
        buf.write(u"\7t\2\2\u0087\u0088\7w\2\2\u0088\u0089\7g\2\2\u0089\22")
        buf.write(u"\3\2\2\2\u008a\u008b\7H\2\2\u008b\u008c\7c\2\2\u008c")
        buf.write(u"\u008d\7n\2\2\u008d\u008e\7u\2\2\u008e\u008f\7g\2\2\u008f")
        buf.write(u"\24\3\2\2\2\u0090\u0091\7k\2\2\u0091\u0092\7h\2\2\u0092")
        buf.write(u"\26\3\2\2\2\u0093\u0094\7g\2\2\u0094\u0095\7n\2\2\u0095")
        buf.write(u"\u0096\7u\2\2\u0096\u0097\7g\2\2\u0097\30\3\2\2\2\u0098")
        buf.write(u"\u009a\t\2\2\2\u0099\u0098\3\2\2\2\u009a\u009b\3\2\2")
        buf.write(u"\2\u009b\u0099\3\2\2\2\u009b\u009c\3\2\2\2\u009c\32\3")
        buf.write(u"\2\2\2\u009d\u009f\t\2\2\2\u009e\u009d\3\2\2\2\u009f")
        buf.write(u"\u00a2\3\2\2\2\u00a0\u009e\3\2\2\2\u00a0\u00a1\3\2\2")
        buf.write(u"\2\u00a1\u00a4\3\2\2\2\u00a2\u00a0\3\2\2\2\u00a3\u00a5")
        buf.write(u"\7\60\2\2\u00a4\u00a3\3\2\2\2\u00a4\u00a5\3\2\2\2\u00a5")
        buf.write(u"\u00a7\3\2\2\2\u00a6\u00a8\t\2\2\2\u00a7\u00a6\3\2\2")
        buf.write(u"\2\u00a8\u00a9\3\2\2\2\u00a9\u00a7\3\2\2\2\u00a9\u00aa")
        buf.write(u"\3\2\2\2\u00aa\u00b4\3\2\2\2\u00ab\u00ad\t\3\2\2\u00ac")
        buf.write(u"\u00ae\t\4\2\2\u00ad\u00ac\3\2\2\2\u00ad\u00ae\3\2\2")
        buf.write(u"\2\u00ae\u00b0\3\2\2\2\u00af\u00b1\t\2\2\2\u00b0\u00af")
        buf.write(u"\3\2\2\2\u00b1\u00b2\3\2\2\2\u00b2\u00b0\3\2\2\2\u00b2")
        buf.write(u"\u00b3\3\2\2\2\u00b3\u00b5\3\2\2\2\u00b4\u00ab\3\2\2")
        buf.write(u"\2\u00b4\u00b5\3\2\2\2\u00b5\34\3\2\2\2\u00b6\u00bb\7")
        buf.write(u")\2\2\u00b7\u00ba\5\37\20\2\u00b8\u00ba\n\5\2\2\u00b9")
        buf.write(u"\u00b7\3\2\2\2\u00b9\u00b8\3\2\2\2\u00ba\u00bd\3\2\2")
        buf.write(u"\2\u00bb\u00b9\3\2\2\2\u00bb\u00bc\3\2\2\2\u00bc\u00be")
        buf.write(u"\3\2\2\2\u00bd\u00bb\3\2\2\2\u00be\u00c9\7)\2\2\u00bf")
        buf.write(u"\u00c4\7$\2\2\u00c0\u00c3\5\37\20\2\u00c1\u00c3\n\6\2")
        buf.write(u"\2\u00c2\u00c0\3\2\2\2\u00c2\u00c1\3\2\2\2\u00c3\u00c6")
        buf.write(u"\3\2\2\2\u00c4\u00c2\3\2\2\2\u00c4\u00c5\3\2\2\2\u00c5")
        buf.write(u"\u00c7\3\2\2\2\u00c6\u00c4\3\2\2\2\u00c7\u00c9\7$\2\2")
        buf.write(u"\u00c8\u00b6\3\2\2\2\u00c8\u00bf\3\2\2\2\u00c9\36\3\2")
        buf.write(u"\2\2\u00ca\u00d2\7^\2\2\u00cb\u00d3\t\7\2\2\u00cc\u00cd")
        buf.write(u"\t\b\2\2\u00cd\u00ce\t\t\2\2\u00ce\u00d3\t\t\2\2\u00cf")
        buf.write(u"\u00d0\t\t\2\2\u00d0\u00d3\t\t\2\2\u00d1\u00d3\t\t\2")
        buf.write(u"\2\u00d2\u00cb\3\2\2\2\u00d2\u00cc\3\2\2\2\u00d2\u00cf")
        buf.write(u"\3\2\2\2\u00d2\u00d1\3\2\2\2\u00d3 \3\2\2\2\u00d4\u00d5")
        buf.write(u"\7>\2\2\u00d5\u00d6\7?\2\2\u00d6\"\3\2\2\2\u00d7\u00d8")
        buf.write(u"\7@\2\2\u00d8\u00d9\7?\2\2\u00d9$\3\2\2\2\u00da\u00db")
        buf.write(u"\7?\2\2\u00db\u00dc\7?\2\2\u00dc&\3\2\2\2\u00dd\u00de")
        buf.write(u"\7#\2\2\u00de\u00df\7?\2\2\u00df(\3\2\2\2\u00e0\u00e1")
        buf.write(u"\7>\2\2\u00e1*\3\2\2\2\u00e2\u00e3\7@\2\2\u00e3,\3\2")
        buf.write(u"\2\2\u00e4\u00e5\7q\2\2\u00e5\u00e6\7t\2\2\u00e6.\3\2")
        buf.write(u"\2\2\u00e7\u00e8\7c\2\2\u00e8\u00e9\7p\2\2\u00e9\u00ea")
        buf.write(u"\7f\2\2\u00ea\60\3\2\2\2\u00eb\u00ec\7p\2\2\u00ec\u00ed")
        buf.write(u"\7q\2\2\u00ed\u00ee\7v\2\2\u00ee\62\3\2\2\2\u00ef\u00f3")
        buf.write(u"\t\n\2\2\u00f0\u00f2\t\13\2\2\u00f1\u00f0\3\2\2\2\u00f2")
        buf.write(u"\u00f5\3\2\2\2\u00f3\u00f1\3\2\2\2\u00f3\u00f4\3\2\2")
        buf.write(u"\2\u00f4\64\3\2\2\2\u00f5\u00f3\3\2\2\2\u00f6\u00f7\7")
        buf.write(u"*\2\2\u00f7\u00f8\b\33\2\2\u00f8\66\3\2\2\2\u00f9\u00fa")
        buf.write(u"\7+\2\2\u00fa\u00fb\b\34\3\2\u00fb8\3\2\2\2\u00fc\u00fd")
        buf.write(u"\7]\2\2\u00fd:\3\2\2\2\u00fe\u00ff\7_\2\2\u00ff<\3\2")
        buf.write(u"\2\2\u0100\u0101\7}\2\2\u0101>\3\2\2\2\u0102\u0103\7")
        buf.write(u"\177\2\2\u0103@\3\2\2\2\u0104\u0105\7.\2\2\u0105B\3\2")
        buf.write(u"\2\2\u0106\u0107\7=\2\2\u0107D\3\2\2\2\u0108\u0109\7")
        buf.write(u"<\2\2\u0109F\3\2\2\2\u010a\u010b\7-\2\2\u010bH\3\2\2")
        buf.write(u"\2\u010c\u010d\7/\2\2\u010dJ\3\2\2\2\u010e\u010f\7,\2")
        buf.write(u"\2\u010fL\3\2\2\2\u0110\u0111\7\61\2\2\u0111N\3\2\2\2")
        buf.write(u"\u0112\u0113\7,\2\2\u0113\u0114\7,\2\2\u0114P\3\2\2\2")
        buf.write(u"\u0115\u0116\7?\2\2\u0116R\3\2\2\2\u0117\u0118\7\60\2")
        buf.write(u"\2\u0118T\3\2\2\2\u0119\u011a\6+\2\2\u011a\u0126\5W,")
        buf.write(u"\2\u011b\u011d\7\17\2\2\u011c\u011b\3\2\2\2\u011c\u011d")
        buf.write(u"\3\2\2\2\u011d\u011e\3\2\2\2\u011e\u0121\7\f\2\2\u011f")
        buf.write(u"\u0121\7\17\2\2\u0120\u011c\3\2\2\2\u0120\u011f\3\2\2")
        buf.write(u"\2\u0121\u0123\3\2\2\2\u0122\u0124\5W,\2\u0123\u0122")
        buf.write(u"\3\2\2\2\u0123\u0124\3\2\2\2\u0124\u0126\3\2\2\2\u0125")
        buf.write(u"\u0119\3\2\2\2\u0125\u0120\3\2\2\2\u0126\u0127\3\2\2")
        buf.write(u"\2\u0127\u0128\b+\4\2\u0128V\3\2\2\2\u0129\u012b\t\f")
        buf.write(u"\2\2\u012a\u0129\3\2\2\2\u012b\u012c\3\2\2\2\u012c\u012a")
        buf.write(u"\3\2\2\2\u012c\u012d\3\2\2\2\u012dX\3\2\2\2\u012e\u0132")
        buf.write(u"\5W,\2\u012f\u0132\5[.\2\u0130\u0132\5]/\2\u0131\u012e")
        buf.write(u"\3\2\2\2\u0131\u012f\3\2\2\2\u0131\u0130\3\2\2\2\u0132")
        buf.write(u"\u0133\3\2\2\2\u0133\u0134\b-\5\2\u0134Z\3\2\2\2\u0135")
        buf.write(u"\u0139\7%\2\2\u0136\u0138\n\r\2\2\u0137\u0136\3\2\2\2")
        buf.write(u"\u0138\u013b\3\2\2\2\u0139\u0137\3\2\2\2\u0139\u013a")
        buf.write(u"\3\2\2\2\u013a\\\3\2\2\2\u013b\u0139\3\2\2\2\u013c\u013e")
        buf.write(u"\7^\2\2\u013d\u013f\5W,\2\u013e\u013d\3\2\2\2\u013e\u013f")
        buf.write(u"\3\2\2\2\u013f\u0145\3\2\2\2\u0140\u0142\7\17\2\2\u0141")
        buf.write(u"\u0140\3\2\2\2\u0141\u0142\3\2\2\2\u0142\u0143\3\2\2")
        buf.write(u"\2\u0143\u0146\7\f\2\2\u0144\u0146\7\17\2\2\u0145\u0141")
        buf.write(u"\3\2\2\2\u0145\u0144\3\2\2\2\u0146^\3\2\2\2\33\2\u009b")
        buf.write(u"\u00a0\u00a4\u00a9\u00ad\u00b2\u00b4\u00b9\u00bb\u00c2")
        buf.write(u"\u00c4\u00c8\u00d2\u00f3\u011c\u0120\u0123\u0125\u012c")
        buf.write(u"\u0131\u0139\u013e\u0141\u0145\6\3\33\2\3\34\3\3+\4\b")
        buf.write(u"\2\2")
        return buf.getvalue()


class SignalFlowV2Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    DEF = 1
    RETURN = 2
    FROM = 3
    IMPORT = 4
    AS = 5
    LAMBDA = 6
    NONE = 7
    TRUE = 8
    FALSE = 9
    IF = 10
    ELSE = 11
    INT = 12
    FLOAT = 13
    STRING = 14
    LE = 15
    GE = 16
    EQ = 17
    NE = 18
    LT = 19
    GT = 20
    OR = 21
    AND = 22
    NOT = 23
    ID = 24
    OPEN_PAREN = 25
    CLOSE_PAREN = 26
    LSQUARE = 27
    RSQUARE = 28
    LBRACE = 29
    RBRACE = 30
    COMMA = 31
    SEMICOLON = 32
    COLON = 33
    PLUS = 34
    MINUS = 35
    MUL = 36
    DIV = 37
    POW = 38
    BINDING = 39
    DOT = 40
    NEWLINE = 41
    SKIP_ = 42
    COMMENT = 43

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'def'", u"'return'", u"'from'", u"'import'", u"'as'", u"'lambda'", 
            u"'None'", u"'True'", u"'False'", u"'if'", u"'else'", u"'<='", 
            u"'>='", u"'=='", u"'!='", u"'<'", u"'>'", u"'or'", u"'and'", 
            u"'not'", u"'('", u"')'", u"'['", u"']'", u"'{'", u"'}'", u"','", 
            u"';'", u"':'", u"'+'", u"'-'", u"'*'", u"'/'", u"'**'", u"'='", 
            u"'.'" ]

    symbolicNames = [ u"<INVALID>",
            u"DEF", u"RETURN", u"FROM", u"IMPORT", u"AS", u"LAMBDA", u"NONE", 
            u"TRUE", u"FALSE", u"IF", u"ELSE", u"INT", u"FLOAT", u"STRING", 
            u"LE", u"GE", u"EQ", u"NE", u"LT", u"GT", u"OR", u"AND", u"NOT", 
            u"ID", u"OPEN_PAREN", u"CLOSE_PAREN", u"LSQUARE", u"RSQUARE", 
            u"LBRACE", u"RBRACE", u"COMMA", u"SEMICOLON", u"COLON", u"PLUS", 
            u"MINUS", u"MUL", u"DIV", u"POW", u"BINDING", u"DOT", u"NEWLINE", 
            u"SKIP_", u"COMMENT" ]

    ruleNames = [ u"DEF", u"RETURN", u"FROM", u"IMPORT", u"AS", u"LAMBDA", 
                  u"NONE", u"TRUE", u"FALSE", u"IF", u"ELSE", u"INT", u"FLOAT", 
                  u"STRING", u"ESCAPE_SEQ", u"LE", u"GE", u"EQ", u"NE", 
                  u"LT", u"GT", u"OR", u"AND", u"NOT", u"ID", u"OPEN_PAREN", 
                  u"CLOSE_PAREN", u"LSQUARE", u"RSQUARE", u"LBRACE", u"RBRACE", 
                  u"COMMA", u"SEMICOLON", u"COLON", u"PLUS", u"MINUS", u"MUL", 
                  u"DIV", u"POW", u"BINDING", u"DOT", u"NEWLINE", u"SPACES", 
                  u"SKIP_", u"COMMENT", u"LINE_JOINING" ]

    grammarFileName = u"SignalFlowV2Lexer.g4"

    def __init__(self, input=None):
        super(SignalFlowV2Lexer, self).__init__(input)
        self.checkVersion("4.5.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


        # A queue where extra tokens are pushed on (see the NEWLINE lexer rule).
        self.tokens = []

        # The stack that keeps track of the indentation level.
        self.indents = []

        # The amount of opened braces, brackets and parenthesis.
        self.opened = 0

        # The most recently produced token.
        self.lastToken = None

    def emitToken(self, t):
        self._token = t
        self.tokens.append(t)

    def nextToken(self):
        # Check if the end-of-file is ahead and there are still some DEDENTS expected.
        if self._input.LA(1) == SignalFlowV2Parser.EOF and self.indents:

            # Remove any trailing EOF tokens from our buffer.
            for i in range(len(self.tokens) -1, -1, -1):
                if (self.tokens[i].type == SignalFlowV2Parser.EOF):
                    del self.tokens[i]

            # First emit an extra line break that serves as the end of the statement.
            self.emitToken(self.commonToken(SignalFlowV2Parser.NEWLINE, "\n"))

            # Now emit as many DEDENT tokens as needed.
            while self.indents:
                self.emitToken(self.createDedent());
                self.indents.pop()

            # Put the EOF back on the token stream.
            self.emitToken(self.commonToken(SignalFlowV2Parser.EOF, "<EOF>"))

        next = Lexer.nextToken(self)

        if next.channel == Token.DEFAULT_CHANNEL:
            # Keep track of the last token on the default channel.
            self.lastToken = next

        return next if not self.tokens else self.tokens.pop(0)

    def createDedent(self):
        dedent = self.commonToken(SignalFlowV2Parser.DEDENT, "")
        dedent.line = self.lastToken.line
        return dedent

    def commonToken(self, type, text):
        stop = self.getCharIndex() - 1
        start = stop if not text else stop - len(text) + 1
        return CommonToken(self._tokenFactorySourcePair, type, self.DEFAULT_TOKEN_CHANNEL, start, stop)

    ## Calculates the indentation of the provided whiteSpace, taking the
    ## following rules into account:
    ##
    ## "Tabs are replaced (from left to right) by one to eight spaces
    ##  such that the total number of characters up to and including
    ##  the replacement is a multiple of eight [...]"
    ##
    ##  -- https://docs.python.org/3.1/reference/lexical_analysis.html#indentation
    @staticmethod
    def getIndentationCount(whiteSpace):
        count = 0;
        for ch in whiteSpace:
            if '\t' == ch:
                count += 8 - (count % 8)
            else:
                count += 1
        return count

    def atStartOfInput(self):
        return self.column == 0 and self.line == 1


    def action(self, localctx, ruleIndex, actionIndex):
    	if self._actions is None:
    		actions = dict()
    		actions[25] = self.OPEN_PAREN_action 
    		actions[26] = self.CLOSE_PAREN_action 
    		actions[41] = self.NEWLINE_action 
    		self._actions = actions
    	action = self._actions.get(ruleIndex, None)
    	if action is not None:
    		action(localctx, actionIndex)
    	else:
    		raise Exception("No registered action for:" + str(ruleIndex))

    def OPEN_PAREN_action(self, localctx , actionIndex):
        if actionIndex == 0:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx , actionIndex):
        if actionIndex == 1:
            self.opened -= 1
     

    def NEWLINE_action(self, localctx , actionIndex):
        if actionIndex == 2:

            newLine = re.sub("[^\r\n]+", "", self.text)
            whiteSpaces = re.sub("[\r\n]+", "", self.text)
            next = self._input.LA(1)
            if self.opened > 0 or next == '\r' or next == '\n' or next == '#':
                # If we are inside a list or on a blank line, ignore all indents,
                # dedents and line breaks.
                self.skip()
            else:
                self.emitToken(self.commonToken(SignalFlowV2Lexer.NEWLINE, newLine));
                indent = SignalFlowV2Lexer.getIndentationCount(whiteSpaces);
                previous = 0 if not self.indents else self.indents[-1]
                if indent == previous:
                    # skip indents of the same size as the present indent-size
                    self.skip()

                elif indent > previous:
                    self.indents.append(indent)
                    self.emitToken(self.commonToken(SignalFlowV2Parser.INDENT, whiteSpaces))
                else:
                    # Possibly emit more than 1 DEDENT token.
                    while self.indents and self.indents[-1] > indent:
                        self.emitToken(self.createDedent())
                        self.indents.pop()
                
     

    def sempred(self, localctx, ruleIndex, predIndex):
        if self._predicates is None:
            preds = dict()
            preds[41] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.atStartOfInput()
         


