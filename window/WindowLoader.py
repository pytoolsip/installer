import os;
import wx;

from _Global import _GG;
from function.base import *;

class WindowLoader(object):
	def __init__(self):
		super(WindowLoader, self).__init__();
		self._className_ = WindowLoader.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__mainApp = wx.App(False);

	def load(self):
		self.createWindow();
		self.runWindow();
		self.install();

	def run(self):
		self.__mainApp.MainLoop();

	def createWindow(self):
		self.__windowCtr = CreateCtr(_GG("g_ProjectPath") + "window/InstallerWindow", None);

	def runWindow(self):
		self.__windowCtr.getUI().Centre();
		self.__windowCtr.getUI().Show(True);

	def closeWindow(self):
		self.__windowCtr.getUI().Close(True);

	def install(self):
		# 校验环境
		self.__windowCtr.verifyEnv();
		# 处理启动事件
		self.__windowCtr.handleInstallerEvent(callbackInfo = {"callback" : self.onInstall});

	def onInstall(self):
		# 延迟1s后关闭安装窗口
		wx.CallLater(1000, self.closeWindow);
		pass;
