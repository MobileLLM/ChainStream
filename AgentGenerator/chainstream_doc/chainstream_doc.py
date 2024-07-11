chinese_chainstream_doc = '''
接下来我将向你介绍ChainStream，这是一个由python代码编写的处理流式数据的开发框架。你需要掌握这一框架的使用方法，按照用户提供给你的任务要求处理一系列数据流，这些数据流由软件或硬件产生。由硬件产生的数据流可以是摄像头产生的图片流，麦克风产生的音频流，GPS产生的位置信息流；由软件产生的数据流可以是由app产生的数据流，电脑的截屏图像流等。你需要选择合适的数据流并设计这些数据流的处理方式来完成用户制定的任务，在这一过程中你也可以创建新的数据流。下面我将介绍这一框架的各个模块以及使用方法：

Stream模块:
Description:
    Stream 类是数据流的核心，每一个数据流都是Stream的实例，Chainstream使用strean_id用来区分不同的数据流。ChainStream通过在数据流上挂载监听函数的方式完成对数据流的中数据的监听与处理，一个数据流上可能挂载多个监听函数，当数据流中有数据进入时，Chainstream会自动调用挂载的监听函数对该数据进行相应处理。下面将介绍有关Stream类的方法
API:
    - chainstream.get_stream(stream_id)：这一方法能够根据stream_id获取一个Stream对象,通常情况下构建Agent实例时需要通过此方法获得输入和输出流
    - chainstream.stream.Stream.for_each(agent, listener_func)：这一方法能够向Stream实例挂载监听函数。listener_func是要挂载的监听函数，agent是挂载这一函数的Agent的标识符
    - chainstream.stream.Stream.unregister_all(agent):这一方法用于注销数据流上挂载的监听函数，指定标识符agent，由这一Agent挂载的所有监听函数都会被注销
    - chainstream.stream.Stream.add_item(data):这一方法用于向数据流推送数据，其中data可以是任意形式的数据，包括图像，音频，文本等
    
Agent模块:
Description:
    你需要创建一个或多个Agent来完成用户指定的任务，你创建的Agent实例需要继承chainstream.agent.Agent类，并向父类传入agent_id作为标识符号，并实现__init__,start(),stop()方法以完成对相关数据流的监听，处理和结果输出。
API:
    - __init__(agent_id):这一方法通过实例化一个新的Agent对象来创建完成任务的Agent，agent_id是必要的参数，用于指定agent的标识符，你也需要将这一参数传入父类中。你也需要在这个方法进行获取或创建数据流，创建数据容器等初始化资源的操作，为任务的执行进行数据准备。
    - start():在这一方法中，你需要定义处理数据流的监听函数，并将这些监听函数绑定到相应的数据流上
    - stop():在这一方法中，你需要注销这个Agent挂载到数据流上的所有监听函数。

BufferContext模块:
Description:
    如果在执行任务的过程中需要对处理后的数据进行存储，你可以使用BufferContext模块创建数据容器。这个数据容器是一个队列，你只能在队尾添加数据，队首取出存储的数据。下面将介绍这一模块的使用方法：
API:
    - chainstream.context.BufferContext():这一方法通过实例化一个新的BufferContext对象来创建数据容器
    - chainstream.context.BufferContext.add(data):通过这一方法向数据容器的队尾添加数据，你可以存储任何形式的数据，包括图像，文本，音频等。
    - chainstream.context.BufferContext.get():通过这一方法取出数据容器队首的数据，原来队首的下一个存储的数据会成为新的队首数据。

LLM模块:
Description:
    LLM模块集成了多种模型，这些模型能够根据输入的处理要求，处理多种类型的输入数据，包括文本、图像和声音。你可以在处理要求中描述你的需求，模型会根据你的要求以及你提供的数据进行相应的回复。请注意，Chainstream并不能保证这些模型的回复一定可靠，你需要尽可能详细地描述你的处理需求。
API:
    - chainstream.llm.get_model(type):这一方法通过实例化一个llm对象，来获得处理数据的模型。type是(['text']),(['image']),(['audio'])中的一种，描述获得的模型需要处理的数据类型。
    - chainstream.llm.make_prompt(query ,data):这是llm对象内的方法，这一方法将处理要求和输入数据转换成模型能够接受的输入，其中query是处理要求，描述了你希望如何处理输入数据，或者你希望从输入数据中获取什么信息，例如："描述这张图片的具体内容"，"这段音频里有几个人说话"。 data是输入数据，需要和模型能够处理的数据类型一致。该方法返回模型能够接受的输入prompt
    - chainstream.llm.query(prompt)：这是llm对象内的方法，向模型发送输入prompt，返回模型的回复。
'''

chinese_one_example = '''
接下来，我将给你一个具体的例子，来展示你应该如何使用ChainStream来完成一个Agent。假设用户想要筛选新消息队列中的英文消息，你可以提供一个这样的Agent：

import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_arxiv_agent")
        self.input_stream = cs.get_stream("all_arxiv")
        self.output_stream = cs.get_stream("cs_arxiv")
        self.llm = get_model(["text"])
        
    def start(self):
        def process_paper(paper):
            paper_content = paper["abstract"]#[:500]        
            prompt = "Is this abstract related to edge LLM agent? Say 'yes' or 'no'."
            prompt = [
                {
                    "role": "user",
                    "content": prompt+paper_content
                }
            ]
            response = self.llm.query(prompt)
            print(response)
            if response == 'Yes':
                print(paper)
                self.output_stream.add_item(paper)
        self.input_stream.for_each(self, process_paper)

    def stop(self):
        self.input_stream.unregister_all(self)
设计之前你必须要导入chainstream模块，你可以仿照上述代码创建不止一个Agent，让它们互相配合来完成用户任务。除非用户提供了函数工具，你只能使用ChainStream中的LLM模块来解决用户的需求。你提供的Agent必须是完整的，可运行的，你需要完成Agent中的每一个函数，用户不会再对你提供的Agent进行修改。你不能使用各个模块没有提供的函数。
如果你已经掌握了ChainStream框架，并可以使用该框架编写Agent处理用户任务，并准备处理用户的需求。请仅生成一个包含三个单引号（注意不是反引号）的代码块，但不要在代码中包含“python”关键字，不要实例化及生成多余的注释。


'''