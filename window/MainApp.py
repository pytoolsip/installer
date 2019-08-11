from tkinter import *

from config.AppConfig import *; # local

class MainApp(Tk):
    def __init__(self):
        super(MainApp, self).__init__();
        self.initTitle();
        self.initSize();

    # 设置标题
    def initTitle(self):
        self.title(AppConfig["Title"]);

    # 设置大小及位置
    def initSize(self):
        width, height = AppConfig["Size"];
        posX, posY = (self.winfo_screenwidth() - width) / 2, (self.winfo_screenheight() - height) / 2;
        self.geometry("%dx%d+%d+%d" % (width, height, posX, posY));