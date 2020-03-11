# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-10 17:26:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-10 17:36:47
import math;

# 获取字符尺寸（中文字符相当于2个英文字符）
def getStrSize(text):
    tlen = len(text);
    return int((len(text.encode('utf-8')) - tlen)/2 + tlen);

# 剪切文本
# @params mode 模式：m->中间裁剪; s->头部裁剪; e->尾部裁剪
def clipText(text, maxSize, mode = "m"):
    diff = getStrSize(text) - maxSize;
    if diff <= 0: # 判断是否需要裁剪
        return text;
    # 裁剪的开始和结束位置
    sIdx, eIdx = 0, len(text);
    if mode == "m":
        mIdx = int(len(text) / 2);
        sIdx = mIdx - int(diff/4);
        eIdx = mIdx + math.ceil(diff/4);
    elif mode == "s":
        eIdx = sIdx + int(diff/2);
    elif mode == "e":
        sIdx = eIdx - int(diff/2);
    # 校验位置
    if eIdx < 0:
        eIdx = 0;
    if sIdx > len(text):
        sIdx = len(text);
    # 更新裁剪大小
    clipSize = getStrSize(text[sIdx:eIdx]);
    while (clipSize < diff and (sIdx > 0 or eIdx < len(text))):
        if sIdx > 0:
            clipSize += getStrSize(text[sIdx]);
            sIdx -= 1;
            if clipSize == diff:
                break;
        if eIdx < len(text):
            clipSize += getStrSize(text[eIdx]);
            eIdx += 1;
    return text[:sIdx] + "..." + text[eIdx:];