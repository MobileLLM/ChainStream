from sandbox_interface import SandboxBatchInterface
from AgentGenerator.generator.stream_mode.chainstream_feedback_guided_generator_for_real_task import \
    ChainstreamFeedbackGuidedGeneratorForRealTask
from ChainStreamSandBox.tasks import get_task_batch


class EvalFeedbackGuidedGeneratorForRealTask(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=2, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="chainstream")

    def get_agent_for_specific_task(self, task, verbose=True, only_print_last=False):
        generator = ChainstreamFeedbackGuidedGeneratorForRealTask(max_loop=10, only_print_last=only_print_last)
        generator.set_verbose(verbose)
        # TODO: fix this para with a new output description
        agent, latency, tokens, loop_count, history = generator.generate_agent(task.output_stream_description, task.input_stream_description,
                                                          task=task)
        return agent, latency, tokens, loop_count, history


if __name__ == '__main__':
    task_list = get_task_batch()
    evaluator = EvalFeedbackGuidedGeneratorForRealTask(task_list, task_log_path="/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-23_05-04-12_chainstream_with_real_task_stdout_err_msg/test_log.json")
    evaluator.start()
