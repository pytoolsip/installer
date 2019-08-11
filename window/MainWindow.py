from tkinter import *

from config.AppConfig import *; # local

class MainWindow(Frame):
    def __init__(self, parent):
        super(MainWindow, self).__init__();
        self.__parent = parent;
        self.pack();
        self.initWindow();
        
    def initWindow(self):
        # 初始化标题
        Label(self, text=AppConfig["Title"], font=("Arial", 24), width=AppConfig["Size"][0], height=4).pack(side=TOP);
        pass;
    
    def install(self):
        pass;