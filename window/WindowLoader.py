import os;
import wx;

from core._Global import _GG;
from function.base import *;

from window.InstallerWindow.InstallerWindowCtr import InstallerWindowCtr;

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
		self.__windowCtr = InstallerWindowCtr();

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
		# 判断是否完成安装
		clientPath = _GG("ClientConfig").Config().Get("pytoolsip", "client", None);
		if clientPath:
			if wx.MessageDialog(self.__windowCtr.getUI(), "是否打开PyToolsIP？", "成功安装PyToolsIP", style = wx.OK|wx.CANCEL|wx.ICON_QUESTION).ShowModal() == wx.ID_OK:
				# 运行工程
				os.system("cd /d {}&start pytoolsip.exe".format(clientPath));
				# 延迟100ms后关闭安装窗口
				wx.CallLater(100, self.closeWindow);
		else:
			wx.CallLater(100, self.onInstall);
