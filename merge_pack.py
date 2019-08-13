# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-08-08 17:50:27
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-08-08 19:47:35
import os, re;

# 导入过滤
importMap = [];

# 检测是否已经加载过
def checkImported(ip):
	if ip in importMap:
		return True;
	importMap.append(ip);
	return False;

# 匹配组合的第一个
def matchFirst(p, s):
	mt = re.match(p, s);
	if mt:
		return mt.group(1).strip();
	return "";

# 根据文件夹，获取内容
def writeContentByFile(path, file):
	with open(path, "r", encoding = "utf-8") as f:
		for line in f.readlines():
			mt = matchFirst("^from\s*(.*)\s*import\s*\*.*#\s*local", line);
			if mt:
				if checkImported(mt):
					continue;
				writeContentByFile(mt.replace(".", "/")+".py", file);
				file.write("\n");
			elif not re.match("^#.*", line):
				# 匹配from import
				fip = matchFirst("^.*(from\s*\w+\s*import\s*[\w+,\*]).*", line);
				if fip:
					if checkImported(fip):
						continue;
				else:
					# 匹配import
					ip = matchFirst("^.*(import\s*\w+).*", line);
					if ip:
						if checkImported(ip):
							continue;
				if line.strip():
					file.write(line);

# 合并文件内容，并输出到指定文件
def merge(srcFile, tgtFile):
	with open(tgtFile, "w+", encoding = "utf-8") as f:
		writeContentByFile(srcFile, f);

# 打包文件
def pack(tgtFile):
	code = os.system(f"pyInstaller -F -w {tgtFile} --distpath=./dist");
	if code != 0:
		raise Exception(f"Pack failed! [code:{code}]");

if __name__ == '__main__':
	tgtPath = "installer.py"; # 目标文件路径
	if os.path.exists("main.py"):
		merge("main.py", tgtPath);
		pack(tgtPath);