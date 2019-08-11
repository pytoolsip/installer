from tkinter import *

from window.MainApp import *; # local
from window.MainWindow import *; # local

if __name__ == '__main__':
    # 加载程序
    App = MainApp();
    # 加载主场景
    MainWindow(App);
    # 运行程序
    App.mainloop();