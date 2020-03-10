# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-26 22:05:03
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-10 17:40:53
import os;
import inspect;
import ctypes;
import subprocess;

# 停止线程
def stopThread(thread):
	try:
		if thread.isAlive():
			tid = ctypes.c_long(thread.ident);
			exctype = SystemExit;
			if not inspect.isclass(exctype):
				exctype = type(exctype);
			res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype));
			if res == 0:
				raise ValueError("Invalid thread !");
			elif res != 1:
				ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None);
				raise SystemError("PyThreadState_SetAsyncExc failed !");
	except Exception as e:
		print("stop thread failed !", e);
	

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call", argDict = {}):
	startupinfo = subprocess.STARTUPINFO();
	startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
	startupinfo.wShowWindow = subprocess.SW_HIDE;
	return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo, **argDict);