from tkinter import *;
from tkinter import ttk;

from config.AppConfig import *; # local

from view.VerSelector import *; # local

class MainWindow(Frame):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent);
        self.__parent = parent;
        self.pack(expand = YES, fill = BOTH);
        self.initWindow();
        
    def initWindow(self):
        # 初始化标题
        Label(self, text=AppConfig["WinTitle"], font=("Arial", 20)).pack(pady = (40, 20));
        # 初始化版权信息
        Label(self, text=AppConfig["Copyright"], font=("宋体", 10)).pack(side = BOTTOM, pady = (20, 0));
        # 初始化下拉框
        self.__vc = VerSelector(self);
        self.__vc.pack();
        pass;
    
    def install(self):
        pass;