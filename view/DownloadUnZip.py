from tkinter import *;
from tkinter import ttk;
from tkinter.filedialog import askdirectory;
import threading;
from urllib import request;
import zipfile;

from config.AppConfig import *; # local
from utils.urlUtil import *; # local
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
        # 初始化进度条
        self.initProgressbar();

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
            task = self.__taskList.pop(0);
            if task["type"] == "download":
                self.__download__(task["url"], task["filepath"]);
            elif task["type"] == "unzip":
                self.__unzip__(task["filepath"], task["dirpath"]);
        elif callable(self.__onComplete):
            self.__onComplete(); # 完成任务列表后回调

    # 下载文件
    def __download__(self, url, filepath):
        request.urlretrieve(url, filepath, self._schedule_);

    def _schedule_(self, block, size, totalSize):
        rate = block*size / totalSize;
        pass;

    # 解压文件
    def __unzip__(self, filepath, dirpath):
        if not os.path.exists(path):
            return;
        self.stopThread(); # 停止之前的进程
        self.__thread = threading.Thread(target = self._unzipFile_, args = (filepath, dirpath));
        self.__thread.start();

    def _unzipFile_(filepath, dirpath):
        zf = zipfile.ZipFile(filepath, "r");
        totalLen = len(zf.namelist());
        completeLen = 0;
        for file in zf.namelist():
            # callback(completeLen/totalLen, file); # 回调函数
            zf.extract(file, dirpath);
            completeLen += 1;
        zf.close();