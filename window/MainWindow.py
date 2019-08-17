from tkinter import *;
from tkinter import ttk;
from tkinter import messagebox;
import os;
import shutil;

from config.AppConfig import *; # local
from event.Instance import *; # local

from view.VerSelector import *; # local
from view.DownloadUnZip import *; # local

class MainWindow(Frame):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent);
        self.__parent = parent;
        self.__thread = None;
        self.__basePath = "";
        self.pack(expand = YES, fill = BOTH);
        self.initWindow();
        self.registerEvent();

    def __del__(self):
        self.stopThread();
        self.unregisterEvent();

    def onDestroy(self, data):
        if self.__thread: # 判断下载线程是否还存在
            if messagebox.askokcancel(title="取消安装", message="正在下载安装中，是否确定要取消本次安装？"):
                self.stopThread(); # 停止子线程
                # 移除安装路径内容
                if self.__basePath and os.path.exists(self.__basePath):
                    shutil.rmtree(self.__basePath);
                    self.__basePath = "";

    def registerEvent(self):
        EventSystem.register(EventID.WM_DELETE_WINDOW, self, "onDestroy");

    def unregisterEvent(self):
        EventSystem.unregister(EventID.WM_DELETE_WINDOW, self, "onDestroy");

    def stopThread(self):
        if self.__thread:
            stopThread(self.__thread);
            self.__thread = None;
        
    def initWindow(self):
        # 初始化标题
        Label(self, text=AppConfig["WinTitle"], font=("Arial", 20)).pack(pady = (40, 20));
        # 初始化版权信息
        Label(self, text=AppConfig["Copyright"], font=("宋体", 10)).pack(side = BOTTOM, pady = (20, 0));
        # 初始化下拉框
        self.__vc = VerSelector(self);
        self.__vc.pack(expand = YES, fill = BOTH);
        # 点击安装回调
        self.__vc.onInstall = self.onInstall;
        # 初始化下载进度条
        self.__du = DownloadUnZip(self);
        self.__du.forget();
        # 初始化提示信息
        self.__tipsVal = StringVar();
        self.__tips = Label(self, textvariable=self.__tipsVal, font=("宋体", 10), bg= AppConfig["ContentColor"]);
        self.__tips.pack(pady = (80, 10));
        # 初始化重新安装按钮
        self.__reInstallBtn = Button(self, text="点击重新安装", command=self.reInstall);
        self.__reInstallBtn.pack(pady = (40, 10));
        self.__reInstallBtn.forget();
        pass;
    
    def onInstall(self, path, version):
        self.__basePath = path; # 重置基本路径
        self.__vc.forget();
        self.downloadIPByThread(path, version);

    # 启动新线程下载平台
    def downloadIPByThread(self, path, version):
        print("downloadIP:", path, version);
        self.__tipsVal.set(f"准备开始下载平台【{version}】...");
        # 创建下载及解压视图
        self.__du.pack(expand = YES, fill = BOTH);
        # 停止之前的子线程
        self.stopThread();
        # 开始请求版本列表的新子线程
        self.__thread = threading.Thread(target = self.downloadIP, args = (path, version, ));
        self.__thread.setDaemon(True)
        self.__thread.start();

    # 下载平台
    def downloadIP(self, path, version):
        self.__tips.forget();
        ret, resp = requestJson({"key":"ptip", "req":"urlList", "version":version});
        if ret:
            urlList = resp.get("urlList", []);
            if len(urlList) > 0:
                def onComplete():
                    self.onComplete(path, version);
                self.__du.start(urlList, path, onComplete = onComplete);
            else:
                messagebox.showerror(title="数据异常", message="下载平台失败！");
                self.showFailedTips("平台数据异常，下载平台失败！");
        else:
            messagebox.showerror(title="网络异常", message="下载平台失败！");
            self.showFailedTips("连接网络异常，下载平台失败！");
        # 置空线程对象
        self.__thread = None;

    def onComplete(self, path, version):
        self.__du.forget();
        self.__tips.pack(pady = (80, 10));
        self.__tipsVal.set(f"平台【{version}】下载安装完成！\n安装路径为：{path}");
        Button(self, text="打开安装路径", command=self.onOpenIPPath).pack(pady = (40, 10));
        pass;

    def onOpenIPPath(self):
        if self.__basePath and os.path.exists(self.__basePath):
            os.system("explorer "+self.__basePath);
            EventSystem.dispatch(EventID.DO_QUIT_APP, {}); # 确定退出窗口
        else:
            messagebox.showerror(title="路径异常", message="打开安装路径失败！");

    def showFailedTips(self, tips):
        self.__du.forget();
        self.__tips.pack(pady = (80, 10));
        self.__tipsVal.set("连接网络异常，下载平台失败！");
        self.__reInstallBtn.pack(pady = (40, 10));

    def reInstall(self):
        self.__tips.forget();
        self.__reInstallBtn.forget();
        self.__vc.pack(expand = YES, fill = BOTH);
        
