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
import wx.grid

from pylab import mpl  
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体 
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题  

class MyFrame(wx.Frame):
    #全局变量
    fileName = ""
    fileExt = "Data files(*.dat;*.txt)|*.dat;*.txt|All files(*.*)|*.*"
    saveExt = "Image files(*.png)|*.png|All files(*.*)|*.*" 
    Dip=[]
    Dia=[]
    Id=0
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,u"结构面统计分析软件",size=(750,530),style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        panel=wx.Panel(self,-1)
        panel.SetBackgroundColour("White")
        #添加按钮
        Button1 = wx.Button(panel, -1, u"导入结构面信息", pos=(25, 20),size=(105,25))
        Button2 = wx.Button(panel, -1, u"走向玫瑰花图", pos=(25, 60),size=(105,25))
        Button3 = wx.Button(panel, -1, u"节理极点图", pos=(25, 100),size=(105,25))
        Button4 = wx.Button(panel, -1, u"极点等密度图", pos=(25, 140),size=(105,25))
        Button5 = wx.Button(panel, -1, u"输出图片", pos=(10, 450),size=(60,30))
        Button6 = wx.Button(panel, -1, u"退出", pos=(90, 450),size=(60,30))

        #绑定按钮事件
        Button1.Bind(wx.EVT_BUTTON,self.openFile)
        Button6.Bind(wx.EVT_BUTTON,self.onClose)
        Button5.Bind(wx.EVT_BUTTON,self.saveFile)
        Button2.Bind(wx.EVT_BUTTON,self.drawRose)
        Button3.Bind(wx.EVT_BUTTON,self.drawPole)
        Button4.Bind(wx.EVT_BUTTON,self.drawContour)

        #添加列表控件
        self.grid = wx.grid.Grid(panel, -1,pos=(10,180), size=(140,260))
        self.grid.SetDefaultColSize(44, resizeExistingCols=True)
        self.grid.SetDefaultRowSize(20, resizeExistingRows=True)
        self.grid.SetRowLabelSize(35)
        self.grid.SetColLabelSize(20)
        self.grid.EnableDragGridSize(enable=False)
        self.grid.EnableEditing(edit=False)
        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)        
        self.grid.CreateGrid(20, 2)
        self.grid.SetColLabelValue(0, u"倾向°")
        self.grid.SetColLabelValue(1, u"倾角°")

        #初始化画布
        self.panel2=wx.Panel(panel,-1,pos=(175,10),size=(400,480))        
        self.panel2.figure = plt.figure(figsize=(7,6))  
        self.panel2.axes = self.panel2.figure.add_subplot(111)
        self.panel2.axes.axis('equal')
        self.panel2.axes.axis('off')
        self.panel2.canvas = FigureCanvas(self.panel2, -1, self.panel2.figure)
        self.panel2.Fit()        

    def openFile(self,event):
        #打开文件对话框
        dlg = wx.FileDialog(self, u"导入结构面信息...", os.getcwd(), style = wx.OPEN, wildcard = self.fileExt)
        if dlg.ShowModal() == wx.ID_OK:
            self.fileName = dlg.GetPath()
            self.readFile()
        dlg.Destroy()

    def readFile(self):
        #读入结构面文件，并将数据分布存到Dip和Dia数组
        if self.fileName:
            self.Dip=[]
            self.Dia=[]
            self.Id=0
            self.grid.ClearGrid()
            f = open(self.fileName, 'r')
            for line in f:
                    if line[-1]=='\n':
                        line=line[0:-1]
                        line=line.split()
                        #print line[0]
                        if line[0]!='#':
                            self.Dip.append(float(line[1]))
                            self.Dia.append(float(line[2]))
                            #print self.Dip[self.Id],self.Dia[self.Id]
                            if self.grid.GetNumberRows()<self.Id+1:
                                self.grid.AppendRows(numRows=1)
                            self.grid.SetCellValue(self.Id, 0, str(self.Dip[self.Id]))
                            self.grid.SetCellValue(self.Id, 1, str(self.Dia[self.Id]))
                            self.Id=self.Id+1
            if self.grid.GetNumberRows()>self.Id:
                self.grid.DeleteRows(pos=self.Id, numRows=self.grid.GetNumberRows()-self.Id)

    def saveFile(self,event):
        dlg = wx.FileDialog(self, u"输出图片", os.getcwd(), style=wx.SAVE | wx.OVERWRITE_PROMPT, wildcard=self.saveExt)
        if dlg.ShowModal() == wx.ID_OK:
            savefile = dlg.GetPath()            
            if not os.path.splitext(savefile)[1]:
                savefile = savefile + ".png"
            self.panel2.figure.savefig(savefile)
        dlg.Destroy()        

    def onClose(self,event):
        ret = wx.MessageBox(u"你真的要离开吗？",  u"提示", wx.OK|wx.CANCEL)
        if ret == wx.OK:
            app.ExitMainLoop()
            #wx.Exit()

    def drawRose(self,event):
        #绘制玫瑰花图
        #初始化画布
        self.panel2.figure = plt.figure(figsize=(7,6))  
        self.panel2.axes = self.panel2.figure.add_subplot(111)
        self.panel2.axes.axis('equal')
        self.panel2.axes.axis('off')
        #设置大圆半径R=1
        #生成投影网外圆
        an = np.linspace(0,np.pi,100)
        self.panel2.axes.plot( np.cos(an), np.sin(an) )
        self.panel2.axes.plot( 0.2*np.cos(an), 0.2*np.sin(an), color='blue')
        self.panel2.axes.plot( 0.4*np.cos(an), 0.4*np.sin(an), color='blue')
        self.panel2.axes.plot( 0.6*np.cos(an), 0.6*np.sin(an), color='blue')
        self.panel2.axes.plot( 0.8*np.cos(an), 0.8*np.sin(an), color='blue')

        #生成投影网刻度
        s = np.linspace(0,np.pi,19)
        for ang in s:
            l = Line2D([np.cos(ang), 0*np.cos(ang)], [np.sin(ang), 0*np.sin(ang)])                                    
            self.panel2.axes.add_line(l)
        self.panel2.axes.text(-0.30, 1.20, u'节理走向玫瑰花图', fontsize=16)
        self.panel2.axes.text(0, 1.05, 'N')
        self.panel2.axes.text(1.05,  0, 'E')
        self.panel2.axes.text(-1.05, 0, 'W')
        self.panel2.axes.text(0.15, -0.05, '30')
        self.panel2.axes.text(0.35, -0.05, '60')
        self.panel2.axes.text(0.55, -0.05, '90')
        self.panel2.axes.text(0.75, -0.05, '120')
        self.panel2.axes.text(0.95, -0.05, '150')
        self.panel2.axes.add_line(Line2D([-0.05,0.05],[0, 0]))
        self.panel2.axes.add_line(Line2D([0, 0],[-0.05,0.05]))

        #统计走向区间
        #sorted(self.Dip)
        a=[[]]
        for i in range(0,36):
            num=0
            sum=0
            #print j,self.Dip[j]
            for j in range(0,len(self.Dip)):
                if self.Dip[j]>=i*10 and self.Dip[j]<i*10+10:
                    #print(j)
                    a[i].append(self.Dip[j])
                    num=num+1
                    sum=sum+self.Dip[j]
            a[i].append(num)
            #print num
            if num==0:
                a[i].append(0)
            else:
                a[i].append(sum/num)            
            #print(a[i][-2],a[i][-1])
            a.append([])

        x=[0,]
        y=[0,]
        for i in range(17,-1,-1):
            #print(a[i][-2],a[i][-1])
            t1=(a[i][-2]+a[i+18][-2])/150.0
            if 0==t1:
                t2=0
            else:
                t2=(a[i][-2]*(180-a[i][-1])+a[i+18][-2]*(360-a[i+18][-1]))/(a[i][-2]+a[i+18][-2])
            #print(t1,t2)
            x.append(t1*np.cos(t2/180*np.pi))
            y.append(t1*np.sin(t2/180*np.pi))
            
        x.append(0)
        y.append(0)        
        self.panel2.axes.fill(x, y, 'r')
        self.panel2.axes.plot(x,y)
        
        self.panel2.canvas = FigureCanvas(self.panel2, -1, self.panel2.figure) 
        self.panel2.Fit()

    def drawPole(self,event):
        #绘制极点图
        #初始化画布
        self.panel2.figure = plt.figure(figsize=(7,6))  
        self.panel2.axes = self.panel2.figure.add_subplot(111)
        self.panel2.axes.axis('equal')
        self.panel2.axes.axis('off')
        #self.panel2.axes.draw()
        #self.panel2.canvas.draw()
        #设置大圆半径R=1.5
        #生成投影网外圆
        an = np.linspace(0,2*np.pi,100)
        self.panel2.axes.plot( 1.5*np.cos(an), 1.5*np.sin(an) )

        #生成投影网刻度
        s = np.linspace(0,2*np.pi,37)
        for ang in s:
            l = Line2D([1.5*np.cos(ang), 1.52*np.cos(ang)], [1.5*np.sin(ang), 1.52*np.sin(ang)])                                    
            self.panel2.axes.add_line(l)
        self.panel2.axes.text(-0.35, 1.7, u'节理极点图', fontsize=16)
        self.panel2.axes.text(0, 1.55, 'N')
        self.panel2.axes.text(1.55,  0, 'E')
        self.panel2.axes.text(-1.60, 0, 'W')
        self.panel2.axes.text(0, -1.65, 'S')

        s = np.linspace(-1.5,1.5,21)
        for ang in s:
            l = Line2D([-1.5, 1.5], [ang, ang],color='black')                                    
            self.panel2.axes.add_line(l)
        s = np.linspace(-1.5,1.5,21)
        for ang in s:
            l = Line2D([ang, ang],[-1.5, 1.5],color='black')                                    
            self.panel2.axes.add_line(l)
        self.panel2.axes.add_line(Line2D([-0.05,0.05],[0, 0]))
        self.panel2.axes.add_line(Line2D([0, 0],[-0.05,0.05]))

        #绘制极点图
        def f1(x,y):
            return 1.5*np.sqrt(2)*np.sin(x/180*np.pi/2)*np.sin(y/180*np.pi)
        def f2(x,y):
            return 1.5*np.sqrt(2)*np.sin(x/180*np.pi/2)*np.cos(y/180*np.pi)
        x=[]
        y=[]
        nmb = self.Id
        while nmb>=0:
            nmb=nmb-1
            x.append(f1(self.Dia[nmb],self.Dip[nmb]))
            y.append(f2(self.Dia[nmb],self.Dip[nmb]))
            self.panel2.axes.plot(x[-1],y[-1],'r.')
             
        #显示结果
        self.panel2.canvas = FigureCanvas(self.panel2, -1, self.panel2.figure) 
        self.panel2.Fit()    

    def drawContour(self,event):
        #绘制等密度图
        #初始化画布
        self.panel2.figure = plt.figure(figsize=(7,6))  
        self.panel2.axes = self.panel2.figure.add_subplot(111)
        self.panel2.axes.axis('equal')
        self.panel2.axes.axis('off')
        #设置大圆半径R=1
        #生成投影网外圆
        #an = np.linspace(0,2*np.pi,100)
        #plt.plot( np.cos(an), np.sin(an), color='white')
        self.panel2.axes.text(-0.4, 1.15, u'节理极点等密度图', fontsize=16)
        self.panel2.axes.text(0, 1.05, 'N')
        self.panel2.axes.text(1.05,  0, 'E')
        self.panel2.axes.text(-1.15, 0, 'W')
        self.panel2.axes.text(0, -1.1, 'S')
        
        #生成极点坐标
        def f1(x,y):
            return np.sqrt(2)*np.sin(x/180*np.pi/2)*np.sin(y/180*np.pi)
        def f2(x,y):
            return np.sqrt(2)*np.sin(x/180*np.pi/2)*np.cos(y/180*np.pi)
        x=[]
        y=[]
        nmb = self.Id
        while nmb>=0:
            nmb=nmb-1
            x.append(f1(self.Dia[nmb],self.Dip[nmb]))
            y.append(f2(self.Dia[nmb],self.Dip[nmb]))
            #plt.plot(x[-1],y[-1],'r.')
             
        #统计极点个数
        num=[]
        x0=[]
        y0=[]
        i=-10
        while i<=10:    
            #print('i =',i)
            #num.append([])
            j=-10
            while j<=10:
                #print('j =',j)  
                if np.sqrt((0.1*i)**2+(0.1*j)**2)<=1:
                    x0.append(0.1*i)
                    y0.append(0.1*j)
                    #num[-1].append(0)
                    num.append(0)
                    #print('%.1f' % x[-1],'%.1f' % y[-1])        
                    k=0
                    while k<len(x):
                        bn = np.sqrt((0.1*i-x[k])**2+(0.1*j-y[k])**2)
                        if bn <= 0.1:
                            #num[-1][-1]=num[-1][-1]+1
                            num[-1]=num[-1]+1
                        k=k+1
                j=j+1        
            i=i+1
        #print(num)
        s = np.linspace(0,2*np.pi,37)
        for ang in s:
            #l = Line2D([np.cos(ang), 1.02*np.cos(ang)], [np.sin(ang), 1.02*np.sin(ang)])                                    
            #ax.add_line(l)
            if 0==np.cos(ang) or 0==np.sin(ang):
                continue
            x0.append(np.cos(ang))
            y0.append(np.sin(ang))
            num.append(0)
            while k<len(x):
                bn = np.sqrt((0.1*i-x[k])**2+(0.1*j-y[k])**2)
                if bn <= 0.1:
                    #num[-1][-1]=num[-1][-1]+1
                    num[-1]=num[-1]+1
        tri=Triangulation(x0, y0)
        atri=tri.get_masked_triangles()

        #绘制tin图
        levels = np.arange(0., 110., 5)
        #plt.triplot(tri)
        a = self.panel2.axes.tricontourf(tri, num, levels=levels)
        self.panel2.figure.colorbar(a,shrink=0.7)

        #显示结果
        self.panel2.canvas = FigureCanvas(self.panel2, -1, self.panel2.figure) 
        self.panel2.Fit()  
                
if __name__=="__main__":
    app=wx.App()
    frame=MyFrame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
