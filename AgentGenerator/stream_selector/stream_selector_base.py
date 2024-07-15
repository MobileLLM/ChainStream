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
            input_stream_prompt = f"The agent should use  the following input stream: {specific_stream}"
        else:
            if select_policy is None or select_policy == 'none':
                input_stream_prompt = ""
            else:
                if select_policy == 'all':
                    all_stream = self.all_stream_list
                elif select_policy == 'llm':
                    all_stream = self._select_stream_by_llm()

                all_stream = self._process_input_stream(all_stream)
                input_stream_prompt = f"There are multiple input streams available. The agent should select some of them: {all_stream}"

        prompt = f"{output_prompt}\n{input_stream_prompt}"
        return prompt

    def process_output_stream_list(self, output_stream_list: StreamListDescription):
        output_stream = self._process_output_stream(output_stream_list)
        prompt = f"""
        Your mission is to programme an agent with chainstream framework to get the following output streams:
        {output_stream}
        """
        return prompt

    def _select_stream_by_llm(self) -> StreamListDescription:
        pass

    def _process_output_stream(self, output_stream_list: StreamListDescription) -> str:
        pass

    def _process_input_stream(self, input_stream_list: StreamListDescription) -> str:
        pass
