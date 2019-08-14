# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-26 22:05:03
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-09-26 22:44:08

import inspect;
import ctypes;

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
	
