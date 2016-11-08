# coding: utf-8

from tkinter import *
import tkinter.font
import tkinter.messagebox

import time
import threading
import os

def get_screen_size(window):  
    return window.winfo_screenwidth(),window.winfo_screenheight()  
  
def get_window_size(window):  
    return window.winfo_reqwidth(),window.winfo_reqheight()  
  
def center_window(root):  
    root.update()
    curWidth = root.winfo_reqwidth()
    curHeight = root.winfo_height()
    scnWidth,scnHeight = root.maxsize()
    root.geometry('%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2))

colors = '''#FFB6C1 LightPink 浅粉红
    #FFC0CB Pink 粉红
    #DC143C Crimson 深红/猩红
    #FFF0F5 LavenderBlush 淡紫红
    #DB7093 PaleVioletRed 弱紫罗兰红
    #FF69B4 HotPink 热情的粉红
    #FF1493 DeepPink 深粉红
    #C71585 MediumVioletRed 中紫罗兰红
    #DA70D6 Orchid 暗紫色/兰花紫
    #D8BFD8 Thistle 蓟色
    #DDA0DD Plum 洋李色/李子紫
    #EE82EE Violet 紫罗兰
    #FF00FF Magenta 洋红/玫瑰红
    #FF00FF Fuchsia 紫红/灯笼海棠
    #8B008B DarkMagenta 深洋红
    #800080 Purple 紫色
    #BA55D3 MediumOrchid 中兰花紫
    #9400D3 DarkViolet 暗紫罗兰
    #9932CC DarkOrchid 暗兰花紫
    #4B0082 Indigo 靛青/紫兰色
    #8A2BE2 BlueViolet 蓝紫罗兰
    #9370DB MediumPurple 中紫色
    #7B68EE MediumSlateBlue 中暗蓝色/中板岩蓝
    #6A5ACD SlateBlue 石蓝色/板岩蓝
    #483D8B DarkSlateBlue 暗灰蓝色/暗板岩蓝
    #E6E6FA Lavender 淡紫色/熏衣草淡紫
    #F8F8FF GhostWhite 幽灵白
    #0000FF Blue 纯蓝
    #0000CD MediumBlue 中蓝色
    #191970 MidnightBlue 午夜蓝
    #00008B DarkBlue 暗蓝色
    #000080 Navy 海军蓝
    #4169E1 RoyalBlue 皇家蓝/宝蓝
    #6495ED CornflowerBlue 矢车菊蓝
    #B0C4DE LightSteelBlue 亮钢蓝
    #778899 LightSlateGray 亮蓝灰/亮石板灰
    #708090 SlateGray 灰石色/石板灰
    #1E90FF DodgerBlue 闪兰色/道奇蓝
    #F0F8FF AliceBlue 爱丽丝蓝
    #4682B4 SteelBlue 钢蓝/铁青
    #87CEFA LightSkyBlue 亮天蓝色
    #87CEEB SkyBlue 天蓝色
    #00BFFF DeepSkyBlue 深天蓝
    #ADD8E6 LightBlue 亮蓝
    #B0E0E6 PowderBlue 粉蓝色/火药青
    #5F9EA0 CadetBlue 军兰色/军服蓝
    #F0FFFF Azure 蔚蓝色
    #E0FFFF LightCyan 淡青色
    #AFEEEE PaleTurquoise 弱绿宝石
    #00FFFF Cyan 青色
    #00FFFF Aqua 浅绿色/水色
    #00CED1 DarkTurquoise 暗绿宝石
    #2F4F4F DarkSlateGray 暗瓦灰色/暗石板灰
    #008B8B DarkCyan 暗青色
    #008080 Teal 水鸭色
    #48D1CC MediumTurquoise 中绿宝石
    #20B2AA LightSeaGreen 浅海洋绿
    #40E0D0 Turquoise 绿宝石
    #7FFFD4 Aquamarine 宝石碧绿
    #66CDAA MediumAquamarine 中宝石碧绿
    #00FA9A MediumSpringGreen 中春绿色
    #F5FFFA MintCream 薄荷奶油
    #00FF7F SpringGreen 春绿色
    #3CB371 MediumSeaGreen 中海洋绿
    #2E8B57 SeaGreen 海洋绿
    #F0FFF0 Honeydew 蜜色/蜜瓜色
    #90EE90 LightGreen 淡绿色
    #98FB98 PaleGreen 弱绿色
    #8FBC8F DarkSeaGreen 暗海洋绿
    #32CD32 LimeGreen 闪光深绿
    #00FF00 Lime 闪光绿
    #228B22 ForestGreen 森林绿
    #008000 Green 纯绿
    #006400 DarkGreen 暗绿色
    #7FFF00 Chartreuse 黄绿色/查特酒绿
    #7CFC00 LawnGreen 草绿色/草坪绿
    #ADFF2F GreenYellow 绿黄色
    #556B2F DarkOliveGreen 暗橄榄绿
    #9ACD32 YellowGreen 黄绿色
    #6B8E23 OliveDrab 橄榄褐色
    #F5F5DC Beige 米色/灰棕色
    #FAFAD2 LightGoldenrodYellow 亮菊黄
    #FFFFF0 Ivory 象牙色
    #FFFFE0 LightYellow 浅黄色
    #FFFF00 Yellow 纯黄
    #808000 Olive 橄榄
    #BDB76B DarkKhaki 暗黄褐色/深卡叽布
    #FFFACD LemonChiffon 柠檬绸
    #EEE8AA PaleGoldenrod 灰菊黄/苍麒麟色
    #F0E68C Khaki 黄褐色/卡叽布
    #FFD700 Gold 金色
    #FFF8DC Cornsilk 玉米丝色
    #DAA520 Goldenrod 金菊黄
    #B8860B DarkGoldenrod 暗金菊黄
    #FFFAF0 FloralWhite 花的白色
    #FDF5E6 OldLace 老花色/旧蕾丝
    #F5DEB3 Wheat 浅黄色/小麦色
    #FFE4B5 Moccasin 鹿皮色/鹿皮靴
    #FFA500 Orange 橙色
    #FFEFD5 PapayaWhip 番木色/番木瓜
    #FFEBCD BlanchedAlmond 白杏色
    #FFDEAD NavajoWhite 纳瓦白/土著白
    #FAEBD7 AntiqueWhite 古董白
    #D2B48C Tan 茶色
    #DEB887 BurlyWood 硬木色
    #FFE4C4 Bisque 陶坯黄
    #FF8C00 DarkOrange 深橙色
    #FAF0E6 Linen 亚麻布
    #CD853F Peru 秘鲁色
    #FFDAB9 PeachPuff 桃肉色
    #F4A460 SandyBrown 沙棕色
    #D2691E Chocolate 巧克力色
    #8B4513 SaddleBrown 重褐色/马鞍棕色
    #FFF5EE Seashell 海贝壳
    #A0522D Sienna 黄土赭色
    #FFA07A LightSalmon 浅鲑鱼肉色
    #FF7F50 Coral 珊瑚
    #FF4500 OrangeRed 橙红色
    #E9967A DarkSalmon 深鲜肉/鲑鱼色
    #FF6347 Tomato 番茄红
    #FFE4E1 MistyRose 浅玫瑰色/薄雾玫瑰
    #FA8072 Salmon 鲜肉/鲑鱼色
    #FFFAFA Snow 雪白色
    #F08080 LightCoral 淡珊瑚色
    #BC8F8F RosyBrown 玫瑰棕色
    #CD5C5C IndianRed 印度红
    #FF0000 Red 纯红
    #A52A2A Brown 棕色
    #B22222 FireBrick 火砖色/耐火砖
    #8B0000 DarkRed 深红色
    #800000 Maroon 栗色
    #FFFFFF White 纯白
    #F5F5F5 WhiteSmoke 白烟
    #DCDCDC Gainsboro 淡灰色
    #D3D3D3 LightGrey 浅灰色
    #C0C0C0 Silver 银灰色
    #A9A9A9 DarkGray 深灰色
    #808080 Gray 灰色
    #696969 DimGray 暗淡灰
    #000000 Black 纯黑'''

class Dc_messagebox():

    def counterDown (self):
        #print (self.title + "  timer is running")
        self.timeout -= 1
        if(self.timeout):
            self.root.attributes ("-alpha", self.timeout / self.reload)
            self.timer = threading.Timer (self.timer_interval, self.counterDown)
            self.timer.start()
            self.root.title(self.title + "-->%d"% int((self.timeout)*self.timer_interval))
        else:
            self.mb_clickYes(self.result)

    def __init__(self, title_data = "", info_data = "",timeout = 0,root = None):
        self.timer_interval = 0.2
        self.timeout = int(timeout /self.timer_interval)
        self.reload = self.timeout

        self.title = title_data
        self.timer = None

        self.result = []

        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title(title_data)
        #######################
        self.root.iconbitmap ('c:/Python34/DLLs/py.ico')
        self.root.attributes ("-alpha", 1)  # 窗口透明度
        #############


        self.frame = Frame(self.root)
        self.frame.pack()
        self.label_name3 = Label(self.frame, text="", fg="#00BFFF", bg="#FFFFFF")
        self.label_name3.config(font=tkinter.font.Font(family='Microsfot YaHei', size=24, weight=tkinter.font.BOLD))
        self.label_name3.pack(fill=BOTH)
        self.label_name = Label(self.frame, text=info_data, fg="#00BFFF", bg="#FFFFFF")
        ## 根据info_data 长度决定size
        width,height = get_screen_size(self.root)
        #print(width,height )
        info_size = int(width/len(info_data))
        if(info_size > 48):info_size = 48
        if(info_size < 12):info_size = 12

        self.label_name.config(font=tkinter.font.Font(family='Microsfot YaHei', size=info_size, weight=tkinter.font.BOLD))
        self.label_name.pack(fill = BOTH)
        self.label_name2 = Label(self.frame, text="", fg="#00BFFF", bg="#FFFFFF")
        self.label_name2.config(font=tkinter.font.Font(family='Microsfot YaHei', size=24, weight=tkinter.font.BOLD))
        self.label_name2.pack(fill=BOTH)

        #####button
        buttonFrame = Frame(self.root)
        buttonFrame.pack(fill = X, side = BOTTOM)
        self.button_ok = Button(buttonFrame,text = "是", command = lambda:self.mb_clickYes(self.result), fg="#FFFFFF", bg="#00BFFF", font=tkinter.font.Font(family = 'Microsfot YaHei',size = 24,weight = tkinter.font.BOLD))
        self.button_ok.pack(expand = True, fill = X, side = LEFT)

        #self.button_cancel = Button(buttonFrame,text = "否", command = lambda:self.mb_clickNo(self.result), fg="#FFFFFF", bg="#00BFFF", font=tkinter.font.Font(family = 'Microsfot YaHei',size = 24,weight = tkinter.font.BOLD))

        self.button_cancel = Button (buttonFrame, text="否", command=lambda: self.mb_clickNo (self.result), fg="#FFFFFF",
                                     bg="#C0C0C0", font=tkinter.font.Font (family='Microsfot YaHei', size=24,
                                                                           weight=tkinter.font.BOLD))

        self.button_cancel.pack(expand = True, fill = X, side = RIGHT)
        center_window(self.root)
        if timeout :
            self.timer = threading.Timer (3, self.counterDown)
            #self.timer.setDaemon(True)
            self.timer.start()
            self.root.mainloop()
            #self.timer.cancel()
            self.root.destroy ()
        else:
            self.root.mainloop ()
            self.root.destroy ()
        #return self.result

    def mb_clickYes(self, result):
        if(self.timer):self.timer.cancel()
        self.button_ok.flash()
        result.append(YES)
        self.root.quit()

    def mb_clickNo(self, result):
        if (self.timer):self.timer.cancel()
        self.button_cancel.flash()
        result.append(NO)
        self.root.quit()

def _test_():
    print ("countdown msgbox")
    Dc_messagebox("Demo MessageBox Count down","This is Demo MessageBox\n" ,timeout= 3)
    print("next msgbox")
    Dc_messagebox ("Demo MessageBox",
               "This is Demo MessageBox\n" + """Dc_messagebox("Demo MessageBox","This is Demo MessageBox\n""")

if __name__=="__main__":
    _test_()