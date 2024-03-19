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
        self.database = DataBaseInterface('postgresql', 'postgres', 'localhost', 5432, {'user': 'postgres', 'password': 'postgres'})
        #KV_Memory or SequentialMemory
        self.type = type
        self.table_name = table_name
        #The name and properties of each column in the data table
        # e.g. {id: VARCHAR(20)}
        self.columns = columns
        self._create_table(load_db_path)
        self._dump_to_db(dump_db_path)
    def _create_table(self, load_db_path):
        if load_db_path:
            self._load_from_db(load_db_path)
        else:
            qe = f"select count(*) from information_schema.tables where table_name = '{self.table_name}';"
            result = self.database.query(qe)[0][0]
            print(result)
            if result > 0:
                raise Exception("Table name conflict")
            tableSetting = ""
            for name, pro in self.columns.items():
                tableSetting += name
                tableSetting += " "
                tableSetting += pro
                tableSetting += ", "
            tableSetting = tableSetting[:-2]
            qe = f"CREATE TABLE {self.table_name} ({tableSetting});"
            self.database.update(qe)

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
    def __init__(self, key_col, table_name, columns, type, load_db_path=None, dump_db_path=None):
        super().__init__(table_name, columns, type, load_db_path=None, dump_db_path=None)
        # 能找到数据的关键值,是一个list,如{id, '1'}或{name, 'helloworld'} 统一用字符串形式
        self.key_col = key_col
    #规定data
    def _add_data(self, data, datatype=None):
        # 定义传进来的数据是字典的形式
        for key, value in data.items():
            qe = f"SELECT COUNT(*) FROM {self.table_name} WHERE '{key}' = '{key}';"
            result = self.database.query(qe)[0][0]
            if result>0:
                if(key==self.key_col[0]):
                    self.key_col[1] = value
            else:
                qe = f"ALTER TABLE {self.table_name} ADD {key} {datatype[key]};"
                self.database.update(qe)
            if isinstance(value, (int, float)):
                qe = f"UPDATE {self.table_name} SET {key} = {value} WHERE {self.key_col[0]} = '{self.key_col[1]}';"
                self.database.update(qe)
            else:
                qe = f"UPDATE {self.table_name} SET {key} = '{value}' WHERE {self.key_col[0]} = '{self.key_col[1]}';"
                self.database.update(qe)

    def _del_data(self, *args, **kwargs):
        for key in args:
            qe = f"SELECT COUNT(*) FROM {self.table_name} WHERE '{key}' = '{key}';"
            result = self.database.query(qe)[0][0]
            if result>0:
                qe = f"ALTER TABLE {self.table_name} DROP COLUMN {key};"
                self.database.update(qe)
    def _find_data(self, *args, **kwargs):
        data = {}
        for key in args:
            qe = f"SELECT COUNT(*) FROM {self.table_name} WHERE '{key}' = '{key}';"
            result = self.database.query(qe)[0][0]
            if result>0:
                qe = f"SELECT {key} FROM {self.table_name};"
                result = self.database.query(qe)
                print(result)
                data[key] = result
        return data


class SequentialMemory(MySQLBaseMemory):
    def _add_data(self, data):
        #传入的是一个list，list每个item是一个字典对应于一条数据
        #默认第一个是key，如果数据库中有这个就更改数据，如果没有就添加数据
        for item in data:
            first_key, first_value = item.items()[0]
            qe = f"SELECT COUNT(*) FROM users WHERE {first_key} = '{first_value}';"
            result = self.database.query(qe)[0][0]
            if result>0: #存在数据就进行更新
                update_data = ""
                for index, key in enumerate(item):
                    if index==0:
                        continue
                    update_data += key
                    update_data += " = "
                    if isinstance(item[key], (int, float)):
                        update_data += str(item[key])
                    else:
                        update_data += ("'" + str(item[key]) + "'")
                    update_data += ", "
                update_data = update_data[:-2]
                qe = f"UPDATE {self.table_name} SET {update_data} WHERE {first_key} = '{first_value}';"
                self.database.update(qe)
            else: #不存在就插入
                keys = ""
                values = ""
                for key, value in item.items():
                    keys += (key+", ")
                    if isinstance(item[key], (int, float)):
                        values += str(values)
                    else:
                        values += ("'"+value+ "'")
                    values += ", "
                keys = keys[:-2]
                values = values[:-2]
                qe = f"INSERT INTO {self.table_name} ({keys}) VALUES ({values});"
                self.database.update(qe)

    def _del_data(self, *args, **kwargs):
        # and 同时满足所有条件删除，or就是满足任意一个就会删除，columns删除列
        is_and = False
        is_or = False
        is_col = False
        if args[0]=='and':
            is_and = True
        elif args[0]=='or':
            is_or = True
        elif args[0]=='columns':
            is_col = True
        if is_and: #删除同时满足所有条件的数据
            condition = ""
            for i in range(len(args)):
                if i==0:
                    continue
                condition += args[i]
                condition += " AND "
            condition = condition[:-5]
            qe = f"DELETE FROM {self.table_name} WHERE {condition};"
            self.database.update(qe)
        elif is_or: #删除满足其中一个条件的数据
            for i in range(len(args)):
                if i==0:
                    continue
                qe = f"DELETE FROM {self.table_name} WHERE {args[i]};"
                self.database.update(qe)
        elif is_col: #删除某些列
            for i in range(len(args)):
                if i==0:
                    continue
                qe = f"ALTER TABLE {self.table_name} DROP COLUMN {args[i]};"
                self.database.update(qe)

    def _find_data(self, *args, **kwargs):
        # and 找到同时满足所有条件，否则满足一个条件
        is_and = False
        is_or = False
        is_col = False
        if args[0]=='and':
            is_and = True
        elif args[0]=='or':
            is_or = True
        elif args[0]=='columns':
            is_col = True
        if is_and:
            condition = ""
            for i in range(len(args)):
                if i==0:
                    continue
                condition += args[i]
                condition += " AND "
            condition = condition[:-5]
            qe = f"SELECT * FROM {self.table_name} WHERE {condition};"
            result = self.database.query(qe)
        if is_or:
            condition = ""
            for i in range(len(args)):
                if i==0:
                    continue
                condition += args[i]
                condition += " OR "
            condition = condition[:-4]
            qe = f"SELECT * FROM {self.table_name} WHERE {condition};"
            result = self.database.query(qe)