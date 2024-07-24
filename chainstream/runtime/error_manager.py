import logging
import datetime
import traceback
import enum
import sys

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


# ERROR_TYPES = ["function_error", "stream_error", "agent_error", "llm_error", "runtime_error", "other_error"]

class ErrorType(enum.Enum):
    FUNCTION_ERROR = "function_error"
    STREAM_ERROR = "stream_error"
    AGENT_ERROR = "agent_error"
    LLM_ERROR = "llm_error"
    RUNTIME_ERROR = "runtime_error"
    OTHER_ERROR = "other_error"


class ErrorManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_count = 0
        self.error_history = {
            "function_error": [],
            "stream_error": [],
            "agent_error": [],
            "llm_error": [],
            "runtime_error": [],
            "other_error": [],
        }

    def record_error(self, error_type, error_message, traceback_obj=None):
        if traceback_obj is None:
            traceback_obj = traceback.format_exc()
        self.error_count += 1
        error_message = f"{error_type}: {error_message}"
        self.logger.error(error_message)
        self.logger.error(traceback_obj)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        error_dict = {
            "time": current_time,
            "error_type": error_type,
            "error_message": error_message,
            "traceback": traceback_obj,
        }

        self.error_history[error_type].append(error_dict)

    def get_error_history(self):
        return self.error_history

    def __len__(self):
        return self.error_count

    def reset_error_history(self):
        self.error_count = 0
        self.error_history = {
            "function_error": [],
            "stream_error": [],
            "agent_error": [],
            "llm_error": [],
            "runtime_error": [],
            "other_error": [],
        }
