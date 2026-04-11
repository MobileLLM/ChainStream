import chainstream as cs
import time

class TextProcessingAgent(cs.agent.Agent):
    """文本处理Agent"""
    is_agent = True

    def __init__(self, agent_id="text_processing_agent"):
        super().__init__(agent_id)

        # 获取输入数据流
        self.input_stream = cs.get_stream(self, "source")

        # 创建输出数据流
        self.output_stream = cs.create_stream(self, "generated_output")

        # 初始化LLM模型
        self.llm = cs.llm.get_model(["text"])

    def start(self):
        """启动数据流处理"""
        def process_text(item):
            """处理输入文本"""
            prompt = cs.llm.make_prompt({
                "task": "请对以下文本内容进行总结：",
                "text": item["text"]
            })
            result = self.llm.query(prompt)
            return {"result": result}

        # 将处理函数绑定到输入流，并将结果发送到输出流
        self.input_stream.for_each(process_text, to_stream=self.output_stream)

    def stop(self):
        """停止数据流处理"""
        self.input_stream.unregister_all(self)

if __name__ == '__main__':
    print("测试文本处理Agent")

    agent = TextProcessingAgent()
    agent.start()

    # 模拟数据输入
    agent.input_stream.add_item({"text": "会议室环境模拟数据包含四种模式：normal、learning、dynamic以及emergency。每种模式有不同的传感器数据生成逻辑。"})

    time.sleep(5)
    agent.stop()