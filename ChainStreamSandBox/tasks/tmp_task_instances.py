ALL_TASK_INSTANCES = None


def get_all_task_instances():
    global ALL_TASK_INSTANCES
    return ALL_TASK_INSTANCES


def set_all_task_instances(task_instances):
    global ALL_TASK_INSTANCES
    ALL_TASK_INSTANCES = task_instances
