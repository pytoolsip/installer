import os;
from _load import Loader;

# 初始化窗口加载器
Loader = Loader(os.getcwd());
Loader.loadGlobalInfo(isConsole = False);
# 导入WindowLoader
from window.WindowLoader import WindowLoader;
winLoader = WindowLoader();

if __name__ == '__main__':
	# 加载并运行启动窗口
	winLoader.load();
	winLoader.run();