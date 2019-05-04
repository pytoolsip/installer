# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-05-03 19:40:59
# @Last Modified by:   Administrator
# @Last Modified time: 2019-05-03 19:40:59

try:
	import ConfigParser;
except Exception as e:
	import configparser as ConfigParser;

import wx,json,os,shutil;

from core._Global import _GG;
from function.base import *;

from behavior.VerifyEnvBehavior import VerifyEnvBehavior;
from behavior.InstallPyPkgBehavior import InstallPyPkgBehavior;
from behavior.UpDownloadBehavior import UpDownloadBehavior;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"verifyPythonEnv" : DoType.AddToRear,
		"verifyPipEnv" : DoType.AddToRear,
		"verifyModuleMap" : DoType.AddToRear,
		"showEntryPyPathDialog" : DoType.AddToRear,
		"showInstallPipMsgDialog" : DoType.AddToRear,
		"showInstallModMsgDialog" : DoType.AddToRear,
		"downloadProject" : DoType.AddToRear,
	};

def __getDepends__():
	return [VerifyEnvBehavior(), InstallPyPkgBehavior(), UpDownloadBehavior()];

class VerifyProjectBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(VerifyProjectBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = VerifyProjectBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	print(obj._className_);
	# 	pass;

	def showEntryPyPathDialog(self, obj, _retTuple = None):
		entryDialog = wx.TextEntryDialog(obj, "未检测到python运行环境，请手动输入python运行程序路径：", "校验python环境失败！");
		if entryDialog.ShowModal() == wx.ID_OK:
			if entryDialog.GetValue():
				obj.showDetailTextCtrl(text = "正在设置python运行环境: {}".format(entryDialog.GetValue()));
				_GG("ClientConfig").Config().Set("env", "python", entryDialog.GetValue()); # 保存python运行环境
				return True;
		return False;

	def showEntryPyVerPathDialog(self, obj, _retTuple = None):
		entryDialog = wx.TextEntryDialog(obj, "检测到的python版本<3.4，请手动输入>3.4版本的python运行程序路径：", "校验python版本失败！");
		if entryDialog.ShowModal() == wx.ID_OK:
			if entryDialog.GetValue():
				obj.showDetailTextCtrl(text = "正在设置python运行环境: {}".format(entryDialog.GetValue()));
				_GG("ClientConfig").Config().Set("env", "python", entryDialog.GetValue()); # 保存python运行环境
				return True;
		return False;

	# 校验python环境
	def verifyPythonEnv(self, obj, _retTuple = None):
		if obj.verifyPythonEnvironment(pythonPath = _GG("ClientConfig").Config().Get("env", "python", None)):
			if not obj.verifyPythonVersion(pythonPath = _GG("ClientConfig").Config().Get("env", "python", None)):
				return False, obj.showEntryPyVerPathDialog;
			return True;
		return False, obj.showEntryPyPathDialog;

	def showInstallPipMsgDialog(self, obj, _retTuple = None):
		messageDialog = wx.MessageDialog(obj, "是否要确认安装pip环境？", "校验pip环境失败！", style = wx.YES_NO|wx.ICON_QUESTION);
		if messageDialog.ShowModal() == wx.ID_YES:
			obj.showDetailTextCtrl(text = "正在安装pip环境...");
			if obj.installPipByEasyInstall():
				obj.showDetailTextCtrl(text = "安装“pip”环境成功。");
			else:
				obj.showDetailTextCtrl(text = "安装“pip”环境失败！");

	# 校验pip安装环境
	def verifyPipEnv(self, obj, _retTuple = None):
		if obj.verifyPipEnvironment(pythonPath = _GG("ClientConfig").Config().Get("env", "python", None)):
			return True;
		return False, obj.showInstallPipMsgDialog;

	def showInstallModMsgDialog(self, obj, modNameList = [], _retTuple = None):
		messageDialog = wx.MessageDialog(obj, "是否要确认安装以下模块？\n" + "\n".join(modNameList), "校验import模块失败！", style = wx.YES_NO|wx.ICON_QUESTION);
		if messageDialog.ShowModal() == wx.ID_YES:
			obj.showDetailTextCtrl(text = "开始安装校验失败的模块...");
			failedNameList = [];
			for modName in modNameList:
				if obj.installPackageByPip(modName):
					obj.showDetailTextCtrl(text = "安装“{}”模块成功。".format(modName));
				else:
					obj.showDetailTextCtrl(text = "安装“{}”模块失败！".format(modName));
					failedNameList.append(modName);
			return len(failedNameList) == 0;
		return False;

	# 校验import模块
	def verifyModuleMap(self, obj, _retTuple = None):
		modNameList = [];
		# 校验模块
		installedPkgDict = obj.getInstalledPackagesByPip(pythonPath = _GG("ClientConfig").Config().Get("env", "python", None))
		for modName in _GG("AppConfig")["ModuleMap"]:
			if modName not in installedPkgDict:
				modNameList.append(modName);
		if len(modNameList) > 0:
			return False, obj.showInstallModMsgDialog, modNameList;
		return True;

	# 下载工程
	def downloadProject(self, obj, _retTuple = None):
		clientPath = _GG("ClientConfig").Config().Get("pytoolsip", "client", None);
		if clientPath:
			if wx.MessageDialog(obj, "检测到已安装PyToolsIP，是否直接启动？", "检测PyToolsIP工程", style = wx.YES_NO|wx.ICON_QUESTION).ShowModal() == wx.ID_YES:
				os.system("cd /d {}&start pytoolsip.exe".format(clientPath));
				return True;
			obj.showDetailTextCtrl(text = "您已安装了PyToolsIP，此次安装失败！");
			return False;
		dirPath, massage = "", "请选择安装路径!";
		while not dirPath:
			messageDialog = wx.MessageDialog(obj, massage, "安装PyToolsIP", style = wx.OK|wx.CANCEL|wx.ICON_INFORMATION);
			if messageDialog.ShowModal() == wx.ID_OK:
				dirPath = wx.DirSelector("选择安装路径");
				if not dirPath:
					massage = "安装路径不能为空，请重新选择安装路径！";
				else:
					# 校验文件夹
					if os.path.exists(os.path.join(dirPath, "PyToolsIP")):
						dirPath, massage = "", "安装路径下不能包含PyToolsIP，请重新选择安装路径！";
			else:
				obj.showDetailTextCtrl(text = "您取消了安装路径的选择，此次安装失败！");
				return False;
		# 下载的文件路径
		filePath = os.path.join(dirPath, "pytoolsip_client.zip");
		def onDownloadComplete(filePath):
			# 校验文件夹
			dirpath = os.path.join(dirPath, "PyToolsIP");
			if not os.path.exists(dirpath):
				os.mkdir(dirpath);
			# 解压pytoolsip_client.zip文件
			def afterUnzip():
				os.remove(filePath); # 删除压缩文件
				_GG("ClientConfig").Config().Set("pytoolsip", "client", dirpath); # 保存pytoolsip-client路径
				# comFilePath = os.path.join(dirPath, "pytoolsip_common.zip")
				# def onDownloadCommon(filePath):
				# 	# 校验文件夹
				# 	compath = os.path.join(dirpath, "assets/common");
				# 	if os.path.exists(compath):
				# 		shutil.rmtree(compath);
				# 	os.mkdir(compath);
				# 	# 解压pytoolsip_common.zip文件
				# 	def afterUnzipCommon():
				# 		os.remove(filePath); # 删除压缩文件
				# 		pass;
				# 	obj.unzipFile(filePath, compath, finishCallback = afterUnzipCommon);
				# 	pass;
				# obj.download(_GG("AppConfig")["CommonUrl"], comFilePath, onComplete = onDownloadCommon);

				# 同步配置文件
				self.syncConfigToClient(dirpath);
				pass;
			obj.unzipFile(filePath, dirpath, finishCallback = afterUnzip);
			pass;
		obj.download(_GG("AppConfig")["ClientUrl"], filePath, onComplete = onDownloadComplete);
		return True;

	# 同步配置文件
	def syncConfigToClient(self, clientPath):
		cfgPath = os.path.join(clientPath, "assets/common/config/ini");
		if not os.path.exists(cfgPath):
			return;
		cfgFile = os.path.join(cfgPath, "config.ini");
		if not os.path.exists(cfgFile):
			return;
		# 获取配置对象
		cfg = ConfigParser.RawConfigParser();
		cfg.read(cfgFile);
		# 同步python路径配置
		if not cfg.has_section("env"):
			cfg.add_section("env");
		cfg.set("env", "python", _GG("ClientConfig").Config().Get("env", "python", ""));
		# 保存配置
		cfg.write(open(cfgFile, "w"), "w");