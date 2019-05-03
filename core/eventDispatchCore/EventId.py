# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-01 10:56:10
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-29 17:34:37

from enum import Enum, unique;

# 自增的事件Id函数
global CUR_EVENT_ID;
CUR_EVENT_ID = -1;
def getNewEventId():
	global CUR_EVENT_ID;
	CUR_EVENT_ID += 1;
	return CUR_EVENT_ID;

# 枚举事件Id
@unique
class EVENT_ID(Enum):
	# 获取新的事件ID【供具体工具创建新的事件ID】
	@staticmethod
	def getNewId():
		return getNewEventId();

	TO_UPDATE_VIEW = getNewEventId(); # 创建事件Id的标准样式
	
	UPDATE_TREE_ITEMS = getNewEventId(); # 更新树状Items事件

	UPDATE_WINDOW_RIGHT_VIEW = getNewEventId(); # 更新右窗口视图

	SHOW_SEARCH_PANEL_EVENT = getNewEventId(); # 显示搜索面板事件

	ESC_DOWN_EVENT = getNewEventId(); # ESC按键事件

	RESTART_APP_EVENT = getNewEventId(); # 重启APP事件

	ADD_LAUNCHER_EVENT = getNewEventId(); # 添加启动事件

	LOGIN_SUCCESS_EVENT = getNewEventId(); # 登录成功事件

	UPDATE_WINDOW_LEFT_VIEW = getNewEventId(); # 更新左窗口视图