from abc import abstractmethod
from chainstream.interfaces import MemoryInterface

class DataBaseInterface:
    def connect(self):
        pass
    def close(self):
        pass
    def query(self, sql):
        pass
    def update(self, sql):
        pass

class MySQLBaseMemory(MemoryInterface):
    def __init__(self, table_name, columns, type, load_db_path=None, dump_db_path=None):
        self.database = DataBaseInterface()
        self.type = type
        self.table_name = table_name
        self.columns = columns
        self._create_table(load_db_path)
        self._dump_to_db(dump_db_path)
    def _create_table(self, load_db_path):
        if load_db_path:
            self._load_from_db(load_db_path)
        else:
            pass
        pass

    def _load_from_db(self, db_path):
        pass

    def _dump_to_db(self):
        pass
    def _check_data(self, column_data):
        pass
    def add_item(self, column_data):
        self._check_data(column_data)
        self._add_data(column_data)
        pass
    @abstractmethod
    def _add_data(self, data):
        raise ("Must implement add_data method")

    def remove_item(self, *args, **kwargs):
        self._del_data(args, kwargs)
        pass
    @abstractmethod
    def _del_data(self, *args, **kwargs):
        raise ("Must implement del_data method")

    def find_item(self, *args, **kwargs):
        self._find_data(args, kwargs)
        pass
    @abstractmethod
    def _find_data(self, *args, **kwargs):
        raise ("Must implement find_data method")

class KV_Memory(MySQLBaseMemory):
    def _add_data(self, data):
        pass
    def _del_data(self, *args, **kwargs):
        pass
    def _find_data(self, *args, **kwargs):
        pass

class SequentialMemory(MySQLBaseMemory):
    def _add_data(self, data):
        pass
    def _del_data(self, *args, **kwargs):
        pass
    def _find_data(self, *args, **kwargs):
        pass