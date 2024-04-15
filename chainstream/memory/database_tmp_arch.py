from chainstream.interfaces import MemoryInterface
from database_memory import DataBaseInterface
import json


class KVMemory(MemoryInterface):
    def __init__(self, json_path):
        self.json_path = json_path
        self.create_json()

    def create_json(self):
        data = {}
        with open(self.json_path, 'w') as json_file:
            json.dump(data, json_file)

    # 规定data
    def add_item(self, data):
        # 定义传进来的数据是字典的形式
        with open(self.json_path, 'r') as file:
            file_data = json.load(file)
        for key, value in data.items():
            file_data[key] = value
        with open(self.json_path, 'w') as file:
            json.dump(file_data, file, indent=4)

    def remove_item(self, keys):
        with open(self.json_path, 'r') as file:
            file_data = json.load(file)
        for key in keys:
            if key in file_data:
                del file_data[key]
        with open(self.json_path, 'w') as file:
            json.dump(file_data, file, indent=4)

    def find_item(self, keys):
        data = {}
        with open(self.json_path, 'r') as file:
            file_data = json.load(file)
        for key in keys:
            if key in file_data:
                data[key] = file_data[key]

        return data


class SequentialMemory(MemoryInterface):
    def __init__(self, table_name, columns_and_setting):
        self.database = DataBaseInterface('sqlite', 'sqlite')
        self.table_name = table_name
        self.columns_and_setting = columns_and_setting
        self._create_table()

    def _create_table(self):
        qe = f"select count(*) from information_schema.tables where table_name = '{self.table_name}';"
        result = self.database.query(qe)[0][0]
        print(result)
        if result > 0:
            raise Exception("Table name conflict")
        qe = f"CREATE TABLE {self.table_name} ({self.columns_and_setting});"
        self.database.update(qe)

    def add_item(self, data):
        # 传入的是一个list，list每个item是一个字典对应于一条数据
        # 默认第一个是key，如果数据库中有这个就更改数据，如果没有就添加数据
        for item in data:
            first_key, first_value = list(item.items())[0]
            print(first_key)
            print(first_value)
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
                print(qe)
                self.database.update(qe)

    def remove_item(self, columns=None, condition=None):
        # 一次删除只能删列或者删除满足条件的
        if columns:
            qe = f"ALTER TABLE {self.table_name} DROP COLUMN {columns};"
            self.database.update(qe)
        elif condition:
            qe = f"DELETE FROM {self.table_name} WHERE {condition};"
            self.database.update(qe)

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
        print(qe)
        return result


def test_seq():
    test_mem = SequentialMemory('images', 'name VARCHAR(20), img VARCHAR(100), test_num INT')
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


def test_kv():
    kv = KVMemory('./test.json')
    kv.add_item({'name': 'test1', 'img': 'this is a img', 'test_num': 100})
    re = kv.find_item(['name', 'img', 'test_num'])
    print(re)
    kv.remove_item(['img'])
    re = kv.find_item(['img'])
    print(re)


if __name__ == '__main__':
    test_seq()
    # test_kv()
