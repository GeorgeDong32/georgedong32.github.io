---
title: Dev Drive
categories: [Windows,Developer Tools]
tags: [Windows]
---

# Dev Drive

## 简介

Dev Drive(开发者驱动器)，是微软基于ReFS文件系统的新型存储卷，目标是提升关键开发者工作负载性能。

其特点包含：

* 文件系统优化
* 安全性控制
* 指定信任、防病毒配置优化(Windows Defender)
* 附加筛选器

微软给出的性能提升如下图：

![Visual Studio Dev Drive](https://devblogs.microsoft.com/visualstudio/wp-content/uploads/sites/4/2023/05/DevDrivePerfChart.png)

## 使用前准备

Dev Drive需要的最低空间为50GB(50*1024MB)，位置可以是硬盘的未分配区域，或是创建一个虚拟磁盘。为了避免无用消耗，我直接创建真实的分区。

首先是压缩出一个未分配空间，然后在设置：存储：磁盘和卷：Create a Dev Drive创建Dev Drive。

## 使用

然后就是迁移nuget包、配置环境变量，之后开始使用。

## 体验

还原Nuget上确实如微软所说，提升较大，不知是什么原理。

但在编译上，哪怕在VS专门优化的情况下，提升也感知不强，python、jupyter也是如此。

不过ReFS的复制性能确实好于NTFS，盘内复制项目速度不错，目测有10%左右的速度提升，应该是针对碎片文件有特殊优化。

但是内存表现上确实比较离谱，存储、复制占用的内存比NTFS大上一些，在我的16G内存机子上表现为5%~11%左右的占用增长。