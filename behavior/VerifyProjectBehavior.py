# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-05-03 19:40:59
# @Last Modified by:   Administrator
# @Last Modified time: 2019-05-03 19:40:59
import wx,json;

from _Global import _GG;
from function.base import *;

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
	};

def __getDepends__():
	return [
		{
			"path" : "VerifyEnvBehavior", 
			"basePath" : _GG("g_ProjectPath") + "behavior/",
		},
		{
			"path" : "InstallPyPkgBehavior", 
			"basePath" : _GG("g_ProjectPath") + "behavior/",
		},
	];

class VerifyProjectBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(VerifyProjectBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = VerifyProjectBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
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
		if hasattr(obj, "verifyPythonEnvironment"):
			if obj.verifyPythonEnvironment(pythonPath = _GG("ClientConfig").Config().Get("env", "python", None)):
				if hasattr(obj, "verifyPythonVersion"):
					if not obj.verifyPythonVersion(pythonPath = _GG("ClientConfig").Config().Get("env", "python", None)):
						return False, obj.showEntryPyVerPathDialog;
				return True;
			else:
				return False, obj.showEntryPyPathDialog;
		raise Exception("There is not attr of verifyPythonEnvironment in obj !");

	def showInstallPipMsgDialog(self, obj, _retTuple = None):
		messageDialog = wx.MessageDialog(obj, "是否要确认安装pip环境？", "校验pip环境失败！", style = wx.YES_NO|wx.ICON_QUESTION);
		if messageDialog.ShowModal() == wx.ID_YES:
			obj.showDetailTextCtrl(text = "正在安装pip环境...");
			if hasattr(obj, "installPipByEasyInstall"):
				if obj.installPipByEasyInstall():
					obj.showDetailTextCtrl(text = "安装“pip”环境成功。");
				else:
					obj.showDetailTextCtrl(text = "安装“pip”环境失败！");

	# 校验pip安装环境
	def verifyPipEnv(self, obj, _retTuple = None):
		if hasattr(obj, "verifyPipEnvironment"):
			if obj.verifyPipEnvironment(pythonPath = _GG("ClientConfig").Config().Get("env", "python", None)):
				return True;
			else:
				return False, obj.showInstallPipMsgDialog;
		raise Exception("There is not attr of verifyPipEnvironment in obj !");

	def showInstallModMsgDialog(self, obj, modNameList = [], _retTuple = None):
		messageDialog = wx.MessageDialog(obj, "是否要确认安装以下模块？\n" + "\n".join(modNameList), "校验import模块失败！", style = wx.YES_NO|wx.ICON_QUESTION);
		if messageDialog.ShowModal() == wx.ID_YES:
			obj.showDetailTextCtrl(text = "开始安装校验失败的模块...");
			if hasattr(obj, "installPackageByPip"):
				failedNameList = [];
				for modName in modNameList:
					if obj.installPackageByPip(modName):
						obj.showDetailTextCtrl(text = "安装“{}”模块成功。".format(modName));
					else:
						obj.showDetailTextCtrl(text = "安装“{}”模块失败！".format(modName));
						failedNameList.append(modName);
				return len(failedNameList) == 0;
			else:
				raise Exception("There is not attr of installPackageByPip in obj !");
		return False;

	# 校验import模块
	def verifyModuleMap(self, obj, _retTuple = None):
		if hasattr(obj, "checkPackageIsInstalled"):
			jsonPath = _GG("g_ProjectPath") + "config/json/importMap.json";
			if os.path.exists(jsonPath):
				modNameList = [];
				# 读取json文件
				with open(jsonPath, "rb") as f:
					moduleMap = json.loads(f.read().decode("utf-8", "ignore"));
					# 校验模块
					installedPkgDict = obj.getInstalledPackagesByPip(pythonPath = _GG("ClientConfig").Config().Get("env", "python", None))
					for modName in moduleMap:
						if modName not in installedPkgDict:
							modNameList.append(modName);
					f.close();
				if len(modNameList) == 0:
					return True;
				else:
					return False, obj.showInstallModMsgDialog, modNameList;
		raise Exception("There is not attr of checkPackageIsInstalled in obj !");
