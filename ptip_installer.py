import os;
from _load import Loader;

# 初始化窗口加载器
Loader = Loader(os.getcwd());
Loader.loadGlobalInfo();
WindowLoader = Loader.getWindowLoader();

if __name__ == '__main__':
	# 加载并运行启动窗口
	WindowLoader.load();
	WindowLoader.run();