from ChainStreamSandBox.tasks import ALL_TASKS
from ChainStreamSandBox.sandbox.chainstream_sandbox import ChainStreamSandBox
from ChainStreamSandBox.sandbox.stream_interface_sandbox import StreamInterfaceSandBox
from AgentGenerator.prompt.feedback_processor import FilterErrorFeedbackProcessor


def test_task(task_id, agent=None):
    task = ALL_TASKS[task_id]()
    sandbox = StreamInterfaceSandBox(task, task.agent_example if agent is None else agent, save_path=None)

    report = sandbox.start_test_agent(return_report_path=False)

    haha = FilterErrorFeedbackProcessor()
    print("feedback:", haha(report))
    print(report["output_stream_items"])
    print(report['stdout'])


if __name__ == '__main__':
    agent = " \nimport threading\nfrom chainstream.stream import Stream\nimport datetime\nimport openai\nimport os\nfrom chainstream.stream import get_stream_interface\n\nopenai_api_key = os.environ['OPENAI_API_KEY']\nopenai_base_url = os.environ.get(\"OPENAI_BASE_URL\")\n\n# Initialize OpenAI API\nopenai.api_key = openai_api_key\nif openai_base_url:\n    openai.api_base = openai_base_url\n\ndef get_email_purpose(content):\n    # Use OpenAI API to classify the purpose of the email\n    response = openai.Completion.create(\n        engine=\"text-davinci-003\",\n        prompt=f\"Classify the purpose of the following email content into one of the following categories: ['Request for Information', 'Meeting Scheduling', 'Project Update', 'Task Assignment', 'Feedback Request', 'Report Submission', 'Inquiry', 'Clarification', 'Approval Request', 'Status Update', 'Other'].\\n\\nEmail Content:\\n{content}\\n\\nPurpose:\",\n        max_tokens=10,\n        n=1,\n        stop=\"\\n\"\n    )\n    purpose = response.choices[0].text.strip()\n    return purpose\n\ndef process_data(is_stop: threading.Event) -> None:\n    source_stream = get_stream_interface('all_email')\n    target_stream = get_stream_interface('purpose_of_work_email')\n\n    batch = []\n    while not is_stop.is_set():\n        item = source_stream.get(timeout=5)\n        if item:\n            content = item['Content']\n            date_str = item['Date']\n            date = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')\n            \n            # Filter emails from June to December\n            if date.month >= 6 and date.month <= 12:\n                purpose = get_email_purpose(content)\n                # Filter for work-related purposes\n                if purpose in ['Request for Information', 'Meeting Scheduling', 'Project Update', \n                               'Task Assignment', 'Feedback Request', 'Report Submission', \n                               'Inquiry', 'Clarification', 'Approval Request', 'Status Update']:\n                    batch.append({'Content': content, 'purpose': purpose})\n                    \n                    # Process in batches of 2\n                    if len(batch) == 2:\n                        # Insert processing logic for batch, e.g., summarization\n                        summarized_purposes = \" \".join([email['purpose'] for email in batch])\n                        for email in batch:\n                            email['summarized_purposes'] = summarized_purposes\n                            target_stream.put(email)\n                        batch = []\n\n        if is_stop.is_set():\n            break\n "
    for i, line in enumerate(agent.split('\n')):
        print(f"{i+1}. {line}")

    test_task("EmailTask2", agent=agent)
