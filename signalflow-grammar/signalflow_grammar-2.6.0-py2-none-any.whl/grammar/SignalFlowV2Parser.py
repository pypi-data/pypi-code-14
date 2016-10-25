# Generated from grammar/SignalFlowV2Parser.g4 by ANTLR 4.5.2
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"F\u01ab\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write(u"\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write(u"\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4")
        buf.write(u"\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30")
        buf.write(u"\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t")
        buf.write(u"\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$")
        buf.write(u"\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t")
        buf.write(u",\3\2\3\2\7\2[\n\2\f\2\16\2^\13\2\3\2\3\2\3\3\3\3\7\3")
        buf.write(u"d\n\3\f\3\16\3g\13\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write(u"\3\5\3\5\5\5s\n\5\3\5\3\5\3\6\3\6\3\6\7\6z\n\6\f\6\16")
        buf.write(u"\6}\13\6\3\7\3\7\3\7\5\7\u0082\n\7\3\b\3\b\3\t\3\t\5")
        buf.write(u"\t\u0088\n\t\3\n\3\n\3\n\7\n\u008d\n\n\f\n\16\n\u0090")
        buf.write(u"\13\n\3\n\5\n\u0093\n\n\3\n\3\n\3\13\3\13\3\13\5\13\u009a")
        buf.write(u"\n\13\3\f\3\f\3\f\5\f\u009f\n\f\3\f\3\f\3\r\3\r\3\r\7")
        buf.write(u"\r\u00a6\n\r\f\r\16\r\u00a9\13\r\3\r\5\r\u00ac\n\r\3")
        buf.write(u"\16\3\16\5\16\u00b0\n\16\3\17\3\17\3\17\3\20\3\20\3\20")
        buf.write(u"\3\20\3\20\3\20\3\20\3\20\3\20\5\20\u00be\n\20\3\21\3")
        buf.write(u"\21\3\21\5\21\u00c3\n\21\3\22\3\22\3\22\5\22\u00c8\n")
        buf.write(u"\22\3\23\3\23\3\23\7\23\u00cd\n\23\f\23\16\23\u00d0\13")
        buf.write(u"\23\3\23\5\23\u00d3\n\23\3\24\3\24\3\24\7\24\u00d8\n")
        buf.write(u"\24\f\24\16\24\u00db\13\24\3\25\3\25\3\25\7\25\u00e0")
        buf.write(u"\n\25\f\25\16\25\u00e3\13\25\3\26\3\26\5\26\u00e7\n\26")
        buf.write(u"\3\27\3\27\3\30\3\30\5\30\u00ed\n\30\3\31\3\31\3\31\3")
        buf.write(u"\31\3\31\3\31\3\31\3\31\3\31\7\31\u00f8\n\31\f\31\16")
        buf.write(u"\31\u00fb\13\31\3\31\3\31\3\31\5\31\u0100\n\31\3\32\3")
        buf.write(u"\32\3\32\3\32\6\32\u0106\n\32\r\32\16\32\u0107\3\32\3")
        buf.write(u"\32\5\32\u010c\n\32\3\33\3\33\3\33\3\33\3\33\3\33\5\33")
        buf.write(u"\u0114\n\33\3\33\5\33\u0117\n\33\3\34\3\34\3\34\3\34")
        buf.write(u"\3\34\3\35\3\35\3\35\7\35\u0121\n\35\f\35\16\35\u0124")
        buf.write(u"\13\35\3\36\3\36\3\36\7\36\u0129\n\36\f\36\16\36\u012c")
        buf.write(u"\13\36\3\37\3\37\3\37\5\37\u0131\n\37\3 \3 \3 \3 \3 ")
        buf.write(u"\3 \3 \3 \3 \3 \3 \5 \u013e\n \3 \7 \u0141\n \f \16 ")
        buf.write(u"\u0144\13 \3!\3!\3!\7!\u0149\n!\f!\16!\u014c\13!\3\"")
        buf.write(u"\3\"\3\"\7\"\u0151\n\"\f\"\16\"\u0154\13\"\3#\3#\3#\5")
        buf.write(u"#\u0159\n#\3$\3$\3$\5$\u015e\n$\3%\3%\7%\u0162\n%\f%")
        buf.write(u"\16%\u0165\13%\3&\3&\3&\3&\3&\3&\6&\u016d\n&\r&\16&\u016e")
        buf.write(u"\3&\3&\3&\5&\u0174\n&\3\'\3\'\3\'\3\'\7\'\u017a\n\'\f")
        buf.write(u"\'\16\'\u017d\13\'\5\'\u017f\n\'\3\'\3\'\3(\3(\5(\u0185")
        buf.write(u"\n(\3(\3(\3)\3)\3)\7)\u018c\n)\f)\16)\u018f\13)\3)\5")
        buf.write(u")\u0192\n)\3*\3*\5*\u0196\n*\3*\3*\3*\5*\u019b\n*\3+")
        buf.write(u"\3+\3+\7+\u01a0\n+\f+\16+\u01a3\13+\3,\3,\5,\u01a7\n")
        buf.write(u",\3,\3,\3,\2\2-\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36")
        buf.write(u" \"$&(*,.\60\62\64\668:<>@BDFHJLNPRTV\2\5\3\3$$\3\2\65")
        buf.write(u"\66\4\2++\67\67\u01c1\2\\\3\2\2\2\4a\3\2\2\2\6j\3\2\2")
        buf.write(u"\2\bp\3\2\2\2\nv\3\2\2\2\f~\3\2\2\2\16\u0083\3\2\2\2")
        buf.write(u"\20\u0087\3\2\2\2\22\u0089\3\2\2\2\24\u0099\3\2\2\2\26")
        buf.write(u"\u009e\3\2\2\2\30\u00a2\3\2\2\2\32\u00af\3\2\2\2\34\u00b1")
        buf.write(u"\3\2\2\2\36\u00b4\3\2\2\2 \u00bf\3\2\2\2\"\u00c4\3\2")
        buf.write(u"\2\2$\u00c9\3\2\2\2&\u00d4\3\2\2\2(\u00dc\3\2\2\2*\u00e4")
        buf.write(u"\3\2\2\2,\u00e8\3\2\2\2.\u00ec\3\2\2\2\60\u00ee\3\2\2")
        buf.write(u"\2\62\u010b\3\2\2\2\64\u0116\3\2\2\2\66\u0118\3\2\2\2")
        buf.write(u"8\u011d\3\2\2\2:\u0125\3\2\2\2<\u0130\3\2\2\2>\u0132")
        buf.write(u"\3\2\2\2@\u0145\3\2\2\2B\u014d\3\2\2\2D\u0158\3\2\2\2")
        buf.write(u"F\u015a\3\2\2\2H\u015f\3\2\2\2J\u0173\3\2\2\2L\u0175")
        buf.write(u"\3\2\2\2N\u0182\3\2\2\2P\u0188\3\2\2\2R\u019a\3\2\2\2")
        buf.write(u"T\u019c\3\2\2\2V\u01a6\3\2\2\2X[\7$\2\2Y[\5\20\t\2ZX")
        buf.write(u"\3\2\2\2ZY\3\2\2\2[^\3\2\2\2\\Z\3\2\2\2\\]\3\2\2\2]_")
        buf.write(u"\3\2\2\2^\\\3\2\2\2_`\7\2\2\3`\3\3\2\2\2ae\5P)\2bd\7")
        buf.write(u"$\2\2cb\3\2\2\2dg\3\2\2\2ec\3\2\2\2ef\3\2\2\2fh\3\2\2")
        buf.write(u"\2ge\3\2\2\2hi\7\2\2\3i\5\3\2\2\2jk\7\3\2\2kl\7%\2\2")
        buf.write(u"lm\5\b\5\2mn\7/\2\2no\5\62\32\2o\7\3\2\2\2pr\7,\2\2q")
        buf.write(u"s\5\n\6\2rq\3\2\2\2rs\3\2\2\2st\3\2\2\2tu\7-\2\2u\t\3")
        buf.write(u"\2\2\2v{\5\f\7\2wx\7.\2\2xz\5\f\7\2yw\3\2\2\2z}\3\2\2")
        buf.write(u"\2{y\3\2\2\2{|\3\2\2\2|\13\3\2\2\2}{\3\2\2\2~\u0081\5")
        buf.write(u"\16\b\2\177\u0080\7\62\2\2\u0080\u0082\5\64\33\2\u0081")
        buf.write(u"\177\3\2\2\2\u0081\u0082\3\2\2\2\u0082\r\3\2\2\2\u0083")
        buf.write(u"\u0084\7%\2\2\u0084\17\3\2\2\2\u0085\u0088\5\22\n\2\u0086")
        buf.write(u"\u0088\5.\30\2\u0087\u0085\3\2\2\2\u0087\u0086\3\2\2")
        buf.write(u"\2\u0088\21\3\2\2\2\u0089\u008e\5\24\13\2\u008a\u008b")
        buf.write(u"\7\60\2\2\u008b\u008d\5\24\13\2\u008c\u008a\3\2\2\2\u008d")
        buf.write(u"\u0090\3\2\2\2\u008e\u008c\3\2\2\2\u008e\u008f\3\2\2")
        buf.write(u"\2\u008f\u0092\3\2\2\2\u0090\u008e\3\2\2\2\u0091\u0093")
        buf.write(u"\7\60\2\2\u0092\u0091\3\2\2\2\u0092\u0093\3\2\2\2\u0093")
        buf.write(u"\u0094\3\2\2\2\u0094\u0095\t\2\2\2\u0095\23\3\2\2\2\u0096")
        buf.write(u"\u009a\5\26\f\2\u0097\u009a\5,\27\2\u0098\u009a\5\32")
        buf.write(u"\16\2\u0099\u0096\3\2\2\2\u0099\u0097\3\2\2\2\u0099\u0098")
        buf.write(u"\3\2\2\2\u009a\25\3\2\2\2\u009b\u009c\5\30\r\2\u009c")
        buf.write(u"\u009d\7\62\2\2\u009d\u009f\3\2\2\2\u009e\u009b\3\2\2")
        buf.write(u"\2\u009e\u009f\3\2\2\2\u009f\u00a0\3\2\2\2\u00a0\u00a1")
        buf.write(u"\5P)\2\u00a1\27\3\2\2\2\u00a2\u00a7\7%\2\2\u00a3\u00a4")
        buf.write(u"\7.\2\2\u00a4\u00a6\7%\2\2\u00a5\u00a3\3\2\2\2\u00a6")
        buf.write(u"\u00a9\3\2\2\2\u00a7\u00a5\3\2\2\2\u00a7\u00a8\3\2\2")
        buf.write(u"\2\u00a8\u00ab\3\2\2\2\u00a9\u00a7\3\2\2\2\u00aa\u00ac")
        buf.write(u"\7.\2\2\u00ab\u00aa\3\2\2\2\u00ab\u00ac\3\2\2\2\u00ac")
        buf.write(u"\31\3\2\2\2\u00ad\u00b0\5\34\17\2\u00ae\u00b0\5\36\20")
        buf.write(u"\2\u00af\u00ad\3\2\2\2\u00af\u00ae\3\2\2\2\u00b0\33\3")
        buf.write(u"\2\2\2\u00b1\u00b2\7\7\2\2\u00b2\u00b3\5&\24\2\u00b3")
        buf.write(u"\35\3\2\2\2\u00b4\u00b5\7\6\2\2\u00b5\u00b6\5(\25\2\u00b6")
        buf.write(u"\u00bd\7\7\2\2\u00b7\u00be\7+\2\2\u00b8\u00b9\7,\2\2")
        buf.write(u"\u00b9\u00ba\5$\23\2\u00ba\u00bb\7-\2\2\u00bb\u00be\3")
        buf.write(u"\2\2\2\u00bc\u00be\5$\23\2\u00bd\u00b7\3\2\2\2\u00bd")
        buf.write(u"\u00b8\3\2\2\2\u00bd\u00bc\3\2\2\2\u00be\37\3\2\2\2\u00bf")
        buf.write(u"\u00c2\7%\2\2\u00c0\u00c1\7\b\2\2\u00c1\u00c3\7%\2\2")
        buf.write(u"\u00c2\u00c0\3\2\2\2\u00c2\u00c3\3\2\2\2\u00c3!\3\2\2")
        buf.write(u"\2\u00c4\u00c7\5(\25\2\u00c5\u00c6\7\b\2\2\u00c6\u00c8")
        buf.write(u"\7%\2\2\u00c7\u00c5\3\2\2\2\u00c7\u00c8\3\2\2\2\u00c8")
        buf.write(u"#\3\2\2\2\u00c9\u00ce\5 \21\2\u00ca\u00cb\7.\2\2\u00cb")
        buf.write(u"\u00cd\5 \21\2\u00cc\u00ca\3\2\2\2\u00cd\u00d0\3\2\2")
        buf.write(u"\2\u00ce\u00cc\3\2\2\2\u00ce\u00cf\3\2\2\2\u00cf\u00d2")
        buf.write(u"\3\2\2\2\u00d0\u00ce\3\2\2\2\u00d1\u00d3\7.\2\2\u00d2")
        buf.write(u"\u00d1\3\2\2\2\u00d2\u00d3\3\2\2\2\u00d3%\3\2\2\2\u00d4")
        buf.write(u"\u00d9\5\"\22\2\u00d5\u00d6\7.\2\2\u00d6\u00d8\5\"\22")
        buf.write(u"\2\u00d7\u00d5\3\2\2\2\u00d8\u00db\3\2\2\2\u00d9\u00d7")
        buf.write(u"\3\2\2\2\u00d9\u00da\3\2\2\2\u00da\'\3\2\2\2\u00db\u00d9")
        buf.write(u"\3\2\2\2\u00dc\u00e1\7%\2\2\u00dd\u00de\7)\2\2\u00de")
        buf.write(u"\u00e0\7%\2\2\u00df\u00dd\3\2\2\2\u00e0\u00e3\3\2\2\2")
        buf.write(u"\u00e1\u00df\3\2\2\2\u00e1\u00e2\3\2\2\2\u00e2)\3\2\2")
        buf.write(u"\2\u00e3\u00e1\3\2\2\2\u00e4\u00e6\7\4\2\2\u00e5\u00e7")
        buf.write(u"\5P)\2\u00e6\u00e5\3\2\2\2\u00e6\u00e7\3\2\2\2\u00e7")
        buf.write(u"+\3\2\2\2\u00e8\u00e9\5*\26\2\u00e9-\3\2\2\2\u00ea\u00ed")
        buf.write(u"\5\60\31\2\u00eb\u00ed\5\6\4\2\u00ec\u00ea\3\2\2\2\u00ec")
        buf.write(u"\u00eb\3\2\2\2\u00ed/\3\2\2\2\u00ee\u00ef\7\f\2\2\u00ef")
        buf.write(u"\u00f0\5\64\33\2\u00f0\u00f1\7/\2\2\u00f1\u00f9\5\62")
        buf.write(u"\32\2\u00f2\u00f3\7\r\2\2\u00f3\u00f4\5\64\33\2\u00f4")
        buf.write(u"\u00f5\7/\2\2\u00f5\u00f6\5\62\32\2\u00f6\u00f8\3\2\2")
        buf.write(u"\2\u00f7\u00f2\3\2\2\2\u00f8\u00fb\3\2\2\2\u00f9\u00f7")
        buf.write(u"\3\2\2\2\u00f9\u00fa\3\2\2\2\u00fa\u00ff\3\2\2\2\u00fb")
        buf.write(u"\u00f9\3\2\2\2\u00fc\u00fd\7\16\2\2\u00fd\u00fe\7/\2")
        buf.write(u"\2\u00fe\u0100\5\62\32\2\u00ff\u00fc\3\2\2\2\u00ff\u0100")
        buf.write(u"\3\2\2\2\u0100\61\3\2\2\2\u0101\u010c\5\22\n\2\u0102")
        buf.write(u"\u0103\7$\2\2\u0103\u0105\7E\2\2\u0104\u0106\5\20\t\2")
        buf.write(u"\u0105\u0104\3\2\2\2\u0106\u0107\3\2\2\2\u0107\u0105")
        buf.write(u"\3\2\2\2\u0107\u0108\3\2\2\2\u0108\u0109\3\2\2\2\u0109")
        buf.write(u"\u010a\7F\2\2\u010a\u010c\3\2\2\2\u010b\u0101\3\2\2\2")
        buf.write(u"\u010b\u0102\3\2\2\2\u010c\63\3\2\2\2\u010d\u0113\58")
        buf.write(u"\35\2\u010e\u010f\7\f\2\2\u010f\u0110\58\35\2\u0110\u0111")
        buf.write(u"\7\16\2\2\u0111\u0112\5\64\33\2\u0112\u0114\3\2\2\2\u0113")
        buf.write(u"\u010e\3\2\2\2\u0113\u0114\3\2\2\2\u0114\u0117\3\2\2")
        buf.write(u"\2\u0115\u0117\5\66\34\2\u0116\u010d\3\2\2\2\u0116\u0115")
        buf.write(u"\3\2\2\2\u0117\65\3\2\2\2\u0118\u0119\7\26\2\2\u0119")
        buf.write(u"\u011a\7%\2\2\u011a\u011b\7/\2\2\u011b\u011c\5\64\33")
        buf.write(u"\2\u011c\67\3\2\2\2\u011d\u0122\5:\36\2\u011e\u011f\7")
        buf.write(u"\27\2\2\u011f\u0121\5:\36\2\u0120\u011e\3\2\2\2\u0121")
        buf.write(u"\u0124\3\2\2\2\u0122\u0120\3\2\2\2\u0122\u0123\3\2\2")
        buf.write(u"\2\u01239\3\2\2\2\u0124\u0122\3\2\2\2\u0125\u012a\5<")
        buf.write(u"\37\2\u0126\u0127\7\30\2\2\u0127\u0129\5<\37\2\u0128")
        buf.write(u"\u0126\3\2\2\2\u0129\u012c\3\2\2\2\u012a\u0128\3\2\2")
        buf.write(u"\2\u012a\u012b\3\2\2\2\u012b;\3\2\2\2\u012c\u012a\3\2")
        buf.write(u"\2\2\u012d\u012e\7\31\2\2\u012e\u0131\5<\37\2\u012f\u0131")
        buf.write(u"\5> \2\u0130\u012d\3\2\2\2\u0130\u012f\3\2\2\2\u0131")
        buf.write(u"=\3\2\2\2\u0132\u0142\5@!\2\u0133\u013e\7:\2\2\u0134")
        buf.write(u"\u013e\7>\2\2\u0135\u013e\7<\2\2\u0136\u013e\7?\2\2\u0137")
        buf.write(u"\u013e\7@\2\2\u0138\u013e\7;\2\2\u0139\u013e\7=\2\2\u013a")
        buf.write(u"\u013e\7\32\2\2\u013b\u013c\7\32\2\2\u013c\u013e\7\31")
        buf.write(u"\2\2\u013d\u0133\3\2\2\2\u013d\u0134\3\2\2\2\u013d\u0135")
        buf.write(u"\3\2\2\2\u013d\u0136\3\2\2\2\u013d\u0137\3\2\2\2\u013d")
        buf.write(u"\u0138\3\2\2\2\u013d\u0139\3\2\2\2\u013d\u013a\3\2\2")
        buf.write(u"\2\u013d\u013b\3\2\2\2\u013e\u013f\3\2\2\2\u013f\u0141")
        buf.write(u"\5@!\2\u0140\u013d\3\2\2\2\u0141\u0144\3\2\2\2\u0142")
        buf.write(u"\u0140\3\2\2\2\u0142\u0143\3\2\2\2\u0143?\3\2\2\2\u0144")
        buf.write(u"\u0142\3\2\2\2\u0145\u014a\5B\"\2\u0146\u0147\t\3\2\2")
        buf.write(u"\u0147\u0149\5B\"\2\u0148\u0146\3\2\2\2\u0149\u014c\3")
        buf.write(u"\2\2\2\u014a\u0148\3\2\2\2\u014a\u014b\3\2\2\2\u014b")
        buf.write(u"A\3\2\2\2\u014c\u014a\3\2\2\2\u014d\u0152\5D#\2\u014e")
        buf.write(u"\u014f\t\4\2\2\u014f\u0151\5D#\2\u0150\u014e\3\2\2\2")
        buf.write(u"\u0151\u0154\3\2\2\2\u0152\u0150\3\2\2\2\u0152\u0153")
        buf.write(u"\3\2\2\2\u0153C\3\2\2\2\u0154\u0152\3\2\2\2\u0155\u0156")
        buf.write(u"\t\3\2\2\u0156\u0159\5D#\2\u0157\u0159\5F$\2\u0158\u0155")
        buf.write(u"\3\2\2\2\u0158\u0157\3\2\2\2\u0159E\3\2\2\2\u015a\u015d")
        buf.write(u"\5H%\2\u015b\u015c\7\61\2\2\u015c\u015e\5D#\2\u015d\u015b")
        buf.write(u"\3\2\2\2\u015d\u015e\3\2\2\2\u015eG\3\2\2\2\u015f\u0163")
        buf.write(u"\5J&\2\u0160\u0162\5R*\2\u0161\u0160\3\2\2\2\u0162\u0165")
        buf.write(u"\3\2\2\2\u0163\u0161\3\2\2\2\u0163\u0164\3\2\2\2\u0164")
        buf.write(u"I\3\2\2\2\u0165\u0163\3\2\2\2\u0166\u0174\5L\'\2\u0167")
        buf.write(u"\u0174\5N(\2\u0168\u0174\7%\2\2\u0169\u0174\7\'\2\2\u016a")
        buf.write(u"\u0174\7(\2\2\u016b\u016d\7&\2\2\u016c\u016b\3\2\2\2")
        buf.write(u"\u016d\u016e\3\2\2\2\u016e\u016c\3\2\2\2\u016e\u016f")
        buf.write(u"\3\2\2\2\u016f\u0174\3\2\2\2\u0170\u0174\7\33\2\2\u0171")
        buf.write(u"\u0174\7\34\2\2\u0172\u0174\7\35\2\2\u0173\u0166\3\2")
        buf.write(u"\2\2\u0173\u0167\3\2\2\2\u0173\u0168\3\2\2\2\u0173\u0169")
        buf.write(u"\3\2\2\2\u0173\u016a\3\2\2\2\u0173\u016c\3\2\2\2\u0173")
        buf.write(u"\u0170\3\2\2\2\u0173\u0171\3\2\2\2\u0173\u0172\3\2\2")
        buf.write(u"\2\u0174K\3\2\2\2\u0175\u017e\7\63\2\2\u0176\u017b\5")
        buf.write(u"\64\33\2\u0177\u0178\7.\2\2\u0178\u017a\5\64\33\2\u0179")
        buf.write(u"\u0177\3\2\2\2\u017a\u017d\3\2\2\2\u017b\u0179\3\2\2")
        buf.write(u"\2\u017b\u017c\3\2\2\2\u017c\u017f\3\2\2\2\u017d\u017b")
        buf.write(u"\3\2\2\2\u017e\u0176\3\2\2\2\u017e\u017f\3\2\2\2\u017f")
        buf.write(u"\u0180\3\2\2\2\u0180\u0181\7\64\2\2\u0181M\3\2\2\2\u0182")
        buf.write(u"\u0184\7,\2\2\u0183\u0185\5P)\2\u0184\u0183\3\2\2\2\u0184")
        buf.write(u"\u0185\3\2\2\2\u0185\u0186\3\2\2\2\u0186\u0187\7-\2\2")
        buf.write(u"\u0187O\3\2\2\2\u0188\u018d\5\64\33\2\u0189\u018a\7.")
        buf.write(u"\2\2\u018a\u018c\5\64\33\2\u018b\u0189\3\2\2\2\u018c")
        buf.write(u"\u018f\3\2\2\2\u018d\u018b\3\2\2\2\u018d\u018e\3\2\2")
        buf.write(u"\2\u018e\u0191\3\2\2\2\u018f\u018d\3\2\2\2\u0190\u0192")
        buf.write(u"\7.\2\2\u0191\u0190\3\2\2\2\u0191\u0192\3\2\2\2\u0192")
        buf.write(u"Q\3\2\2\2\u0193\u0195\7,\2\2\u0194\u0196\5T+\2\u0195")
        buf.write(u"\u0194\3\2\2\2\u0195\u0196\3\2\2\2\u0196\u0197\3\2\2")
        buf.write(u"\2\u0197\u019b\7-\2\2\u0198\u0199\7)\2\2\u0199\u019b")
        buf.write(u"\7%\2\2\u019a\u0193\3\2\2\2\u019a\u0198\3\2\2\2\u019b")
        buf.write(u"S\3\2\2\2\u019c\u01a1\5V,\2\u019d\u019e\7.\2\2\u019e")
        buf.write(u"\u01a0\5V,\2\u019f\u019d\3\2\2\2\u01a0\u01a3\3\2\2\2")
        buf.write(u"\u01a1\u019f\3\2\2\2\u01a1\u01a2\3\2\2\2\u01a2U\3\2\2")
        buf.write(u"\2\u01a3\u01a1\3\2\2\2\u01a4\u01a5\7%\2\2\u01a5\u01a7")
        buf.write(u"\7\62\2\2\u01a6\u01a4\3\2\2\2\u01a6\u01a7\3\2\2\2\u01a7")
        buf.write(u"\u01a8\3\2\2\2\u01a8\u01a9\5\64\33\2\u01a9W\3\2\2\2\64")
        buf.write(u"Z\\er{\u0081\u0087\u008e\u0092\u0099\u009e\u00a7\u00ab")
        buf.write(u"\u00af\u00bd\u00c2\u00c7\u00ce\u00d2\u00d9\u00e1\u00e6")
        buf.write(u"\u00ec\u00f9\u00ff\u0107\u010b\u0113\u0116\u0122\u012a")
        buf.write(u"\u0130\u013d\u0142\u014a\u0152\u0158\u015d\u0163\u016e")
        buf.write(u"\u0173\u017b\u017e\u0184\u018d\u0191\u0195\u019a\u01a1")
        buf.write(u"\u01a6")
        return buf.getvalue()


class SignalFlowV2Parser ( Parser ):

    grammarFileName = "SignalFlowV2Parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'def'", u"'return'", u"'raise'", u"'from'", 
                     u"'import'", u"'as'", u"'global'", u"'nonlocal'", u"'assert'", 
                     u"'if'", u"'elif'", u"'else'", u"'while'", u"'for'", 
                     u"'in'", u"'try'", u"'finally'", u"'with'", u"'except'", 
                     u"'lambda'", u"'or'", u"'and'", u"'not'", u"'is'", 
                     u"'None'", u"'True'", u"'False'", u"'class'", u"'yield'", 
                     u"'del'", u"'pass'", u"'continue'", u"'break'", u"<INVALID>", 
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                     u"'.'", u"'...'", u"'*'", u"'('", u"')'", u"','", u"':'", 
                     u"';'", u"'**'", u"'='", u"'['", u"']'", u"'+'", u"'-'", 
                     u"'/'", u"'{'", u"'}'", u"'<'", u"'>'", u"'=='", u"'>='", 
                     u"'<='", u"'<>'", u"'!='", u"'@'", u"'->'" ]

    symbolicNames = [ u"<INVALID>", u"DEF", u"RETURN", u"RAISE", u"FROM", 
                      u"IMPORT", u"AS", u"GLOBAL", u"NONLOCAL", u"ASSERT", 
                      u"IF", u"ELIF", u"ELSE", u"WHILE", u"FOR", u"IN", 
                      u"TRY", u"FINALLY", u"WITH", u"EXCEPT", u"LAMBDA", 
                      u"OR", u"AND", u"NOT", u"IS", u"NONE", u"TRUE", u"FALSE", 
                      u"CLASS", u"YIELD", u"DEL", u"PASS", u"CONTINUE", 
                      u"BREAK", u"NEWLINE", u"ID", u"STRING", u"INT", u"FLOAT", 
                      u"DOT", u"ELLIPSE", u"STAR", u"OPEN_PAREN", u"CLOSE_PAREN", 
                      u"COMMA", u"COLON", u"SEMICOLON", u"POWER", u"ASSIGN", 
                      u"OPEN_BRACK", u"CLOSE_BRACK", u"ADD", u"MINUS", u"DIV", 
                      u"OPEN_BRACE", u"CLOSE_BRACE", u"LESS_THAN", u"GREATER_THAN", 
                      u"EQUALS", u"GT_EQ", u"LT_EQ", u"NOT_EQ_1", u"NOT_EQ_2", 
                      u"AT", u"ARROW", u"SKIP_", u"COMMENT", u"INDENT", 
                      u"DEDENT" ]

    RULE_program = 0
    RULE_eval_input = 1
    RULE_function_definition = 2
    RULE_parameters = 3
    RULE_var_args_list = 4
    RULE_var_args_list_param_def = 5
    RULE_var_args_list_param_name = 6
    RULE_statement = 7
    RULE_simple_statement = 8
    RULE_small_statement = 9
    RULE_expr_statement = 10
    RULE_id_list = 11
    RULE_import_statement = 12
    RULE_import_name = 13
    RULE_import_from = 14
    RULE_import_as_name = 15
    RULE_dotted_as_name = 16
    RULE_import_as_names = 17
    RULE_dotted_as_names = 18
    RULE_dotted_name = 19
    RULE_return_statement = 20
    RULE_flow_statement = 21
    RULE_compound_statement = 22
    RULE_if_statement = 23
    RULE_suite = 24
    RULE_test = 25
    RULE_lambdef = 26
    RULE_or_test = 27
    RULE_and_test = 28
    RULE_not_test = 29
    RULE_comparison = 30
    RULE_expr = 31
    RULE_term = 32
    RULE_factor = 33
    RULE_power = 34
    RULE_atom_expr = 35
    RULE_atom = 36
    RULE_list_expr = 37
    RULE_tuple_expr = 38
    RULE_testlist = 39
    RULE_trailer = 40
    RULE_actual_args = 41
    RULE_argument = 42

    ruleNames =  [ u"program", u"eval_input", u"function_definition", u"parameters", 
                   u"var_args_list", u"var_args_list_param_def", u"var_args_list_param_name", 
                   u"statement", u"simple_statement", u"small_statement", 
                   u"expr_statement", u"id_list", u"import_statement", u"import_name", 
                   u"import_from", u"import_as_name", u"dotted_as_name", 
                   u"import_as_names", u"dotted_as_names", u"dotted_name", 
                   u"return_statement", u"flow_statement", u"compound_statement", 
                   u"if_statement", u"suite", u"test", u"lambdef", u"or_test", 
                   u"and_test", u"not_test", u"comparison", u"expr", u"term", 
                   u"factor", u"power", u"atom_expr", u"atom", u"list_expr", 
                   u"tuple_expr", u"testlist", u"trailer", u"actual_args", 
                   u"argument" ]

    EOF = Token.EOF
    DEF=1
    RETURN=2
    RAISE=3
    FROM=4
    IMPORT=5
    AS=6
    GLOBAL=7
    NONLOCAL=8
    ASSERT=9
    IF=10
    ELIF=11
    ELSE=12
    WHILE=13
    FOR=14
    IN=15
    TRY=16
    FINALLY=17
    WITH=18
    EXCEPT=19
    LAMBDA=20
    OR=21
    AND=22
    NOT=23
    IS=24
    NONE=25
    TRUE=26
    FALSE=27
    CLASS=28
    YIELD=29
    DEL=30
    PASS=31
    CONTINUE=32
    BREAK=33
    NEWLINE=34
    ID=35
    STRING=36
    INT=37
    FLOAT=38
    DOT=39
    ELLIPSE=40
    STAR=41
    OPEN_PAREN=42
    CLOSE_PAREN=43
    COMMA=44
    COLON=45
    SEMICOLON=46
    POWER=47
    ASSIGN=48
    OPEN_BRACK=49
    CLOSE_BRACK=50
    ADD=51
    MINUS=52
    DIV=53
    OPEN_BRACE=54
    CLOSE_BRACE=55
    LESS_THAN=56
    GREATER_THAN=57
    EQUALS=58
    GT_EQ=59
    LT_EQ=60
    NOT_EQ_1=61
    NOT_EQ_2=62
    AT=63
    ARROW=64
    SKIP_=65
    COMMENT=66
    INDENT=67
    DEDENT=68

    def __init__(self, input):
        super(SignalFlowV2Parser, self).__init__(input)
        self.checkVersion("4.5.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgramContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ProgramContext, self).__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def NEWLINE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NEWLINE)
            else:
                return self.getToken(SignalFlowV2Parser.NEWLINE, i)

        def statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.StatementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.StatementContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_program

        def enterRule(self, listener):
            if hasattr(listener, "enterProgram"):
                listener.enterProgram(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitProgram"):
                listener.exitProgram(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitProgram"):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = SignalFlowV2Parser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DEF) | (1 << SignalFlowV2Parser.RETURN) | (1 << SignalFlowV2Parser.FROM) | (1 << SignalFlowV2Parser.IMPORT) | (1 << SignalFlowV2Parser.IF) | (1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.NEWLINE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                self.state = 88
                token = self._input.LA(1)
                if token in [SignalFlowV2Parser.NEWLINE]:
                    self.state = 86
                    self.match(SignalFlowV2Parser.NEWLINE)

                elif token in [SignalFlowV2Parser.DEF, SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.IF, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS]:
                    self.state = 87
                    self.statement()

                else:
                    raise NoViableAltException(self)

                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 93
            self.match(SignalFlowV2Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Eval_inputContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Eval_inputContext, self).__init__(parent, invokingState)
            self.parser = parser

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def NEWLINE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NEWLINE)
            else:
                return self.getToken(SignalFlowV2Parser.NEWLINE, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_eval_input

        def enterRule(self, listener):
            if hasattr(listener, "enterEval_input"):
                listener.enterEval_input(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitEval_input"):
                listener.exitEval_input(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitEval_input"):
                return visitor.visitEval_input(self)
            else:
                return visitor.visitChildren(self)




    def eval_input(self):

        localctx = SignalFlowV2Parser.Eval_inputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_eval_input)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.testlist()
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.NEWLINE:
                self.state = 96
                self.match(SignalFlowV2Parser.NEWLINE)
                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 102
            self.match(SignalFlowV2Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Function_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Function_definitionContext, self).__init__(parent, invokingState)
            self.parser = parser

        def DEF(self):
            return self.getToken(SignalFlowV2Parser.DEF, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def parameters(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.ParametersContext,0)


        def suite(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.SuiteContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_function_definition

        def enterRule(self, listener):
            if hasattr(listener, "enterFunction_definition"):
                listener.enterFunction_definition(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFunction_definition"):
                listener.exitFunction_definition(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFunction_definition"):
                return visitor.visitFunction_definition(self)
            else:
                return visitor.visitChildren(self)




    def function_definition(self):

        localctx = SignalFlowV2Parser.Function_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_function_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.match(SignalFlowV2Parser.DEF)
            self.state = 105
            self.match(SignalFlowV2Parser.ID)
            self.state = 106
            self.parameters()
            self.state = 107
            self.match(SignalFlowV2Parser.COLON)
            self.state = 108
            self.suite()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ParametersContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ParametersContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def var_args_list(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_listContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_parameters

        def enterRule(self, listener):
            if hasattr(listener, "enterParameters"):
                listener.enterParameters(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitParameters"):
                listener.exitParameters(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitParameters"):
                return visitor.visitParameters(self)
            else:
                return visitor.visitChildren(self)




    def parameters(self):

        localctx = SignalFlowV2Parser.ParametersContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_parameters)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            self.match(SignalFlowV2Parser.OPEN_PAREN)
            self.state = 112
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ID:
                self.state = 111
                self.var_args_list()


            self.state = 114
            self.match(SignalFlowV2Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_listContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_listContext, self).__init__(parent, invokingState)
            self.parser = parser

        def var_args_list_param_def(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Var_args_list_param_defContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_list_param_defContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list"):
                listener.enterVar_args_list(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list"):
                listener.exitVar_args_list(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list"):
                return visitor.visitVar_args_list(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list(self):

        localctx = SignalFlowV2Parser.Var_args_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_var_args_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.var_args_list_param_def()
            self.state = 121
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 117
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 118
                self.var_args_list_param_def()
                self.state = 123
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_list_param_defContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_list_param_defContext, self).__init__(parent, invokingState)
            self.parser = parser

        def var_args_list_param_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_list_param_nameContext,0)


        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list_param_def

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list_param_def"):
                listener.enterVar_args_list_param_def(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list_param_def"):
                listener.exitVar_args_list_param_def(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list_param_def"):
                return visitor.visitVar_args_list_param_def(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list_param_def(self):

        localctx = SignalFlowV2Parser.Var_args_list_param_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_var_args_list_param_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.var_args_list_param_name()
            self.state = 127
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ASSIGN:
                self.state = 125
                self.match(SignalFlowV2Parser.ASSIGN)
                self.state = 126
                self.test()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_list_param_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_list_param_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list_param_name

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list_param_name"):
                listener.enterVar_args_list_param_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list_param_name"):
                listener.exitVar_args_list_param_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list_param_name"):
                return visitor.visitVar_args_list_param_name(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list_param_name(self):

        localctx = SignalFlowV2Parser.Var_args_list_param_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_var_args_list_param_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self.match(SignalFlowV2Parser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.StatementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def simple_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Simple_statementContext,0)


        def compound_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Compound_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterStatement"):
                listener.enterStatement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitStatement"):
                listener.exitStatement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitStatement"):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = SignalFlowV2Parser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_statement)
        try:
            self.state = 133
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 131
                self.simple_statement()

            elif token in [SignalFlowV2Parser.DEF, SignalFlowV2Parser.IF]:
                self.enterOuterAlt(localctx, 2)
                self.state = 132
                self.compound_statement()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simple_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Simple_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def small_statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Small_statementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Small_statementContext,i)


        def NEWLINE(self):
            return self.getToken(SignalFlowV2Parser.NEWLINE, 0)

        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_simple_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterSimple_statement"):
                listener.enterSimple_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSimple_statement"):
                listener.exitSimple_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSimple_statement"):
                return visitor.visitSimple_statement(self)
            else:
                return visitor.visitChildren(self)




    def simple_statement(self):

        localctx = SignalFlowV2Parser.Simple_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_simple_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 135
            self.small_statement()
            self.state = 140
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 136
                    self.match(SignalFlowV2Parser.SEMICOLON)
                    self.state = 137
                    self.small_statement() 
                self.state = 142
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

            self.state = 144
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.SEMICOLON:
                self.state = 143
                self.match(SignalFlowV2Parser.SEMICOLON)


            self.state = 146
            _la = self._input.LA(1)
            if not(_la==SignalFlowV2Parser.EOF or _la==SignalFlowV2Parser.NEWLINE):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Small_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Small_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Expr_statementContext,0)


        def flow_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Flow_statementContext,0)


        def import_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_small_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterSmall_statement"):
                listener.enterSmall_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSmall_statement"):
                listener.exitSmall_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSmall_statement"):
                return visitor.visitSmall_statement(self)
            else:
                return visitor.visitChildren(self)




    def small_statement(self):

        localctx = SignalFlowV2Parser.Small_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_small_statement)
        try:
            self.state = 151
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 148
                self.expr_statement()

            elif token in [SignalFlowV2Parser.RETURN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 149
                self.flow_statement()

            elif token in [SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 150
                self.import_statement()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Expr_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Expr_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def id_list(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Id_listContext,0)


        def ASSIGN(self):
            return self.getToken(SignalFlowV2Parser.ASSIGN, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_expr_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterExpr_statement"):
                listener.enterExpr_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitExpr_statement"):
                listener.exitExpr_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitExpr_statement"):
                return visitor.visitExpr_statement(self)
            else:
                return visitor.visitChildren(self)




    def expr_statement(self):

        localctx = SignalFlowV2Parser.Expr_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_expr_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 153
                self.id_list()
                self.state = 154
                self.match(SignalFlowV2Parser.ASSIGN)


            self.state = 158
            self.testlist()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Id_listContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Id_listContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_id_list

        def enterRule(self, listener):
            if hasattr(listener, "enterId_list"):
                listener.enterId_list(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitId_list"):
                listener.exitId_list(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitId_list"):
                return visitor.visitId_list(self)
            else:
                return visitor.visitChildren(self)




    def id_list(self):

        localctx = SignalFlowV2Parser.Id_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_id_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self.match(SignalFlowV2Parser.ID)
            self.state = 165
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 161
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 162
                    self.match(SignalFlowV2Parser.ID) 
                self.state = 167
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

            self.state = 169
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 168
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def import_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_nameContext,0)


        def import_from(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_fromContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_statement"):
                listener.enterImport_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_statement"):
                listener.exitImport_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_statement"):
                return visitor.visitImport_statement(self)
            else:
                return visitor.visitChildren(self)




    def import_statement(self):

        localctx = SignalFlowV2Parser.Import_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_import_statement)
        try:
            self.state = 173
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.IMPORT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 171
                self.import_name()

            elif token in [SignalFlowV2Parser.FROM]:
                self.enterOuterAlt(localctx, 2)
                self.state = 172
                self.import_from()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IMPORT(self):
            return self.getToken(SignalFlowV2Parser.IMPORT, 0)

        def dotted_as_names(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_as_namesContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_name

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_name"):
                listener.enterImport_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_name"):
                listener.exitImport_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_name"):
                return visitor.visitImport_name(self)
            else:
                return visitor.visitChildren(self)




    def import_name(self):

        localctx = SignalFlowV2Parser.Import_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_import_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            self.match(SignalFlowV2Parser.IMPORT)
            self.state = 176
            self.dotted_as_names()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_fromContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_fromContext, self).__init__(parent, invokingState)
            self.parser = parser

        def FROM(self):
            return self.getToken(SignalFlowV2Parser.FROM, 0)

        def dotted_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_nameContext,0)


        def IMPORT(self):
            return self.getToken(SignalFlowV2Parser.IMPORT, 0)

        def import_as_names(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_as_namesContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_from

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_from"):
                listener.enterImport_from(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_from"):
                listener.exitImport_from(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_from"):
                return visitor.visitImport_from(self)
            else:
                return visitor.visitChildren(self)




    def import_from(self):

        localctx = SignalFlowV2Parser.Import_fromContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_import_from)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.match(SignalFlowV2Parser.FROM)
            self.state = 179
            self.dotted_name()
            self.state = 180
            self.match(SignalFlowV2Parser.IMPORT)
            self.state = 187
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.STAR]:
                self.state = 181
                self.match(SignalFlowV2Parser.STAR)

            elif token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.state = 182
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 183
                self.import_as_names()
                self.state = 184
                self.match(SignalFlowV2Parser.CLOSE_PAREN)

            elif token in [SignalFlowV2Parser.ID]:
                self.state = 186
                self.import_as_names()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_as_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_as_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def AS(self):
            return self.getToken(SignalFlowV2Parser.AS, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_as_name

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_as_name"):
                listener.enterImport_as_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_as_name"):
                listener.exitImport_as_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_as_name"):
                return visitor.visitImport_as_name(self)
            else:
                return visitor.visitChildren(self)




    def import_as_name(self):

        localctx = SignalFlowV2Parser.Import_as_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_import_as_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 189
            self.match(SignalFlowV2Parser.ID)
            self.state = 192
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.AS:
                self.state = 190
                self.match(SignalFlowV2Parser.AS)
                self.state = 191
                self.match(SignalFlowV2Parser.ID)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_as_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_as_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def dotted_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_nameContext,0)


        def AS(self):
            return self.getToken(SignalFlowV2Parser.AS, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_as_name

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_as_name"):
                listener.enterDotted_as_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_as_name"):
                listener.exitDotted_as_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_as_name"):
                return visitor.visitDotted_as_name(self)
            else:
                return visitor.visitChildren(self)




    def dotted_as_name(self):

        localctx = SignalFlowV2Parser.Dotted_as_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_dotted_as_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.dotted_name()
            self.state = 197
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.AS:
                self.state = 195
                self.match(SignalFlowV2Parser.AS)
                self.state = 196
                self.match(SignalFlowV2Parser.ID)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_as_namesContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_as_namesContext, self).__init__(parent, invokingState)
            self.parser = parser

        def import_as_name(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Import_as_nameContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Import_as_nameContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_as_names

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_as_names"):
                listener.enterImport_as_names(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_as_names"):
                listener.exitImport_as_names(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_as_names"):
                return visitor.visitImport_as_names(self)
            else:
                return visitor.visitChildren(self)




    def import_as_names(self):

        localctx = SignalFlowV2Parser.Import_as_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_import_as_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 199
            self.import_as_name()
            self.state = 204
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 200
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 201
                    self.import_as_name() 
                self.state = 206
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

            self.state = 208
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 207
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_as_namesContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_as_namesContext, self).__init__(parent, invokingState)
            self.parser = parser

        def dotted_as_name(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Dotted_as_nameContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_as_nameContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_as_names

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_as_names"):
                listener.enterDotted_as_names(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_as_names"):
                listener.exitDotted_as_names(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_as_names"):
                return visitor.visitDotted_as_names(self)
            else:
                return visitor.visitChildren(self)




    def dotted_as_names(self):

        localctx = SignalFlowV2Parser.Dotted_as_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_dotted_as_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            self.dotted_as_name()
            self.state = 215
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 211
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 212
                self.dotted_as_name()
                self.state = 217
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_name

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_name"):
                listener.enterDotted_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_name"):
                listener.exitDotted_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_name"):
                return visitor.visitDotted_name(self)
            else:
                return visitor.visitChildren(self)




    def dotted_name(self):

        localctx = SignalFlowV2Parser.Dotted_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_dotted_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 218
            self.match(SignalFlowV2Parser.ID)
            self.state = 223
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.DOT:
                self.state = 219
                self.match(SignalFlowV2Parser.DOT)
                self.state = 220
                self.match(SignalFlowV2Parser.ID)
                self.state = 225
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Return_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Return_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(SignalFlowV2Parser.RETURN, 0)

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_return_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterReturn_statement"):
                listener.enterReturn_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitReturn_statement"):
                listener.exitReturn_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitReturn_statement"):
                return visitor.visitReturn_statement(self)
            else:
                return visitor.visitChildren(self)




    def return_statement(self):

        localctx = SignalFlowV2Parser.Return_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_return_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 226
            self.match(SignalFlowV2Parser.RETURN)
            self.state = 228
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                self.state = 227
                self.testlist()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Flow_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Flow_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def return_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Return_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_flow_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterFlow_statement"):
                listener.enterFlow_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFlow_statement"):
                listener.exitFlow_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFlow_statement"):
                return visitor.visitFlow_statement(self)
            else:
                return visitor.visitChildren(self)




    def flow_statement(self):

        localctx = SignalFlowV2Parser.Flow_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_flow_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 230
            self.return_statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Compound_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Compound_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def if_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.If_statementContext,0)


        def function_definition(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Function_definitionContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_compound_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterCompound_statement"):
                listener.enterCompound_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitCompound_statement"):
                listener.exitCompound_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitCompound_statement"):
                return visitor.visitCompound_statement(self)
            else:
                return visitor.visitChildren(self)




    def compound_statement(self):

        localctx = SignalFlowV2Parser.Compound_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_compound_statement)
        try:
            self.state = 234
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.IF]:
                self.enterOuterAlt(localctx, 1)
                self.state = 232
                self.if_statement()

            elif token in [SignalFlowV2Parser.DEF]:
                self.enterOuterAlt(localctx, 2)
                self.state = 233
                self.function_definition()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class If_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.If_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(SignalFlowV2Parser.IF, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def suite(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.SuiteContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.SuiteContext,i)


        def ELIF(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ELIF)
            else:
                return self.getToken(SignalFlowV2Parser.ELIF, i)

        def ELSE(self):
            return self.getToken(SignalFlowV2Parser.ELSE, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_if_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterIf_statement"):
                listener.enterIf_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitIf_statement"):
                listener.exitIf_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitIf_statement"):
                return visitor.visitIf_statement(self)
            else:
                return visitor.visitChildren(self)




    def if_statement(self):

        localctx = SignalFlowV2Parser.If_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_if_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 236
            self.match(SignalFlowV2Parser.IF)
            self.state = 237
            self.test()
            self.state = 238
            self.match(SignalFlowV2Parser.COLON)
            self.state = 239
            self.suite()
            self.state = 247
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.ELIF:
                self.state = 240
                self.match(SignalFlowV2Parser.ELIF)
                self.state = 241
                self.test()
                self.state = 242
                self.match(SignalFlowV2Parser.COLON)
                self.state = 243
                self.suite()
                self.state = 249
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 253
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ELSE:
                self.state = 250
                self.match(SignalFlowV2Parser.ELSE)
                self.state = 251
                self.match(SignalFlowV2Parser.COLON)
                self.state = 252
                self.suite()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SuiteContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.SuiteContext, self).__init__(parent, invokingState)
            self.parser = parser

        def simple_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Simple_statementContext,0)


        def NEWLINE(self):
            return self.getToken(SignalFlowV2Parser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(SignalFlowV2Parser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(SignalFlowV2Parser.DEDENT, 0)

        def statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.StatementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.StatementContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_suite

        def enterRule(self, listener):
            if hasattr(listener, "enterSuite"):
                listener.enterSuite(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSuite"):
                listener.exitSuite(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSuite"):
                return visitor.visitSuite(self)
            else:
                return visitor.visitChildren(self)




    def suite(self):

        localctx = SignalFlowV2Parser.SuiteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_suite)
        self._la = 0 # Token type
        try:
            self.state = 265
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 255
                self.simple_statement()

            elif token in [SignalFlowV2Parser.NEWLINE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 256
                self.match(SignalFlowV2Parser.NEWLINE)
                self.state = 257
                self.match(SignalFlowV2Parser.INDENT)
                self.state = 259 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 258
                    self.statement()
                    self.state = 261 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DEF) | (1 << SignalFlowV2Parser.RETURN) | (1 << SignalFlowV2Parser.FROM) | (1 << SignalFlowV2Parser.IMPORT) | (1 << SignalFlowV2Parser.IF) | (1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS))) != 0)):
                        break

                self.state = 263
                self.match(SignalFlowV2Parser.DEDENT)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TestContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TestContext, self).__init__(parent, invokingState)
            self.parser = parser

        def or_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Or_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Or_testContext,i)


        def IF(self):
            return self.getToken(SignalFlowV2Parser.IF, 0)

        def ELSE(self):
            return self.getToken(SignalFlowV2Parser.ELSE, 0)

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def lambdef(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.LambdefContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_test

        def enterRule(self, listener):
            if hasattr(listener, "enterTest"):
                listener.enterTest(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTest"):
                listener.exitTest(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTest"):
                return visitor.visitTest(self)
            else:
                return visitor.visitChildren(self)




    def test(self):

        localctx = SignalFlowV2Parser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 276
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 267
                self.or_test()
                self.state = 273
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.IF:
                    self.state = 268
                    self.match(SignalFlowV2Parser.IF)
                    self.state = 269
                    self.or_test()
                    self.state = 270
                    self.match(SignalFlowV2Parser.ELSE)
                    self.state = 271
                    self.test()



            elif token in [SignalFlowV2Parser.LAMBDA]:
                self.enterOuterAlt(localctx, 2)
                self.state = 275
                self.lambdef()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LambdefContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.LambdefContext, self).__init__(parent, invokingState)
            self.parser = parser

        def LAMBDA(self):
            return self.getToken(SignalFlowV2Parser.LAMBDA, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def COLON(self):
            return self.getToken(SignalFlowV2Parser.COLON, 0)

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_lambdef

        def enterRule(self, listener):
            if hasattr(listener, "enterLambdef"):
                listener.enterLambdef(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitLambdef"):
                listener.exitLambdef(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitLambdef"):
                return visitor.visitLambdef(self)
            else:
                return visitor.visitChildren(self)




    def lambdef(self):

        localctx = SignalFlowV2Parser.LambdefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_lambdef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 278
            self.match(SignalFlowV2Parser.LAMBDA)
            self.state = 279
            self.match(SignalFlowV2Parser.ID)
            self.state = 280
            self.match(SignalFlowV2Parser.COLON)
            self.state = 281
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Or_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Or_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def and_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.And_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.And_testContext,i)


        def OR(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.OR)
            else:
                return self.getToken(SignalFlowV2Parser.OR, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_or_test

        def enterRule(self, listener):
            if hasattr(listener, "enterOr_test"):
                listener.enterOr_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitOr_test"):
                listener.exitOr_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitOr_test"):
                return visitor.visitOr_test(self)
            else:
                return visitor.visitChildren(self)




    def or_test(self):

        localctx = SignalFlowV2Parser.Or_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_or_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 283
            self.and_test()
            self.state = 288
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.OR:
                self.state = 284
                self.match(SignalFlowV2Parser.OR)
                self.state = 285
                self.and_test()
                self.state = 290
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class And_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.And_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def not_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Not_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Not_testContext,i)


        def AND(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.AND)
            else:
                return self.getToken(SignalFlowV2Parser.AND, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_and_test

        def enterRule(self, listener):
            if hasattr(listener, "enterAnd_test"):
                listener.enterAnd_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAnd_test"):
                listener.exitAnd_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAnd_test"):
                return visitor.visitAnd_test(self)
            else:
                return visitor.visitChildren(self)




    def and_test(self):

        localctx = SignalFlowV2Parser.And_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_and_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 291
            self.not_test()
            self.state = 296
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.AND:
                self.state = 292
                self.match(SignalFlowV2Parser.AND)
                self.state = 293
                self.not_test()
                self.state = 298
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Not_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Not_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(SignalFlowV2Parser.NOT, 0)

        def not_test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Not_testContext,0)


        def comparison(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.ComparisonContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_not_test

        def enterRule(self, listener):
            if hasattr(listener, "enterNot_test"):
                listener.enterNot_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitNot_test"):
                listener.exitNot_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitNot_test"):
                return visitor.visitNot_test(self)
            else:
                return visitor.visitChildren(self)




    def not_test(self):

        localctx = SignalFlowV2Parser.Not_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_not_test)
        try:
            self.state = 302
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.NOT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 299
                self.match(SignalFlowV2Parser.NOT)
                self.state = 300
                self.not_test()

            elif token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 2)
                self.state = 301
                self.comparison()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ComparisonContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ComparisonContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.ExprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.ExprContext,i)


        def LESS_THAN(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.LESS_THAN)
            else:
                return self.getToken(SignalFlowV2Parser.LESS_THAN, i)

        def LT_EQ(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.LT_EQ)
            else:
                return self.getToken(SignalFlowV2Parser.LT_EQ, i)

        def EQUALS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.EQUALS)
            else:
                return self.getToken(SignalFlowV2Parser.EQUALS, i)

        def NOT_EQ_1(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT_EQ_1)
            else:
                return self.getToken(SignalFlowV2Parser.NOT_EQ_1, i)

        def NOT_EQ_2(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT_EQ_2)
            else:
                return self.getToken(SignalFlowV2Parser.NOT_EQ_2, i)

        def GREATER_THAN(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.GREATER_THAN)
            else:
                return self.getToken(SignalFlowV2Parser.GREATER_THAN, i)

        def GT_EQ(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.GT_EQ)
            else:
                return self.getToken(SignalFlowV2Parser.GT_EQ, i)

        def IS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.IS)
            else:
                return self.getToken(SignalFlowV2Parser.IS, i)

        def NOT(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT)
            else:
                return self.getToken(SignalFlowV2Parser.NOT, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_comparison

        def enterRule(self, listener):
            if hasattr(listener, "enterComparison"):
                listener.enterComparison(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitComparison"):
                listener.exitComparison(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitComparison"):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = SignalFlowV2Parser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 304
            self.expr()
            self.state = 320
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.IS) | (1 << SignalFlowV2Parser.LESS_THAN) | (1 << SignalFlowV2Parser.GREATER_THAN) | (1 << SignalFlowV2Parser.EQUALS) | (1 << SignalFlowV2Parser.GT_EQ) | (1 << SignalFlowV2Parser.LT_EQ) | (1 << SignalFlowV2Parser.NOT_EQ_1) | (1 << SignalFlowV2Parser.NOT_EQ_2))) != 0):
                self.state = 315
                self._errHandler.sync(self);
                la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
                if la_ == 1:
                    self.state = 305
                    self.match(SignalFlowV2Parser.LESS_THAN)
                    pass

                elif la_ == 2:
                    self.state = 306
                    self.match(SignalFlowV2Parser.LT_EQ)
                    pass

                elif la_ == 3:
                    self.state = 307
                    self.match(SignalFlowV2Parser.EQUALS)
                    pass

                elif la_ == 4:
                    self.state = 308
                    self.match(SignalFlowV2Parser.NOT_EQ_1)
                    pass

                elif la_ == 5:
                    self.state = 309
                    self.match(SignalFlowV2Parser.NOT_EQ_2)
                    pass

                elif la_ == 6:
                    self.state = 310
                    self.match(SignalFlowV2Parser.GREATER_THAN)
                    pass

                elif la_ == 7:
                    self.state = 311
                    self.match(SignalFlowV2Parser.GT_EQ)
                    pass

                elif la_ == 8:
                    self.state = 312
                    self.match(SignalFlowV2Parser.IS)
                    pass

                elif la_ == 9:
                    self.state = 313
                    self.match(SignalFlowV2Parser.IS)
                    self.state = 314
                    self.match(SignalFlowV2Parser.NOT)
                    pass


                self.state = 317
                self.expr()
                self.state = 322
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ExprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def term(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TermContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TermContext,i)


        def ADD(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ADD)
            else:
                return self.getToken(SignalFlowV2Parser.ADD, i)

        def MINUS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.MINUS)
            else:
                return self.getToken(SignalFlowV2Parser.MINUS, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterExpr"):
                listener.enterExpr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitExpr"):
                listener.exitExpr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitExpr"):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = SignalFlowV2Parser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 323
            self.term()
            self.state = 328
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.ADD or _la==SignalFlowV2Parser.MINUS:
                self.state = 324
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.ADD or _la==SignalFlowV2Parser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 325
                self.term()
                self.state = 330
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TermContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TermContext, self).__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.FactorContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,i)


        def STAR(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.STAR)
            else:
                return self.getToken(SignalFlowV2Parser.STAR, i)

        def DIV(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.DIV)
            else:
                return self.getToken(SignalFlowV2Parser.DIV, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_term

        def enterRule(self, listener):
            if hasattr(listener, "enterTerm"):
                listener.enterTerm(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTerm"):
                listener.exitTerm(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTerm"):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = SignalFlowV2Parser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 331
            self.factor()
            self.state = 336
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.STAR or _la==SignalFlowV2Parser.DIV:
                self.state = 332
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.STAR or _la==SignalFlowV2Parser.DIV):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 333
                self.factor()
                self.state = 338
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FactorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.FactorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def factor(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,0)


        def ADD(self):
            return self.getToken(SignalFlowV2Parser.ADD, 0)

        def MINUS(self):
            return self.getToken(SignalFlowV2Parser.MINUS, 0)

        def power(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.PowerContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_factor

        def enterRule(self, listener):
            if hasattr(listener, "enterFactor"):
                listener.enterFactor(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFactor"):
                listener.exitFactor(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFactor"):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = SignalFlowV2Parser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_factor)
        self._la = 0 # Token type
        try:
            self.state = 342
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 339
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.ADD or _la==SignalFlowV2Parser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 340
                self.factor()

            elif token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK]:
                self.enterOuterAlt(localctx, 2)
                self.state = 341
                self.power()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PowerContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.PowerContext, self).__init__(parent, invokingState)
            self.parser = parser

        def atom_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Atom_exprContext,0)


        def POWER(self):
            return self.getToken(SignalFlowV2Parser.POWER, 0)

        def factor(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_power

        def enterRule(self, listener):
            if hasattr(listener, "enterPower"):
                listener.enterPower(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitPower"):
                listener.exitPower(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitPower"):
                return visitor.visitPower(self)
            else:
                return visitor.visitChildren(self)




    def power(self):

        localctx = SignalFlowV2Parser.PowerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_power)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 344
            self.atom_expr()
            self.state = 347
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.POWER:
                self.state = 345
                self.match(SignalFlowV2Parser.POWER)
                self.state = 346
                self.factor()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Atom_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Atom_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.AtomContext,0)


        def trailer(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TrailerContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TrailerContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_atom_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterAtom_expr"):
                listener.enterAtom_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAtom_expr"):
                listener.exitAtom_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAtom_expr"):
                return visitor.visitAtom_expr(self)
            else:
                return visitor.visitChildren(self)




    def atom_expr(self):

        localctx = SignalFlowV2Parser.Atom_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_atom_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 349
            self.atom()
            self.state = 353
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.DOT or _la==SignalFlowV2Parser.OPEN_PAREN:
                self.state = 350
                self.trailer()
                self.state = 355
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AtomContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.AtomContext, self).__init__(parent, invokingState)
            self.parser = parser

        def list_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.List_exprContext,0)


        def tuple_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Tuple_exprContext,0)


        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def INT(self):
            return self.getToken(SignalFlowV2Parser.INT, 0)

        def FLOAT(self):
            return self.getToken(SignalFlowV2Parser.FLOAT, 0)

        def STRING(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.STRING)
            else:
                return self.getToken(SignalFlowV2Parser.STRING, i)

        def NONE(self):
            return self.getToken(SignalFlowV2Parser.NONE, 0)

        def TRUE(self):
            return self.getToken(SignalFlowV2Parser.TRUE, 0)

        def FALSE(self):
            return self.getToken(SignalFlowV2Parser.FALSE, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_atom

        def enterRule(self, listener):
            if hasattr(listener, "enterAtom"):
                listener.enterAtom(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAtom"):
                listener.exitAtom(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAtom"):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = SignalFlowV2Parser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.state = 369
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.OPEN_BRACK]:
                self.enterOuterAlt(localctx, 1)
                self.state = 356
                self.list_expr()

            elif token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 357
                self.tuple_expr()

            elif token in [SignalFlowV2Parser.ID]:
                self.enterOuterAlt(localctx, 3)
                self.state = 358
                self.match(SignalFlowV2Parser.ID)

            elif token in [SignalFlowV2Parser.INT]:
                self.enterOuterAlt(localctx, 4)
                self.state = 359
                self.match(SignalFlowV2Parser.INT)

            elif token in [SignalFlowV2Parser.FLOAT]:
                self.enterOuterAlt(localctx, 5)
                self.state = 360
                self.match(SignalFlowV2Parser.FLOAT)

            elif token in [SignalFlowV2Parser.STRING]:
                self.enterOuterAlt(localctx, 6)
                self.state = 362 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 361
                    self.match(SignalFlowV2Parser.STRING)
                    self.state = 364 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==SignalFlowV2Parser.STRING):
                        break


            elif token in [SignalFlowV2Parser.NONE]:
                self.enterOuterAlt(localctx, 7)
                self.state = 366
                self.match(SignalFlowV2Parser.NONE)

            elif token in [SignalFlowV2Parser.TRUE]:
                self.enterOuterAlt(localctx, 8)
                self.state = 367
                self.match(SignalFlowV2Parser.TRUE)

            elif token in [SignalFlowV2Parser.FALSE]:
                self.enterOuterAlt(localctx, 9)
                self.state = 368
                self.match(SignalFlowV2Parser.FALSE)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class List_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.List_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_BRACK(self):
            return self.getToken(SignalFlowV2Parser.OPEN_BRACK, 0)

        def CLOSE_BRACK(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_BRACK, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_list_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterList_expr"):
                listener.enterList_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitList_expr"):
                listener.exitList_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitList_expr"):
                return visitor.visitList_expr(self)
            else:
                return visitor.visitChildren(self)




    def list_expr(self):

        localctx = SignalFlowV2Parser.List_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_list_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 371
            self.match(SignalFlowV2Parser.OPEN_BRACK)
            self.state = 380
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                self.state = 372
                self.test()
                self.state = 377
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==SignalFlowV2Parser.COMMA:
                    self.state = 373
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 374
                    self.test()
                    self.state = 379
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 382
            self.match(SignalFlowV2Parser.CLOSE_BRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Tuple_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Tuple_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_tuple_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterTuple_expr"):
                listener.enterTuple_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTuple_expr"):
                listener.exitTuple_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTuple_expr"):
                return visitor.visitTuple_expr(self)
            else:
                return visitor.visitChildren(self)




    def tuple_expr(self):

        localctx = SignalFlowV2Parser.Tuple_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_tuple_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 384
            self.match(SignalFlowV2Parser.OPEN_PAREN)
            self.state = 386
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                self.state = 385
                self.testlist()


            self.state = 388
            self.match(SignalFlowV2Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TestlistContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TestlistContext, self).__init__(parent, invokingState)
            self.parser = parser

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_testlist

        def enterRule(self, listener):
            if hasattr(listener, "enterTestlist"):
                listener.enterTestlist(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTestlist"):
                listener.exitTestlist(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTestlist"):
                return visitor.visitTestlist(self)
            else:
                return visitor.visitChildren(self)




    def testlist(self):

        localctx = SignalFlowV2Parser.TestlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_testlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 390
            self.test()
            self.state = 395
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,44,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 391
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 392
                    self.test() 
                self.state = 397
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,44,self._ctx)

            self.state = 399
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 398
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TrailerContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TrailerContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def actual_args(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Actual_argsContext,0)


        def DOT(self):
            return self.getToken(SignalFlowV2Parser.DOT, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_trailer

        def enterRule(self, listener):
            if hasattr(listener, "enterTrailer"):
                listener.enterTrailer(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTrailer"):
                listener.exitTrailer(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTrailer"):
                return visitor.visitTrailer(self)
            else:
                return visitor.visitChildren(self)




    def trailer(self):

        localctx = SignalFlowV2Parser.TrailerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_trailer)
        self._la = 0 # Token type
        try:
            self.state = 408
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.enterOuterAlt(localctx, 1)
                self.state = 401
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 403
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                    self.state = 402
                    self.actual_args()


                self.state = 405
                self.match(SignalFlowV2Parser.CLOSE_PAREN)

            elif token in [SignalFlowV2Parser.DOT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 406
                self.match(SignalFlowV2Parser.DOT)
                self.state = 407
                self.match(SignalFlowV2Parser.ID)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Actual_argsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Actual_argsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def argument(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.ArgumentContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.ArgumentContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_actual_args

        def enterRule(self, listener):
            if hasattr(listener, "enterActual_args"):
                listener.enterActual_args(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitActual_args"):
                listener.exitActual_args(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitActual_args"):
                return visitor.visitActual_args(self)
            else:
                return visitor.visitChildren(self)




    def actual_args(self):

        localctx = SignalFlowV2Parser.Actual_argsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_actual_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 410
            self.argument()
            self.state = 415
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 411
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 412
                self.argument()
                self.state = 417
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgumentContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ArgumentContext, self).__init__(parent, invokingState)
            self.parser = parser

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def ASSIGN(self):
            return self.getToken(SignalFlowV2Parser.ASSIGN, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_argument

        def enterRule(self, listener):
            if hasattr(listener, "enterArgument"):
                listener.enterArgument(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitArgument"):
                listener.exitArgument(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitArgument"):
                return visitor.visitArgument(self)
            else:
                return visitor.visitChildren(self)




    def argument(self):

        localctx = SignalFlowV2Parser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_argument)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 420
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
            if la_ == 1:
                self.state = 418
                self.match(SignalFlowV2Parser.ID)
                self.state = 419
                self.match(SignalFlowV2Parser.ASSIGN)


            self.state = 422
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





