# slope-surface

## 程序名称

赤平投影图绘制程序&结构面统计分析软件系统

## 运行环境

Python 2.7.8 + wxPython 3.0

## 安装须知

安装文件夹【install】中的软件，先安装Python27，再将其与组件安装到Python27所在目录。

## 使用方法

1. 赤平投影图绘制程序：

	双击touying.pyw文件，用Python27环境打开，即可出现程序界面。然后输入相关参数，点击【绘制投影】即可生成图形，点击【输出图片】可将图片保存。

	![赤平投影图绘制程序](https://raw.githubusercontent.com/Yibo-Li/slope-surface/master/%E8%B5%A4%E5%B9%B3%E6%8A%95%E5%BD%B1%E5%9B%BE%E7%BB%98%E5%88%B6%E8%BD%AF%E4%BB%B6.png)

2. 结构面统计分析软件：

	双击tongji.pyw文件，用Python27环境打开，即可出现程序界面。先点击【导入结构面信息】导入数据，如导入本文件夹中的joints.dat文件，然后点击【走向玫瑰花图】、【节理极点图】、【极点等密度图】可绘制相应图形，点击【输出图片】可以保存图形。

	![结构面统计分析软件](https://raw.githubusercontent.com/Yibo-Li/slope-surface/master/%E7%BB%93%E6%9E%84%E9%9D%A2%E7%BB%9F%E8%AE%A1%E5%88%86%E6%9E%90%E8%BD%AF%E4%BB%B6.png)

## 注意
1. 如果安装Python27组件时，没有正确获得Python27所在目录，请先修改注册表中的Python27所在目录，然后再安装Python27组件。
2. 确保tongji.pyw和touying.pyw文件所在目录无中文。
3. 如果双击tongji.pyw和touying.pyw文件无法打开，可能是你的电脑上已经安装有其他Python版本。可以从Python2.7.8的命令行打开程序文件来运行。
4. 如果遇到任何问题，可以提交issue处理。

### Just enjoy it!
