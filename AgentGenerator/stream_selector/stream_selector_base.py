from ..io_model import StreamListDescription
from ..utils import TextGPTModel


class StreamSelectorBase:
    def __init__(self, all_stream_list: StreamListDescription = None):
        self.all_stream_list = all_stream_list

        self.llm = TextGPTModel()

    def select_stream(self, output_stream_list: StreamListDescription, specific_stream=None, select_policy='none'):
        assert select_policy in ['all', 'llm', 'none', None]

        output_prompt = self._process_output_stream(output_stream_list)

        if specific_stream is not None:
            input_stream_prompt = f"The agent should use the following input stream: {specific_stream}"
        else:
            if select_policy is None or select_policy == 'none':
                input_stream_prompt = ""
            else:
                all_stream = None
                if select_policy == 'all':
                    all_stream = self.all_stream_list
                elif select_policy == 'llm':
                    all_stream = self._select_stream_by_llm()

                all_stream = self._process_input_stream(all_stream)
                input_stream_prompt = f"\nThere are multiple input streams available. The agent should select some of them:\n{all_stream}"

        prompt = f"{output_prompt}\n{input_stream_prompt}"

        prompt = prompt + "\n All the input streams and output streams listed above are already defined in the chainstream framework, you can directly use them through `chainstream.stream.get_stream(agent, stream_id)`. Besides, you can also define your own stream if needed by using the `chainstream.stream.create_stream(agent, stream_id)` API. Note that you don't need to create the output stream list beforehand."

        return prompt

    def set_all_stream_list(self, all_stream_list: StreamListDescription):
        self.all_stream_list = all_stream_list

    def _process_output_stream(self, output_stream_list: StreamListDescription):
        # output_stream = self._process_output_stream(output_stream_list)
        tmp_prompt = ""
        for stream in output_stream_list:
            tmp_prompt += f"{str(stream)}\n"
        output_stream = tmp_prompt[:-1]

        prompt = f"""Your mission is to programme an agent with chainstream framework to get the following output streams:\n{output_stream}"""
        return prompt

    def _select_stream_by_llm(self) -> StreamListDescription:
        pass

    def _process_input_stream(self, input_stream_list: StreamListDescription) -> str:
        tmp_prompt = ""
        for stream in input_stream_list:
            tmp_prompt += f"{str(stream)}\n"
        input_stream = tmp_prompt[:-1]
        return input_stream
