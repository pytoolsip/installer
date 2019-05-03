# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-08-25 13:25:32
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:39

from hotKeyCore.HotKeyConfig import *;

from _Global import _GG;
from function.base import *;

# 热键对象
class HotKeyObj(object):
	def __init__(self):
		super(HotKeyObj, self).__init__();
		self.__config = {};
		self.addConfig(config = HotKeyConfig);

	def addConfig(self, config = {}):
		for k,v in config.items():
			if k not in self.__config:
				self.__config[k] = [];
			self.__config[k].append(v);

	def removeConfig(self, config = {}):
		for k,v in config.items():
			if k in self.__config and v in self.__config[k]:
				self.__config[k].remove(v);
				if len(self.__config) == 0:
					self.__config.pop(k);

	def getIDList(self, key):
		return self.__config.get(key, []);

# 热键管理类
class HotKeyManager(object):
	def __init__(self):
		super(HotKeyManager, self).__init__();
		self._className_ = HotKeyManager.__name__;
		self.__HotKeyObj = HotKeyObj();

	def addHotKeyConfig(self, config = {}):
		self.__HotKeyObj.addConfig(config = config);

	def removeHotKeyConfig(self, config = {}):
		self.__HotKeyObj.removeConfig(config = config);

	def dispatchEvent(self, event):
		# 允许下个控件接收该事件
		event.DoAllowNextEvent();
		# # UnicodeKey为0，则不进行事件处理
		# if event.GetUnicodeKey() == 0 and (event.GetKeyCode() < 340 or event.GetKeyCode() > 351): # 兼容F1 ~ F12
		# 	return;
		# 根据事件获取热键值
		hotKey = self.getHotKeyByEvent(event);
		# 分发相应事件对应的事件
		eventIdList = self.__HotKeyObj.getIDList(hotKey);
		for eventId in eventIdList:
			_GG("EventDispatcher").dispatch(eventId, {"event" : event, "hotKey" : hotKey});

	# 根据事件获取热键值
	def getHotKeyByEvent(self, event):
		key = [];
		if event.ControlDown():
			key.append("CTRL");
		if event.AltDown():
			key.append("ALT");
		if event.ShiftDown():
			key.append("SHIFT");
		if event.GetKeyCode() >= 340 and event.GetKeyCode() <= 351:
			key.append("F" + str(event.GetKeyCode() - 339)); # F1 ~ F12
		elif event.GetKeyCode() in KeyCodeMap:
			key.append(KeyCodeMap[event.GetKeyCode()]);
		elif event.GetUnicodeKey() in UnicodeKeyMap:
			key.append(UnicodeKeyMap[event.GetUnicodeKey()]);
		else:
			key.append(chr(event.GetUnicodeKey()).upper());
		return "_".join(key);