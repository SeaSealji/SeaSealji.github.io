---
title: "阅读笔记：EMR-Diff 与高光谱超分辨率"
slug: "reading-emr-diff"
date: "2026-09-22"
description: "用多模态残差和边缘感知噪声，理解 EMR-Diff 的短程扩散过程。"
draft: false
learning_note: true
build:
  list: never
  render: always
categories: ["技术"]
tags: ["论文阅读", "高光谱", "超分辨率", "扩散模型"]
---

## 为什么不从纯噪声开始

高光谱超分辨率要把低分辨率高光谱图像（LR-HSI）的光谱信息，与高分辨率多光谱图像（HR-MSI）的空间结构合在一起。普通扩散模型从纯噪声逐步生成图像，反向链较长；所有位置使用相同的噪声，也难把学习重点放在缺失的边缘细节上。

## EMR-Diff 的流程

方法先将 LR-HSI 上采样，再与 HR-MSI 拼接，得到一个已经包含两种观测信息的起点。目标 HR-HSI 与这个起点之间的差异被视为多模态残差。扩散过程围绕这段残差进行，而不是从完全无关的高斯噪声重新生成整幅图像。

{{< paper-figure src="/images/learning-notes/emr-diff-architecture.png" alt="EMR-Diff 整体架构，展示多模态残差、边缘感知噪声与反向去噪流程" caption="原论文 Figure 2：EMR-Diff 的整体流程。" >}}

HR-MSI 经过 Sobel 算子提取边缘，再用边缘强度调制噪声：结构变化明显的位置获得更强的训练扰动。反向网络 BAF-UNet 分成两路，一路处理当前扩散状态，另一路持续提供上采样 LR-HSI 与 HR-MSI 的条件信息；多尺度特征在去噪过程中交互。训练阶段需要真值 HR-HSI 构造目标与监督，推理阶段则只使用观测图像及其条件。

{{< paper-figure src="/images/learning-notes/emr-diff-baf-unet.png" alt="EMR-Diff 的 BAF-UNet 双分支多尺度去噪网络结构" caption="原论文 Figure 4：BAF-UNet 的双分支结构。" >}}

## 读完留下的理解

这篇方法把“生成一张图”变成“沿观测与目标之间的残差修正一张图”。边缘感知噪声则把有限的去噪能力更多放到高频结构上。理解模型时，要分清训练时才有的真值路径，与推理时真正可用的 LR-HSI、HR-MSI 和边缘条件。

[查看原论文](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_EMR-Diff_Edge-aware_Multimodal_Residual_Diffusion_Model_for_Hyperspectral_Image_Super-resolution_CVPR_2026_paper.html)
