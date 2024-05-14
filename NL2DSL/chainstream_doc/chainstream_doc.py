chinese_api_prompt = '''
向你介绍ChainStream，一个python编写的流式LLM Agent开发框架，其主要目的是编写LLM为主的处理流式的传感器数据并完成感知任务的Agent。传感器包括硬件传感器和软件传感器，硬件传感器包括摄像头、麦克风、定位传感器，而软件传感器则范围更广，比如app、网络API、截屏等都算软件传感器的范围。感知任务则主要是借助LLM的能力更好的理解物理世界的过程，不同于传统方法使用定制模型解决定制任务，ChainStream更注重借助LLM的通用能力去更好的理解物理世界，当然如果需要的话也可以使用各种小模型作为工具来帮助感知。下面介绍一下ChainStream的用法：

Agent模块:
Description:
    这是每个agent所必须继承的基类，其主要功能是实现流式数据的监听、数据处理、数据输出等功能。
API:
    - 所编写的Agent必须继承该chainstream.agent.Agent类，并实现__init__、start、stop方法
    - 在__init__()中申请所需的所有资源，并向父类__init__(agent_id)方法中传入新Agent的全局标识agent_id
    - 在start中给流绑定监听函数，可以自定义监听函数
    - 在stop中释放资源

Stream模块:
Description:
    Stream相当于数据管道，其上监听着多个函数，当有数据到来时，会自动调用监听函数进行处理。
API:
    - chainstream.get_stream(stream_id), 根据stream_id获取一个Stream对象
    - chainstream.create_stream(stream_id), 创建一个新的Stream对象，并返回该对象
    - chainstream.stream.Stream.register_listener(agent, listener_func), 向Stream对象注册监听函数
    - chainstream.stream.Stream.unregister_listener(agent), 向Stream对象注销监听函数

    
Buffer模块:
Description:
    Buffer是你可以使用的一个数据容器，你可以向其中添加数据，也可以从其中读取数据。
API:
    - chainstream.context.BufferContext(), 创建一个新的Buffer对象，并返回该对象
    - chainstream.context.BufferContext.add(data), 向Buffer中添加数据
    - chainstream.context.BufferContext.get(), 从Buffer中读取数据


LLM模块:
Description:
    LLM模块封装了各种大模型，你只需要关心所需要LLM的模态是什么，就可以直接调用相应的API来完成任务。make_prompt()方法可以将多模态的输入数据转换为统一的输入格式，query()方法可以向模型发送提示并获取模型的回答。
API:
    - chainstream.llm.get_model(type), 创建一个新的LLM对象，并返回该对象, type是['text', 'image', 'audio']的子集
    - chainstream.llm.make_prompt(str | image | audio | BufferContext | Memory), 创建一个新的LLM提示对象，并返回该对象
    - chainstream.llm.query(prompt), 向LLM模型发送提示，并返回模型的回答

Memory模块:
Description:
    Memory模块封装了各种数据存储方式，你可以向其中添加数据，也可以从其中读取数据。
API:
    - chainstream.memory.get_memory(memory_id), 根据memory_id获取一个Memory对象
    - chainstream.memory.create_memory(memory_id), 创建一个新的Memory对象，并返回该对象
    - chainstream.memory.Memory.add(data), 向Memory中添加数据
    - chainstream.memory.Memory.get(), 从Memory中读取数据

接下来，我将给你一个具体的例子，来展示如何使用ChainStream来完成一个Agent。假设你想要完成

```python
import 

```


'''