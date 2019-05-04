# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-05-03 17:23:43
# @Last Modified by:   Administrator
# @Last Modified time: 2019-05-03 17:23:43
import wx;

from core._Global import _GG;
from function.base import *;

class InstallerWindowUI(wx.Frame):
	"""docstring for InstallerWindowUI"""
	def __init__(self, parent, id = -1, title = "", pos = (0,0), size = (0,0), style = wx.DEFAULT_FRAME_STYLE, curPath = "", windowCtr = None):
		super(InstallerWindowUI, self).__init__(parent, id, title = title, pos = pos, size = size, style = style);
		self._className_ = InstallerWindowUI.__name__;
		self._curPath = curPath;
		self.__windowCtr = windowCtr;

	def getCtr(self):
		return self.__windowCtr;

	def initWindow(self):
		self.createViewCtrs();
		self.initWindowLayout();
		self.Centre();
		self.Show(True);
		pass;

	def createViewCtrs(self):
		self.getCtr().createCtrByKey("InstallerGaugeView", _GG("g_ProjectPath") + "view/InstallerGaugeView", params = {"size" : (self.GetSize()[0], -1)}); # , parent = self, params = {}
		self.createTitle();
		self.createReverifyButton();
		self.createDetailTextCtrl();
		self.createCopyrightInfo();
		pass;

	def initWindowLayout(self):
		hbox = wx.BoxSizer(wx.HORIZONTAL);
		vbox = wx.BoxSizer(wx.VERTICAL);
		vbox.Add(self.__title, 0, wx.ALIGN_CENTER|wx.TOP, 40);
		vbox.Add(self.__reverifyButton, 0, wx.ALIGN_CENTER|wx.TOP, 40)
		vbox.Add(self.getCtr().getUIByKey("InstallerGaugeView"), 0, wx.ALIGN_CENTER);
		vbox.Add(self.__detailTextCtrl, 0, wx.ALIGN_CENTER|wx.TOP, 10)
		vbox.Add(self.__copyrightInfo, 0, wx.ALIGN_CENTER|wx.TOP, 4);
		hbox.Add(vbox, 0, wx.ALIGN_TOP|wx.LEFT|wx.RIGHT, 20);
		self.SetSizer(hbox);
		pass;

	def updateWindow(self, data):
		pass;

	def createTitle(self):
		self.__title = wx.StaticText(self, label = _GG("AppConfig")["AppTitle"], style = wx.ALIGN_CENTER);
		font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD);
		self.__title.SetFont(font);

	def createReverifyButton(self):
		self.__reverifyButton = wx.Button(self, label = u"重新安装", size = (-1, 32));
		self.__reverifyButton.Bind(event = wx.EVT_BUTTON, handler = self.getCtr().onReverifyButton);
		wx.CallAfter(self.showReverifyButton, False);

	def createDetailTextCtrl(self):
		self.__detailTextCtrl = wx.TextCtrl(self, value = "", size = (self.GetSize().x, 160), style = wx.TE_READONLY|wx.TE_MULTILINE);
		wx.CallAfter(self.showDetailTextCtrl, False);

	def createCopyrightInfo(self):
		self.__copyrightInfo = wx.StaticText(self, label = _GG("AppConfig")["CopyrightInfo"], style = wx.ALIGN_CENTER);

	def showReverifyButton(self, isShow = True):
		self.__reverifyButton.Show(isShow);

	def showDetailTextCtrl(self, isShow = True, text = "", isReset = False):
		self.__detailTextCtrl.Show(isShow);
		if isShow and text != "":
			if isReset:
				self.__detailTextCtrl.SetValue(text);
			else:
				if self.__detailTextCtrl.GetValue():
					text = "\n" + text;
				self.__detailTextCtrl.AppendText(text);
		elif isReset:
			self.__detailTextCtrl.SetValue("");