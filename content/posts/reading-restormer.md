---
title: "阅读笔记：Restormer 与高分辨率图像复原"
slug: "reading-restormer"
date: "2026-09-16"
description: "理解 Restormer 如何用通道注意力与门控卷积处理高分辨率图像。"
draft: false
learning_note: true
build:
  list: never
  render: always
categories: ["技术"]
tags: ["论文阅读", "图像复原", "Transformer", "注意力机制"]
---

## 高分辨率图像为什么难做注意力

图像复原既要照顾局部纹理，也要利用远处的上下文。标准空间自注意力需要构造与像素数相关的 `HW × HW` 矩阵，分辨率越高，代价越大；只限制在局部窗口内，又可能失去更广的上下文。

## Restormer 的两个关键模块

Restormer 使用四层 U-Net 式编码器—解码器，核心块由 MDTA 和 GDFN 组成。MDTA 先通过点卷积与深度卷积把局部信息写入 `Q/K/V`，再把注意力关系转到通道轴，计算较小的 `C × C` 相关矩阵。它不是忽略空间，而是先在空间上提取局部结构，再以通道关系聚合全局上下文。

{{< paper-figure src="/images/learning-notes/restormer-architecture.png" alt="Restormer 编码器解码器架构，以及 MDTA 和 GDFN 模块" caption="原论文 Figure 2：整体网络与 MDTA、GDFN 结构。" >}}

GDFN 则替代普通逐像素前馈网络：两条含深度卷积的分支分别产生特征与门控，逐元素相乘后再投影回原通道。网络还使用尺度变化、跳跃连接和顶层细化模块，让深层上下文与浅层细节重新汇合。

## 读完留下的理解

Restormer 的效率来自注意力计算位置的改变，而不只是“用了一个更小的 Transformer”。读结构图时，可以先沿编码器和解码器看信息如何降采样、再恢复，再进入每个块看 MDTA 负责的通道交互和 GDFN 负责的内容门控。

[查看原论文](https://openaccess.thecvf.com/content/CVPR2022/html/Zamir_Restormer_Efficient_Transformer_for_High-Resolution_Image_Restoration_CVPR_2022_paper.html)
