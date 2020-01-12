from tkinter import *;
from tkinter import ttk;
from tkinter import messagebox;
from tkinter.filedialog import askdirectory;
import threading;
import os;

from config.AppConfig import *; # local
from utils.urlUtil import *; # local
from utils.threadUtil import *; # local

class VerSelector(Frame):
    def __init__(self, parent):
        super(VerSelector, self).__init__(parent, borderwidth = 1, relief = GROOVE, bg= AppConfig["ContentColor"]);
        self.__parent = parent;
        self.__thread = None;
        self.pack(expand = YES, fill = BOTH);
        self.initView();
        
    def initView(self):
        Label(self, text="- 选择安装配置 -", font=("宋体", 12), fg="gray", bg= AppConfig["ContentColor"]).pack(pady = (20, 10));
        # 初始化下拉框
        self.initVerCombobox();
        # 初始化路径输入框
        self.initPathEntry();
        # 初始化Pip安装镜像
        self.initPipInstallImg();
        # 点击安装按钮
        Button(self, text="确认安装", command=self.__onInstall__, width=20).pack(pady = (20, 20));

    def initVerCombobox(self):
        f = Frame(self, borderwidth = 2, relief = GROOVE);
        f.pack(pady = 10);
        Label(f, text="安装版本:", font=("宋体", 10)).grid(row = 0, column = 0);
        self.__cbb = ttk.Combobox(f, state="readonly", width=30);
        self.__cbb.grid(row = 0, column = 1, rowspan = 2);
        self.__updateBtn = Button(f, text="更新列表", command=self.requestVerListByThread);
        self.__updateBtn.grid(row = 0, column = 2);
        self.requestVerListByThread();
    
    def initPathEntry(self):
        self.__etVal = StringVar(); # 绑定文本框的变量
        f = Frame(self, borderwidth = 2, relief = GROOVE);
        f.pack(pady = 10);
        Label(f, text="安装路径:", font=("宋体", 10)).grid(row = 0, column = 0);
        Entry(f, textvariable = self.__etVal, width=30).grid(row = 0, column = 1);
        Button(f, text="选择路径", command=self.onSelectPath).grid(row = 0, column = 2);

    def initPipInstallImg(self):
        f = Frame(self, borderwidth = 2, relief = GROOVE);
        f.pack(pady = 10);
        Label(f, text="PIP安装镜像:", font=("宋体", 10)).grid(row = 0, column = 0);
        self.__pii = ttk.Combobox(f, state="readonly", width=32);
        self.__pii.grid(row = 0, column = 1, rowspan = 2);
        # 更新配置
        piiKeyList, default = self.getPiiKeyList();
        self.__pii.configure(value = piiKeyList);
        if len(piiKeyList) > 0:
            self.__pii.current(default);

    def getPiiKeyList(self):
        ret, default = [], 0;
        for pii in AppConfig.get("piiList", []):
            ret.append(pii["key"]);
            if default == 0 and pii.get("isDefault", False):
                default = len(ret) - 1;
        return ret, default;

    def getPiiValByKey(self, key):
        for pii in AppConfig.get("piiList", []):
            if pii["key"] == key:
                return pii["val"];
        return "";

    def onSelectPath(self):
        path = askdirectory();
        if path:
            self.__etVal.set(path);

    def __onInstall__(self):
        if not self.__cbb.get().strip():
            messagebox.showinfo(title="安装提示", message="请求版本信息不能为空！");
            return;
        if not os.path.exists(self.__etVal.get().strip()):
            messagebox.showinfo(title="安装提示", message="所选择的安装路径不存在！");
            return;
        if hasattr(self, "onInstall"):
            self.onInstall(self.__etVal.get(), self.__cbb.get(), self.getPiiValByKey(self.__pii.get()));
        pass;

    # 启动新线程请求版本列表
    def requestVerListByThread(self):
        self.__updateBtn.configure(state = DISABLED); # 不允许点击更新版本列表按钮
        # 停止之前的子线程
        if self.__thread:
            stopThread(self.__thread);
        # 开始请求版本列表的新子线程
        self.__thread = threading.Thread(target = self.requestVerList);
        self.__thread.setDaemon(True)
        self.__thread.start();

    # 请求平台版本列表
    def requestVerList(self):
        ret, resp = requestJson({"key":"ptip", "req":"verList"});
        if ret:
            verList = resp.get("verList", []);
            self.__cbb.configure(value = verList);
            if len(verList) > 0:
                self.__cbb.current(0);
        else:
            messagebox.showerror(title="网络异常", message="请求版本信息列表失败！");
        # 允许点击更新版本列表按钮
        self.__updateBtn.configure(state = NORMAL);
        # 置空线程对象
        self.__thread = None;