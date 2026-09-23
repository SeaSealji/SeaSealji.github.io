---
title: "阅读笔记：未配准高光谱图像超分辨率"
slug: "reading-unregistered-hsi-super-resolution"
date: "2026-09-23"
description: "从端元与丰度出发，理解未配准 RGB 参考图像如何辅助高光谱超分辨率。"
draft: false
learning_note: true
build:
  list: never
  render: always
categories: ["技术"]
tags: ["论文阅读", "高光谱", "超分辨率", "图像配准"]
---

## 为什么要研究未配准融合

融合式高光谱超分辨率通常用低空间分辨率高光谱图像（LR-HSI）提供光谱信息，再用高空间分辨率 RGB 图像提供细节。但两张图可能来自不同传感器，存在平移、形变或视差。先精确配准容易引入伪影，直接拼接又把配准、细节迁移和光谱重建三件事同时交给网络。

## 核心思路

这篇论文把高光谱图像拆成两部分：描述材料光谱的端元，以及描述各材料空间分布的丰度。未配准主要影响空间对应关系，因此方法先从上采样的 LR-HSI 中用 SVD 得到端元和初始丰度，让 RGB 参考图像主要帮助细化丰度图，而不是直接生成全部光谱波段。

{{< paper-figure src="/images/learning-notes/uaf-architecture.png" alt="未配准高光谱超分辨率模型的整体架构及 CFDA、SCACA、SCMF 模块" caption="原论文 Figure 3：整体架构与三个关键模块。" >}}

丰度网络是多尺度编码器—解码器。CFDA 在特征层粗到细地聚合未配准的 RGB 信息；SCACA 让参考结构参与丰度的空间、通道注意力；SCMF 在解码时动态融合不同尺度的特征。最后用固定端元混合预测的丰度残差，并加回上采样 LR-HSI，得到高分辨率高光谱图像。

## 读完留下的理解

最值得记住的不是某一个注意力模块，而是问题的改写：**光谱基底尽量由 LR-HSI 保证，RGB 负责提供更细的空间分布线索**。这样把未配准参考图像的作用限定得更清楚，也减少了让网络直接学习完整光谱的负担。这里处理的是特征层的对齐与融合，并不等于先获得了完美的像素级配准。

[查看原论文](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Enhancing_Unregistered_Hyperspectral_Image_Super-Resolution_via_Unmixing-based_Abundance_Fusion_Learning_CVPR_2026_paper.html)
