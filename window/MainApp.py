from tkinter import *
from tkinter import messagebox;

from event.Instance import *; # local
from config.AppConfig import *; # local

class MainApp(Tk):
    def __init__(self):
        super(MainApp, self).__init__();
        self.initTitle();
        self.initSize();
        self.protocol("WM_DELETE_WINDOW", self.onDestroy);

    # 设置标题
    def initTitle(self):
        self.title(AppConfig["Title"]);

    # 设置大小及位置
    def initSize(self):
        width, height = AppConfig["Size"];
        posX, posY = (self.winfo_screenwidth() - width) / 2, (self.winfo_screenheight() - height) / 2;
        self.geometry("%dx%d+%d+%d" % (width, height, posX, posY));

    def onDestroy(self):
        if messagebox.askokcancel(title="取消安装", message="是否确定退出本次安装？"):
            EventSystem.dispatch(EventID.WM_DELETE_WINDOW, {});
            self.destroy();