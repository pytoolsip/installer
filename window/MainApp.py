from tkinter import *
import time;
import os;
import base64;

from event.Instance import *; # local
from config.AppConfig import *; # local

class MainApp(Tk):
    def __init__(self):
        super(MainApp, self).__init__();
        self.initTitle();
        self.initSize();
        self.initIcon();
        self.protocol("WM_DELETE_WINDOW", self.onDestroy);
        self.registerEvent();

    def __del__(self):
        self.unregisterEvent();

    def registerEvent(self):
        EventSystem.register(EventID.DO_QUIT_APP, self, "onQuit");

    def unregisterEvent(self):
        EventSystem.unregister(EventID.DO_QUIT_APP, self, "onQuit");

    # 设置标题
    def initTitle(self):
        self.title(AppConfig["Title"]);

    # 设置大小及位置
    def initSize(self):
        width, height = AppConfig["Size"];
        posX, posY = (self.winfo_screenwidth() - width) / 2, (self.winfo_screenheight() - height) / 2;
        self.geometry("%dx%d+%d+%d" % (width, height, posX, posY));

    # 初始化图标
    def initIcon(self):
        if "AppIcon" in PngConfig:
            img = base64.b64decode(PngConfig["AppIcon"].encode());
            fileName = f"temp_dzjh_{time.time()}.ico";
            with open(fileName, 'wb') as f:
                f.write(img);
            self.iconbitmap(fileName);
            os.remove(fileName);

    # 关闭窗口
    def onDestroy(self):
        EventSystem.dispatch(EventID.WM_DELETE_WINDOW, {});
        self.destroy();

    # 退出窗口
    def onQuit(self, data = None):
        self.quit();