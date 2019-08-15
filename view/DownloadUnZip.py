from tkinter import *;
from tkinter import ttk;
from tkinter.filedialog import askdirectory;
import threading;
from urllib import request;
import threading;
import zipfile;
import os;

from config.AppConfig import *; # local
from utils.urlUtil import *; # local
from utils.threadUtil import *; # local
from event.Instance import *; # local

class DownloadUnZip(Frame):
    def __init__(self, parent):
        super(DownloadUnZip, self).__init__(parent, borderwidth = 1, relief = GROOVE, bg= AppConfig["ContentColor"]);
        self.__parent = parent;
        self.__taskList = [];
        self.__taskCnt = 0;
        self.pack(expand = YES, fill = BOTH);
        self.update();
        self.initView();

    def __del__(self):
        self.stopThread();
        self.unregisterEvent();

    def onDestroy(self, data):
        self.stopThread();

    def registerEvent(self):
        EventSystem.register(EventID.WM_DELETE_WINDOW, self, "onDestroy");

    def unregisterEvent(self):
        EventSystem.unregister(EventID.WM_DELETE_WINDOW, self, "onDestroy");

    def stopThread(self):
        if self.__thread:
            stopThread(self.__thread);
            self.__thread = None;
            
    def initView(self):
        Label(self, text="- 下载与解压 -", font=("宋体", 12), fg="gray", bg= AppConfig["ContentColor"]).pack(pady = (30, 10));
        # 初始化提示
        self.initTips();
        # 初始化进度条
        self.initProgressbar();

    def initTips(self):
        self.__tips = StringVar();
        Label(self, textvariable=self.__tips, font=("宋体", 10), bg= AppConfig["ContentColor"]).pack(pady = (30, 10));

    def initProgressbar(self):
        self.__progress = IntVar();
        ttk.Progressbar(self, length=int(self.winfo_width()*0.9), variable = self.__progress).pack();

    def start(self, urlInfoList, basePath, onComplete = None):
        # 重置任务列表
        self.__taskList = [];
        for urlInfo in urlInfoList:
            url = urlInfo["url"];
            fileName = os.path.basename(url);
            filepath = os.path.join(basePath, urlInfo["path"], fileName);
            self.__taskList.append({"type" : "download", "url" : url, "filepath" : filepath});
            # 判断是否zip文件
            name, ext = os.path.splitext(fileName);
            if ext == ".zip":
                self.__taskList.append({"type" : "unzip", "filepath" : filepath, "dirpath" : os.path.join(basePath, urlInfo["path"], name)});
        self.__taskCnt = len(self.__taskList); # 重置任务总数
        self.__onComplete = onComplete; # 重置完成任务列表的回调
        self.runTaskList(); # 运行任务

    def runTaskList(self):
        if len(self.__taskList) > 0:
            self.__progress.set((self.__taskCnt - len(self.__taskList))/self.__taskCnt * 100);
            task = self.__taskList.pop(0);
            if task["type"] == "download":
                self.__download__(task["url"], task["filepath"]);
            elif task["type"] == "unzip":
                self.__unzip__(task["filepath"], task["dirpath"]);
        else:
            self.__progress.set(100);
            if callable(self.__onComplete):
                self.__onComplete(); # 完成任务列表后回调

    # 获取上次的进度
    def getLastProgress(self):
        return (self.__taskCnt - len(self.__taskList))/self.__taskCnt * 100;

    # 下载文件
    def __download__(self, url, filepath):
        self.__tips.set(f"正在下载：{url}");
        request.urlretrieve(url, filepath, self._schedule_);

    # 下载回调
    def _schedule_(self, block, size, totalSize):
        rate = block*size / totalSize * 100;
        self.__progress.set(self.getLastProgress() + rate);
        tips = re.sub("\[%d+\%\]", "", self.__tips.get());
        if block*size < totalSize:
            rate = round(rate, 2);
            self.__tips.set(f"{tips} [{rate}%]");
        else:
            url = tips.replace("正在下载：", "").strip();
            self.__tips.set(f"完成下载：{url}");
        pass;

    # 解压文件
    def __unzip__(self, filepath, dirpath):
        if not os.path.exists(filepath):
            return;
        self.stopThread(); # 停止之前的进程
        self.__thread = threading.Thread(target = self._unzipFile_, args = (filepath, dirpath));
        self.__thread.start();

    # 解压回调
    def _unzipFile_(self, filepath, dirpath):
        zf = zipfile.ZipFile(filepath, "r");
        totalCnt = len(zf.namelist());
        completeCnt = 0;
        for file in zf.namelist():
            self.__tips.set(f"正在解压：{file}");
            zf.extract(file, dirpath);
            completeCnt += 1;
            self.__progress.set(self.getLastProgress() + completeCnt/totalCnt * 100);
        zf.close();
        self.__tips.set(f"完成解压：{filepath}");