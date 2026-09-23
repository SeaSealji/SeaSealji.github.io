---
title: "阅读笔记：LWTformer 与可学习小波"
slug: "reading-lwtformer"
date: "2026-09-16"
description: "从低频字形和高频笔画出发，理解 LWTformer 的小波下采样与注意力设计。"
draft: false
learning_note: true
build:
  list: never
  render: always
categories: ["技术"]
tags: ["论文阅读", "图像复原", "小波", "Transformer"]
---

## 为什么要把频率拆开

古代汉字图像的磨损、断裂和背景纹理常与细笔画混在一起。普通下采样可能直接丢掉纤细边缘；只在空间域增强细节，又难区分真实笔画与噪声。论文的出发点是：字形主体与方向性笔画分别对应不同的频率成分，恢复时不应一概处理。

## 网络如何保留笔画

LWTformer 使用 U-Net 式编码器—解码器，把可学习二维小波变换嵌入降采样过程。低频近似子带保留整体字形，水平、垂直和对角高频子带提供不同方向的笔画线索。WaveDown 在缩小特征图时保存并调制这些信息，而不是只依赖普通卷积下采样。

{{< paper-figure src="/images/learning-notes/lwtformer-architecture.png" alt="LWTformer 整体网络，以及 SEA 与 WaveDown 模块" caption="原论文 Figure 3：整体架构、SEA 与 WaveDown。" >}}

空间增强注意力 SEA 负责整体结构，带小波门控的 WACGA 则利用不同子带增强局部细节。两类模块与前馈网络交替工作；训练目标同时考虑像素、频域和感知层面的差异。

{{< paper-figure src="/images/learning-notes/lwtformer-wacga.png" alt="LWTformer 中 WACGA 小波门控注意力模块的内部结构" caption="原论文 Figure 4：WACGA 如何使用不同频带。" >}}

## 读完留下的理解

这篇方法的关键不是简单地把小波当作预处理，而是让分频直接参与特征传播：**低频守住字形，高频按方向守住笔画，再由模型选择值得增强的部分**。看架构时，可以先找 WaveDown 如何连接编码层，再看 WACGA 怎样把频带信息送回注意力分支。

[查看原论文](https://openaccess.thecvf.com/content/CVPR2026F/html/Ruan_LWTformer_A_Detail-Aware_Learnable_Wavelet-Transformer_for_Ancient_Chinese_Character_Image_CVPRF_2026_paper.html)
