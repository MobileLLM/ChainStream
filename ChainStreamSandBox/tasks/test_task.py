from ChainStreamSandBox.tasks import ALL_TASKS
from ChainStreamSandBox.sandbox.chainstream_sandbox import ChainStreamSandBox


def test_task(task_id):
    task = ALL_TASKS[task_id]()
    sandbox = ChainStreamSandBox(task, task.agent_example, save_path=None)

    report = sandbox.start_test_agent(return_report_path=False)

    print(report["output_stream_items"])


if __name__ == '__main__':
    test_task("WeatherTask3")
