from tkinter import *;
from tkinter import ttk;
from tkinter import font;
from tkinter.filedialog import askdirectory;
import threading;
from urllib import request;
import threading;
import zipfile;
import os;
import time;
import random;

from config.AppConfig import *; # local
from utils.textUtil import *; # local
from utils.urlUtil import *; # local
from utils.threadUtil import *; # local
from event.Instance import *; # local

# 检测路径
def checkPath(path):
    if not path:
        return "";
    path = path.replace("\\", "/");
    if path[0] == "/":
        return path[1:];
    return path;

class DownloadUnZip(Frame):
    def __init__(self, parent):
        super(DownloadUnZip, self).__init__(parent, borderwidth = 1, relief = GROOVE, bg= AppConfig["ContentColor"]);
        self.__parent = parent;
        self.__taskList = [];
        self.__taskCnt = 0;
        self.pack(expand = YES, fill = BOTH);
        self.update();
        self.initView();
            
    def initView(self):
        Label(self, text="- 正在下载与解压平台 -", font=("宋体", 12, font.BOLD), fg= "#464646", bg= AppConfig["ContentColor"]).pack(pady = (30, 30));
        # 初始化提示
        self.initTips();
        # 初始化进度条
        self.initProgressbar();
        # 初始化第二提示
        self.initSecondTips();

    def initTips(self):
        self.__tips = StringVar();
        Label(self, textvariable=self.__tips, font=("宋体", 10), bg= AppConfig["ContentColor"]).pack(padx = 10, pady = (20, 10));

    def initProgressbar(self):
        self.__progress = IntVar();
        ttk.Progressbar(self, length=int(self.__parent.winfo_width()), variable = self.__progress).pack(padx = 10, pady = (0, 40));

    def initSecondTips(self):
        self.__secondIndex = -1;
        self.__secondTips = StringVar();
        Label(self, textvariable=self.__secondTips, font=("宋体", 10), fg= "#565656", bg= AppConfig["ContentColor"]).pack(padx = 10, pady = (40, 30));
        self.updateSecondTips();

    def updateSecondTips(self):
        tipsList = [
            "* 安装及初次运行平台时，请确保能正常连接网络",
            "* 安装完成后，初次运行平台时，会进行平台依赖模块的安装",
            "* 更多详情，请关注平台官网：ptip.jdreamheart.com",
        ];
        if self.__secondIndex < 0:
            self.__secondIndex =  random.randint(0, len(tipsList) - 1);
        else:
            self.__secondIndex = (self.__secondIndex + 1) % len(tipsList);
        self.__secondTips.set(tipsList[self.__secondIndex]);
        self.after(5000, self.updateSecondTips);

    def start(self, urlInfoList, basePath, onComplete = None):
        # print(f"Start download and unzip urlInfoList({urlInfoList}).");
        # 重置任务列表
        self.__taskList = [];
        for urlInfo in urlInfoList:
            name, url = urlInfo.get("name", ""), urlInfo["url"];
            fileName = os.path.basename(url);
            _, ext = os.path.splitext(fileName);
            if name:
                filepath = os.path.join(basePath, checkPath(urlInfo["path"]), name+ext);
            else:
                filepath = os.path.join(basePath, checkPath(urlInfo["path"]), fileName);
            filepath = filepath.replace("\\", "/");
            self.__taskList.append({"type" : "download", "url" : AppConfig["homeUrl"] + url, "filepath" : filepath});
            # 判断是否zip文件
            if ext == ".zip":
                self.__taskList.append({"type" : "unzip", "filepath" : filepath, "dirpath" : os.path.join(basePath, checkPath(urlInfo["path"]))});
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
            # 执行下个任务
            self.runTaskList();
        else:
            self.__progress.set(100);
            if callable(self.__onComplete):
                self.__onComplete(); # 完成任务列表后回调

    # 获取上次的进度
    def getLastProgress(self):
        return (self.__taskCnt - len(self.__taskList) - 1)/self.__taskCnt * 100;

    # 校验文件路径
    def __checkFilePath__(self, filePath):
        dirPath = os.path.dirname(filePath);
        if not os.path.exists(dirPath):
            os.mkdir(dirPath);

    # 下载文件
    def __download__(self, url, filepath):
        self.__tips.set(self.clipText(f"正在下载：{url}"));
        self.__checkFilePath__(filepath);
        request.urlretrieve(url, filepath, self._schedule_);

    # 下载回调
    def _schedule_(self, block, size, totalSize):
        rate = block*size / totalSize * 100;
        self.__progress.set(self.getLastProgress() + rate/self.__taskCnt);
        tips = re.sub("\[\d+.?\d+\%\]", "", self.__tips.get());
        if block*size < totalSize:
            self.__tips.set(self.clipText(f"{tips}[%.2f%%]" % rate));
        else:
            url = tips.replace("正在下载：", "").strip();
            self.__tips.set(self.clipText(f"完成下载：{url}"));
        pass;

    # 解压文件
    def __unzip__(self, filepath, dirpath, isRmZip = True):
        if not os.path.exists(filepath):
            return;
        self.__tips.set(self.clipText(f"开始解压：{filepath}"));
        self._unzipFile_(filepath, dirpath, isRmZip);

    # 解压回调
    def _unzipFile_(self, filepath, dirpath, isRmZip = True):
        with zipfile.ZipFile(filepath, "r") as zf:
            totalCnt = len(zf.namelist());
            completeCnt = 0;
            for file in zf.namelist():
                self.__tips.set(self.clipText(f"正在解压：{file}"));
                zf.extract(file, dirpath);
                completeCnt += 1;
                self.__progress.set(self.getLastProgress() + completeCnt/totalCnt * 100/self.__taskCnt);
            zf.close();
            # 移除zip文件
            if isRmZip:
                self.__tips.set(self.clipText(f"正在移除文件：{filepath}"));
                os.remove(filepath);
            self.__tips.set(self.clipText(f"完成解压：{filepath}"));

    # 裁剪文本
    def clipText(self, text):
        return clipText(text, 80);