from tkinter import *;
from tkinter import ttk;
import os;

from config.AppConfig import *; # local
from event.Instance import *; # local

from view.VerSelector import *; # local
from view.DownloadUnZip import *; # local

class MainWindow(Frame):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent);
        self.__parent = parent;
        self.__thread = None;
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
        # 点击下载回调
        self.__vc.onInstall = self.onInstall;
        pass;

    def initTips(self):
        self.__tips = StringVar();
        Label(self, textvariable=self.__tips, font=("宋体", 10), bg= AppConfig["ContentColor"]).pack(pady = (30, 10));
    
    def onInstall(self, path, version):
        self.__vc.pack_forget();
        self.initTips();
        self.downloadIPByThread();

    # 启动新线程下载平台
    def downloadIPByThread(self, path, version):
        print("downloadIP:", path, version);
        self.__tips.set(f"开始安装平台【{version}】...");
        # 停止之前的子线程
        if self.__thread:
            stopThread(self.__thread);
        # 开始请求版本列表的新子线程
        self.__thread = threading.Thread(target = self.downloadIP, args = (path, version, ));
        self.__thread.setDaemon(True)
        self.__thread.start();

    # 下载平台
    def downloadIP(self, path, version):
        ret, urlList = requestJson({"key":"ptip", "req":"urlList", "version":version});
        self.__tips.set("");
        if ret:
            self.__du = DownloadUnZip(self);
            self.__du.pack();
            def onComplete():
                self.onComplete(path, version);
            self.__du.start(urlList, path, onComplete = onComplete);
        else:
            messagebox.showerror(title="网络异常", message="下载平台失败！");
        # 置空线程对象
        self.__thread = None;

    def onComplete(self, path, version):
        self.__du.pack_forget();
        self.__tips.set(f"平台【{version}】安装完成。\n安装路径为：{path}");
        Button(self, text="打开程序目录", command=self.onOpenIPPath).pack();

    def onOpenIPPath(self, path):
        os.system(f"explorer {path}");
        EventSystem.dispatch(EventID.DO_QUIT_APP, {}); # 确定退出窗口