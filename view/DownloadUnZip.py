from tkinter import *;
from tkinter import ttk;
from tkinter.filedialog import askdirectory;
import threading;

from config.AppConfig import *; # local
from utils.urlUtil import *; # local

class DownloadUnZip(Frame):
    def __init__(self, parent):
        super(DownloadUnZip, self).__init__(parent, borderwidth = 1, relief = GROOVE, bg= AppConfig["ContentColor"]);
        self.__parent = parent;
        self.pack(expand = YES, fill = BOTH);
        self.initView();

    def initView(self):
        Label(self, text="- 下载解压 -", font=("宋体", 12), fg="gray", bg= AppConfig["ContentColor"]).pack(pady = (30, 10));
        # 初始化进度条
        self.initProgressbar();
        # 点击安装按钮
        Button(self, text="点击安装", command=self.__onInstall__, width=20).pack(pady = 10);

    def initProgressbar(self):
        self.__progress = IntVar();
        ttk.Progressbar((f, state="readonly", variable = self.__progress).pack();