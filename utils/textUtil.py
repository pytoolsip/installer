# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-10 17:26:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-10 17:36:47

# 剪切文本
# @params mode 模式：m->中间裁剪; s->头部裁剪; e->尾部裁剪
def clipText(text, maxLen, mode = "m"):
    diff = len(text) - maxLen;
    if diff <= 0: # 判断是否需要裁剪
        return text;
    # 裁剪的开始和结束位置
    sIdx, eIdx = 0, len(text);
    if mode == "m":
        mIdx = int(len(text) / 2);
        sIdx = mIdx - int(diff/2);
        eIdx = mIdx + math.ceil(diff/2);
    elif mode == "s":
        eIdx = sIdx + diff;
    elif mode == "e":
        sIdx = eIdx - diff;
    # 校验位置
    if eIdx < 0:
        eIdx = 0;
    if sIdx > len(text):
        sIdx = len(text);
    return text[:sIdx] + "..." + text[eIdx:];