---
title: "阅读笔记：InvDet 与红外小目标检测"
slug: "reading-invdet"
date: "2026-09-11"
description: "用可逆编码与目标感知重建，理解红外小目标在下采样中的信息保留。"
draft: false
learning_note: true
build:
  list: never
  render: always
categories: ["技术"]
tags: ["论文阅读", "红外图像", "小目标检测", "可逆网络"]
---

## 问题在下采样时就出现了

红外小目标可能只有几个像素，亮度和边缘也不明显。检测网络不断下采样时，目标信息容易被压进背景；等解码器上采样，已经丢失的信号不能凭空恢复。直接加入普通重建分支也有矛盾：重建希望保留整张图的细节，检测却需要忽略无关背景。

## 可逆编码与目标感知重建

InvDet 在浅层使用 HaarDownsample 和可逆块，让中间表示可以沿逆路径重建输入；深层则继续使用普通卷积块提取语义。训练时，从可逆 latent 进入逆重建路径，用重建误差检查信息保留情况。TARM 在这条路径上调制目标相关的低频与高频信息，GCTM 依据目标框几何和红外灰度一致性产生像素权重，让重建更关注目标区域。

{{< paper-figure src="/images/learning-notes/invdet-architecture.png" alt="InvDet 可逆编码器、目标感知重建与检测分支的整体架构" caption="原论文 Figure 2：可逆编码、目标感知重建和检测路径。" >}}

检测与重建使用分开的优化更新，避免重建梯度直接干扰检测。推理时不再运行逆重建路径，只保留检测分支。

## 读完留下的理解

可逆性在这里不是为了输出一张更漂亮的图，而是给小目标信息是否在编码时消失提供约束。真正需要同时理解的还有目标感知权重和梯度解耦：否则辅助重建任务可能把精力花在大面积背景上，甚至影响检测目标。

[查看原论文](https://openaccess.thecvf.com/content/CVPR2026/html/Yan_Target-Aware_Invertible_Encoder_with_Reconstruction_Guidance_for_Infrared_Small_Target_CVPR_2026_paper.html)
