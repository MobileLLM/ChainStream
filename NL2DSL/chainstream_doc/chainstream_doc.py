chinese_api_prompt = '''
向你介绍ChainStream，一个python编写的流式LLM Agent开发框架，其主要目的是编写LLM为主的处理流式的传感器数据并完成感知任务的Agent。传感器包括硬件传感器和软件传感器，硬件传感器包括摄像头、麦克风、定位传感器，而软件传感器则范围更广，比如app、网络API、截屏等都算软件传感器的范围。感知任务则主要是借助LLM的能力更好的理解物理世界的过程，不同于传统方法使用定制模型解决定制任务，ChainStream更注重借助LLM的通用能力去更好的理解物理世界，当然如果需要的话也可以使用各种小模型作为工具来帮助感知。下面介绍一下ChainStream的用法：

chainstream.agent.Agent:
Description:
    - 所编写的Agent必须继承该Agent类，并实现init、start、stop方法
    - 
* 在__init__()中申请所需的所有资源，并向父类init方法中传入新Agent的全局标识agent_id
* 在start中给流绑定监听函数，可以自定义监听函数
* 在stop中释放资源

chainstream.stream
* get_stream：名字
* create_stream：名字
* stream.register_listener方法
* stream.unregister_listener方法

buffer

* buffer（）
* buffer.add（）
* buffer.read（）

llm

* get_model
* make_prompt
* query

memory

* get_memory
* create_memory
* memory.add
* memory.

'''