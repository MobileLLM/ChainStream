from .log_actions import LogAction


def log_to_console(agent, message):
    LogAction(agent, message).execute()


def notify_user(agent, message, feedback_type=None):
    pass
