#!python3
# -*- coding: utf-8 -*-

import time
import uiautomation as automation

def main():
    firefoxWindow = automation.WindowControl(searchDepth = 1, ClassName = 'MozillaWindowClass')
    if not firefoxWindow.Exists(0):
        automation.Logger.WriteLine('please run Firefox first', automation.ConsoleColor.Yellow)
        return
    firefoxWindow.ShowWindow(automation.ShowWindow.Maximize)
    firefoxWindow.SetActive()
    time.sleep(1)
    tab = automation.TabControl(searchFromControl= firefoxWindow)
    newTabButton = automation.ButtonControl(searchFromControl= tab, searchDepth= 1)
    newTabButton.Click()
    edit = automation.EditControl(searchFromControl= firefoxWindow)
    #edit.Click()
    edit.SendKeys('http://global.bing.com/?rb=0&setmkt=en-us&setlang=en-us{Enter}')
    time.sleep(2)
    searchEdit = automation.FindControl(firefoxWindow,
                           lambda c:(isinstance(c, automation.EditControl) or isinstance(c, automation.ComboBoxControl)) and c.Name == 'Enter your search term'
                           )
    #searchEdit.Click()
    searchEdit.SendKeys('PythonUIAutomation4Windows site:www.oschina.net{Enter}',0.05)
    link = automation.HyperlinkControl(searchFromControl= firefoxWindow, SubName = 'PythonUIAutomation4Windows首页')
    if not link.Exists():
        return
    automation.Win32API.PressKey(automation.Keys.VK_CONTROL)
    link.Click()  #press control to open the page in a new tab
    automation.Win32API.ReleaseKey(automation.Keys.VK_CONTROL)
    newTab = automation.TabItemControl(searchFromControl= tab, SubName = 'PythonUIAutomation4Windows首页')
    newTab.Click()
    link = automation.HyperlinkControl(searchFromControl= firefoxWindow, Name = 'yinkaisheng/PythonUIAutomation4Windows')
    sx, sy = automation.Win32API.GetScreenSize()
    left, top, right, bottom = link.BoundingRectangle
    while bottom <= 0 or top > sy:
        automation.Logger.WriteLine('press PageDown')
        automation.SendKeys('{PageDown}')
        time.sleep(1)
        left, top, right, bottom = link.BoundingRectangle
    automation.Win32API.PressKey(automation.Keys.VK_CONTROL)
    link.Click()
    automation.Win32API.ReleaseKey(automation.Keys.VK_CONTROL)
    newTab = automation.TabItemControl(searchFromControl= tab, SubName = 'yinkaisheng/PythonUIAutomation4Windows')
    newTab.Click()
    starLink = automation.HyperlinkControl(searchFromControl= firefoxWindow, SubName = 'Star')
    if starLink.Exists(5):
        automation.GetConsoleWindow().SetActive()
        automation.Logger.WriteLine('Star PythonUIAutomation4Windows after 2 seconds', automation.ConsoleColor.Yellow)
        time.sleep(2)
        firefoxWindow.SetActive()
        time.sleep(1)
        starLink.Click()
        time.sleep(2)

if __name__ == '__main__':
    main()
    automation.GetConsoleWindow().SetActive()
    input('press Enter to exit')
