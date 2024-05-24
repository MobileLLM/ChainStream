# from task_example/*/config.py import all tasks and put them in a list
# import task_config_base

ALL_TASKS = {}

# import all tasks
from tasks.sms_task.sms_task import WorkSmsTaskConfig
from tasks.arxiv_task.arxiv_task import CSArxivTaskConfig

ALL_TASKS['WorkSmsTask'] = WorkSmsTaskConfig
ALL_TASKS['ArxivTask'] = CSArxivTaskConfig