# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-04-22 12:01:48
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-16 15:09:26

import os;

from core._Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName",
	};

def __getExposeMethod__(DoType):
	return {
		"verifyPythonEnvironment" : DoType.AddToRear,
		"verifyPythonVersion" : DoType.AddToRear,
		"verifyPipEnvironment" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class VerifyEnvBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(VerifyEnvBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = VerifyEnvBehavior.__name__;
		pass;

	# 校验python环境
	def verifyPythonEnvironment(self, obj, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system("cd /d " + pythonPath.replace("\\", "/") + "&python.exe -V") == 0:
				return True;
		else:
			if os.system("python -V") == 0:
				return True;
		return False;

	# 校验python版本
	def verifyPythonVersion(self, obj, pythonPath = None, _retTuple = None):
		ret = "";
		if pythonPath:
			ret = os.popen("cd /d " + pythonPath.replace("\\", "/") + "&python.exe -V").read();
		else:
			ret = os.popen("python -V").read();
		if ret:
			retList = ret.split(" ");
			if len(retList) > 1:
				vList = retList[1].split(".");
				if len(vList) < 3:
					return False;
				if int(vList[0]) >= 3 and int(vList[1]) >= 4:
					return True;
		return False;

	def verifyPipEnvironment(self, obj, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system("cd /d " + pythonPath.replace("\\", "/") + "/Scripts&pip.exe -V") == 0:
				return True;
		else:
			if os.system("pip -V") == 0:
				return True;
		return False;
