# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-19 14:22:56
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-28 18:34:16
import wx;

# 加载工程
from window.WindowLoader import WindowLoader;
from core import _Global as _G;
from core.behaviorCore.BaseBehavior import BaseBehavior;
from core.behaviorCore.BehaviorManager import BehaviorManager;
from core.eventDispatchCore.EventDispatcher import EventDispatcher;
from core.eventDispatchCore.EventId import EVENT_ID;
from core.timerCore.TimerManager import TimerManager;

from config import AppConfig;
from config import ClientConfig;

class GlobalWindowObject(object):
	def __init__(self):
		super(GlobalWindowObject, self).__init__();
		pass;

class Loader(object):
	def __init__(self, mainPath):
		super(Loader, self).__init__();
		self._className_ = Loader.__name__;
		self.__mainPath = mainPath.replace("\\", "/");
		_G.initGlobal_GTo_Global(); # 初始化全局变量
		pass;

	def getWindowLoader(self):
		if not hasattr(self,"WindowLoader"):
			self.WindowLoader = WindowLoader();
		return self.WindowLoader;

	def lockGlobal_G(self):
		_G.lockGlobal_GTo_Global(); # 锁定全局变量

	def loadGlobalInfo(self):
		self.loadUniqueIdFunc(); # 加载唯一Id的全局函数
		self.loadPaths(); # 加载全局路径名变量
		self.loadObjects(); # 加载全局对象变量
		self.loadConfigs(); # 加载全局配置变量
		self.loadResources(); # 加载全局资源变量
		self.lockGlobal_G(); # 锁定全局变量
		pass;

	# 加载唯一Id的全局函数
	def loadUniqueIdFunc(self):
		global uniqueId;
		uniqueId = 0;
		def getUniqueId():
			global uniqueId;
			uniqueId += 1;
			return uniqueId;
		_G.setGlobalVarTo_Global("getUniqueId", getUniqueId);

	# 加载全局路径名变量
	def loadPaths(self):
		_G.setGlobalVarTo_Global("g_ProjectPath", self.__mainPath + "/");
		pass;

	# 加载全局对象变量
	def loadObjects(self):
		_G.setGlobalVarTo_Global("BaseBehavior", BaseBehavior); # 设置组件基础类变量（未实例化）
		_G.setGlobalVarTo_Global("WindowObject", GlobalWindowObject()); # 设置窗口类的全局变量
		_G.setGlobalVarTo_Global("BehaviorManager", BehaviorManager()); # 设置组件管理器的全局变量
		_G.setGlobalVarTo_Global("EventDispatcher", EventDispatcher()); # 设置事件分发器的全局变量
		_G.setGlobalVarTo_Global("EVENT_ID", EVENT_ID); # 设置事件枚举Id的全局变量
		_G.setGlobalVarTo_Global("TimerManager", TimerManager()); # 设置定时器管理器的全局变量
		pass;

	# 加载全局配置变量
	def loadConfigs(self):
		print("Loading configs......");
		_G.setGlobalVarTo_Global("AppConfig", AppConfig);
		_G.setGlobalVarTo_Global("ClientConfig", ClientConfig()); # 设置客户端配置的全局变量
		print("Loaded configs!");
		pass;

	# 加载全局资源变量
	def loadResources(self):
		print("Loading resources......");
		print("Loaded resources!");
		pass;