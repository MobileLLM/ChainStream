from chainstream.interfaces import AgentInterface
import logging
from .agent_recorder import AgentRecorder
import inspect
import datetime


class AgentMeta:
    """
    AgentMeta is a class that stores metadata of an agent.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.agent_id = kwargs.get("agent_id")
        self.agent_file_path = kwargs.get("agent_file_path") if kwargs.get("agent_file_path") else ""
        self.description = kwargs.get("description") if kwargs.get("description") else ""
        self.type = kwargs.get("type") if kwargs.get("type") else "base"
        self.created_at = datetime.datetime.now()
        self.status = kwargs.get("status") if kwargs.get("status") else "running"

        # TODO: 增加权限、优先级、分组等属性
        # self.permissions = []
        # self.priority = 0
        # self.group = ""

    def __dict__(self):
        return {
            "agent_id": self.agent_id,
            "agent_file_path": self.agent_file_path,
            "description": self.description,
            "type": self.type,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status
        }


def record_start(func):
    """
    A decorator that records the start of an agent.
    """
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)

        from chainstream.sandbox_recorder import SANDBOX_RECORDER
        if SANDBOX_RECORDER is not None:
            agent_id = self.agent_id
            inspect_stack = inspect.stack()
            start_res = res
            SANDBOX_RECORDER.record_start(agent_id, start_res, inspect_stack)

        return res

    return wrapper


class Agent(AgentInterface):
    """
    Agent is the base class for all agents. Your Agent instances should inherit from the `chainstream.agent.Agent`
    class, providing an `agent_id` identifier and implementing the `__init__`, `start()`, and `stop()` methods to
    manage data stream listening, processing, and output.

    Specifically,
        1. `__init__` should call `super().__init__(agent_id)` with a valid agent_id and obtain required resources.
        2. `start` to define listener func and register them to target streams.
        3. `stop` to unregister listener func and release resources.
    """
    agent_store_base_path = None

    def __init__(self, agent_id: str = None) -> None:
        """
        This method instantiates a new Agent object. The `agent_id` parameter
        specifies the agent's identifier, which should also be passed to the parent class's `__init__(agent_id)`
        method. Initialization tasks, such as obtaining or creating data streams and getting LLM models,
        should be performed here.

        """
        super().__init__()

        if agent_id is None:
            raise ValueError("agent_id must be specified, please make sure you call `super().__init__(agent_id)` with a valid agent_id")
        if not isinstance(agent_id, str):
            raise ValueError(f"agent_id must be a string, but got {type(agent_id)}")

        self.agent_id = agent_id
        caller_frame = inspect.currentframe().f_back

        self.metaData = AgentMeta(agent_id=agent_id, agent_file_path=caller_frame.f_globals['__file__'])
        self.logger = logging.getLogger(self.agent_id)
        self.recorder = AgentRecorder(agentMetaData=self.metaData)

        from chainstream.runtime import cs_server_core
        cs_server_core.register_agent(agent=self)

        from chainstream.sandbox_recorder import SANDBOX_RECORDER
        if SANDBOX_RECORDER is not None:
            agent_id = self.agent_id
            inspect_stack = inspect.stack()
            SANDBOX_RECORDER.record_instantiate(agent_id, inspect_stack)

    @record_start
    def start(self) -> None:
        """
        Define and bind data stream listener functions in this method.
        """
        pass

    def stop(self) -> None:
        """
        Unregister all listener functions attached to the data streams by this Agent in this method.
        """
        pass

    def get_meta_data(self):
        return self.metaData.__dict__()

    @staticmethod
    def set_agent_store_base_path(path):
        Agent.agent_store_base_path = path
