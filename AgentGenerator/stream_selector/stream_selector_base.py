from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.utils import TextGPTModel


STREAM_SELECT_PROMPT = """
请扮演一个程序员来执行一个编程任务的早期
"""


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


if __name__ == '__main__':
    from ChainStreamSandBox.tasks import get_task_with_data_batch
    task_list = get_task_with_data_batch()
    input_stream_set = set()
    all_stream_list_repeated = []
    for task_name, task_class in task_list.items():
        tmp_input_streams = task_class().input_stream_description
        for input_stream in tmp_input_streams.streams:
            input_stream_set.add(str(input_stream))
            all_stream_list_repeated.append(str(input_stream))

    all_stream_list = list(input_stream_set)
    print(all_stream_list)

    stream_name_set = set()
    input_stream_dict = {}
    for s in all_stream_list:
        tmp_name = s.split()[0].split("=")[-1]

        print(tmp_name)
        stream_name_set.add(tmp_name)
    for s in all_stream_list_repeated:
        tmp_name = s.split()[0].split("=")[-1]
        if tmp_name not in input_stream_dict:
            input_stream_dict[tmp_name] = []
        input_stream_dict[tmp_name].append(s)

    print(stream_name_set)
    print(f"total stream names: {len(stream_name_set)}")
    print(f"total streams: {len(input_stream_set)}")
    for s, v in input_stream_dict.items():
        print(f"stream name: {s} : {v}")
    print(f"tot task streams: {len(all_stream_list_repeated)}")
    a = 1