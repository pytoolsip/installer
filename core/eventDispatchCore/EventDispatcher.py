# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-01 10:11:02
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 18:10:12

from eventDispatchCore import EventId as G_EVENT;

from enum import Enum, unique;

# 枚举事件状态
@unique
class EventState(Enum):
	NormalState = 0;
	UnRegisterState = 1;

class EventDispatcher(object):
	"""docstring for EventDispatcher"""
	def __init__(self):
		super(EventDispatcher, self).__init__();
		self.__dispatchDepth = 0;
		self.__registerIds = [];
		self.__listeners = [];
		self.initByEventIds();

	def initByEventIds(self):
		# 事件Id是从0开始自增，故而range函数的参数为当前事件Id值加1
		for i in range(G_EVENT.CUR_EVENT_ID + 1):
			self.__registerIds.append({});
			self.__listeners.append([]);

	def updateEventIds(self):
		eventCount = max(len(self.__registerIds), len(self.__listeners));
		if G_EVENT.CUR_EVENT_ID + 1 > eventCount:
			for i in range(eventCount, G_EVENT.CUR_EVENT_ID + 1):
				self.__registerIds.append({});
				self.__listeners.append([]);

	def checkIsExistRegisterId(self, eventId, targetObj, callbackName):
		registerIdsDict = self.__registerIds[eventId];
		targetObjId = id(targetObj);
		if (targetObjId in registerIdsDict) and (callbackName in registerIdsDict[targetObjId]):
			return True;
		return False;

	def addRegisterId(self, eventId, targetObj, callbackName):
		registerIdsDict = self.__registerIds[eventId];
		targetObjId = id(targetObj);
		if targetObjId in registerIdsDict:
			registerIdsDict[targetObjId].append(callbackName);
		else:
			registerIdsDict[targetObjId] = [callbackName];
		pass;

	def removeRegisterId(self, eventId, targetObjId, callbackId):
		registerIdsDict = self.__registerIds[eventId];
		registerIdsDict[targetObjId].pop(callbackId);

	def register(self, event, targetObj, callbackName):
		try:
			eventId = event.value;
			if not self.checkIsExistRegisterId(eventId, targetObj, callbackName):
				self.__listeners[eventId].append({"target" : targetObj, "callbackName" : callbackName, "state" : EventState.NormalState});
				self.addRegisterId(eventId, targetObj, callbackName);
			else:
				raise Exception("Can\'t register the event(\"{0}\") repeatedly!".format(event));
		except Exception:
			raise Exception("Can\'t register the event(\"{0}\") !".format(event));

	def unregister(self, event, targetObj, callbackName):
		eventId = event.value;
		targetObjId = id(targetObj);
		listeners = self.__listeners[eventId];
		for i in range(len(listeners)-1, 0 ,-1):
			listener = listeners[i];
			if targetObjId == id(listener["target"]) and callbackName == listener["callbackName"]:
				listener["state"] = EventState.UnRegisterState;
				if self.__dispatchDepth == 0:
					self.removeRegisterId(eventId, targetObjId, callbackId);
					listeners.pop(i);

	def unregisterByTaget(self, event, targetObj):
		eventId = event.value;
		targetObjId = id(targetObj);
		listeners = self.__listeners[eventId];
		for i in range(len(listeners)-1, 0 ,-1):
			listener = listeners[i];
			if targetObjId == id(listener["target"]):
				listener["state"] = EventState.UnRegisterState;
				if self.__dispatchDepth == 0:
					listeners.pop(i);

	def dispatch(self, event, data, callObj = None):
		try:
			self.__dispatchDepth += 1;
			eventId = event.value;
			listeners = self.__listeners[eventId];
			if len(listeners) > 0:
				for listener in listeners:
					if listener["state"] == EventState.NormalState:
						targetObj = listener["target"];
						# 判断并初始化targetObj的EventIdListByDispatched_属性
						if not hasattr(targetObj, "_EventKeyListByDispatched_"):
							targetObj._EventKeyListByDispatched_ = [];
						# 判断eventKey是否在targetObj.EventIdListByDispatched_中
						eventKey = str(eventId) + listener["callbackName"];
						if eventKey not in targetObj._EventKeyListByDispatched_:
							targetObj._EventKeyListByDispatched_.append(eventKey);
							# 执行所注册事件的方法
							getattr(targetObj, listener["callbackName"])(data);
							# 移除targetObj的EventKeyListByDispatched_属性
							targetObj._EventKeyListByDispatched_.remove(eventKey);
						else:
							raise Exception("It calls the function(\"{0}\") of object(id:\"{1}\") in recursion !".format(listener["callbackName"], id(targetObj)));
			else:
				_GG("Log").w("It has not event(\"{0}\") to dispatch !".format(eventId));
			self.__dispatchDepth -= 1;
			pass;
		except Exception as e:
			raise Exception("It doesn\'t dispatch the event(\"{0}\") ! [{1}] .".format(eventId, e));
