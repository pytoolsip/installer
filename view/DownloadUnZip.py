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
        self.update();
        self.initView();

    def initView(self):
        Label(self, text="- 下载与解压 -", font=("宋体", 12), fg="gray", bg= AppConfig["ContentColor"]).pack(pady = (30, 10));
        # 初始化进度条
        self.initProgressbar();

    def initProgressbar(self):
        self.__progress = IntVar();
        ttk.Progressbar(self, length=int(self.winfo_width()*0.9), variable = self.__progress).pack();

    def download(self):
        self.__progress.set(10);