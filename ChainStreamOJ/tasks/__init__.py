# from task_example/*/config.py import all tasks and put them in a list
# import task_config_base

ALL_TASKS = {}

# import all tasks
from tasks.sms_task.sms_task import WorkSmsTaskConfig
from tasks.arxiv_task.arxiv_task import ArxivTaskConfig
from tasks.email_task.email_task import EmailTaskConfig
from tasks.news_task.news_task import NewsTaskConfig
from tasks.stock_task.stock_task import StockTaskConfig
from tasks.daily_dialogue_task.daily_dialogue_task import DialogueTaskConfig
ALL_TASKS['WorkSmsTask'] = WorkSmsTaskConfig
ALL_TASKS['ArxivTask'] = ArxivTaskConfig
ALL_TASKS['EmailTask'] = EmailTaskConfig
ALL_TASKS['NewsTask'] = NewsTaskConfig
ALL_TASKS['StockTask'] = StockTaskConfig
ALL_TASKS['DialogueTask'] = DialogueTaskConfig