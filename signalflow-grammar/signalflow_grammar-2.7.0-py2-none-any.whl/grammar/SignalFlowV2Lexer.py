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
        buf.write(u"D\u01f3\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4")
        buf.write(u"\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r")
        buf.write(u"\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22")
        buf.write(u"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4")
        buf.write(u"\30\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35")
        buf.write(u"\t\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4")
        buf.write(u"$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t")
        buf.write(u",\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63")
        buf.write(u"\t\63\4\64\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\4")
        buf.write(u"9\t9\4:\t:\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA")
        buf.write(u"\4B\tB\4C\tC\4D\tD\4E\tE\4F\tF\3\2\3\2\3\2\3\2\3\3\3")
        buf.write(u"\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3")
        buf.write(u"\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3")
        buf.write(u"\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3")
        buf.write(u"\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13")
        buf.write(u"\3\13\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\16\3")
        buf.write(u"\16\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\20\3\20")
        buf.write(u"\3\20\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3")
        buf.write(u"\22\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\24\3\24\3\24")
        buf.write(u"\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\25\3\25\3")
        buf.write(u"\25\3\26\3\26\3\26\3\27\3\27\3\27\3\27\3\30\3\30\3\30")
        buf.write(u"\3\30\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\33\3")
        buf.write(u"\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34\3\34\3\35")
        buf.write(u"\3\35\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3")
        buf.write(u"\36\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3 \3!\3!\3!\3!\3")
        buf.write(u"!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3\"\3#\3#\3#\5#\u0143")
        buf.write(u"\n#\3#\3#\5#\u0147\n#\3#\5#\u014a\n#\5#\u014c\n#\3#\3")
        buf.write(u"#\3$\3$\7$\u0152\n$\f$\16$\u0155\13$\3%\3%\3%\7%\u015a")
        buf.write(u"\n%\f%\16%\u015d\13%\3%\3%\3%\3%\7%\u0163\n%\f%\16%\u0166")
        buf.write(u"\13%\3%\5%\u0169\n%\3&\6&\u016c\n&\r&\16&\u016d\3\'\7")
        buf.write(u"\'\u0171\n\'\f\'\16\'\u0174\13\'\3\'\5\'\u0177\n\'\3")
        buf.write(u"\'\6\'\u017a\n\'\r\'\16\'\u017b\3\'\3\'\5\'\u0180\n\'")
        buf.write(u"\3\'\6\'\u0183\n\'\r\'\16\'\u0184\5\'\u0187\n\'\3(\3")
        buf.write(u"(\3(\3(\3(\3(\3(\3(\5(\u0191\n(\3)\3)\3*\3*\3*\3*\3+")
        buf.write(u"\3+\3,\3,\3,\3-\3-\3-\3.\3.\3/\3/\3\60\3\60\3\61\3\61")
        buf.write(u"\3\61\3\62\3\62\3\63\3\63\3\63\3\64\3\64\3\64\3\65\3")
        buf.write(u"\65\3\66\3\66\3\67\3\67\38\38\38\39\39\39\3:\3:\3;\3")
        buf.write(u";\3<\3<\3<\3=\3=\3=\3>\3>\3>\3?\3?\3?\3@\3@\3@\3A\3A")
        buf.write(u"\3B\3B\3B\3C\6C\u01d7\nC\rC\16C\u01d8\3D\3D\3D\5D\u01de")
        buf.write(u"\nD\3D\3D\3E\3E\7E\u01e4\nE\fE\16E\u01e7\13E\3F\3F\5")
        buf.write(u"F\u01eb\nF\3F\5F\u01ee\nF\3F\3F\5F\u01f2\nF\2\2G\3\3")
        buf.write(u"\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16")
        buf.write(u"\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61")
        buf.write(u"\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O\2")
        buf.write(u"Q)S*U+W,Y-[.]/_\60a\61c\62e\63g\64i\65k\66m\67o8q9s:")
        buf.write(u"u;w<y={>}?\177@\u0081A\u0083B\u0085\2\u0087C\u0089D\u008b")
        buf.write(u"\2\3\2\16\5\2C\\aac|\6\2\62;C\\aac|\6\2\f\f\17\17))^")
        buf.write(u"^\6\2\f\f\17\17$$^^\3\2\62;\4\2GGgg\4\2--//\n\2$$))^")
        buf.write(u"^ddhhppttvv\3\2\62\65\3\2\629\4\2\13\13\"\"\4\2\f\f\17")
        buf.write(u"\17\u020a\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2")
        buf.write(u"\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2")
        buf.write(u"\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2")
        buf.write(u"\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2")
        buf.write(u"\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2")
        buf.write(u"\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2")
        buf.write(u"\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3")
        buf.write(u"\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2")
        buf.write(u"G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2Q\3\2\2\2")
        buf.write(u"\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2")
        buf.write(u"\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2")
        buf.write(u"\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3")
        buf.write(u"\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2")
        buf.write(u"y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081")
        buf.write(u"\3\2\2\2\2\u0083\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2")
        buf.write(u"\2\2\3\u008d\3\2\2\2\5\u0091\3\2\2\2\7\u0098\3\2\2\2")
        buf.write(u"\t\u009e\3\2\2\2\13\u00a3\3\2\2\2\r\u00aa\3\2\2\2\17")
        buf.write(u"\u00ad\3\2\2\2\21\u00b4\3\2\2\2\23\u00bd\3\2\2\2\25\u00c4")
        buf.write(u"\3\2\2\2\27\u00c7\3\2\2\2\31\u00cc\3\2\2\2\33\u00d1\3")
        buf.write(u"\2\2\2\35\u00d7\3\2\2\2\37\u00db\3\2\2\2!\u00de\3\2\2")
        buf.write(u"\2#\u00e2\3\2\2\2%\u00ea\3\2\2\2\'\u00ef\3\2\2\2)\u00f6")
        buf.write(u"\3\2\2\2+\u00fd\3\2\2\2-\u0100\3\2\2\2/\u0104\3\2\2\2")
        buf.write(u"\61\u0108\3\2\2\2\63\u010b\3\2\2\2\65\u0110\3\2\2\2\67")
        buf.write(u"\u0115\3\2\2\29\u011b\3\2\2\2;\u0121\3\2\2\2=\u0127\3")
        buf.write(u"\2\2\2?\u012b\3\2\2\2A\u0130\3\2\2\2C\u0139\3\2\2\2E")
        buf.write(u"\u014b\3\2\2\2G\u014f\3\2\2\2I\u0168\3\2\2\2K\u016b\3")
        buf.write(u"\2\2\2M\u0172\3\2\2\2O\u0188\3\2\2\2Q\u0192\3\2\2\2S")
        buf.write(u"\u0194\3\2\2\2U\u0198\3\2\2\2W\u019a\3\2\2\2Y\u019d\3")
        buf.write(u"\2\2\2[\u01a0\3\2\2\2]\u01a2\3\2\2\2_\u01a4\3\2\2\2a")
        buf.write(u"\u01a6\3\2\2\2c\u01a9\3\2\2\2e\u01ab\3\2\2\2g\u01ae\3")
        buf.write(u"\2\2\2i\u01b1\3\2\2\2k\u01b3\3\2\2\2m\u01b5\3\2\2\2o")
        buf.write(u"\u01b7\3\2\2\2q\u01ba\3\2\2\2s\u01bd\3\2\2\2u\u01bf\3")
        buf.write(u"\2\2\2w\u01c1\3\2\2\2y\u01c4\3\2\2\2{\u01c7\3\2\2\2}")
        buf.write(u"\u01ca\3\2\2\2\177\u01cd\3\2\2\2\u0081\u01d0\3\2\2\2")
        buf.write(u"\u0083\u01d2\3\2\2\2\u0085\u01d6\3\2\2\2\u0087\u01dd")
        buf.write(u"\3\2\2\2\u0089\u01e1\3\2\2\2\u008b\u01e8\3\2\2\2\u008d")
        buf.write(u"\u008e\7f\2\2\u008e\u008f\7g\2\2\u008f\u0090\7h\2\2\u0090")
        buf.write(u"\4\3\2\2\2\u0091\u0092\7t\2\2\u0092\u0093\7g\2\2\u0093")
        buf.write(u"\u0094\7v\2\2\u0094\u0095\7w\2\2\u0095\u0096\7t\2\2\u0096")
        buf.write(u"\u0097\7p\2\2\u0097\6\3\2\2\2\u0098\u0099\7t\2\2\u0099")
        buf.write(u"\u009a\7c\2\2\u009a\u009b\7k\2\2\u009b\u009c\7u\2\2\u009c")
        buf.write(u"\u009d\7g\2\2\u009d\b\3\2\2\2\u009e\u009f\7h\2\2\u009f")
        buf.write(u"\u00a0\7t\2\2\u00a0\u00a1\7q\2\2\u00a1\u00a2\7o\2\2\u00a2")
        buf.write(u"\n\3\2\2\2\u00a3\u00a4\7k\2\2\u00a4\u00a5\7o\2\2\u00a5")
        buf.write(u"\u00a6\7r\2\2\u00a6\u00a7\7q\2\2\u00a7\u00a8\7t\2\2\u00a8")
        buf.write(u"\u00a9\7v\2\2\u00a9\f\3\2\2\2\u00aa\u00ab\7c\2\2\u00ab")
        buf.write(u"\u00ac\7u\2\2\u00ac\16\3\2\2\2\u00ad\u00ae\7i\2\2\u00ae")
        buf.write(u"\u00af\7n\2\2\u00af\u00b0\7q\2\2\u00b0\u00b1\7d\2\2\u00b1")
        buf.write(u"\u00b2\7c\2\2\u00b2\u00b3\7n\2\2\u00b3\20\3\2\2\2\u00b4")
        buf.write(u"\u00b5\7p\2\2\u00b5\u00b6\7q\2\2\u00b6\u00b7\7p\2\2\u00b7")
        buf.write(u"\u00b8\7n\2\2\u00b8\u00b9\7q\2\2\u00b9\u00ba\7e\2\2\u00ba")
        buf.write(u"\u00bb\7c\2\2\u00bb\u00bc\7n\2\2\u00bc\22\3\2\2\2\u00bd")
        buf.write(u"\u00be\7c\2\2\u00be\u00bf\7u\2\2\u00bf\u00c0\7u\2\2\u00c0")
        buf.write(u"\u00c1\7g\2\2\u00c1\u00c2\7t\2\2\u00c2\u00c3\7v\2\2\u00c3")
        buf.write(u"\24\3\2\2\2\u00c4\u00c5\7k\2\2\u00c5\u00c6\7h\2\2\u00c6")
        buf.write(u"\26\3\2\2\2\u00c7\u00c8\7g\2\2\u00c8\u00c9\7n\2\2\u00c9")
        buf.write(u"\u00ca\7k\2\2\u00ca\u00cb\7h\2\2\u00cb\30\3\2\2\2\u00cc")
        buf.write(u"\u00cd\7g\2\2\u00cd\u00ce\7n\2\2\u00ce\u00cf\7u\2\2\u00cf")
        buf.write(u"\u00d0\7g\2\2\u00d0\32\3\2\2\2\u00d1\u00d2\7y\2\2\u00d2")
        buf.write(u"\u00d3\7j\2\2\u00d3\u00d4\7k\2\2\u00d4\u00d5\7n\2\2\u00d5")
        buf.write(u"\u00d6\7g\2\2\u00d6\34\3\2\2\2\u00d7\u00d8\7h\2\2\u00d8")
        buf.write(u"\u00d9\7q\2\2\u00d9\u00da\7t\2\2\u00da\36\3\2\2\2\u00db")
        buf.write(u"\u00dc\7k\2\2\u00dc\u00dd\7p\2\2\u00dd \3\2\2\2\u00de")
        buf.write(u"\u00df\7v\2\2\u00df\u00e0\7t\2\2\u00e0\u00e1\7{\2\2\u00e1")
        buf.write(u"\"\3\2\2\2\u00e2\u00e3\7h\2\2\u00e3\u00e4\7k\2\2\u00e4")
        buf.write(u"\u00e5\7p\2\2\u00e5\u00e6\7c\2\2\u00e6\u00e7\7n\2\2\u00e7")
        buf.write(u"\u00e8\7n\2\2\u00e8\u00e9\7{\2\2\u00e9$\3\2\2\2\u00ea")
        buf.write(u"\u00eb\7y\2\2\u00eb\u00ec\7k\2\2\u00ec\u00ed\7v\2\2\u00ed")
        buf.write(u"\u00ee\7j\2\2\u00ee&\3\2\2\2\u00ef\u00f0\7g\2\2\u00f0")
        buf.write(u"\u00f1\7z\2\2\u00f1\u00f2\7e\2\2\u00f2\u00f3\7g\2\2\u00f3")
        buf.write(u"\u00f4\7r\2\2\u00f4\u00f5\7v\2\2\u00f5(\3\2\2\2\u00f6")
        buf.write(u"\u00f7\7n\2\2\u00f7\u00f8\7c\2\2\u00f8\u00f9\7o\2\2\u00f9")
        buf.write(u"\u00fa\7d\2\2\u00fa\u00fb\7f\2\2\u00fb\u00fc\7c\2\2\u00fc")
        buf.write(u"*\3\2\2\2\u00fd\u00fe\7q\2\2\u00fe\u00ff\7t\2\2\u00ff")
        buf.write(u",\3\2\2\2\u0100\u0101\7c\2\2\u0101\u0102\7p\2\2\u0102")
        buf.write(u"\u0103\7f\2\2\u0103.\3\2\2\2\u0104\u0105\7p\2\2\u0105")
        buf.write(u"\u0106\7q\2\2\u0106\u0107\7v\2\2\u0107\60\3\2\2\2\u0108")
        buf.write(u"\u0109\7k\2\2\u0109\u010a\7u\2\2\u010a\62\3\2\2\2\u010b")
        buf.write(u"\u010c\7P\2\2\u010c\u010d\7q\2\2\u010d\u010e\7p\2\2\u010e")
        buf.write(u"\u010f\7g\2\2\u010f\64\3\2\2\2\u0110\u0111\7V\2\2\u0111")
        buf.write(u"\u0112\7t\2\2\u0112\u0113\7w\2\2\u0113\u0114\7g\2\2\u0114")
        buf.write(u"\66\3\2\2\2\u0115\u0116\7H\2\2\u0116\u0117\7c\2\2\u0117")
        buf.write(u"\u0118\7n\2\2\u0118\u0119\7u\2\2\u0119\u011a\7g\2\2\u011a")
        buf.write(u"8\3\2\2\2\u011b\u011c\7e\2\2\u011c\u011d\7n\2\2\u011d")
        buf.write(u"\u011e\7c\2\2\u011e\u011f\7u\2\2\u011f\u0120\7u\2\2\u0120")
        buf.write(u":\3\2\2\2\u0121\u0122\7{\2\2\u0122\u0123\7k\2\2\u0123")
        buf.write(u"\u0124\7g\2\2\u0124\u0125\7n\2\2\u0125\u0126\7f\2\2\u0126")
        buf.write(u"<\3\2\2\2\u0127\u0128\7f\2\2\u0128\u0129\7g\2\2\u0129")
        buf.write(u"\u012a\7n\2\2\u012a>\3\2\2\2\u012b\u012c\7r\2\2\u012c")
        buf.write(u"\u012d\7c\2\2\u012d\u012e\7u\2\2\u012e\u012f\7u\2\2\u012f")
        buf.write(u"@\3\2\2\2\u0130\u0131\7e\2\2\u0131\u0132\7q\2\2\u0132")
        buf.write(u"\u0133\7p\2\2\u0133\u0134\7v\2\2\u0134\u0135\7k\2\2\u0135")
        buf.write(u"\u0136\7p\2\2\u0136\u0137\7w\2\2\u0137\u0138\7g\2\2\u0138")
        buf.write(u"B\3\2\2\2\u0139\u013a\7d\2\2\u013a\u013b\7t\2\2\u013b")
        buf.write(u"\u013c\7g\2\2\u013c\u013d\7c\2\2\u013d\u013e\7m\2\2\u013e")
        buf.write(u"D\3\2\2\2\u013f\u0140\6#\2\2\u0140\u014c\5\u0085C\2\u0141")
        buf.write(u"\u0143\7\17\2\2\u0142\u0141\3\2\2\2\u0142\u0143\3\2\2")
        buf.write(u"\2\u0143\u0144\3\2\2\2\u0144\u0147\7\f\2\2\u0145\u0147")
        buf.write(u"\7\17\2\2\u0146\u0142\3\2\2\2\u0146\u0145\3\2\2\2\u0147")
        buf.write(u"\u0149\3\2\2\2\u0148\u014a\5\u0085C\2\u0149\u0148\3\2")
        buf.write(u"\2\2\u0149\u014a\3\2\2\2\u014a\u014c\3\2\2\2\u014b\u013f")
        buf.write(u"\3\2\2\2\u014b\u0146\3\2\2\2\u014c\u014d\3\2\2\2\u014d")
        buf.write(u"\u014e\b#\2\2\u014eF\3\2\2\2\u014f\u0153\t\2\2\2\u0150")
        buf.write(u"\u0152\t\3\2\2\u0151\u0150\3\2\2\2\u0152\u0155\3\2\2")
        buf.write(u"\2\u0153\u0151\3\2\2\2\u0153\u0154\3\2\2\2\u0154H\3\2")
        buf.write(u"\2\2\u0155\u0153\3\2\2\2\u0156\u015b\7)\2\2\u0157\u015a")
        buf.write(u"\5O(\2\u0158\u015a\n\4\2\2\u0159\u0157\3\2\2\2\u0159")
        buf.write(u"\u0158\3\2\2\2\u015a\u015d\3\2\2\2\u015b\u0159\3\2\2")
        buf.write(u"\2\u015b\u015c\3\2\2\2\u015c\u015e\3\2\2\2\u015d\u015b")
        buf.write(u"\3\2\2\2\u015e\u0169\7)\2\2\u015f\u0164\7$\2\2\u0160")
        buf.write(u"\u0163\5O(\2\u0161\u0163\n\5\2\2\u0162\u0160\3\2\2\2")
        buf.write(u"\u0162\u0161\3\2\2\2\u0163\u0166\3\2\2\2\u0164\u0162")
        buf.write(u"\3\2\2\2\u0164\u0165\3\2\2\2\u0165\u0167\3\2\2\2\u0166")
        buf.write(u"\u0164\3\2\2\2\u0167\u0169\7$\2\2\u0168\u0156\3\2\2\2")
        buf.write(u"\u0168\u015f\3\2\2\2\u0169J\3\2\2\2\u016a\u016c\t\6\2")
        buf.write(u"\2\u016b\u016a\3\2\2\2\u016c\u016d\3\2\2\2\u016d\u016b")
        buf.write(u"\3\2\2\2\u016d\u016e\3\2\2\2\u016eL\3\2\2\2\u016f\u0171")
        buf.write(u"\t\6\2\2\u0170\u016f\3\2\2\2\u0171\u0174\3\2\2\2\u0172")
        buf.write(u"\u0170\3\2\2\2\u0172\u0173\3\2\2\2\u0173\u0176\3\2\2")
        buf.write(u"\2\u0174\u0172\3\2\2\2\u0175\u0177\7\60\2\2\u0176\u0175")
        buf.write(u"\3\2\2\2\u0176\u0177\3\2\2\2\u0177\u0179\3\2\2\2\u0178")
        buf.write(u"\u017a\t\6\2\2\u0179\u0178\3\2\2\2\u017a\u017b\3\2\2")
        buf.write(u"\2\u017b\u0179\3\2\2\2\u017b\u017c\3\2\2\2\u017c\u0186")
        buf.write(u"\3\2\2\2\u017d\u017f\t\7\2\2\u017e\u0180\t\b\2\2\u017f")
        buf.write(u"\u017e\3\2\2\2\u017f\u0180\3\2\2\2\u0180\u0182\3\2\2")
        buf.write(u"\2\u0181\u0183\t\6\2\2\u0182\u0181\3\2\2\2\u0183\u0184")
        buf.write(u"\3\2\2\2\u0184\u0182\3\2\2\2\u0184\u0185\3\2\2\2\u0185")
        buf.write(u"\u0187\3\2\2\2\u0186\u017d\3\2\2\2\u0186\u0187\3\2\2")
        buf.write(u"\2\u0187N\3\2\2\2\u0188\u0190\7^\2\2\u0189\u0191\t\t")
        buf.write(u"\2\2\u018a\u018b\t\n\2\2\u018b\u018c\t\13\2\2\u018c\u0191")
        buf.write(u"\t\13\2\2\u018d\u018e\t\13\2\2\u018e\u0191\t\13\2\2\u018f")
        buf.write(u"\u0191\t\13\2\2\u0190\u0189\3\2\2\2\u0190\u018a\3\2\2")
        buf.write(u"\2\u0190\u018d\3\2\2\2\u0190\u018f\3\2\2\2\u0191P\3\2")
        buf.write(u"\2\2\u0192\u0193\7\60\2\2\u0193R\3\2\2\2\u0194\u0195")
        buf.write(u"\7\60\2\2\u0195\u0196\7\60\2\2\u0196\u0197\7\60\2\2\u0197")
        buf.write(u"T\3\2\2\2\u0198\u0199\7,\2\2\u0199V\3\2\2\2\u019a\u019b")
        buf.write(u"\7*\2\2\u019b\u019c\b,\3\2\u019cX\3\2\2\2\u019d\u019e")
        buf.write(u"\7+\2\2\u019e\u019f\b-\4\2\u019fZ\3\2\2\2\u01a0\u01a1")
        buf.write(u"\7.\2\2\u01a1\\\3\2\2\2\u01a2\u01a3\7<\2\2\u01a3^\3\2")
        buf.write(u"\2\2\u01a4\u01a5\7=\2\2\u01a5`\3\2\2\2\u01a6\u01a7\7")
        buf.write(u",\2\2\u01a7\u01a8\7,\2\2\u01a8b\3\2\2\2\u01a9\u01aa\7")
        buf.write(u"?\2\2\u01aad\3\2\2\2\u01ab\u01ac\7]\2\2\u01ac\u01ad\b")
        buf.write(u"\63\5\2\u01adf\3\2\2\2\u01ae\u01af\7_\2\2\u01af\u01b0")
        buf.write(u"\b\64\6\2\u01b0h\3\2\2\2\u01b1\u01b2\7-\2\2\u01b2j\3")
        buf.write(u"\2\2\2\u01b3\u01b4\7/\2\2\u01b4l\3\2\2\2\u01b5\u01b6")
        buf.write(u"\7\61\2\2\u01b6n\3\2\2\2\u01b7\u01b8\7}\2\2\u01b8\u01b9")
        buf.write(u"\b8\7\2\u01b9p\3\2\2\2\u01ba\u01bb\7\177\2\2\u01bb\u01bc")
        buf.write(u"\b9\b\2\u01bcr\3\2\2\2\u01bd\u01be\7>\2\2\u01bet\3\2")
        buf.write(u"\2\2\u01bf\u01c0\7@\2\2\u01c0v\3\2\2\2\u01c1\u01c2\7")
        buf.write(u"?\2\2\u01c2\u01c3\7?\2\2\u01c3x\3\2\2\2\u01c4\u01c5\7")
        buf.write(u"@\2\2\u01c5\u01c6\7?\2\2\u01c6z\3\2\2\2\u01c7\u01c8\7")
        buf.write(u">\2\2\u01c8\u01c9\7?\2\2\u01c9|\3\2\2\2\u01ca\u01cb\7")
        buf.write(u">\2\2\u01cb\u01cc\7@\2\2\u01cc~\3\2\2\2\u01cd\u01ce\7")
        buf.write(u"#\2\2\u01ce\u01cf\7?\2\2\u01cf\u0080\3\2\2\2\u01d0\u01d1")
        buf.write(u"\7B\2\2\u01d1\u0082\3\2\2\2\u01d2\u01d3\7/\2\2\u01d3")
        buf.write(u"\u01d4\7@\2\2\u01d4\u0084\3\2\2\2\u01d5\u01d7\t\f\2\2")
        buf.write(u"\u01d6\u01d5\3\2\2\2\u01d7\u01d8\3\2\2\2\u01d8\u01d6")
        buf.write(u"\3\2\2\2\u01d8\u01d9\3\2\2\2\u01d9\u0086\3\2\2\2\u01da")
        buf.write(u"\u01de\5\u0085C\2\u01db\u01de\5\u0089E\2\u01dc\u01de")
        buf.write(u"\5\u008bF\2\u01dd\u01da\3\2\2\2\u01dd\u01db\3\2\2\2\u01dd")
        buf.write(u"\u01dc\3\2\2\2\u01de\u01df\3\2\2\2\u01df\u01e0\bD\t\2")
        buf.write(u"\u01e0\u0088\3\2\2\2\u01e1\u01e5\7%\2\2\u01e2\u01e4\n")
        buf.write(u"\r\2\2\u01e3\u01e2\3\2\2\2\u01e4\u01e7\3\2\2\2\u01e5")
        buf.write(u"\u01e3\3\2\2\2\u01e5\u01e6\3\2\2\2\u01e6\u008a\3\2\2")
        buf.write(u"\2\u01e7\u01e5\3\2\2\2\u01e8\u01ea\7^\2\2\u01e9\u01eb")
        buf.write(u"\5\u0085C\2\u01ea\u01e9\3\2\2\2\u01ea\u01eb\3\2\2\2\u01eb")
        buf.write(u"\u01f1\3\2\2\2\u01ec\u01ee\7\17\2\2\u01ed\u01ec\3\2\2")
        buf.write(u"\2\u01ed\u01ee\3\2\2\2\u01ee\u01ef\3\2\2\2\u01ef\u01f2")
        buf.write(u"\7\f\2\2\u01f0\u01f2\7\17\2\2\u01f1\u01ed\3\2\2\2\u01f1")
        buf.write(u"\u01f0\3\2\2\2\u01f2\u008c\3\2\2\2\33\2\u0142\u0146\u0149")
        buf.write(u"\u014b\u0153\u0159\u015b\u0162\u0164\u0168\u016d\u0172")
        buf.write(u"\u0176\u017b\u017f\u0184\u0186\u0190\u01d8\u01dd\u01e5")
        buf.write(u"\u01ea\u01ed\u01f1\n\3#\2\3,\3\3-\4\3\63\5\3\64\6\38")
        buf.write(u"\7\39\b\b\2\2")
        return buf.getvalue()


class SignalFlowV2Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    DEF = 1
    RETURN = 2
    RAISE = 3
    FROM = 4
    IMPORT = 5
    AS = 6
    GLOBAL = 7
    NONLOCAL = 8
    ASSERT = 9
    IF = 10
    ELIF = 11
    ELSE = 12
    WHILE = 13
    FOR = 14
    IN = 15
    TRY = 16
    FINALLY = 17
    WITH = 18
    EXCEPT = 19
    LAMBDA = 20
    OR = 21
    AND = 22
    NOT = 23
    IS = 24
    NONE = 25
    TRUE = 26
    FALSE = 27
    CLASS = 28
    YIELD = 29
    DEL = 30
    PASS = 31
    CONTINUE = 32
    BREAK = 33
    NEWLINE = 34
    ID = 35
    STRING = 36
    INT = 37
    FLOAT = 38
    DOT = 39
    ELLIPSE = 40
    STAR = 41
    OPEN_PAREN = 42
    CLOSE_PAREN = 43
    COMMA = 44
    COLON = 45
    SEMICOLON = 46
    POWER = 47
    ASSIGN = 48
    OPEN_BRACK = 49
    CLOSE_BRACK = 50
    ADD = 51
    MINUS = 52
    DIV = 53
    OPEN_BRACE = 54
    CLOSE_BRACE = 55
    LESS_THAN = 56
    GREATER_THAN = 57
    EQUALS = 58
    GT_EQ = 59
    LT_EQ = 60
    NOT_EQ_1 = 61
    NOT_EQ_2 = 62
    AT = 63
    ARROW = 64
    SKIP_ = 65
    COMMENT = 66

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'def'", u"'return'", u"'raise'", u"'from'", u"'import'", u"'as'", 
            u"'global'", u"'nonlocal'", u"'assert'", u"'if'", u"'elif'", 
            u"'else'", u"'while'", u"'for'", u"'in'", u"'try'", u"'finally'", 
            u"'with'", u"'except'", u"'lambda'", u"'or'", u"'and'", u"'not'", 
            u"'is'", u"'None'", u"'True'", u"'False'", u"'class'", u"'yield'", 
            u"'del'", u"'pass'", u"'continue'", u"'break'", u"'.'", u"'...'", 
            u"'*'", u"'('", u"')'", u"','", u"':'", u"';'", u"'**'", u"'='", 
            u"'['", u"']'", u"'+'", u"'-'", u"'/'", u"'{'", u"'}'", u"'<'", 
            u"'>'", u"'=='", u"'>='", u"'<='", u"'<>'", u"'!='", u"'@'", 
            u"'->'" ]

    symbolicNames = [ u"<INVALID>",
            u"DEF", u"RETURN", u"RAISE", u"FROM", u"IMPORT", u"AS", u"GLOBAL", 
            u"NONLOCAL", u"ASSERT", u"IF", u"ELIF", u"ELSE", u"WHILE", u"FOR", 
            u"IN", u"TRY", u"FINALLY", u"WITH", u"EXCEPT", u"LAMBDA", u"OR", 
            u"AND", u"NOT", u"IS", u"NONE", u"TRUE", u"FALSE", u"CLASS", 
            u"YIELD", u"DEL", u"PASS", u"CONTINUE", u"BREAK", u"NEWLINE", 
            u"ID", u"STRING", u"INT", u"FLOAT", u"DOT", u"ELLIPSE", u"STAR", 
            u"OPEN_PAREN", u"CLOSE_PAREN", u"COMMA", u"COLON", u"SEMICOLON", 
            u"POWER", u"ASSIGN", u"OPEN_BRACK", u"CLOSE_BRACK", u"ADD", 
            u"MINUS", u"DIV", u"OPEN_BRACE", u"CLOSE_BRACE", u"LESS_THAN", 
            u"GREATER_THAN", u"EQUALS", u"GT_EQ", u"LT_EQ", u"NOT_EQ_1", 
            u"NOT_EQ_2", u"AT", u"ARROW", u"SKIP_", u"COMMENT" ]

    ruleNames = [ u"DEF", u"RETURN", u"RAISE", u"FROM", u"IMPORT", u"AS", 
                  u"GLOBAL", u"NONLOCAL", u"ASSERT", u"IF", u"ELIF", u"ELSE", 
                  u"WHILE", u"FOR", u"IN", u"TRY", u"FINALLY", u"WITH", 
                  u"EXCEPT", u"LAMBDA", u"OR", u"AND", u"NOT", u"IS", u"NONE", 
                  u"TRUE", u"FALSE", u"CLASS", u"YIELD", u"DEL", u"PASS", 
                  u"CONTINUE", u"BREAK", u"NEWLINE", u"ID", u"STRING", u"INT", 
                  u"FLOAT", u"ESCAPE_SEQ", u"DOT", u"ELLIPSE", u"STAR", 
                  u"OPEN_PAREN", u"CLOSE_PAREN", u"COMMA", u"COLON", u"SEMICOLON", 
                  u"POWER", u"ASSIGN", u"OPEN_BRACK", u"CLOSE_BRACK", u"ADD", 
                  u"MINUS", u"DIV", u"OPEN_BRACE", u"CLOSE_BRACE", u"LESS_THAN", 
                  u"GREATER_THAN", u"EQUALS", u"GT_EQ", u"LT_EQ", u"NOT_EQ_1", 
                  u"NOT_EQ_2", u"AT", u"ARROW", u"SPACES", u"SKIP_", u"COMMENT", 
                  u"LINE_JOINING" ]

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
    		actions[33] = self.NEWLINE_action 
    		actions[42] = self.OPEN_PAREN_action 
    		actions[43] = self.CLOSE_PAREN_action 
    		actions[49] = self.OPEN_BRACK_action 
    		actions[50] = self.CLOSE_BRACK_action 
    		actions[54] = self.OPEN_BRACE_action 
    		actions[55] = self.CLOSE_BRACE_action 
    		self._actions = actions
    	action = self._actions.get(ruleIndex, None)
    	if action is not None:
    		action(localctx, actionIndex)
    	else:
    		raise Exception("No registered action for:" + str(ruleIndex))

    def NEWLINE_action(self, localctx , actionIndex):
        if actionIndex == 0:

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
                
     

    def OPEN_PAREN_action(self, localctx , actionIndex):
        if actionIndex == 1:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx , actionIndex):
        if actionIndex == 2:
            self.opened -= 1
     

    def OPEN_BRACK_action(self, localctx , actionIndex):
        if actionIndex == 3:
            self.opened += 1
     

    def CLOSE_BRACK_action(self, localctx , actionIndex):
        if actionIndex == 4:
            self.opened -= 1
     

    def OPEN_BRACE_action(self, localctx , actionIndex):
        if actionIndex == 5:
            self.opened += 1
     

    def CLOSE_BRACE_action(self, localctx , actionIndex):
        if actionIndex == 6:
            self.opened -= 1
     

    def sempred(self, localctx, ruleIndex, predIndex):
        if self._predicates is None:
            preds = dict()
            preds[33] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx, predIndex):
            if predIndex == 0:
                return self.atStartOfInput()
         


