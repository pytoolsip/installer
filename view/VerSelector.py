from tkinter import *;
from tkinter import ttk;
from tkinter.filedialog import askdirectory;
import threading;

from config.AppConfig import *; # local
from utils.urlUtil import *; # local

class VerSelector(Frame):
    def __init__(self, parent):
        super(VerSelector, self).__init__(parent, borderwidth = 1, relief = GROOVE, bg= AppConfig["ContentColor"]);
        self.__parent = parent;
        self.pack(expand = YES, fill = BOTH);
        self.initView();
        
    def initView(self):
        Label(self, text="- 选择安装 -", font=("宋体", 12), fg="gray", bg= AppConfig["ContentColor"]).pack(pady = (30, 10));
        # 初始化下拉框
        self.initVerCombobox();
        # 初始化路径输入框
        self.initPathEntry();
        # 点击安装按钮
        Button(self, text="点击安装", command=self.__onInstall__, width=20).pack(pady = 10);

    def initVerCombobox(self):
        f = Frame(self, borderwidth = 2, relief = GROOVE);
        f.pack(pady = 10);
        Label(f, text="安装版本:", font=("宋体", 10)).grid(row = 0, column = 0);
        self.__cbb = ttk.Combobox(f, state="readonly");
        self.__cbb.grid(row = 0, column = 1, rowspan = 2);
        threading.Thread(target = self.requestVerList).start(); # 请求版本列表
    
    def initPathEntry(self):
        self.__etVal = StringVar(); # 绑定文本框的变量
        f = Frame(self, borderwidth = 2, relief = GROOVE);
        f.pack(pady = 10);
        Label(f, text="安装路径:", font=("宋体", 10)).grid(row = 0, column = 0);
        Entry(f, textvariable = self.__etVal).grid(row = 0, column = 1);
        Button(f, text="选择路径", command=self.onSelectPath).grid(row = 0, column = 2);

    def onSelectPath(self):
        path = askdirectory();
        if path:
            self.__etVal.set(path);

    def __onInstall__(self):
        if hasattr(self, "onInstall"):
            self.onInstall(self.__etVal.get(), self.__cbb.get());
        pass;

    # 请求平台版本列表
    def requestVerList(self):
        verList = requestJson({"req":"verList", "key":"ptip"});
        self.__cbb.configure(value = verList);
        if len(verList) > 0:
            self.__cbb.current(0);