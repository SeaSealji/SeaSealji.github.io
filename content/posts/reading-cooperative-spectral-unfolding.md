---
title: "阅读笔记：光谱重建与语义分割的协同展开"
slug: "reading-cooperative-spectral-unfolding"
date: "2026-09-11"
description: "理解 CRSDUN 如何让高光谱重建与语义分割在每个展开阶段互相提供信息。"
draft: false
learning_note: true
build:
  list: never
  render: always
categories: ["技术"]
tags: ["论文阅读", "高光谱", "深度展开", "语义分割"]
---

## 为什么不先重建、再分割

CASSI 把三维高光谱图像压缩成二维测量，重建本来就是一个欠定问题。如果先独立重建，再把结果交给分割器，重建伪影会传到下游；分割任务也无法反过来告诉重建器，哪些结构最影响语义判断。

## 两个任务怎样协同

CRSDUN 把光谱重建和语义分割写进同一个可展开的优化过程。它使用一个可学习的光谱字典，把像素光谱与类别系数联系起来；每个阶段都交替更新两类变量。重建步骤结合 CASSI 测量一致性、上一阶段的光谱估计和当前语义图；分割步骤则读取新的重建结果，用 LISTA 式软阈值更新类别表示。

{{< paper-figure src="/images/learning-notes/crsdun-architecture.png" alt="CRSDUN 光谱重建与语义分割协同展开的整体架构" caption="原论文 Figure 3：重建与分割交替更新的整体流程。" >}}

两个近端网络使用 CAT 处理特征。在其中，CASTA 用语义特征初始化对象级 super-token，再聚合高光谱像素信息并反馈到像素域。这样交换发生在多个展开阶段，而不是最终输出前做一次拼接。训练时各阶段同时受到重建与分割目标的监督，推理时只需要测量和成像系统信息。

{{< paper-figure src="/images/learning-notes/crsdun-casta.png" alt="CRSDUN 的 CAT 与 CASTA 模块，展示光谱和语义特征交互" caption="原论文 Figure 4：CAT 与 CASTA 跨任务交互模块。" >}}

## 读完留下的理解

这篇方法的主线是双向约束：语义结构帮助恢复光谱，恢复出的像素细节又帮助更新语义。读架构图时，先沿“重建更新 → 分割更新 → 下一阶段”的循环看数据流，再看 CASTA 如何完成跨任务交互，比只盯着两个 U-Net 分支更容易抓住方法核心。

[查看原论文](https://openaccess.thecvf.com/content/CVPR2026/html/He_Joint_Spectral_Image_Reconstruction_and_Semantic_Segmentation_with_Cooperative_Unfolding_CVPR_2026_paper.html)
