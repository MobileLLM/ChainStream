# 快速入门

## 1.什么是 NL-Sense Benchmark？

ChainStream框架旨在支撑更强大Agent的开发和运行，其核心为流式架构，该架构下的Agent代码较难进行Debug和评估，所以我们设计了专门用于Agent测试和评估的Sandbox。

ChainStream的一大主要功能就是根据自然语言生成Agent代码，我们设计了Agent Generator来实现从NL到Code的转换，并在当前主要关注其在感知任务上的效果。但当前缺少从NL直接到感知任务的数据集，所以我们设计了NL-Sense Benchmark作为该领域的评测数据集。

NL-Sense Benchmark是一个开源的NL-to-Sense任务数据集，由多个Task和一套评测 metric 组成。评测的原理是在Sandbox中构造一个拟合真实感知场景的环境，并观测待评测的agent在其中的行为，并分析其输出得到仿真结果，每个Task都代表某一种环境。

具体的，一个task主要包含：
- 任务描述：任务的自然语言描述
- 仿真环境：包括数据、数据在sandbox中的输入顺序、时机等，以及要监听的输出
- 标准程序：人工编写并检查过的 Agent 代码，用于评测仿真结果

由于感知任务的复杂性，难以直接人为标注每个任务输出的标准答案，所以NL-Sense Benchmark的评测方法是比较待测试Agent的输出与标准Agent输出的相似度。

## 2.NL-Sense Benchmark 的构成

NL-Sense Benchmark 共包含Task、Metric和 Sandbox 三个部分。

### 2.1.Sandbox

实际上，ChainStream中支持三类Sandbox，对应了ChainStream Runtime中支持的三种Agent的API类型：

![sandbox_type.png](..%2Fimg%2Fsandbox_type.png)

具体的：

- ChainStream监听函数式：是ChainStream框架Agent的主要API，核心是继承 `chainstream.Agent` 类，编写流转换函数，并通过 `stream.for_each` 等方法完成函数和流的拓扑连接。构造完成后的Agent被分散到各处，其并发运行由ChainStream Runtime统一维护。
- Batch式：为其他框架Agent设计的批次转换式API。Sandbox自动收集所有输入流数据，统一转换为批次数据后传入Agent，Agent返回结果后再统一分发至各个输出流。无法并发，仅作为Sandbox测试API使用，不推荐使用。
- StreamInterface式：为其他框架使用ChainStream流数据设计的API。通过 `stream.get` 和 `stream.put` 等方法与流式 API 交互，实现ChainStream快速融入其他框架。其中 `stream.get` 和 `stream.put` 支持事件驱动，可以实现异步数据传输。

### 2.2.Task

截止到2024年10月，NL-Sense Benchmark共包含覆盖常见感知领域的100+个Task，其中数据来自于10+不同领域各种模态的数据集。在未来，我们希望能够不断扩充Task数量。

### 2.3.Metric

目前，NL-Sense Benchmark的评测方法是比较Agent的运行成功率以及待测试Agent的输出与标准Agent输出的相似度。其中结果相似度主要依靠动态规划寻找结果序列的最优匹配。

此外，我们还实现了一个代码相似度的评估方法，用于衡量Agent生成的代码与标准答案的相似度。由于代码的多样性，该指标仅供残稿而不作为正式评测标准。

## 3.使用 NL-Sense Benchmark 评测
### 3.1.准备

1. Clone ChainStream项目后，Benchmark主要位于 `ChainStreamSandBox` 目录下。
2. Benchmark所使用的原始数据位于 `ChainStreamSandBox/raw_data` 目录下，部分数据以压缩包形式提供。需要手动解压。

### 3.2.开始仿真

#### 3.2.1.单任务

#### 3.2.2.多任务

### 3.3.结果评估

#### 3.3.1.Execute Rate

#### 3.3.2.Result Score

## 4.评估其他 Agent

## 5.定制化

