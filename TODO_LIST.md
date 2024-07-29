TODO List

* Benchmark 尽量在7月的第一个周出来

  * 准备好task
    * 有dataset：>100 task，包含常见模态和输入。主要为基础任务。
    * 有dataset+无dataset：>200 task。主要为基础任务加部分较难的任务。
  * 设计评测指标
    * 运行成功率：已完成。
    * 端到端评测：人工编写Agent和自动生成Agent的结果相似度比较
      * 核心是一个比较序列相似度的Function。序列长度和内部item都可能不同。
      * 多次重复生成。
    * 代码层面评测：
      * 源码评测：BLEU
      * AST评测：CodeBLEU
      * LLM

* Agent Generator

  * 调prompt
    * chainstream doc的优化
    * 增加动态例子选择的能力（）
    * user prompt模版优化
  * 看情况决定要不要加入循环生成，根据报错调整代码之类的方法
  * baseline
    * 找一找其他Agent框架有没有自动生成Agent的能力
    * 新写一个新的generator
      * Python + ChainStream
      * Python + LangChain
      * Python + OpenAI库 doc （测一下shot的数量）
      * GPT4o 直接感知 （批量给数据）
  * 分析

* Model Selection

  * 写完，跑通
    * 后端的模型实例写完：one-api和ollama的部署
    * 完成相似度比较函数
      * BLEU
      * 。。。
    * 具体的选择策略
      * 并行的
      * 串行的
  * 主要的评测指标
    * 和GPT4o比较benchmark上的正确性
    * token fee
    * 整体的完成时延

  * baseline
    * 只选性能最好的
    * 只选最便宜的

* 写paper 

  * 七月中下开始写故事
  * 八月中完成所有实验和分析