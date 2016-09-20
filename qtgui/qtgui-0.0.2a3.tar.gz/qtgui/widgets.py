# 项目：qt封装的库函数
# 模块：自定义的控件
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-08-22 20:01

from PyQt5.QtWidgets import *

class MTreeWidget(QTreeWidget):
    def setColumnWidths(self,*widths):
        if self.columnCount!=len(widths):
            self.setColumnCount(len(widths))
        for i,width in enumerate(widths):
            self.setColumnWidth(i,width)

    def setLabels(self,labels):
        lbls=labels.split("|")
        if self.columnCount!=len(lbls):
            self.setColumnCount(len(lbls))
        self.setHeaderLabels(lbls)

    def setData(self,data):
        def proc_child(owner,data):
            for child in data.childs():
                attrib=child.attrib
                text=attrib['text'] if 'text' in attrib \
                  else [child.tag]
                item=QTreeWidgetItem(owner,text)
                if 'icon' in attrib:
                    for i,icon in enumerate(attrib['icon']):
                        item.setIcon(i,QIcon(icon))
                proc_child(item,child)
        proc_child(self,data)
            
class MTableWidget(QTableWidget):
    def setColumnWidths(self,*widths):
        if self.columnCount!=len(widths):
            self.setColumnCount(len(widths))
        for i,width in enumerate(widths):
            self.setColumnWidth(i,width)

    def setHLabels(self,labels):
        lbls=labels.split("|")
        if self.columnCount!=len(lbls):
            self.setColumnCount(len(lbls))
        self.setHorizontalHeaderLabels(lbls)

    def setData(self,data):
        self.setRowCount(len(data))
        for r,row in enumerate(data):
            for c,col in enumerate(row):
                self.setItem(r,c,QTableWidgetItem(col))
                
    def data(self):
        d=[]
        for r in range(self.rowCount()):
            row=[]
            for c in range(self.columnCount()):
                item=self.item(r,c)
                if item is not None:
                    row.append(self.item(r,c).text())
            if row:
                d.append(row)
        return d

class MCheckBoxGroup(QGroupBox):
    buttons={}
    _columns=4
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.layout=QGridLayout(self)
        self.setLayout(self.layout)
        self.vals=set()
        
    def setColumns(self,columns):
        if columns>0:
            self._columns=columns
    
    def columns(self):
        return self._columns
    
    def setItems(self,items):
        [button.close() for button in self.buttons]
        self.buttons={}
        for i,(value,label) in enumerate(items):
            button=QCheckBox(label,self)
            self.layout.addWidget(button,i//self._columns,
                                  i%self._columns)
            self.buttons[button]=value
            
    def values(self):
        return [value for button,value in self.buttons.items()\
                if button.isChecked()]
                            
    def setValues(self,values):
        self.vals=set(values)
        [button.setChecked(value in values) for button,value \
         in self.buttons.items()]
    
    def delta(self):
        new=set(self.values())
        return list(self.vals-new),list(new-self.vals)
    
    def selectAll(self):
        [button.setChecked(True) for button in self.buttons]
    
    def deSelectAll(self):
        [button.setChecked(False) for button in self.buttons]
        

class MComboBox(QComboBox):
    '''自定义的ComboBox类
    新增setItems函数，便于使用Items来设置下拉菜单    
    '''
    def setCurrentText(self,value):
        pass
    def setItems(self,items):
        self.clear()            #清理下拉菜单
        self.addItems(items)    #新增下拉菜单
        
class MTextEdit(QTextEdit):
    '''
    自定义的多行文本编辑类
    新增plainText方法
    '''
    def plainText(self):        
        return self.toPlainText()  #获取纯文本
