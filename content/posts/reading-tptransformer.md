---
title: "阅读笔记：TPTransformer 与张量注意力"
slug: "reading-tptransformer"
date: "2026-09-22"
description: "将可学习稀疏残差、深度展开和张量乘积注意力放在一条高光谱超分流程中理解。"
draft: false
learning_note: true
build:
  list: never
  render: always
categories: ["技术"]
tags: ["论文阅读", "高光谱", "超分辨率", "深度展开", "Transformer"]
---

## 问题从哪里来

高光谱超分辨率需要同时恢复空间细节和保持波段间关系。已有深度展开方法往往用固定的稀疏惩罚描述插值误差，但不同图像和波段的残差分布并不完全相同。另一方面，把高光谱特征展平成矩阵再做普通注意力，会削弱原本的空间—光谱多维结构。

## 方法如何展开

论文把上采样的低分辨率高光谱图像分解为较干净的低秩部分和稀疏残差，使用可学习的稀疏指数 `p`，再将优化过程展开成多个 stage。每个阶段交替更新低秩项、稀疏残差和重建结果，而不是一次前向就结束。

{{< paper-figure src="/images/learning-notes/tptransformer-architecture.png" alt="TPTransformer 基于自适应 p-RPCA 的深度展开网络架构" caption="原论文 Figure 3：自适应 p-RPCA 展开与重建流程。" >}}

低秩先验网络中的 TPTransformer 不把每个注意力头仅当作二维矩阵，而是保留一个三阶张量及其 tube 轴。沿该轴做 FFT 后，t-product 可以拆成多个频率切片上的矩阵乘法；再通过逆变换回到原表示。网络同时使用空间二维卷积和光谱三维卷积，补充局部结构先验。

## 读完留下的理解

这篇论文可以分两层看：外层是“低秩图像＋可变稀疏残差”的迭代优化，内层才是用张量乘积改造的注意力模块。这样更容易看清 TPTransformer 的位置：它服务于每个展开阶段的低秩更新，并不是贴在重建结果后面的独立增强器。

[查看原论文](https://openaccess.thecvf.com/content/CVPR2026F/html/Xu_TPTransformer_Tensor-Tensor_Product_Transformer_for_Hyperspectral_Image_Super-Resolution_CVPRF_2026_paper.html)
