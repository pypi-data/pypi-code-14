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
        buf.write(u".\u014c\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4")
        buf.write(u"\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r")
        buf.write(u"\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22")
        buf.write(u"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4")
        buf.write(u"\30\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35")
        buf.write(u"\t\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4")
        buf.write(u"$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t")
        buf.write(u",\4-\t-\4.\t.\4/\t/\4\60\t\60\3\2\3\2\3\2\3\2\3\3\3\3")
        buf.write(u"\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5")
        buf.write(u"\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write(u"\3\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\n\3\n")
        buf.write(u"\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3")
        buf.write(u"\r\6\r\u009c\n\r\r\r\16\r\u009d\3\16\7\16\u00a1\n\16")
        buf.write(u"\f\16\16\16\u00a4\13\16\3\16\5\16\u00a7\n\16\3\16\6\16")
        buf.write(u"\u00aa\n\16\r\16\16\16\u00ab\3\16\3\16\5\16\u00b0\n\16")
        buf.write(u"\3\16\6\16\u00b3\n\16\r\16\16\16\u00b4\5\16\u00b7\n\16")
        buf.write(u"\3\17\3\17\3\17\7\17\u00bc\n\17\f\17\16\17\u00bf\13\17")
        buf.write(u"\3\17\3\17\3\17\3\17\7\17\u00c5\n\17\f\17\16\17\u00c8")
        buf.write(u"\13\17\3\17\5\17\u00cb\n\17\3\20\3\20\3\20\3\20\3\20")
        buf.write(u"\3\20\3\20\3\20\5\20\u00d5\n\20\3\21\3\21\3\21\3\22\3")
        buf.write(u"\22\3\22\3\23\3\23\3\23\3\24\3\24\3\24\3\25\3\25\3\26")
        buf.write(u"\3\26\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\31\3\31\3")
        buf.write(u"\31\3\31\3\32\3\32\3\32\3\33\3\33\7\33\u00f7\n\33\f\33")
        buf.write(u"\16\33\u00fa\13\33\3\34\3\34\3\34\3\35\3\35\3\35\3\36")
        buf.write(u"\3\36\3\37\3\37\3 \3 \3!\3!\3\"\3\"\3#\3#\3$\3$\3%\3")
        buf.write(u"%\3&\3&\3\'\3\'\3(\3(\3)\3)\3)\3*\3*\3+\3+\3,\3,\3,\5")
        buf.write(u",\u0122\n,\3,\3,\5,\u0126\n,\3,\5,\u0129\n,\5,\u012b")
        buf.write(u"\n,\3,\3,\3-\6-\u0130\n-\r-\16-\u0131\3.\3.\3.\5.\u0137")
        buf.write(u"\n.\3.\3.\3/\3/\7/\u013d\n/\f/\16/\u0140\13/\3\60\3\60")
        buf.write(u"\5\60\u0144\n\60\3\60\5\60\u0147\n\60\3\60\3\60\5\60")
        buf.write(u"\u014b\n\60\2\2\61\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n")
        buf.write(u"\23\13\25\f\27\r\31\16\33\17\35\20\37\2!\21#\22%\23\'")
        buf.write(u"\24)\25+\26-\27/\30\61\31\63\32\65\33\67\349\35;\36=")
        buf.write(u"\37? A!C\"E#G$I%K&M\'O(Q)S*U+W,Y\2[-]._\2\3\2\16\3\2")
        buf.write(u"\62;\4\2GGgg\4\2--//\6\2\f\f\17\17))^^\6\2\f\f\17\17")
        buf.write(u"$$^^\n\2$$))^^ddhhppttvv\3\2\62\65\3\2\629\5\2C\\aac")
        buf.write(u"|\6\2\62;C\\aac|\4\2\13\13\"\"\4\2\f\f\17\17\u0163\2")
        buf.write(u"\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3")
        buf.write(u"\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2")
        buf.write(u"\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write(u"\2\2\2\35\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write(u"\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2")
        buf.write(u"\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2")
        buf.write(u"\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2")
        buf.write(u"\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3")
        buf.write(u"\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2")
        buf.write(u"U\3\2\2\2\2W\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\3a\3\2\2\2")
        buf.write(u"\5e\3\2\2\2\7l\3\2\2\2\tq\3\2\2\2\13x\3\2\2\2\r{\3\2")
        buf.write(u"\2\2\17\u0082\3\2\2\2\21\u0087\3\2\2\2\23\u008c\3\2\2")
        buf.write(u"\2\25\u0092\3\2\2\2\27\u0095\3\2\2\2\31\u009b\3\2\2\2")
        buf.write(u"\33\u00a2\3\2\2\2\35\u00ca\3\2\2\2\37\u00cc\3\2\2\2!")
        buf.write(u"\u00d6\3\2\2\2#\u00d9\3\2\2\2%\u00dc\3\2\2\2\'\u00df")
        buf.write(u"\3\2\2\2)\u00e2\3\2\2\2+\u00e4\3\2\2\2-\u00e6\3\2\2\2")
        buf.write(u"/\u00e9\3\2\2\2\61\u00ed\3\2\2\2\63\u00f1\3\2\2\2\65")
        buf.write(u"\u00f4\3\2\2\2\67\u00fb\3\2\2\29\u00fe\3\2\2\2;\u0101")
        buf.write(u"\3\2\2\2=\u0103\3\2\2\2?\u0105\3\2\2\2A\u0107\3\2\2\2")
        buf.write(u"C\u0109\3\2\2\2E\u010b\3\2\2\2G\u010d\3\2\2\2I\u010f")
        buf.write(u"\3\2\2\2K\u0111\3\2\2\2M\u0113\3\2\2\2O\u0115\3\2\2\2")
        buf.write(u"Q\u0117\3\2\2\2S\u011a\3\2\2\2U\u011c\3\2\2\2W\u012a")
        buf.write(u"\3\2\2\2Y\u012f\3\2\2\2[\u0136\3\2\2\2]\u013a\3\2\2\2")
        buf.write(u"_\u0141\3\2\2\2ab\7f\2\2bc\7g\2\2cd\7h\2\2d\4\3\2\2\2")
        buf.write(u"ef\7t\2\2fg\7g\2\2gh\7v\2\2hi\7w\2\2ij\7t\2\2jk\7p\2")
        buf.write(u"\2k\6\3\2\2\2lm\7h\2\2mn\7t\2\2no\7q\2\2op\7o\2\2p\b")
        buf.write(u"\3\2\2\2qr\7k\2\2rs\7o\2\2st\7r\2\2tu\7q\2\2uv\7t\2\2")
        buf.write(u"vw\7v\2\2w\n\3\2\2\2xy\7c\2\2yz\7u\2\2z\f\3\2\2\2{|\7")
        buf.write(u"n\2\2|}\7c\2\2}~\7o\2\2~\177\7d\2\2\177\u0080\7f\2\2")
        buf.write(u"\u0080\u0081\7c\2\2\u0081\16\3\2\2\2\u0082\u0083\7P\2")
        buf.write(u"\2\u0083\u0084\7q\2\2\u0084\u0085\7p\2\2\u0085\u0086")
        buf.write(u"\7g\2\2\u0086\20\3\2\2\2\u0087\u0088\7V\2\2\u0088\u0089")
        buf.write(u"\7t\2\2\u0089\u008a\7w\2\2\u008a\u008b\7g\2\2\u008b\22")
        buf.write(u"\3\2\2\2\u008c\u008d\7H\2\2\u008d\u008e\7c\2\2\u008e")
        buf.write(u"\u008f\7n\2\2\u008f\u0090\7u\2\2\u0090\u0091\7g\2\2\u0091")
        buf.write(u"\24\3\2\2\2\u0092\u0093\7k\2\2\u0093\u0094\7h\2\2\u0094")
        buf.write(u"\26\3\2\2\2\u0095\u0096\7g\2\2\u0096\u0097\7n\2\2\u0097")
        buf.write(u"\u0098\7u\2\2\u0098\u0099\7g\2\2\u0099\30\3\2\2\2\u009a")
        buf.write(u"\u009c\t\2\2\2\u009b\u009a\3\2\2\2\u009c\u009d\3\2\2")
        buf.write(u"\2\u009d\u009b\3\2\2\2\u009d\u009e\3\2\2\2\u009e\32\3")
        buf.write(u"\2\2\2\u009f\u00a1\t\2\2\2\u00a0\u009f\3\2\2\2\u00a1")
        buf.write(u"\u00a4\3\2\2\2\u00a2\u00a0\3\2\2\2\u00a2\u00a3\3\2\2")
        buf.write(u"\2\u00a3\u00a6\3\2\2\2\u00a4\u00a2\3\2\2\2\u00a5\u00a7")
        buf.write(u"\7\60\2\2\u00a6\u00a5\3\2\2\2\u00a6\u00a7\3\2\2\2\u00a7")
        buf.write(u"\u00a9\3\2\2\2\u00a8\u00aa\t\2\2\2\u00a9\u00a8\3\2\2")
        buf.write(u"\2\u00aa\u00ab\3\2\2\2\u00ab\u00a9\3\2\2\2\u00ab\u00ac")
        buf.write(u"\3\2\2\2\u00ac\u00b6\3\2\2\2\u00ad\u00af\t\3\2\2\u00ae")
        buf.write(u"\u00b0\t\4\2\2\u00af\u00ae\3\2\2\2\u00af\u00b0\3\2\2")
        buf.write(u"\2\u00b0\u00b2\3\2\2\2\u00b1\u00b3\t\2\2\2\u00b2\u00b1")
        buf.write(u"\3\2\2\2\u00b3\u00b4\3\2\2\2\u00b4\u00b2\3\2\2\2\u00b4")
        buf.write(u"\u00b5\3\2\2\2\u00b5\u00b7\3\2\2\2\u00b6\u00ad\3\2\2")
        buf.write(u"\2\u00b6\u00b7\3\2\2\2\u00b7\34\3\2\2\2\u00b8\u00bd\7")
        buf.write(u")\2\2\u00b9\u00bc\5\37\20\2\u00ba\u00bc\n\5\2\2\u00bb")
        buf.write(u"\u00b9\3\2\2\2\u00bb\u00ba\3\2\2\2\u00bc\u00bf\3\2\2")
        buf.write(u"\2\u00bd\u00bb\3\2\2\2\u00bd\u00be\3\2\2\2\u00be\u00c0")
        buf.write(u"\3\2\2\2\u00bf\u00bd\3\2\2\2\u00c0\u00cb\7)\2\2\u00c1")
        buf.write(u"\u00c6\7$\2\2\u00c2\u00c5\5\37\20\2\u00c3\u00c5\n\6\2")
        buf.write(u"\2\u00c4\u00c2\3\2\2\2\u00c4\u00c3\3\2\2\2\u00c5\u00c8")
        buf.write(u"\3\2\2\2\u00c6\u00c4\3\2\2\2\u00c6\u00c7\3\2\2\2\u00c7")
        buf.write(u"\u00c9\3\2\2\2\u00c8\u00c6\3\2\2\2\u00c9\u00cb\7$\2\2")
        buf.write(u"\u00ca\u00b8\3\2\2\2\u00ca\u00c1\3\2\2\2\u00cb\36\3\2")
        buf.write(u"\2\2\u00cc\u00d4\7^\2\2\u00cd\u00d5\t\7\2\2\u00ce\u00cf")
        buf.write(u"\t\b\2\2\u00cf\u00d0\t\t\2\2\u00d0\u00d5\t\t\2\2\u00d1")
        buf.write(u"\u00d2\t\t\2\2\u00d2\u00d5\t\t\2\2\u00d3\u00d5\t\t\2")
        buf.write(u"\2\u00d4\u00cd\3\2\2\2\u00d4\u00ce\3\2\2\2\u00d4\u00d1")
        buf.write(u"\3\2\2\2\u00d4\u00d3\3\2\2\2\u00d5 \3\2\2\2\u00d6\u00d7")
        buf.write(u"\7>\2\2\u00d7\u00d8\7?\2\2\u00d8\"\3\2\2\2\u00d9\u00da")
        buf.write(u"\7@\2\2\u00da\u00db\7?\2\2\u00db$\3\2\2\2\u00dc\u00dd")
        buf.write(u"\7?\2\2\u00dd\u00de\7?\2\2\u00de&\3\2\2\2\u00df\u00e0")
        buf.write(u"\7#\2\2\u00e0\u00e1\7?\2\2\u00e1(\3\2\2\2\u00e2\u00e3")
        buf.write(u"\7>\2\2\u00e3*\3\2\2\2\u00e4\u00e5\7@\2\2\u00e5,\3\2")
        buf.write(u"\2\2\u00e6\u00e7\7q\2\2\u00e7\u00e8\7t\2\2\u00e8.\3\2")
        buf.write(u"\2\2\u00e9\u00ea\7c\2\2\u00ea\u00eb\7p\2\2\u00eb\u00ec")
        buf.write(u"\7f\2\2\u00ec\60\3\2\2\2\u00ed\u00ee\7p\2\2\u00ee\u00ef")
        buf.write(u"\7q\2\2\u00ef\u00f0\7v\2\2\u00f0\62\3\2\2\2\u00f1\u00f2")
        buf.write(u"\7k\2\2\u00f2\u00f3\7u\2\2\u00f3\64\3\2\2\2\u00f4\u00f8")
        buf.write(u"\t\n\2\2\u00f5\u00f7\t\13\2\2\u00f6\u00f5\3\2\2\2\u00f7")
        buf.write(u"\u00fa\3\2\2\2\u00f8\u00f6\3\2\2\2\u00f8\u00f9\3\2\2")
        buf.write(u"\2\u00f9\66\3\2\2\2\u00fa\u00f8\3\2\2\2\u00fb\u00fc\7")
        buf.write(u"*\2\2\u00fc\u00fd\b\34\2\2\u00fd8\3\2\2\2\u00fe\u00ff")
        buf.write(u"\7+\2\2\u00ff\u0100\b\35\3\2\u0100:\3\2\2\2\u0101\u0102")
        buf.write(u"\7]\2\2\u0102<\3\2\2\2\u0103\u0104\7_\2\2\u0104>\3\2")
        buf.write(u"\2\2\u0105\u0106\7}\2\2\u0106@\3\2\2\2\u0107\u0108\7")
        buf.write(u"\177\2\2\u0108B\3\2\2\2\u0109\u010a\7.\2\2\u010aD\3\2")
        buf.write(u"\2\2\u010b\u010c\7=\2\2\u010cF\3\2\2\2\u010d\u010e\7")
        buf.write(u"<\2\2\u010eH\3\2\2\2\u010f\u0110\7-\2\2\u0110J\3\2\2")
        buf.write(u"\2\u0111\u0112\7/\2\2\u0112L\3\2\2\2\u0113\u0114\7,\2")
        buf.write(u"\2\u0114N\3\2\2\2\u0115\u0116\7\61\2\2\u0116P\3\2\2\2")
        buf.write(u"\u0117\u0118\7,\2\2\u0118\u0119\7,\2\2\u0119R\3\2\2\2")
        buf.write(u"\u011a\u011b\7?\2\2\u011bT\3\2\2\2\u011c\u011d\7\60\2")
        buf.write(u"\2\u011dV\3\2\2\2\u011e\u011f\6,\2\2\u011f\u012b\5Y-")
        buf.write(u"\2\u0120\u0122\7\17\2\2\u0121\u0120\3\2\2\2\u0121\u0122")
        buf.write(u"\3\2\2\2\u0122\u0123\3\2\2\2\u0123\u0126\7\f\2\2\u0124")
        buf.write(u"\u0126\7\17\2\2\u0125\u0121\3\2\2\2\u0125\u0124\3\2\2")
        buf.write(u"\2\u0126\u0128\3\2\2\2\u0127\u0129\5Y-\2\u0128\u0127")
        buf.write(u"\3\2\2\2\u0128\u0129\3\2\2\2\u0129\u012b\3\2\2\2\u012a")
        buf.write(u"\u011e\3\2\2\2\u012a\u0125\3\2\2\2\u012b\u012c\3\2\2")
        buf.write(u"\2\u012c\u012d\b,\4\2\u012dX\3\2\2\2\u012e\u0130\t\f")
        buf.write(u"\2\2\u012f\u012e\3\2\2\2\u0130\u0131\3\2\2\2\u0131\u012f")
        buf.write(u"\3\2\2\2\u0131\u0132\3\2\2\2\u0132Z\3\2\2\2\u0133\u0137")
        buf.write(u"\5Y-\2\u0134\u0137\5]/\2\u0135\u0137\5_\60\2\u0136\u0133")
        buf.write(u"\3\2\2\2\u0136\u0134\3\2\2\2\u0136\u0135\3\2\2\2\u0137")
        buf.write(u"\u0138\3\2\2\2\u0138\u0139\b.\5\2\u0139\\\3\2\2\2\u013a")
        buf.write(u"\u013e\7%\2\2\u013b\u013d\n\r\2\2\u013c\u013b\3\2\2\2")
        buf.write(u"\u013d\u0140\3\2\2\2\u013e\u013c\3\2\2\2\u013e\u013f")
        buf.write(u"\3\2\2\2\u013f^\3\2\2\2\u0140\u013e\3\2\2\2\u0141\u0143")
        buf.write(u"\7^\2\2\u0142\u0144\5Y-\2\u0143\u0142\3\2\2\2\u0143\u0144")
        buf.write(u"\3\2\2\2\u0144\u014a\3\2\2\2\u0145\u0147\7\17\2\2\u0146")
        buf.write(u"\u0145\3\2\2\2\u0146\u0147\3\2\2\2\u0147\u0148\3\2\2")
        buf.write(u"\2\u0148\u014b\7\f\2\2\u0149\u014b\7\17\2\2\u014a\u0146")
        buf.write(u"\3\2\2\2\u014a\u0149\3\2\2\2\u014b`\3\2\2\2\33\2\u009d")
        buf.write(u"\u00a2\u00a6\u00ab\u00af\u00b4\u00b6\u00bb\u00bd\u00c4")
        buf.write(u"\u00c6\u00ca\u00d4\u00f8\u0121\u0125\u0128\u012a\u0131")
        buf.write(u"\u0136\u013e\u0143\u0146\u014a\6\3\34\2\3\35\3\3,\4\b")
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
    IS = 24
    ID = 25
    OPEN_PAREN = 26
    CLOSE_PAREN = 27
    LSQUARE = 28
    RSQUARE = 29
    LBRACE = 30
    RBRACE = 31
    COMMA = 32
    SEMICOLON = 33
    COLON = 34
    PLUS = 35
    MINUS = 36
    MUL = 37
    DIV = 38
    POW = 39
    BINDING = 40
    DOT = 41
    NEWLINE = 42
    SKIP_ = 43
    COMMENT = 44

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'def'", u"'return'", u"'from'", u"'import'", u"'as'", u"'lambda'", 
            u"'None'", u"'True'", u"'False'", u"'if'", u"'else'", u"'<='", 
            u"'>='", u"'=='", u"'!='", u"'<'", u"'>'", u"'or'", u"'and'", 
            u"'not'", u"'is'", u"'('", u"')'", u"'['", u"']'", u"'{'", u"'}'", 
            u"','", u"';'", u"':'", u"'+'", u"'-'", u"'*'", u"'/'", u"'**'", 
            u"'='", u"'.'" ]

    symbolicNames = [ u"<INVALID>",
            u"DEF", u"RETURN", u"FROM", u"IMPORT", u"AS", u"LAMBDA", u"NONE", 
            u"TRUE", u"FALSE", u"IF", u"ELSE", u"INT", u"FLOAT", u"STRING", 
            u"LE", u"GE", u"EQ", u"NE", u"LT", u"GT", u"OR", u"AND", u"NOT", 
            u"IS", u"ID", u"OPEN_PAREN", u"CLOSE_PAREN", u"LSQUARE", u"RSQUARE", 
            u"LBRACE", u"RBRACE", u"COMMA", u"SEMICOLON", u"COLON", u"PLUS", 
            u"MINUS", u"MUL", u"DIV", u"POW", u"BINDING", u"DOT", u"NEWLINE", 
            u"SKIP_", u"COMMENT" ]

    ruleNames = [ u"DEF", u"RETURN", u"FROM", u"IMPORT", u"AS", u"LAMBDA", 
                  u"NONE", u"TRUE", u"FALSE", u"IF", u"ELSE", u"INT", u"FLOAT", 
                  u"STRING", u"ESCAPE_SEQ", u"LE", u"GE", u"EQ", u"NE", 
                  u"LT", u"GT", u"OR", u"AND", u"NOT", u"IS", u"ID", u"OPEN_PAREN", 
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
    		actions[26] = self.OPEN_PAREN_action 
    		actions[27] = self.CLOSE_PAREN_action 
    		actions[42] = self.NEWLINE_action 
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
            preds[42] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.atStartOfInput()
         


