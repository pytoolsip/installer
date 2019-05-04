# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-05-03 22:24:20
# @Last Modified by:   Administrator
# @Last Modified time: 2019-05-03 22:24:20

import wx;

from core._Global import _GG;
from function.base import *;

class InstallerGaugeViewUI(wx.Panel):
	"""docstring for InstallerGaugeViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(InstallerGaugeViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = InstallerGaugeViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_NONE,
			"fgColour" : wx.Colour(0,0,0),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createGauge();
		self.createInfoText();
		pass;
		
	def initViewLayout(self):
		vbox = wx.BoxSizer(wx.VERTICAL);
		vbox.Add(self.__text);
		vbox.Add(self.__gauge, flag = wx.ALIGN_CENTER);
		self.SetSizer(vbox);
		pass;

	def updateView(self, data):
		if "text" in data:
			self.__text.SetLabel(data["text"]);
		if "textColor" in data:
			self.__text.SetForegroundColour(data["textColor"]);
		if "gauge" in data:
			self.__gauge.SetValue(data["gauge"] * self.__gauge.GetRange());
		if "isReset" in data:
			self.resetView(data);
		pass;

	def createGauge(self):
		self.__gauge = wx.Gauge(self, size = (self.GetSize()[0], 20), style = wx.GA_SMOOTH);

	def createInfoText(self):
		self.__text = wx.StaticText(self, label = "正在启动...", style = wx.ALIGN_LEFT);

	def resetView(self, data = {}):
		self.updateView({
			"text" : "",
			"textColor" : self.__params["fgColour"],
			"gauge" : 0,
		});