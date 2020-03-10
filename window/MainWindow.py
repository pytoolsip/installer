from tkinter import *;
from tkinter import ttk;
from tkinter import messagebox;
import os;
import shutil;

from config.AppConfig import *; # local
from event.Instance import *; # local
from utils.textUtil import *; # local
from utils.urlUtil import *; # local
from utils.threadUtil import *; # local

from view.VerSelector import *; # local
from view.DownloadUnZip import *; # local

class MainWindow(Frame):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent);
        self.__parent = parent;
        self.__thread = None;
        self.__basePath = "";
        self.__pii = ""; # pip安装镜像
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
        # 初始化内容
        self.initContent()

    def initContent(self):
        f = Frame(self, borderwidth = 2, relief = GROOVE, bg= AppConfig["ContentColor"]);
        f.pack(expand = YES, fill = BOTH);
        # 初始化下拉框
        self.__vc = VerSelector(f);
        self.__vc.pack(expand = YES, fill = BOTH);
        # self.__vc.forget();
        # 点击安装回调
        self.__vc.onInstall = self.onInstall;
        # 初始化下载进度条
        self.__du = DownloadUnZip(f);
        self.__du.forget();
        # 初始化提示信息
        self.__tipsVal = StringVar();
        self.__tips = Label(f, textvariable=self.__tipsVal, font=("宋体", 10), bg= AppConfig["ContentColor"]);
        self.__tips.pack(pady = (80, 10));
        # 初始化重新安装按钮
        self.__reInstallBtn = Button(f, text="点击重新安装", command=self.reInstall);
        self.__reInstallBtn.forget();
        # 初始化完成安装按钮
        self.__finishBtn = Button(f, text="完成安装", command=self.onFinish);
        self.__finishBtn.forget();
        # 完成安装后的选项
        self.__createLnkVal = BooleanVar();
        self.__createLnk = Checkbutton(f, text="生成桌面快捷方式", variable = self.__createLnkVal, onvalue = True, offvalue = False);
        self.__createLnkVal.set(True);
        self.__createLnk.forget();
        self.__openPathVal = BooleanVar();
        self.__openPath = Checkbutton(f, text="打开安装目录", variable = self.__openPathVal, onvalue = True, offvalue = False);
        self.__openPath.forget();
        self.__runPtipVal = BooleanVar();
        self.__runPtip = Checkbutton(f, text="运行PyToolsIP", variable = self.__runPtipVal, onvalue = True, offvalue = False);
        self.__runPtipVal.set(True);
        self.__runPtip.forget();
        pass;
    
    def onInstall(self, path, version, piiVal):
        self.__pii = piiVal; # 重置pip安装镜像
        self.__basePath = os.path.join(path, "PyToolsIP"); # 重置基本路径
        if not os.path.exists(self.__basePath):
            os.makedirs(self.__basePath);
        self.__vc.forget();
        self.downloadIPByThread(version);

    # 启动新线程下载平台
    def downloadIPByThread(self, version):
        # print("downloadIP:", self.__basePath, version);
        self.__tipsVal.set(f"准备开始下载平台【{version}】...");
        # 创建下载及解压视图
        self.__du.pack(expand = YES, fill = BOTH);
        # 停止之前的子线程
        self.stopThread();
        # 开始请求版本列表的新子线程
        self.__thread = threading.Thread(target = self.downloadIP, args = (version, ));
        self.__thread.setDaemon(True)
        self.__thread.start();

    # 下载平台
    def downloadIP(self, version):
        self.__tips.forget();
        ret, resp = requestJson({"key":"ptip", "req":"urlList", "version":version});
        if ret:
            urlList = resp.get("urlList", []);
            if len(urlList) > 0:
                self.saveUrlList(urlList);
                def onComplete():
                    self.savePii();
                    self.onComplete(version);
                self.__du.start(urlList, self.__basePath, onComplete = onComplete);
            else:
                messagebox.showerror(title="数据异常", message="下载平台失败！");
                self.showFailedTips("平台数据异常，下载平台失败！");
        else:
            messagebox.showerror(title="网络异常", message="下载平台失败！");
            self.showFailedTips("网络连接异常，下载平台失败！");
        # 置空线程对象
        self.__thread = None;

    # 保存url列表数据
    def saveUrlList(self, urlList):
        dataPath = os.path.join(self.__basePath, "data"); # 数据路径
        if not os.path.exists(dataPath):
            os.makedirs(dataPath);
        with open(os.path.join(dataPath, "url_list.json"), "w") as f:
            f.write(json.dumps({"urlList" : urlList}));

    def onComplete(self, version):
        self.__du.forget();
        self.__tips.pack(pady = (60, 10));
        self.__tipsVal.set(f"已完成平台【{version}】安装！\n"+self.clipText("安装路径为："+ os.path.abspath(self.__basePath)));
        # 操作选项
        self.__createLnk.pack(pady = (20, 10));
        self.__openPath.pack(pady = (20, 10));
        self.__runPtip.pack(pady = (20, 10));
        # 完成按钮
        self.__finishBtn.pack(pady = (20, 10));
        pass;

    def onFinish(self):
        if self.__basePath and os.path.exists(self.__basePath):
            basePath = os.path.abspath(self.__basePath);
            exeName = "pytoolsip.exe";
            exePath = os.path.join(basePath, exeName);
            # 创建桌面快捷方式
            if self.__createLnkVal.get():
                mklnkPath = os.path.join(basePath, "run", "makelnk.bat");
                if os.path.exists(mklnkPath) and os.path.exists(exePath):
                    runCmd(" ".join([mklnkPath, exePath, "PyToolsIP", "Python工具集成平台"]));
            # 打开安装目录
            if self.__openPathVal.get():
                runCmd("cmd /c explorer " + basePath);
            # 运行PyToolsIP
            if self.__runPtipVal.get():
                if os.path.exists(exePath):
                    os.system(f"start /d {basePath} {exeName}");
            # 确定退出窗口
            EventSystem.dispatch(EventID.DO_QUIT_APP, {});
        else:
            messagebox.showerror(title="路径异常", message="打开安装路径失败！");

    def showFailedTips(self, tips):
        self.__du.forget();
        self.__tips.pack(pady = (80, 10));
        self.__tipsVal.set(tips);
        self.__reInstallBtn.pack(pady = (40, 10));

    def reInstall(self):
        self.__tips.forget();
        self.__reInstallBtn.forget();
        self.__vc.pack(expand = YES, fill = BOTH);
        
    def savePii(self):
        cfgPath = os.path.join(self.__basePath, "data", "config"); # 配置路径
        if not os.path.exists(cfgPath):
            os.makedirs(cfgPath);
        with open(os.path.join(cfgPath, "setting_cfg.json"), "w") as f:
            f.write(json.dumps({
                "pip_install_image" : self.__pii,
            }));
            
    # 裁剪文本
    def clipText(self, text):
        return clipText(text, 80);