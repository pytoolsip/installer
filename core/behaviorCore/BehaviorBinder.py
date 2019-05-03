# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-24 22:31:21
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-16 14:55:15

from behaviorCore.BaseBehavior import DoType;

class BehaviorBinder(object):
	def __init__(self):
		super(BehaviorBinder, self).__init__();
		self._className_ = BehaviorBinder.__name__;
		pass;

	# 绑定组件到对象上
	def bindBehaviorToObj(self, behavior, obj):
		self.bindExposeDataOfBehaviorToObj(behavior, obj);
		self.bindExposeMethodOfBehaviorToObj(behavior, obj);
		pass;

	# 解绑组件
	def unbindBehaviorToObj(self, behavior, obj):
		self.unbindExposeDataOfBehaviorToObj(behavior, obj);
		self.unbindExposeMethodOfBehaviorToObj(behavior, obj);
		pass;

	# 绑定组件暴露的数据到对象上
	def bindExposeDataOfBehaviorToObj(self, behavior, obj):
		if not hasattr(obj, "behavior_exposeDataDict__"):
			obj.behavior_exposeDataDict__ = {};
		# 绑定组件导出属性
		exposeData = behavior.getBehaviorExposeData();
		for dataKey,data in exposeData.items():
			if dataKey in obj.behavior_exposeDataDict__: # obj.behavior_exposeDataDict__.has_key(dataKey)
				# 新添对应dataKey的导出数据
				obj.behavior_exposeDataDict__[dataKey]["behaviorInfos"].append({
					"data" : data,
					"behaviorId" : behavior.getBehaviorId(),
				});
			else:
				# 新建对应dataKey的导出数据
				obj.behavior_exposeDataDict__[dataKey] = {
					"oriData" : None,
					"curBehaviorId" : None,
					"behaviorInfos" : [{
						"data" : data,
						"behaviorId" : behavior.getBehaviorId(),
					}],
				};
				if hasattr(obj, dataKey):
					obj.behavior_exposeDataDict__[dataKey]["oriData"] = getattr(obj, dataKey);
				# 根据数据key值设置新数据
				self.setNewDataByDataKey(obj, dataKey, behaviorInfo = {"data" : data, "behaviorId" : behavior.getBehaviorId(),});

	# 绑定组件暴露的数据到对象上
	def bindExposeMethodOfBehaviorToObj(self, behavior, obj):
		if not hasattr(obj, "behavior_exposeMethodDict__"):
			obj.behavior_exposeMethodDict__ = {};
		# 绑定组件导出方法
		exposeMethod = behavior.getBehaviorExposeMethod();
		# 不允许组件导出方法的字段
		if hasattr(obj, "excludeMethod"):
			excludeMethod = obj.excludeMethod;
		else:
			excludeMethod = {};
		for methodKey,methodType in exposeMethod.items():
			if (methodKey in excludeMethod) and excludeMethod[methodKey] == True: # (not excludeMethod.has_key(methodKey)) or (excludeMethod[methodKey] == False)
				continue;
			if methodKey in obj.behavior_exposeMethodDict__: # obj.behavior_exposeMethodDict__.has_key(methodKey)
				# 新添对应methodKey的导出方法
				obj.behavior_exposeMethodDict__[methodKey]["behaviorInfos"].append({
					"behaviorId" : behavior.getBehaviorId(),
					"methodType" : methodType,
					"function" : getattr(behavior, methodKey),
				});
			else:
				# 新建对应methodKey的导出方法
				obj.behavior_exposeMethodDict__[methodKey] = {
					"oriFunc" : None,
					"behaviorInfos" : [{
						"behaviorId" : behavior.getBehaviorId(),
						"methodType" : methodType,
						"function" : getattr(behavior, methodKey),
					}],
				};
				if hasattr(obj, methodKey):
					obj.behavior_exposeMethodDict__[methodKey]["oriFunc"] = getattr(obj, methodKey);
				# 根据方法key值设置新方法
				self.setNewMethodByMethodKey(obj, methodKey);

	# 根据方法类型分离组件方法
	def splitBehaviorInfosByMethodType(self, behaviorInfos):
		frontBehaviorInfoList = [];
		overrideBehaviorInfoList = [];
		rearBehaviorInfoList = [];
		for behaviorInfo in behaviorInfos:
			if behaviorInfo["methodType"] == DoType.AddToFront:
				frontBehaviorInfoList.append(behaviorInfo);
			elif behaviorInfo["methodType"] == DoType.Override:
				overrideBehaviorInfoList.append(behaviorInfo);
			elif behaviorInfo["methodType"] == DoType.AddToRear:
				rearBehaviorInfoList.append(behaviorInfo);
			else:
				raise Exception("The methodType of behavior(id : \"{0}\") is error!".format(behaviorInfo["behaviorId"]));
		return frontBehaviorInfoList, overrideBehaviorInfoList, rearBehaviorInfoList;

	# 根据方法key值设置新方法
	def setNewMethodByMethodKey(self, obj, methodKey):
		# 定义新函数
		def newMethod(*argList, **argDict):
			if methodKey in obj.behavior_exposeMethodDict__:
				methodInfo = obj.behavior_exposeMethodDict__[methodKey];
				# 根据方法类型分离组件函数信息
				frontBehaviorInfoList, overrideBehaviorInfoList, rearBehaviorInfoList = self.splitBehaviorInfosByMethodType(methodInfo["behaviorInfos"]);
				# 判断是否有覆写函数
				if len(overrideBehaviorInfoList) > 0:
					_GG("Log").w("The behavior(id : \"{0}\") would override the method key of \"{1}\"!".format(overrideBehaviorInfoList[0]["behaviorId"], obj._className_));
					return overrideBehaviorInfoList[0]["function"](obj, *argList, **argDict);
				# 返回值
				_retTuple = None;
				# 前置组件函数
				for behaviorInfo in frontBehaviorInfoList:
					_retTuple = behaviorInfo["function"](obj, *argList, _retTuple = _retTuple, **argDict);
				# 对象的原始函数
				if methodInfo["oriFunc"]:
					_retTuple = methodInfo["oriFunc"](*argList, **argDict);
				# 后置组件函数
				for behaviorInfo in rearBehaviorInfoList:
					_retTuple = behaviorInfo["function"](obj, *argList, _retTuple = _retTuple, **argDict);
				return _retTuple;
		# 重置obj的methodKey函数
		setattr(obj, methodKey, newMethod);

	# 根据数据key值设置新数据
	def setNewDataByDataKey(self, obj, dataKey):
		dataInfo = obj.behavior_exposeDataDict__[dataKey];
		if len(dataInfo["behaviorInfos"]) > 0:
			_GG("Log").w("The behavior(id : \"{0}\") is setting the data key of \"{1}\"!".format(dataInfo["behaviorInfos"][-1]["behaviorId"], obj._className_));
			setattr(obj, dataKey, dataInfo["behaviorInfos"][-1]["data"]);
			obj.behavior_exposeDataDict__[dataKey]["curBehaviorId"] = dataInfo["behaviorInfos"][-1]["behaviorId"];

	# 解绑组件暴露的数据到对象上
	def unbindExposeDataOfBehaviorToObj(self, behavior, obj):
		if hasattr(obj, "behavior_exposeDataDict__"):
			exposeData = behavior.getBehaviorExposeData();
			for dataKey,_ in exposeData.items():
				if dataKey in obj.behavior_exposeDataDict__: # obj.behavior_exposeDataDict__.has_key(dataKey)
					# 移除相应的组件数据信息
					behaviorInfoList = obj.behavior_exposeDataDict__[dataKey]["behaviorInfos"];
					for idx in behaviorInfoList:
						if behaviorInfoList[idx]["behaviorId"] == behavior.getBehaviorId():
							behaviorInfoList.pop(idx);
					# 根据dataKey更新导出数据
					self.updateExposeDataByDataKey(obj, dataKey);

	# 解绑组件暴露的方法
	def unbindExposeMethodOfBehaviorToObj(self, behavior, obj):
		if hasattr(obj, "behavior_exposeMethodDict__"):
			exposeMethod = behavior.getBehaviorExposeMethod();
			for methodKey,_ in exposeMethod.items():
				if methodKey in obj.behavior_exposeMethodDict__: # obj.behavior_exposeMethodDict__.has_key(methodKey)
					# 移除相应的组件函数信息
					behaviorInfoList = obj.behavior_exposeMethodDict__[methodKey]["behaviorInfos"];
					for idx in behaviorInfoList:
						if behaviorInfoList[idx]["behaviorId"] == behavior.getBehaviorId():
							behaviorInfoList.pop(idx);
					# 根据dataKey更新导出函数
					self.updateExposeMethodByMethodKey(obj, dataKey);

	# 根据dataKey更新导出数据
	def updateExposeDataByDataKey(self, obj, dataKey):
		# 根据所绑定的组件信息，重置obj的dataKey属性
		if len(obj.behavior_exposeDataDict__[dataKey]["behaviorInfos"]) > 0:
			behaviorInfoList = obj.behavior_exposeDataDict__[dataKey]["behaviorInfos"];
			# 判断当前组件类型
			if obj.behavior_exposeDataDict__[dataKey]["curBehaviorId"] != behaviorInfoList[-1]["behaviorId"]:
				setattr(obj, dataKey, behaviorInfoList[-1]["data"]);
				obj.behavior_exposeDataDict__[dataKey]["curBehaviorId"] = behaviorInfoList[-1]["behaviorId"];
		else:
			if obj.behavior_exposeDataDict__[dataKey]["curBehaviorId"]:
				if obj.behavior_exposeDataDict__[dataKey]["oriData"]:
					setattr(obj, dataKey, obj.behavior_exposeDataDict__[dataKey]["oriData"]);
				else:
					delattr(obj, dataKey);
			obj.behavior_exposeDataDict__.pop(dataKey);

	# 根据dataKey更新导出函数
	def updateExposeMethodByMethodKey(self, obj, methodKey):
		# 根据所绑定的组件信息，重置obj的methodKey属性
		if len(obj.behavior_exposeMethodDict__[methodKey]["behaviorInfos"]) == 0:
			if obj.behavior_exposeMethodDict__[methodKey]["oriFunc"]:
				setattr(obj, methodKey, obj.behavior_exposeMethodDict__[methodKey]["oriFunc"]);
			else:
				delattr(obj, methodKey);
			obj.behavior_exposeMethodDict__.pop(methodKey);