# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-01-13 22:29:38
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-14 17:32:19
import wx;

class TimerManager(object):
	def __init__(self):
		super(TimerManager, self).__init__()
		self.__timerMap = {};

	def createTimer(self, parent, tid = -1, callback = None):
		timer = wx.Timer(parent, id = tid);
		if callable(callback):
			parent.Bind(wx.EVT_TIMER, callback, timer);
		self.__timerMap[id(timer)] = timer;
		return timer;

	def deleteTimer(self, timer):
		if id(timer) in self.__timerMap:
			self.__timerMap.pop(id(timer));
		if timer.IsRunning():
			timer.Stop();

	def clearAllTimer(self):
		for timer in self.__timerMap.values():
			self.deleteTimer(timer);