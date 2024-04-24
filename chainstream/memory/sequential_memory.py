from base_memory import BaseMemory, DEFAULT_SQL_PATH
from database_interface import DataBaseInterface


class SequentialMemory(BaseMemory):
    def __init__(self, memory_id, columns_and_setting, database_path=None):
        super().__init__(memory_id=memory_id)
        self.type = 'sql'
        self.database_path = database_path if database_path else DEFAULT_SQL_PATH
        self.database = DataBaseInterface('sqlite', self.database_path)
        self.table_name = memory_id
        self.columns_and_setting = columns_and_setting
        self._create_table()

    def _create_table(self):
        try:
            # Check if the table already exists in SQLite
            query = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{self.table_name}';"
            result = self.database.query(query)[0][0]
            if result > 0:
                raise Exception("Table name conflict")

            # Create table in SQLite
            query = f"CREATE TABLE {self.table_name} ({self.columns_and_setting});"
            self.database.update(query)
        except Exception as e:
            print(f"Failed to create table: {str(e)}")

    def add_item(self, data):
        # 传入的是一个list，list每个item是一个字典对应于一条数据
        # 默认第一个是key，如果数据库中有这个就更改数据，如果没有就添加数据
        for item in data:
            first_key, first_value = list(item.items())[0]
            qe = f"SELECT COUNT(*) FROM {self.table_name} WHERE {first_key} = '{first_value}';"
            result = self.database.query(qe)[0][0]
            if result > 0:  # 存在数据就进行更新
                update_data = ""
                for index, key in enumerate(item):
                    if index == 0:
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
            else:  # 不存在就插入
                keys = ""
                values = ""
                for key, value in item.items():
                    keys += (key + ", ")
                    if isinstance(item[key], (int, float)):
                        values += str(value)
                    else:
                        values += ("'" + value + "'")
                    values += ", "
                keys = keys[:-2]
                values = values[:-2]
                qe = f"INSERT INTO {self.table_name} ({keys}) VALUES ({values});"

                self.database.update(qe)

    def remove_item(self, columns=None, condition=None):
        # 一次删除只能删列或者删除满足条件的
        if columns:
            qe = f"ALTER TABLE {self.table_name} DROP COLUMN {columns};"
            self.database.update(qe)
        elif condition:
            qe = f"DELETE FROM {self.table_name} WHERE {condition};"
            self.database.update(qe)

    def __getitem__(self, item):
        return self.find_item(columns=item)

    def find_item(self, columns=None, condition=None):
        if columns and condition:
            qe = f"SELECT {columns} FROM {self.table_name} WHERE {condition};"
            result = self.database.query(qe)
        elif columns:
            qe = f"SELECT {columns} FROM {self.table_name};"
            result = self.database.query(qe)
        elif condition:
            qe = f"SELECT * FROM {self.table_name} WHERE {condition};"
            result = self.database.query(qe)
        return result


def test_seq():
    test_mem = SequentialMemory('testTable', 'name VARCHAR(20), img VARCHAR(100), test_num INT')
    data = [{'name': 'test1', 'img': 'this is a img', 'test_num': 100},
            {'name': 'test2', 'img': 'this is a img', 'test_num': 101}]
    test_mem.add_item(data)
    result = test_mem.find_item(columns='name, test_num')
    print(result)
    result = test_mem.find_item(columns='name, test_num', condition='test_num=101')
    print(result)
    test_mem.remove_item(condition='test_num=101')
    result = test_mem.find_item(columns='name, test_num')
    print(result)
