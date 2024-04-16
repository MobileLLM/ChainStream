from chainstream.interfaces import MemoryInterface
import os
from chainstream.runtime import cs_server_core

DATABASE_PATH_BASE = os.path.join(cs_server_core.output_dir, 'database')
DEFAULT_SQL_PATH = os.path.join(DATABASE_PATH_BASE, cs_server_core.default_sql_name)

# DATABASE_PATH_BASE = '.'
# DEFAULT_SQL_PATH = os.path.join(DATABASE_PATH_BASE, 'test.db')


class BaseMemory(MemoryInterface):
    def __init__(self, *args, **kwargs):
        self.type = None
        self.memory_id = kwargs.get('memory_id', None)
        # self.recorder = MemRecorder()
        pass

