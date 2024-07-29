# ChainStream是什么？

ChainStream是一个致力于更好支持Agent实现长时间感知能力的Agent开发框架，框架采用了事件驱动的多层流式结构，目的是为了实现Agent的长时间感知能力以及信息分享能力。

## 什么是流？什么是事件驱动？
流就是一个数据管道，类似于水管，有入口和出口。Agent可以在任意时刻把任意内容放入流中，这个数据就会随着管道自动流向下游的Agent。

流和Agent的关系通过监听来实现，这很像微信的公众号订阅，或者youtube的频道订阅：

- 微信用户订阅了某个公众号，当该公众号有新文章发布时，微信会自动推送给用户。
- Youtube用户订阅了某个频道，当该频道有新的视频发布时，Youtube会自动推送给用户。
- Agent订阅了某个流，当该流中有新的数据时，ChainStream会自动把数据推送给Agent。

这种提前监听、自动推送的机制，就是事件驱动的核心。事件驱动的主要优点就是在大型计算图中减少非必要计算。

## Agent在ChainStream中是什么样子的？

Agent中的函数可以被订阅到某个流上，也可以往某个流中写入数据。Agent作为具有某种功能的逻辑概念可以包括一个或多个函数。

我们可以把Agent Function看作流的转换函数。比如，对于一个监控摄像头而言，其作为源头可以源源不断的视频流，流中的单位是视频帧。当我们构造了一个Person Detection Agent，它可以订阅到这个视频流、对其进行目标检测并将有人出现的帧推到新的流中。
我们就获得了Person Stream。进一步，我们可以在该流上监听一个Face Recognition Agent来产生人脸检测的Face Stream。以此类推，我们可以构造出一个复杂的Agent流图。

根据上面例子可以看出，ChainStream的核心思想就是通过多个原子化的转换步骤来逐步实现感知任务。并且每个中间步骤流都可以被其他Agent所使用，比如Face Stream可以被用来做情感识别、身份识别、口罩识别等子任务。这使得Agent之间的共享更加方便。

对于ChainStream Runtime而言，其工作就是维护由所有Agent合并得到一个大的Stream Flow Graph中，并通过事件驱动的机制来实现流的自动推送。并且对该Graph进行各种系统优化。

## ChainStream VS Agent开发框架？

目前已经有太多Agent框架了，其中不乏有LangChain、AutoGPT、MetaGPT之类的成熟且大型的框架。ChainStream和他们有什么区别？

其中最明显的区别就是：ChainStream目前还太小了:laughing:，从框架体量上和成熟度上来讲ChainStream都还差很多，我们还有很长的路要走。

当然，核心的区别其实很明显：

- 面向不同的Agent类型：大多数已有Agent框架都是编写Problem-solving Agent的，而ChainStream主要面向Context-aware Agent，这类Agent需要长时间的感知能力。
- 偏向感知的侧重点：ChainStream目前专注于更好的解决长时间感知问题，就我们所知，ChainStream是第一个专门为感知开发独立模块的框架。
- 独特的结构：所有Agent都并入一张大的事件驱动流图中，便于Agent之间的信息共享和系统全局优化。
- 面向边缘场景：大多数Agent框架都面向云端，而ChainStream面向边缘场景，我们尝试打通不同边缘设备间的传感器界限。

总的来说，ChainStream作为一个概念上较新的框架，还处于起步阶段。**在短期上，我们希望它能够聚焦于更好的Agent的长时间感知能力，提供一套小而精的Agent感知解决方案。
在长期上，我们同样抱有ChainStream成为大型Agent开发框架的梦想，发掘其边缘应用开发部署的潜力，希望能够借开源社区之力完善其各方面能力**。

