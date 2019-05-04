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

def GetConfigKeyMap():
	return {
		"Config" : _GG("g_ProjectPath") + "config/ini/config.ini",
	};

class Config(object):
	"""docstring for Config"""
	def __init__(self, path):
		super(Config, self).__init__();
		self.__path = path;
		self.__initConfig__();

	def __initConfig__(self):
		self.__config = ConfigParser.RawConfigParser();
		self.__config.read(self.__path);

	def Set(self, section, option, value):
		if not self.__config.has_section(section):
			self.__config.add_section(section);
		self.__config.set(section, option, value);
		self.__config.write(open(self.__path, "w"), "w");

	def Get(self, section, option, defaultValue = None):
		if self.__config.has_option(section, option):
			return self.__config.get(section, option);
		return defaultValue;


class ClientConfig(object):
	"""docstring for ClientConfig"""
	def __init__(self,):
		super(ClientConfig, self).__init__();
		# 初始化配置对象
		confKeyMap = GetConfigKeyMap();
		self.__config = Config(confKeyMap["Config"]);
		pass;

	def Config(self):
		return self.__config;