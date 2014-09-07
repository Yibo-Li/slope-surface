#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Arrow, RegularPolygon
from matplotlib.tri import Triangulation
from collections import Counter
from numpy import arange, sin, pi
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas  

import os
import wx

from pylab import mpl  
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体 
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

class MyFrame(wx.Frame):
    input1="180"
    input2="60"
    input3="115"
    input4="45"
    input5="245"
    input6="45"
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,u"赤平投影图绘制程序 @李轶博",size=(355,570),style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        panel=wx.Panel(self,-1)
        panel.SetBackgroundColour("White")
        
        #添加文本
        wx.StaticText(panel, -1, u"倾向（°）", pos=(105, 15))
        wx.StaticText(panel, -1, u"倾角（°）", pos=(235, 15))
        wx.StaticText(panel, -1, u"边    坡", pos=(30, 45))
        wx.StaticText(panel, -1, u"结构面J1", pos=(30, 85))
        wx.StaticText(panel, -1, u"结构面J2", pos=(30, 125))

        #添加文本框
        self.Text1 = wx.TextCtrl(panel, -1, value="180", pos=(100, 40),size=(70,20))
        self.Text2 = wx.TextCtrl(panel, -1, value="60", pos=(230, 40),size=(70,20))
        self.Text3 = wx.TextCtrl(panel, -1, value="115", pos=(100, 80),size=(70,20))
        self.Text4 = wx.TextCtrl(panel, -1, value="45", pos=(230, 80),size=(70,20))
        self.Text5 = wx.TextCtrl(panel, -1, value="245", pos=(100, 120),size=(70,20))
        self.Text6 = wx.TextCtrl(panel, -1, value="45", pos=(230, 120),size=(70,20))

        #添加按钮
        Button1 = wx.Button(panel, -1, u"绘制投影", pos=(20, 500),size=(90,25))        
        Button2 = wx.Button(panel, -1, u"输出图片", pos=(130, 500),size=(90,25))
        Button3 = wx.Button(panel, -1, u"退出", pos=(240, 500),size=(90,25))

        #绑定按钮事件
        Button1.Bind(wx.EVT_BUTTON,self.draw)
        Button2.Bind(wx.EVT_BUTTON,self.save)
        Button3.Bind(wx.EVT_BUTTON,self.close)

        #初始化画布
        self.panel2=wx.Panel(panel,-1,pos=(15,165),size=(320,320))        
        self.panel2.figure = plt.figure(figsize=(4,4))  
        self.panel2.axes = self.panel2.figure.add_subplot(111)
        self.panel2.axes.axis('equal')
        self.panel2.axes.axis('off')
        self.panel2.canvas = FigureCanvas(self.panel2, -1, self.panel2.figure)
        self.panel2.Fit()  

    def close(self,event):
        ret = wx.MessageBox(u"你真的要离开吗？",  u"提示", wx.OK|wx.CANCEL)
        if ret == wx.OK:
            app.ExitMainLoop()
            #wx.Exit()    

    def save(self,event):
        saveExt = "Image files(*.png)|*.png|All files(*.*)|*.*" 
        dlg = wx.FileDialog(self, u"输出图片", os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT, wildcard=saveExt)
        if dlg.ShowModal() == wx.ID_OK:
            savefile = dlg.GetPath()            
            if not os.path.splitext(savefile)[1]:
                savefile = savefile + ".png"
            self.panel2.figure.savefig(savefile)
        dlg.Destroy()

    def draw(self,event):
        #获取参数
        self.input1=self.Text1.GetValue()
        self.input2=self.Text2.GetValue()
        self.input3=self.Text3.GetValue()
        self.input4=self.Text4.GetValue()
        self.input5=self.Text5.GetValue()
        self.input6=self.Text6.GetValue()
        #初始化画布
        self.panel2.figure = plt.figure(figsize=(4,4))  
        self.panel2.axes = self.panel2.figure.add_subplot(111)
        self.panel2.axes.axis('equal')
        self.panel2.axes.axis('off')

        #设置大圆半径R=1
        #生成投影网外圆
        an = np.linspace(0,2*np.pi,100)
        self.panel2.axes.plot( np.cos(an), np.sin(an) )

        #生成投影网刻度
        s = np.linspace(0,2*np.pi,37)
        for ang in s:
            l = Line2D([np.cos(ang), 1.02*np.cos(ang)], [np.sin(ang), 1.02*np.sin(ang)])                                    
            self.panel2.axes.add_line(l)
        self.panel2.axes.text(0, 1.05, 'N')
        self.panel2.axes.text(1.05,  0, 'E')
        self.panel2.axes.text(-1.15, 0, 'W')
        self.panel2.axes.text(0, -1.1, 'S')

        #生成结构面圆弧J1
        qinxiang1=float(self.input3)/180*np.pi
        qinjiao1=float(self.input4)/180*np.pi
        t1=-qinjiao1/np.pi*180-qinxiang1/np.pi*180
        t2=2*(90-qinxiang1/np.pi*180)-t1

        banjing=1/np.cos(qinjiao1)
        yuanxin=[np.tan(qinjiao1)*np.sin(qinxiang1),np.tan(qinjiao1)*np.cos(qinxiang1)]
        circle=Arc(yuanxin,2*banjing,2*banjing,color='purple',fill=False,theta1=t2,theta2=t1)
        self.panel2.axes.add_patch(circle)

        t3=np.tan(qinjiao1)*np.sin(qinxiang1)-np.cos(np.pi/2-qinxiang1)/np.cos(qinjiao1)
        t4=np.tan(qinjiao1)*np.cos(qinxiang1)-np.sin(np.pi/2-qinxiang1)/np.cos(qinjiao1)
        self.panel2.axes.arrow(t3,t4,0-t3,0-t4,length_includes_head=True,color='purple')
        
        self.panel2.axes.annotate('J1', xy=(t3, t4), xytext=(t3-0.2, t4),arrowprops=dict(facecolor='black',arrowstyle="->"))
        
        #生成结构面圆弧J2
        qinxiang2=float(self.input5)/180*np.pi
        qinjiao2=float(self.input6)/180*np.pi
        t1=-qinjiao2/np.pi*180-qinxiang2/np.pi*180
        t2=2*(90-qinxiang2/np.pi*180)-t1

        banjing=1/np.cos(qinjiao2)
        yuanxin=[np.tan(qinjiao2)*np.sin(qinxiang2),np.tan(qinjiao2)*np.cos(qinxiang2)]
        circle=Arc(yuanxin,2*banjing,2*banjing,color='purple',fill=False,theta1=t2,theta2=t1)
        self.panel2.axes.add_patch(circle)

        t3=np.tan(qinjiao2)*np.sin(qinxiang2)-np.cos(np.pi/2-qinxiang2)/np.cos(qinjiao2)
        t4=np.tan(qinjiao2)*np.cos(qinxiang2)-np.sin(np.pi/2-qinxiang2)/np.cos(qinjiao2)
        self.panel2.axes.arrow(t3,t4,0-t3,0-t4,length_includes_head=True,color='purple')

        self.panel2.axes.annotate('J2', xy=(t3, t4), xytext=(t3+0.2, t4),arrowprops=dict(facecolor='black',arrowstyle="->"))

        #生成坡面圆弧
        qinxiang3=float(self.input1)/180*np.pi
        qinjiao3=float(self.input2)/180*np.pi
        t1=-qinjiao3/np.pi*180-qinxiang3/np.pi*180
        t2=2*(90-qinxiang3/np.pi*180)-t1

        banjing=1/np.cos(qinjiao3)
        yuanxin=[np.tan(qinjiao3)*np.sin(qinxiang3),np.tan(qinjiao3)*np.cos(qinxiang3)]
        circle=Arc(yuanxin,2*banjing,2*banjing,color='red',fill=False,theta1=t2,theta2=t1)
        self.panel2.axes.add_patch(circle)

        t3=np.tan(qinjiao3)*np.sin(qinxiang3)-np.cos(np.pi/2-qinxiang3)/np.cos(qinjiao3)
        t4=np.tan(qinjiao3)*np.cos(qinxiang3)-np.sin(np.pi/2-qinxiang3)/np.cos(qinjiao3)
        self.panel2.axes.arrow(t3,t4,0-t3,0-t4,length_includes_head=True,color='red')

        self.panel2.axes.annotate('Slope', xy=(t3, t4), xytext=(t3+0.2, t4),arrowprops=dict(facecolor='black',arrowstyle="->"))

        #生成结构面交割线投影
        x1=np.tan(qinjiao1)*np.sin(qinxiang1)
        y1=np.tan(qinjiao1)*np.cos(qinxiang1)
        x2=np.tan(qinjiao2)*np.sin(qinxiang2)
        y2=np.tan(qinjiao2)*np.cos(qinxiang2)
        #plt.axes().arrow(x1,y1,0-x1,0-y1,length_includes_head=True)
        #plt.axes().arrow(x2,y2,0-x2,0-y2,length_includes_head=True)
        r1=1/np.cos(qinjiao1)
        r2=1/np.cos(qinjiao2)
        #print(r1)
        #print(r2)
        d=np.sqrt((x1-x2)**2+(y1-y2)**2)
        #print(d)
        x=(r1**2-r2**2+d**2)/(2*d)
        #print(x)
        a=np.arctan((y1-y2)/(x1-x2))
        b=a+np.pi/2
        if x1>=x2:
            if (x1-(x*np.cos(a)))>=x2 and (x1-(x*np.cos(a)))<=x1:
                x0=x1-(x*np.cos(a))
                y0=y1-(x*np.sin(a))
            else:
                x0=x1+(x*np.cos(a))
                y0=y1+(x*np.sin(a))
        else:
            if (x1-(x*np.cos(a)))>=x1 and (x1-(x*np.cos(a)))<=x2:
                x0=x1-(x*np.cos(a))
                y0=y1-(x*np.sin(a))
            else:
                x0=x1+(x*np.cos(a))
                y0=y1+(x*np.sin(a))
        #plt.axes().arrow(x0,y0,0-x0,0-y0,length_includes_head=True)
        h=np.sqrt(r1**2.0-x**2)
        t3=x0+(h*np.cos(b))
        t4=y0+(h*np.sin(b))
        if np.sqrt(t3**2+t4**2)>1:            
            t3=x0-(h*np.cos(b))
            t4=y0-(h*np.sin(b))
        #print('交割线倾向',90-b/np.pi*180)#交割线倾向
        #print('交割线倾角',90-2*np.arctan(np.sqrt(t3**2+t4**2))*180/np.pi)#交割线倾角
        self.panel2.axes.arrow(t3,t4,0-t3,0-t4,length_includes_head=True,color='green')
        
        #显示结果
        self.panel2.canvas = FigureCanvas(self.panel2, -1, self.panel2.figure) 
        self.panel2.Fit() 

if __name__=="__main__":
    app=wx.App()
    frame=MyFrame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
