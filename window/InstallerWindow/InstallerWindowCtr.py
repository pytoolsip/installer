# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-05-03 17:23:43
# @Last Modified by:   Administrator
# @Last Modified time: 2019-05-03 17:23:43
import os,copy,threading;
import wx;

from _Global import _GG;
from InstallerWindowUI import *;

class InstallerWindowCtr(object):
	"""docstring for InstallerWindowCtr"""
	def __init__(self, parent = None, params = {}):
		super(InstallerWindowCtr, self).__init__();
		self._className_ = InstallerWindowCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent);
		self.bindBehaviors();
		self.scheduleTaskList = []; # 调度任务列表

	def __del__(self):
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent = None):
		# 创建视图UI类
		windowTitle = "安装PyToolsIP";
		windowSize = (640,420);
		windowStyle = wx.DEFAULT_FRAME_STYLE^(wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU);
		self.__ui = InstallerWindowUI(parent, id = -1, title = windowTitle, size = windowSize, style = windowStyle, curPath = self._curPath, windowCtr = self);
		self.__ui.SetBackgroundColour(wx.Colour(250,250,250));
		self.__ui.initWindow();

	def getUI(self):
		return self.__ui;
		
	"""
		key : 索引所创建控制类的key值
		path : 所创建控制类的路径
		parent : 所创建控制类的UI的父节点，默认为本UI
		params : 扩展参数
	"""
	def createCtrByKey(self, key, path, parent = None, params = {}):
		if not parent:
			parent = self.getUI();
		self.__CtrMap[key] = CreateCtr(path, parent, params = params);

	def getCtrByKey(self, key):
		return self.__CtrMap.get(key, None);

	def getUIByKey(self, key):
		ctr = self.getCtrByKey(key);
		if ctr:
			return ctr.getUI();
		return None;
			
	def updateWindow(self, data):
		self.__ui.updateWindow(data);

	def bindBehaviors(self):
		_GG("BehaviorManager").bindBehavior(self.getUI(), {"path" : _GG("g_ProjectPath") + "behavior/VerifyProjectBehavior"});
		pass;

	# 重新校验按钮回调
	def onReverifyButton(self, event = None):
		self.getUI().showReverifyButton(isShow = False);
		self.getUI().showDetailTextCtrl(isShow = False, isReset = True);
		self.handleInstallerEvent();
		pass;

	# 添加调度任务
	def addScheduleTask(self, data):
		if callable(data.get("scheduleTask")):
			# 添加到任务列表
			self.scheduleTaskList.append({
				"task" : data["scheduleTask"],
				"text" : data.get("text", "开始校验运行环境"),
				"args" : data.get("args", {}),
				"failInfo" : data.get("failInfo", {}),
			});

	def handleInstallerEvent(self, callbackInfo = {}, failCallbackInfo = {}):
		# 保存回调函数信息
		if callable(callbackInfo.get("callback")):
			self.launcherCallbackInfo = {
				"callback" : callbackInfo.get("callback"),
				"args": callbackInfo.get("args", {}),
				"failCallback" : failCallbackInfo.get("callback"),
				"failArgs" : failCallbackInfo.get("args", {}),
			};
		# 重置加载进度视图
		self.getCtrByKey("InstallerGaugeView").updateView({"isReset" : True});
		# 处理调度任务列表
		self.handleScheduleTaskList(copy.copy(self.scheduleTaskList));

	def handleScheduleTaskList(self, scheduleTaskList = []):
		if len(scheduleTaskList) > 0:
			taskInfo = scheduleTaskList.pop(0);
			self.getCtrByKey("InstallerGaugeView").updateView({
				"text" : taskInfo["text"],
				"gauge" : 1 - (len(scheduleTaskList) + 1)/len(self.scheduleTaskList),
			});
			# 启动线程
			threading.Thread(target = self.handleScheduleTask, args = (taskInfo, scheduleTaskList, )).start();
		else:
			self.getCtrByKey("InstallerGaugeView").updateView({
				"text" : "已完成安装，开始运行PyToolsIP。",
				"gauge" : 1,
			});
			if hasattr(self, "launcherCallbackInfo"):
				self.launcherCallbackInfo["callback"](*self.launcherCallbackInfo["args"].get("list", []), **self.launcherCallbackInfo["args"].get("dict", {}));

	def handleScheduleTask(self, taskInfo, scheduleTaskList = []):
		isContinue, taskResult = self.handleScheduleTaskInfo(taskInfo);
		if not isContinue:
			# 显示重新校验按钮
			wx.CallAfter(self.getUI().showReverifyButton);
			# 调用校验失败后的相关回调函数
			failInfo = taskInfo.get("failInfo", {});
			wx.CallAfter(self.getCtrByKey("InstallerGaugeView").updateView, {
				"text" : failInfo.get("text", "校验失败！"),
				"textColor" : failInfo.get("textColor", wx.Colour(255, 0, 0)),
			});
			failCallback = None;
			failArgs = {};
			if isinstance(taskResult, tuple) and len(taskResult) > 0:
				failCallback = taskResult[0];
				if len(taskResult) > 1:
					failArgs["list"] = taskResult[1:];
			if not callable(failCallback) and callable(failInfo.get("failCallback")):
				failCallback = failInfo.get("failCallback");
				failArgs = failInfo.get("failArgs", {});
			if callable(failCallback):
				def failCallbackFunc():
					if failCallback(*failArgs.get("list", []), **failArgs.get("dict", {})):
						self.getCtrByKey("InstallerGaugeView").updateView({"textColor" : wx.Colour(0, 0, 0)})
						# 继续执行任务列表中的任务
						scheduleTaskList.insert(0, taskInfo);
						self.handleScheduleTaskList(scheduleTaskList);
				wx.CallAfter(failCallbackFunc);
			else:
				# 调用校验失败后的回调函数
				if hasattr(self, "launcherCallbackInfo") and callable(self.launcherCallbackInfo.get("failCallback")):
					failArgs = self.launcherCallbackInfo.get("failArgs", {});
					wx.CallAfter(self.launcherCallbackInfo.get("failCallback"), *failArgs.get("list", []), **failArgs.get("dict", {}));
			return; # 不执行以下逻辑
		# 继续执行任务列表中的任务
		wx.CallAfter(self.handleScheduleTaskList, scheduleTaskList);

	def handleScheduleTaskInfo(self, taskInfo = {}):
		isContinue, taskResult = True, None;
		if callable(taskInfo.get("task")):
			args = taskInfo.get("args", {});
			result = taskInfo.get("task")(*args.get("list", []), **args.get("dict", {}));
			if isinstance(result, tuple) and len(result) > 0:
				isContinue = result[0];
				if len(result) > 1:
					taskResult = result[1:];
			else:
				isContinue = result;
		return isContinue, taskResult;

	# 校验环境
	def verifyEnv(self):
		self.addScheduleTask({
			"scheduleTask" : self.getUI().verifyPythonEnv,
			"text" : "正在校验python环境",
			"failInfo" : {
				"text" : "校验python环境失败！",
				# "failCallback" : self.showEntryPyPathDialog,
			},
		});
		self.addScheduleTask({
			"scheduleTask" : self.getUI().verifyPipEnv,
			"text" : "正在校验pip环境",
			"failInfo" : {
				"text" : "校验pip环境失败！",
				# "failCallback" : self.showInstallPipMsgDialog,
			},
		});
		self.addScheduleTask({
			"scheduleTask" : self.getUI().verifyModuleMap,
			"text" : "正在校验工程所需模块",
			"failInfo" : {
				"text" : "校验工程所需模块失败！",
				# "failCallback" : self.showInstallModMsgDialog,
			},
		});
		self.addScheduleTask({
			"scheduleTask" : self.getUI().downloadProject,
			"text" : "正在检查并下载工程",
			"failInfo" : {
				"text" : "下载工程失败！",
				# "failCallback" : self.showInstallModMsgDialog,
			},
		});