# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-02-24 05:57:41
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-09 16:40:47

try:
	import ConfigParser;
except Exception as e:
	import configparser as ConfigParser;

from core._Global import _GG;
from function.base import *;

class Config(object):
	"""docstring for Config"""
	def __init__(self):
		super(Config, self).__init__();
		self.__initConfig__();

	def __initConfig__(self):
		self.__config = {};

	def Set(self, section, option, value):
		if section not in self.__config:
			self.__config[section] = {};
		self.__config[section][option] = value;

	def Get(self, section, option, defaultValue = None):
		if section in self.__config:
			return self.__config[section].get(option, defaultValue);
		return defaultValue;


class ClientConfig(object):
	"""docstring for ClientConfig"""
	def __init__(self,):
		super(ClientConfig, self).__init__();
		# 初始化配置对象
		self.__config = Config();
		pass;

	def Config(self):
		return self.__config;