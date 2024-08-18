from ..io_model import StreamListDescription
from ..utils import TextGPTModel


def _process_stream(stream_list: StreamListDescription):
    tmp_prompt = ""
    for stream in stream_list:
        tmp_prompt += f"{str(stream)}\n"
    str_stream = tmp_prompt[:-1]

    return str_stream


class StreamSelectorBase:
    def __init__(self, all_stream_list: StreamListDescription = None):
        self.all_stream_list = all_stream_list

        self.llm = TextGPTModel()

    def select_stream(self, output_stream_list: StreamListDescription, specific_stream=None, select_policy='none'):
        assert select_policy in ['all', 'llm', 'none', None]

        output_stream = _process_stream(output_stream_list)

        if specific_stream is not None:
            return _process_stream(specific_stream)
        else:
            if select_policy is None or select_policy == 'none':
                return ""
            else:
                input_stream = None
                if select_policy == 'all':
                    input_stream = self.all_stream_list
                elif select_policy == 'llm':
                    input_stream = self._select_stream_by_llm(output_stream)

                input_stream = _process_stream(input_stream)

        return output_stream, input_stream

    def set_all_stream_list(self, all_stream_list: StreamListDescription):
        self.all_stream_list = all_stream_list

    def _select_stream_by_llm(self, output_stream) -> StreamListDescription:
        pass
