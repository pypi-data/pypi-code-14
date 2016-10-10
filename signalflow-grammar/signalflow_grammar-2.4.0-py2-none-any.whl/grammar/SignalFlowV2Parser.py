# Generated from grammar/SignalFlowV2Parser.g4 by ANTLR 4.5.2
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"/\u0189\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write(u"\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write(u"\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4")
        buf.write(u"\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30")
        buf.write(u"\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t")
        buf.write(u"\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$")
        buf.write(u"\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\3\2\3")
        buf.write(u"\2\7\2Y\n\2\f\2\16\2\\\13\2\3\2\3\2\3\3\3\3\7\3b\n\3")
        buf.write(u"\f\3\16\3e\13\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3")
        buf.write(u"\5\5\5q\n\5\3\5\3\5\3\6\3\6\3\6\7\6x\n\6\f\6\16\6{\13")
        buf.write(u"\6\3\7\3\7\3\7\5\7\u0080\n\7\3\b\3\b\3\t\3\t\5\t\u0086")
        buf.write(u"\n\t\3\n\3\n\3\n\7\n\u008b\n\n\f\n\16\n\u008e\13\n\3")
        buf.write(u"\n\5\n\u0091\n\n\3\n\3\n\3\13\3\13\3\13\5\13\u0098\n")
        buf.write(u"\13\3\f\3\f\3\f\5\f\u009d\n\f\3\f\3\f\3\r\3\r\3\r\7\r")
        buf.write(u"\u00a4\n\r\f\r\16\r\u00a7\13\r\3\r\5\r\u00aa\n\r\3\16")
        buf.write(u"\3\16\5\16\u00ae\n\16\3\17\3\17\3\17\3\20\3\20\3\20\3")
        buf.write(u"\20\3\20\3\20\3\20\3\20\3\20\5\20\u00bc\n\20\3\21\3\21")
        buf.write(u"\3\21\5\21\u00c1\n\21\3\22\3\22\3\22\5\22\u00c6\n\22")
        buf.write(u"\3\23\3\23\3\23\7\23\u00cb\n\23\f\23\16\23\u00ce\13\23")
        buf.write(u"\3\23\5\23\u00d1\n\23\3\24\3\24\3\24\7\24\u00d6\n\24")
        buf.write(u"\f\24\16\24\u00d9\13\24\3\25\3\25\3\25\7\25\u00de\n\25")
        buf.write(u"\f\25\16\25\u00e1\13\25\3\26\3\26\5\26\u00e5\n\26\3\27")
        buf.write(u"\3\27\3\30\3\30\3\31\3\31\3\31\3\31\6\31\u00ef\n\31\r")
        buf.write(u"\31\16\31\u00f0\3\31\3\31\5\31\u00f5\n\31\3\32\3\32\3")
        buf.write(u"\32\3\32\3\32\3\32\5\32\u00fd\n\32\3\32\5\32\u0100\n")
        buf.write(u"\32\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34\7\34\u010a")
        buf.write(u"\n\34\f\34\16\34\u010d\13\34\3\35\3\35\3\35\7\35\u0112")
        buf.write(u"\n\35\f\35\16\35\u0115\13\35\3\36\3\36\3\36\5\36\u011a")
        buf.write(u"\n\36\3\37\3\37\3\37\7\37\u011f\n\37\f\37\16\37\u0122")
        buf.write(u"\13\37\3 \3 \3 \7 \u0127\n \f \16 \u012a\13 \3!\3!\3")
        buf.write(u"!\7!\u012f\n!\f!\16!\u0132\13!\3\"\3\"\3\"\5\"\u0137")
        buf.write(u"\n\"\3#\3#\3#\5#\u013c\n#\3$\3$\7$\u0140\n$\f$\16$\u0143")
        buf.write(u"\13$\3%\3%\3%\3%\3%\3%\6%\u014b\n%\r%\16%\u014c\3%\3")
        buf.write(u"%\3%\5%\u0152\n%\3&\3&\3&\3&\7&\u0158\n&\f&\16&\u015b")
        buf.write(u"\13&\5&\u015d\n&\3&\3&\3\'\3\'\5\'\u0163\n\'\3\'\3\'")
        buf.write(u"\3(\3(\3(\7(\u016a\n(\f(\16(\u016d\13(\3(\5(\u0170\n")
        buf.write(u"(\3)\3)\5)\u0174\n)\3)\3)\3)\5)\u0179\n)\3*\3*\3*\7*")
        buf.write(u"\u017e\n*\f*\16*\u0181\13*\3+\3+\5+\u0185\n+\3+\3+\3")
        buf.write(u"+\2\2,\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*")
        buf.write(u",.\60\62\64\668:<>@BDFHJLNPRT\2\6\3\3++\3\2\21\26\3\2")
        buf.write(u"$%\3\2&\'\u0195\2Z\3\2\2\2\4_\3\2\2\2\6h\3\2\2\2\bn\3")
        buf.write(u"\2\2\2\nt\3\2\2\2\f|\3\2\2\2\16\u0081\3\2\2\2\20\u0085")
        buf.write(u"\3\2\2\2\22\u0087\3\2\2\2\24\u0097\3\2\2\2\26\u009c\3")
        buf.write(u"\2\2\2\30\u00a0\3\2\2\2\32\u00ad\3\2\2\2\34\u00af\3\2")
        buf.write(u"\2\2\36\u00b2\3\2\2\2 \u00bd\3\2\2\2\"\u00c2\3\2\2\2")
        buf.write(u"$\u00c7\3\2\2\2&\u00d2\3\2\2\2(\u00da\3\2\2\2*\u00e2")
        buf.write(u"\3\2\2\2,\u00e6\3\2\2\2.\u00e8\3\2\2\2\60\u00f4\3\2\2")
        buf.write(u"\2\62\u00ff\3\2\2\2\64\u0101\3\2\2\2\66\u0106\3\2\2\2")
        buf.write(u"8\u010e\3\2\2\2:\u0119\3\2\2\2<\u011b\3\2\2\2>\u0123")
        buf.write(u"\3\2\2\2@\u012b\3\2\2\2B\u0136\3\2\2\2D\u0138\3\2\2\2")
        buf.write(u"F\u013d\3\2\2\2H\u0151\3\2\2\2J\u0153\3\2\2\2L\u0160")
        buf.write(u"\3\2\2\2N\u0166\3\2\2\2P\u0178\3\2\2\2R\u017a\3\2\2\2")
        buf.write(u"T\u0184\3\2\2\2VY\7+\2\2WY\5\20\t\2XV\3\2\2\2XW\3\2\2")
        buf.write(u"\2Y\\\3\2\2\2ZX\3\2\2\2Z[\3\2\2\2[]\3\2\2\2\\Z\3\2\2")
        buf.write(u"\2]^\7\2\2\3^\3\3\2\2\2_c\5N(\2`b\7+\2\2a`\3\2\2\2be")
        buf.write(u"\3\2\2\2ca\3\2\2\2cd\3\2\2\2df\3\2\2\2ec\3\2\2\2fg\7")
        buf.write(u"\2\2\3g\5\3\2\2\2hi\7\3\2\2ij\7\32\2\2jk\5\b\5\2kl\7")
        buf.write(u"#\2\2lm\5\60\31\2m\7\3\2\2\2np\7\33\2\2oq\5\n\6\2po\3")
        buf.write(u"\2\2\2pq\3\2\2\2qr\3\2\2\2rs\7\34\2\2s\t\3\2\2\2ty\5")
        buf.write(u"\f\7\2uv\7!\2\2vx\5\f\7\2wu\3\2\2\2x{\3\2\2\2yw\3\2\2")
        buf.write(u"\2yz\3\2\2\2z\13\3\2\2\2{y\3\2\2\2|\177\5\16\b\2}~\7")
        buf.write(u")\2\2~\u0080\5\62\32\2\177}\3\2\2\2\177\u0080\3\2\2\2")
        buf.write(u"\u0080\r\3\2\2\2\u0081\u0082\7\32\2\2\u0082\17\3\2\2")
        buf.write(u"\2\u0083\u0086\5\22\n\2\u0084\u0086\5.\30\2\u0085\u0083")
        buf.write(u"\3\2\2\2\u0085\u0084\3\2\2\2\u0086\21\3\2\2\2\u0087\u008c")
        buf.write(u"\5\24\13\2\u0088\u0089\7\"\2\2\u0089\u008b\5\24\13\2")
        buf.write(u"\u008a\u0088\3\2\2\2\u008b\u008e\3\2\2\2\u008c\u008a")
        buf.write(u"\3\2\2\2\u008c\u008d\3\2\2\2\u008d\u0090\3\2\2\2\u008e")
        buf.write(u"\u008c\3\2\2\2\u008f\u0091\7\"\2\2\u0090\u008f\3\2\2")
        buf.write(u"\2\u0090\u0091\3\2\2\2\u0091\u0092\3\2\2\2\u0092\u0093")
        buf.write(u"\t\2\2\2\u0093\23\3\2\2\2\u0094\u0098\5\26\f\2\u0095")
        buf.write(u"\u0098\5,\27\2\u0096\u0098\5\32\16\2\u0097\u0094\3\2")
        buf.write(u"\2\2\u0097\u0095\3\2\2\2\u0097\u0096\3\2\2\2\u0098\25")
        buf.write(u"\3\2\2\2\u0099\u009a\5\30\r\2\u009a\u009b\7)\2\2\u009b")
        buf.write(u"\u009d\3\2\2\2\u009c\u0099\3\2\2\2\u009c\u009d\3\2\2")
        buf.write(u"\2\u009d\u009e\3\2\2\2\u009e\u009f\5N(\2\u009f\27\3\2")
        buf.write(u"\2\2\u00a0\u00a5\7\32\2\2\u00a1\u00a2\7!\2\2\u00a2\u00a4")
        buf.write(u"\7\32\2\2\u00a3\u00a1\3\2\2\2\u00a4\u00a7\3\2\2\2\u00a5")
        buf.write(u"\u00a3\3\2\2\2\u00a5\u00a6\3\2\2\2\u00a6\u00a9\3\2\2")
        buf.write(u"\2\u00a7\u00a5\3\2\2\2\u00a8\u00aa\7!\2\2\u00a9\u00a8")
        buf.write(u"\3\2\2\2\u00a9\u00aa\3\2\2\2\u00aa\31\3\2\2\2\u00ab\u00ae")
        buf.write(u"\5\34\17\2\u00ac\u00ae\5\36\20\2\u00ad\u00ab\3\2\2\2")
        buf.write(u"\u00ad\u00ac\3\2\2\2\u00ae\33\3\2\2\2\u00af\u00b0\7\6")
        buf.write(u"\2\2\u00b0\u00b1\5&\24\2\u00b1\35\3\2\2\2\u00b2\u00b3")
        buf.write(u"\7\5\2\2\u00b3\u00b4\5(\25\2\u00b4\u00bb\7\6\2\2\u00b5")
        buf.write(u"\u00bc\7&\2\2\u00b6\u00b7\7\33\2\2\u00b7\u00b8\5$\23")
        buf.write(u"\2\u00b8\u00b9\7\34\2\2\u00b9\u00bc\3\2\2\2\u00ba\u00bc")
        buf.write(u"\5$\23\2\u00bb\u00b5\3\2\2\2\u00bb\u00b6\3\2\2\2\u00bb")
        buf.write(u"\u00ba\3\2\2\2\u00bc\37\3\2\2\2\u00bd\u00c0\7\32\2\2")
        buf.write(u"\u00be\u00bf\7\7\2\2\u00bf\u00c1\7\32\2\2\u00c0\u00be")
        buf.write(u"\3\2\2\2\u00c0\u00c1\3\2\2\2\u00c1!\3\2\2\2\u00c2\u00c5")
        buf.write(u"\5(\25\2\u00c3\u00c4\7\7\2\2\u00c4\u00c6\7\32\2\2\u00c5")
        buf.write(u"\u00c3\3\2\2\2\u00c5\u00c6\3\2\2\2\u00c6#\3\2\2\2\u00c7")
        buf.write(u"\u00cc\5 \21\2\u00c8\u00c9\7!\2\2\u00c9\u00cb\5 \21\2")
        buf.write(u"\u00ca\u00c8\3\2\2\2\u00cb\u00ce\3\2\2\2\u00cc\u00ca")
        buf.write(u"\3\2\2\2\u00cc\u00cd\3\2\2\2\u00cd\u00d0\3\2\2\2\u00ce")
        buf.write(u"\u00cc\3\2\2\2\u00cf\u00d1\7!\2\2\u00d0\u00cf\3\2\2\2")
        buf.write(u"\u00d0\u00d1\3\2\2\2\u00d1%\3\2\2\2\u00d2\u00d7\5\"\22")
        buf.write(u"\2\u00d3\u00d4\7!\2\2\u00d4\u00d6\5\"\22\2\u00d5\u00d3")
        buf.write(u"\3\2\2\2\u00d6\u00d9\3\2\2\2\u00d7\u00d5\3\2\2\2\u00d7")
        buf.write(u"\u00d8\3\2\2\2\u00d8\'\3\2\2\2\u00d9\u00d7\3\2\2\2\u00da")
        buf.write(u"\u00df\7\32\2\2\u00db\u00dc\7*\2\2\u00dc\u00de\7\32\2")
        buf.write(u"\2\u00dd\u00db\3\2\2\2\u00de\u00e1\3\2\2\2\u00df\u00dd")
        buf.write(u"\3\2\2\2\u00df\u00e0\3\2\2\2\u00e0)\3\2\2\2\u00e1\u00df")
        buf.write(u"\3\2\2\2\u00e2\u00e4\7\4\2\2\u00e3\u00e5\5N(\2\u00e4")
        buf.write(u"\u00e3\3\2\2\2\u00e4\u00e5\3\2\2\2\u00e5+\3\2\2\2\u00e6")
        buf.write(u"\u00e7\5*\26\2\u00e7-\3\2\2\2\u00e8\u00e9\5\6\4\2\u00e9")
        buf.write(u"/\3\2\2\2\u00ea\u00f5\5\22\n\2\u00eb\u00ec\7+\2\2\u00ec")
        buf.write(u"\u00ee\7.\2\2\u00ed\u00ef\5\20\t\2\u00ee\u00ed\3\2\2")
        buf.write(u"\2\u00ef\u00f0\3\2\2\2\u00f0\u00ee\3\2\2\2\u00f0\u00f1")
        buf.write(u"\3\2\2\2\u00f1\u00f2\3\2\2\2\u00f2\u00f3\7/\2\2\u00f3")
        buf.write(u"\u00f5\3\2\2\2\u00f4\u00ea\3\2\2\2\u00f4\u00eb\3\2\2")
        buf.write(u"\2\u00f5\61\3\2\2\2\u00f6\u00fc\5\66\34\2\u00f7\u00f8")
        buf.write(u"\7\f\2\2\u00f8\u00f9\5\66\34\2\u00f9\u00fa\7\r\2\2\u00fa")
        buf.write(u"\u00fb\5\62\32\2\u00fb\u00fd\3\2\2\2\u00fc\u00f7\3\2")
        buf.write(u"\2\2\u00fc\u00fd\3\2\2\2\u00fd\u0100\3\2\2\2\u00fe\u0100")
        buf.write(u"\5\64\33\2\u00ff\u00f6\3\2\2\2\u00ff\u00fe\3\2\2\2\u0100")
        buf.write(u"\63\3\2\2\2\u0101\u0102\7\b\2\2\u0102\u0103\7\32\2\2")
        buf.write(u"\u0103\u0104\7#\2\2\u0104\u0105\5\62\32\2\u0105\65\3")
        buf.write(u"\2\2\2\u0106\u010b\58\35\2\u0107\u0108\7\27\2\2\u0108")
        buf.write(u"\u010a\58\35\2\u0109\u0107\3\2\2\2\u010a\u010d\3\2\2")
        buf.write(u"\2\u010b\u0109\3\2\2\2\u010b\u010c\3\2\2\2\u010c\67\3")
        buf.write(u"\2\2\2\u010d\u010b\3\2\2\2\u010e\u0113\5:\36\2\u010f")
        buf.write(u"\u0110\7\30\2\2\u0110\u0112\5:\36\2\u0111\u010f\3\2\2")
        buf.write(u"\2\u0112\u0115\3\2\2\2\u0113\u0111\3\2\2\2\u0113\u0114")
        buf.write(u"\3\2\2\2\u01149\3\2\2\2\u0115\u0113\3\2\2\2\u0116\u0117")
        buf.write(u"\7\31\2\2\u0117\u011a\5:\36\2\u0118\u011a\5<\37\2\u0119")
        buf.write(u"\u0116\3\2\2\2\u0119\u0118\3\2\2\2\u011a;\3\2\2\2\u011b")
        buf.write(u"\u0120\5> \2\u011c\u011d\t\3\2\2\u011d\u011f\5> \2\u011e")
        buf.write(u"\u011c\3\2\2\2\u011f\u0122\3\2\2\2\u0120\u011e\3\2\2")
        buf.write(u"\2\u0120\u0121\3\2\2\2\u0121=\3\2\2\2\u0122\u0120\3\2")
        buf.write(u"\2\2\u0123\u0128\5@!\2\u0124\u0125\t\4\2\2\u0125\u0127")
        buf.write(u"\5@!\2\u0126\u0124\3\2\2\2\u0127\u012a\3\2\2\2\u0128")
        buf.write(u"\u0126\3\2\2\2\u0128\u0129\3\2\2\2\u0129?\3\2\2\2\u012a")
        buf.write(u"\u0128\3\2\2\2\u012b\u0130\5B\"\2\u012c\u012d\t\5\2\2")
        buf.write(u"\u012d\u012f\5B\"\2\u012e\u012c\3\2\2\2\u012f\u0132\3")
        buf.write(u"\2\2\2\u0130\u012e\3\2\2\2\u0130\u0131\3\2\2\2\u0131")
        buf.write(u"A\3\2\2\2\u0132\u0130\3\2\2\2\u0133\u0134\t\4\2\2\u0134")
        buf.write(u"\u0137\5B\"\2\u0135\u0137\5D#\2\u0136\u0133\3\2\2\2\u0136")
        buf.write(u"\u0135\3\2\2\2\u0137C\3\2\2\2\u0138\u013b\5F$\2\u0139")
        buf.write(u"\u013a\7(\2\2\u013a\u013c\5B\"\2\u013b\u0139\3\2\2\2")
        buf.write(u"\u013b\u013c\3\2\2\2\u013cE\3\2\2\2\u013d\u0141\5H%\2")
        buf.write(u"\u013e\u0140\5P)\2\u013f\u013e\3\2\2\2\u0140\u0143\3")
        buf.write(u"\2\2\2\u0141\u013f\3\2\2\2\u0141\u0142\3\2\2\2\u0142")
        buf.write(u"G\3\2\2\2\u0143\u0141\3\2\2\2\u0144\u0152\5J&\2\u0145")
        buf.write(u"\u0152\5L\'\2\u0146\u0152\7\32\2\2\u0147\u0152\7\16\2")
        buf.write(u"\2\u0148\u0152\7\17\2\2\u0149\u014b\7\20\2\2\u014a\u0149")
        buf.write(u"\3\2\2\2\u014b\u014c\3\2\2\2\u014c\u014a\3\2\2\2\u014c")
        buf.write(u"\u014d\3\2\2\2\u014d\u0152\3\2\2\2\u014e\u0152\7\t\2")
        buf.write(u"\2\u014f\u0152\7\n\2\2\u0150\u0152\7\13\2\2\u0151\u0144")
        buf.write(u"\3\2\2\2\u0151\u0145\3\2\2\2\u0151\u0146\3\2\2\2\u0151")
        buf.write(u"\u0147\3\2\2\2\u0151\u0148\3\2\2\2\u0151\u014a\3\2\2")
        buf.write(u"\2\u0151\u014e\3\2\2\2\u0151\u014f\3\2\2\2\u0151\u0150")
        buf.write(u"\3\2\2\2\u0152I\3\2\2\2\u0153\u015c\7\35\2\2\u0154\u0159")
        buf.write(u"\5\62\32\2\u0155\u0156\7!\2\2\u0156\u0158\5\62\32\2\u0157")
        buf.write(u"\u0155\3\2\2\2\u0158\u015b\3\2\2\2\u0159\u0157\3\2\2")
        buf.write(u"\2\u0159\u015a\3\2\2\2\u015a\u015d\3\2\2\2\u015b\u0159")
        buf.write(u"\3\2\2\2\u015c\u0154\3\2\2\2\u015c\u015d\3\2\2\2\u015d")
        buf.write(u"\u015e\3\2\2\2\u015e\u015f\7\36\2\2\u015fK\3\2\2\2\u0160")
        buf.write(u"\u0162\7\33\2\2\u0161\u0163\5N(\2\u0162\u0161\3\2\2\2")
        buf.write(u"\u0162\u0163\3\2\2\2\u0163\u0164\3\2\2\2\u0164\u0165")
        buf.write(u"\7\34\2\2\u0165M\3\2\2\2\u0166\u016b\5\62\32\2\u0167")
        buf.write(u"\u0168\7!\2\2\u0168\u016a\5\62\32\2\u0169\u0167\3\2\2")
        buf.write(u"\2\u016a\u016d\3\2\2\2\u016b\u0169\3\2\2\2\u016b\u016c")
        buf.write(u"\3\2\2\2\u016c\u016f\3\2\2\2\u016d\u016b\3\2\2\2\u016e")
        buf.write(u"\u0170\7!\2\2\u016f\u016e\3\2\2\2\u016f\u0170\3\2\2\2")
        buf.write(u"\u0170O\3\2\2\2\u0171\u0173\7\33\2\2\u0172\u0174\5R*")
        buf.write(u"\2\u0173\u0172\3\2\2\2\u0173\u0174\3\2\2\2\u0174\u0175")
        buf.write(u"\3\2\2\2\u0175\u0179\7\34\2\2\u0176\u0177\7*\2\2\u0177")
        buf.write(u"\u0179\7\32\2\2\u0178\u0171\3\2\2\2\u0178\u0176\3\2\2")
        buf.write(u"\2\u0179Q\3\2\2\2\u017a\u017f\5T+\2\u017b\u017c\7!\2")
        buf.write(u"\2\u017c\u017e\5T+\2\u017d\u017b\3\2\2\2\u017e\u0181")
        buf.write(u"\3\2\2\2\u017f\u017d\3\2\2\2\u017f\u0180\3\2\2\2\u0180")
        buf.write(u"S\3\2\2\2\u0181\u017f\3\2\2\2\u0182\u0183\7\32\2\2\u0183")
        buf.write(u"\u0185\7)\2\2\u0184\u0182\3\2\2\2\u0184\u0185\3\2\2\2")
        buf.write(u"\u0185\u0186\3\2\2\2\u0186\u0187\5\62\32\2\u0187U\3\2")
        buf.write(u"\2\2\60XZcpy\177\u0085\u008c\u0090\u0097\u009c\u00a5")
        buf.write(u"\u00a9\u00ad\u00bb\u00c0\u00c5\u00cc\u00d0\u00d7\u00df")
        buf.write(u"\u00e4\u00f0\u00f4\u00fc\u00ff\u010b\u0113\u0119\u0120")
        buf.write(u"\u0128\u0130\u0136\u013b\u0141\u014c\u0151\u0159\u015c")
        buf.write(u"\u0162\u016b\u016f\u0173\u0178\u017f\u0184")
        return buf.getvalue()


class SignalFlowV2Parser ( Parser ):

    grammarFileName = "SignalFlowV2Parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'def'", u"'return'", u"'from'", u"'import'", 
                     u"'as'", u"'lambda'", u"'None'", u"'True'", u"'False'", 
                     u"'if'", u"'else'", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                     u"'<='", u"'>='", u"'=='", u"'!='", u"'<'", u"'>'", 
                     u"'or'", u"'and'", u"'not'", u"<INVALID>", u"'('", 
                     u"')'", u"'['", u"']'", u"'{'", u"'}'", u"','", u"';'", 
                     u"':'", u"'+'", u"'-'", u"'*'", u"'/'", u"'**'", u"'='", 
                     u"'.'" ]

    symbolicNames = [ u"<INVALID>", u"DEF", u"RETURN", u"FROM", u"IMPORT", 
                      u"AS", u"LAMBDA", u"NONE", u"TRUE", u"FALSE", u"IF", 
                      u"ELSE", u"INT", u"FLOAT", u"STRING", u"LE", u"GE", 
                      u"EQ", u"NE", u"LT", u"GT", u"OR", u"AND", u"NOT", 
                      u"ID", u"OPEN_PAREN", u"CLOSE_PAREN", u"LSQUARE", 
                      u"RSQUARE", u"LBRACE", u"RBRACE", u"COMMA", u"SEMICOLON", 
                      u"COLON", u"PLUS", u"MINUS", u"MUL", u"DIV", u"POW", 
                      u"BINDING", u"DOT", u"NEWLINE", u"SKIP_", u"COMMENT", 
                      u"INDENT", u"DEDENT" ]

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
    RULE_suite = 23
    RULE_test = 24
    RULE_lambdef = 25
    RULE_or_test = 26
    RULE_and_test = 27
    RULE_not_test = 28
    RULE_comparison = 29
    RULE_expr = 30
    RULE_term = 31
    RULE_factor = 32
    RULE_power = 33
    RULE_atom_expr = 34
    RULE_atom = 35
    RULE_list_expr = 36
    RULE_tuple_expr = 37
    RULE_testlist = 38
    RULE_trailer = 39
    RULE_actual_args = 40
    RULE_argument = 41

    ruleNames =  [ u"program", u"eval_input", u"function_definition", u"parameters", 
                   u"var_args_list", u"var_args_list_param_def", u"var_args_list_param_name", 
                   u"statement", u"simple_statement", u"small_statement", 
                   u"expr_statement", u"id_list", u"import_statement", u"import_name", 
                   u"import_from", u"import_as_name", u"dotted_as_name", 
                   u"import_as_names", u"dotted_as_names", u"dotted_name", 
                   u"return_statement", u"flow_statement", u"compound_statement", 
                   u"suite", u"test", u"lambdef", u"or_test", u"and_test", 
                   u"not_test", u"comparison", u"expr", u"term", u"factor", 
                   u"power", u"atom_expr", u"atom", u"list_expr", u"tuple_expr", 
                   u"testlist", u"trailer", u"actual_args", u"argument" ]

    EOF = Token.EOF
    DEF=1
    RETURN=2
    FROM=3
    IMPORT=4
    AS=5
    LAMBDA=6
    NONE=7
    TRUE=8
    FALSE=9
    IF=10
    ELSE=11
    INT=12
    FLOAT=13
    STRING=14
    LE=15
    GE=16
    EQ=17
    NE=18
    LT=19
    GT=20
    OR=21
    AND=22
    NOT=23
    ID=24
    OPEN_PAREN=25
    CLOSE_PAREN=26
    LSQUARE=27
    RSQUARE=28
    LBRACE=29
    RBRACE=30
    COMMA=31
    SEMICOLON=32
    COLON=33
    PLUS=34
    MINUS=35
    MUL=36
    DIV=37
    POW=38
    BINDING=39
    DOT=40
    NEWLINE=41
    SKIP_=42
    COMMENT=43
    INDENT=44
    DEDENT=45

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
            self.state = 88
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DEF) | (1 << SignalFlowV2Parser.RETURN) | (1 << SignalFlowV2Parser.FROM) | (1 << SignalFlowV2Parser.IMPORT) | (1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.LSQUARE) | (1 << SignalFlowV2Parser.PLUS) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NEWLINE))) != 0):
                self.state = 86
                token = self._input.LA(1)
                if token in [SignalFlowV2Parser.NEWLINE]:
                    self.state = 84
                    self.match(SignalFlowV2Parser.NEWLINE)

                elif token in [SignalFlowV2Parser.DEF, SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.STRING, SignalFlowV2Parser.NOT, SignalFlowV2Parser.ID, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.LSQUARE, SignalFlowV2Parser.PLUS, SignalFlowV2Parser.MINUS]:
                    self.state = 85
                    self.statement()

                else:
                    raise NoViableAltException(self)

                self.state = 90
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 91
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
            self.state = 93
            self.testlist()
            self.state = 97
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.NEWLINE:
                self.state = 94
                self.match(SignalFlowV2Parser.NEWLINE)
                self.state = 99
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 100
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
            self.state = 102
            self.match(SignalFlowV2Parser.DEF)
            self.state = 103
            self.match(SignalFlowV2Parser.ID)
            self.state = 104
            self.parameters()
            self.state = 105
            self.match(SignalFlowV2Parser.COLON)
            self.state = 106
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
            self.state = 108
            self.match(SignalFlowV2Parser.OPEN_PAREN)
            self.state = 110
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ID:
                self.state = 109
                self.var_args_list()


            self.state = 112
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
            self.state = 114
            self.var_args_list_param_def()
            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 115
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 116
                self.var_args_list_param_def()
                self.state = 121
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
            self.state = 122
            self.var_args_list_param_name()
            self.state = 125
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.BINDING:
                self.state = 123
                self.match(SignalFlowV2Parser.BINDING)
                self.state = 124
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
            self.state = 127
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
            self.state = 131
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.STRING, SignalFlowV2Parser.NOT, SignalFlowV2Parser.ID, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.LSQUARE, SignalFlowV2Parser.PLUS, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 129
                self.simple_statement()

            elif token in [SignalFlowV2Parser.DEF]:
                self.enterOuterAlt(localctx, 2)
                self.state = 130
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
            self.state = 133
            self.small_statement()
            self.state = 138
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 134
                    self.match(SignalFlowV2Parser.SEMICOLON)
                    self.state = 135
                    self.small_statement() 
                self.state = 140
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

            self.state = 142
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.SEMICOLON:
                self.state = 141
                self.match(SignalFlowV2Parser.SEMICOLON)


            self.state = 144
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
            self.state = 149
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.STRING, SignalFlowV2Parser.NOT, SignalFlowV2Parser.ID, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.LSQUARE, SignalFlowV2Parser.PLUS, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 146
                self.expr_statement()

            elif token in [SignalFlowV2Parser.RETURN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 147
                self.flow_statement()

            elif token in [SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 148
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


        def BINDING(self):
            return self.getToken(SignalFlowV2Parser.BINDING, 0)

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
            self.state = 154
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 151
                self.id_list()
                self.state = 152
                self.match(SignalFlowV2Parser.BINDING)


            self.state = 156
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
            self.state = 158
            self.match(SignalFlowV2Parser.ID)
            self.state = 163
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 159
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 160
                    self.match(SignalFlowV2Parser.ID) 
                self.state = 165
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

            self.state = 167
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 166
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
            self.state = 171
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.IMPORT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 169
                self.import_name()

            elif token in [SignalFlowV2Parser.FROM]:
                self.enterOuterAlt(localctx, 2)
                self.state = 170
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
            self.state = 173
            self.match(SignalFlowV2Parser.IMPORT)
            self.state = 174
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
            self.state = 176
            self.match(SignalFlowV2Parser.FROM)
            self.state = 177
            self.dotted_name()
            self.state = 178
            self.match(SignalFlowV2Parser.IMPORT)
            self.state = 185
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.MUL]:
                self.state = 179
                self.match(SignalFlowV2Parser.MUL)

            elif token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.state = 180
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 181
                self.import_as_names()
                self.state = 182
                self.match(SignalFlowV2Parser.CLOSE_PAREN)

            elif token in [SignalFlowV2Parser.ID]:
                self.state = 184
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
            self.state = 187
            self.match(SignalFlowV2Parser.ID)
            self.state = 190
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.AS:
                self.state = 188
                self.match(SignalFlowV2Parser.AS)
                self.state = 189
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
            self.state = 192
            self.dotted_name()
            self.state = 195
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.AS:
                self.state = 193
                self.match(SignalFlowV2Parser.AS)
                self.state = 194
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
            self.state = 197
            self.import_as_name()
            self.state = 202
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 198
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 199
                    self.import_as_name() 
                self.state = 204
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

            self.state = 206
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 205
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
            self.state = 208
            self.dotted_as_name()
            self.state = 213
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 209
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 210
                self.dotted_as_name()
                self.state = 215
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
            self.state = 216
            self.match(SignalFlowV2Parser.ID)
            self.state = 221
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.DOT:
                self.state = 217
                self.match(SignalFlowV2Parser.DOT)
                self.state = 218
                self.match(SignalFlowV2Parser.ID)
                self.state = 223
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
            self.state = 224
            self.match(SignalFlowV2Parser.RETURN)
            self.state = 226
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.LSQUARE) | (1 << SignalFlowV2Parser.PLUS) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                self.state = 225
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
            self.state = 228
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
            self.enterOuterAlt(localctx, 1)
            self.state = 230
            self.function_definition()
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
        self.enterRule(localctx, 46, self.RULE_suite)
        self._la = 0 # Token type
        try:
            self.state = 242
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.STRING, SignalFlowV2Parser.NOT, SignalFlowV2Parser.ID, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.LSQUARE, SignalFlowV2Parser.PLUS, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 232
                self.simple_statement()

            elif token in [SignalFlowV2Parser.NEWLINE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 233
                self.match(SignalFlowV2Parser.NEWLINE)
                self.state = 234
                self.match(SignalFlowV2Parser.INDENT)
                self.state = 236 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 235
                    self.statement()
                    self.state = 238 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DEF) | (1 << SignalFlowV2Parser.RETURN) | (1 << SignalFlowV2Parser.FROM) | (1 << SignalFlowV2Parser.IMPORT) | (1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.LSQUARE) | (1 << SignalFlowV2Parser.PLUS) | (1 << SignalFlowV2Parser.MINUS))) != 0)):
                        break

                self.state = 240
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
        self.enterRule(localctx, 48, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 253
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.STRING, SignalFlowV2Parser.NOT, SignalFlowV2Parser.ID, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.LSQUARE, SignalFlowV2Parser.PLUS, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 244
                self.or_test()
                self.state = 250
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.IF:
                    self.state = 245
                    self.match(SignalFlowV2Parser.IF)
                    self.state = 246
                    self.or_test()
                    self.state = 247
                    self.match(SignalFlowV2Parser.ELSE)
                    self.state = 248
                    self.test()



            elif token in [SignalFlowV2Parser.LAMBDA]:
                self.enterOuterAlt(localctx, 2)
                self.state = 252
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
        self.enterRule(localctx, 50, self.RULE_lambdef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 255
            self.match(SignalFlowV2Parser.LAMBDA)
            self.state = 256
            self.match(SignalFlowV2Parser.ID)
            self.state = 257
            self.match(SignalFlowV2Parser.COLON)
            self.state = 258
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
        self.enterRule(localctx, 52, self.RULE_or_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 260
            self.and_test()
            self.state = 265
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.OR:
                self.state = 261
                self.match(SignalFlowV2Parser.OR)
                self.state = 262
                self.and_test()
                self.state = 267
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
        self.enterRule(localctx, 54, self.RULE_and_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 268
            self.not_test()
            self.state = 273
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.AND:
                self.state = 269
                self.match(SignalFlowV2Parser.AND)
                self.state = 270
                self.not_test()
                self.state = 275
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
        self.enterRule(localctx, 56, self.RULE_not_test)
        try:
            self.state = 279
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.NOT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 276
                self.match(SignalFlowV2Parser.NOT)
                self.state = 277
                self.not_test()

            elif token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.STRING, SignalFlowV2Parser.ID, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.LSQUARE, SignalFlowV2Parser.PLUS, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 2)
                self.state = 278
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


        def LT(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.LT)
            else:
                return self.getToken(SignalFlowV2Parser.LT, i)

        def LE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.LE)
            else:
                return self.getToken(SignalFlowV2Parser.LE, i)

        def EQ(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.EQ)
            else:
                return self.getToken(SignalFlowV2Parser.EQ, i)

        def NE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NE)
            else:
                return self.getToken(SignalFlowV2Parser.NE, i)

        def GT(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.GT)
            else:
                return self.getToken(SignalFlowV2Parser.GT, i)

        def GE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.GE)
            else:
                return self.getToken(SignalFlowV2Parser.GE, i)

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
        self.enterRule(localctx, 58, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 281
            self.expr()
            self.state = 286
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LE) | (1 << SignalFlowV2Parser.GE) | (1 << SignalFlowV2Parser.EQ) | (1 << SignalFlowV2Parser.NE) | (1 << SignalFlowV2Parser.LT) | (1 << SignalFlowV2Parser.GT))) != 0):
                self.state = 282
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LE) | (1 << SignalFlowV2Parser.GE) | (1 << SignalFlowV2Parser.EQ) | (1 << SignalFlowV2Parser.NE) | (1 << SignalFlowV2Parser.LT) | (1 << SignalFlowV2Parser.GT))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 283
                self.expr()
                self.state = 288
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


        def PLUS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.PLUS)
            else:
                return self.getToken(SignalFlowV2Parser.PLUS, i)

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
        self.enterRule(localctx, 60, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 289
            self.term()
            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.PLUS or _la==SignalFlowV2Parser.MINUS:
                self.state = 290
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.PLUS or _la==SignalFlowV2Parser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 291
                self.term()
                self.state = 296
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


        def MUL(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.MUL)
            else:
                return self.getToken(SignalFlowV2Parser.MUL, i)

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
        self.enterRule(localctx, 62, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 297
            self.factor()
            self.state = 302
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.MUL or _la==SignalFlowV2Parser.DIV:
                self.state = 298
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.MUL or _la==SignalFlowV2Parser.DIV):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 299
                self.factor()
                self.state = 304
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


        def PLUS(self):
            return self.getToken(SignalFlowV2Parser.PLUS, 0)

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
        self.enterRule(localctx, 64, self.RULE_factor)
        self._la = 0 # Token type
        try:
            self.state = 308
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.PLUS, SignalFlowV2Parser.MINUS]:
                self.enterOuterAlt(localctx, 1)
                self.state = 305
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.PLUS or _la==SignalFlowV2Parser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 306
                self.factor()

            elif token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.STRING, SignalFlowV2Parser.ID, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.LSQUARE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 307
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


        def POW(self):
            return self.getToken(SignalFlowV2Parser.POW, 0)

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
        self.enterRule(localctx, 66, self.RULE_power)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 310
            self.atom_expr()
            self.state = 313
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.POW:
                self.state = 311
                self.match(SignalFlowV2Parser.POW)
                self.state = 312
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
        self.enterRule(localctx, 68, self.RULE_atom_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 315
            self.atom()
            self.state = 319
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.OPEN_PAREN or _la==SignalFlowV2Parser.DOT:
                self.state = 316
                self.trailer()
                self.state = 321
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
        self.enterRule(localctx, 70, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.state = 335
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.LSQUARE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 322
                self.list_expr()

            elif token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 323
                self.tuple_expr()

            elif token in [SignalFlowV2Parser.ID]:
                self.enterOuterAlt(localctx, 3)
                self.state = 324
                self.match(SignalFlowV2Parser.ID)

            elif token in [SignalFlowV2Parser.INT]:
                self.enterOuterAlt(localctx, 4)
                self.state = 325
                self.match(SignalFlowV2Parser.INT)

            elif token in [SignalFlowV2Parser.FLOAT]:
                self.enterOuterAlt(localctx, 5)
                self.state = 326
                self.match(SignalFlowV2Parser.FLOAT)

            elif token in [SignalFlowV2Parser.STRING]:
                self.enterOuterAlt(localctx, 6)
                self.state = 328 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 327
                    self.match(SignalFlowV2Parser.STRING)
                    self.state = 330 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==SignalFlowV2Parser.STRING):
                        break


            elif token in [SignalFlowV2Parser.NONE]:
                self.enterOuterAlt(localctx, 7)
                self.state = 332
                self.match(SignalFlowV2Parser.NONE)

            elif token in [SignalFlowV2Parser.TRUE]:
                self.enterOuterAlt(localctx, 8)
                self.state = 333
                self.match(SignalFlowV2Parser.TRUE)

            elif token in [SignalFlowV2Parser.FALSE]:
                self.enterOuterAlt(localctx, 9)
                self.state = 334
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

        def LSQUARE(self):
            return self.getToken(SignalFlowV2Parser.LSQUARE, 0)

        def RSQUARE(self):
            return self.getToken(SignalFlowV2Parser.RSQUARE, 0)

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
        self.enterRule(localctx, 72, self.RULE_list_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 337
            self.match(SignalFlowV2Parser.LSQUARE)
            self.state = 346
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.LSQUARE) | (1 << SignalFlowV2Parser.PLUS) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                self.state = 338
                self.test()
                self.state = 343
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==SignalFlowV2Parser.COMMA:
                    self.state = 339
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 340
                    self.test()
                    self.state = 345
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 348
            self.match(SignalFlowV2Parser.RSQUARE)
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
        self.enterRule(localctx, 74, self.RULE_tuple_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 350
            self.match(SignalFlowV2Parser.OPEN_PAREN)
            self.state = 352
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.LSQUARE) | (1 << SignalFlowV2Parser.PLUS) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                self.state = 351
                self.testlist()


            self.state = 354
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
        self.enterRule(localctx, 76, self.RULE_testlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 356
            self.test()
            self.state = 361
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,40,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 357
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 358
                    self.test() 
                self.state = 363
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,40,self._ctx)

            self.state = 365
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 364
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
        self.enterRule(localctx, 78, self.RULE_trailer)
        self._la = 0 # Token type
        try:
            self.state = 374
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.enterOuterAlt(localctx, 1)
                self.state = 367
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 369
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.LSQUARE) | (1 << SignalFlowV2Parser.PLUS) | (1 << SignalFlowV2Parser.MINUS))) != 0):
                    self.state = 368
                    self.actual_args()


                self.state = 371
                self.match(SignalFlowV2Parser.CLOSE_PAREN)

            elif token in [SignalFlowV2Parser.DOT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 372
                self.match(SignalFlowV2Parser.DOT)
                self.state = 373
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
        self.enterRule(localctx, 80, self.RULE_actual_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 376
            self.argument()
            self.state = 381
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 377
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 378
                self.argument()
                self.state = 383
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

        def BINDING(self):
            return self.getToken(SignalFlowV2Parser.BINDING, 0)

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
        self.enterRule(localctx, 82, self.RULE_argument)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 386
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,45,self._ctx)
            if la_ == 1:
                self.state = 384
                self.match(SignalFlowV2Parser.ID)
                self.state = 385
                self.match(SignalFlowV2Parser.BINDING)


            self.state = 388
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





