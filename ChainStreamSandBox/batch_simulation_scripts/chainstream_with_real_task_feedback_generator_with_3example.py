from sandbox_interface import SandboxBatchInterface
from AgentGenerator.generator.stream_mode.chainstream_feedback_guided_generator_for_real_task_with_example import \
    ChainstreamFeedbackGuidedGeneratorForRealTaskWithExample
from ChainStreamSandBox.tasks import get_task_with_data_batch


class EvalFeedbackGuidedGeneratorForRealTaskWithExample(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=1, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="chainstream")

    def get_agent_for_specific_task(self, task, verbose=True, only_print_last=True):
        generator = ChainstreamFeedbackGuidedGeneratorForRealTaskWithExample(task_name_now=task.__class__.__name__, max_loop=10, only_print_last=only_print_last, framework_example_number=0, feedback_example_number=3)
        generator.set_verbose(verbose)
        # TODO: fix this para with a new output description
        agent, latency, tokens, loop_count, history, selected_example = generator.generate_agent(task.output_stream_description, task.input_stream_description,
                                                          task=task)
        return agent, latency, tokens, loop_count, history, selected_example


if __name__ == '__main__':
    task_list = get_task_with_data_batch()
    evaluator = EvalFeedbackGuidedGeneratorForRealTaskWithExample(task_list, task_log_path="/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-02_02-52-19_chainstream_feedback_0shot_3example_after_debug/test_log.json")
    evaluator.start()
