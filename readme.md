# ProMan

ProMan是一个用Python编写，界面使用Pyside2的进程管理软件，能够列出当前系统内的进程名、PID、端口占用，并提供按进程名和端口筛选的功能，可以选中进程主动结束进程。

## 安装

您可以从[这里](https://github.com/96bearli/ProMan/releases)下载最新版本的ProMan软件，并解压到任意目录。

(目前仅支持windows下进程的管理)

您也可以从源代码编译ProMan软件，需要先安装Python3和Pyside2库：

## 使用

```bash
python process_manager.py
```

运行ProMan软件后，您会看到一个类似于任务管理器的界面，显示了当前系统内的所有进程信息。您可以通过点击表头来对进程进行排序，或者在搜索框中输入关键字来筛选进程。您还可以通过右键菜单或者工具栏按钮来结束选中的进程。

## 贡献

欢迎任何人对本项目进行贡献，无论是提交问题、建议、文档还是代码。请参考贡献指南来了解如何参与本项目。

## 许可

ProMan使用MIT许可证发布，详情请参见LICENSE文件。

