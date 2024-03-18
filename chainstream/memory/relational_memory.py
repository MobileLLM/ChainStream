from chainstream.interfaces import MemoryInterface
from database_memory import DataBaseInterface
import json

class RelationalMemory(MemoryInterface):
    def __init__(self, memory_id):
        super().__init__()
        self.memory_id = memory_id
        self.items = []

    def add_item(self, data_item):
        self.items.append(data_item)

    def delete_item(self, data_item):
        if data_item in self.items:
            self.items.remove(data_item)
        else:
            raise ValueError("Item not found in memory")

    def select_keys(self, keys, type='and', none_value=None):
        result = []
        for item in self.items:
            if type == 'and':
                if all(key in item for key in keys):
                    result.append({key: item[key] for key in keys})
            elif type == 'or':
                if any(key in item for key in keys):
                    tmp = {key: item[key] for key in item if key in keys}
                    tmp.update({k: none_value for k in keys if k not in tmp})
                    result.append(tmp)
        return result
    
    def mem2json(self, filepath):
        with open(filepath, 'w') as file:
            json.dump(self.items, file)
    def json2mem(self, filepath):
        with open(filepath, 'r') as file:
            json_data = json.load(file)
            print(json_data)
            return json_data

    def preAction(self, tableName, tableSetting, dbInterface):
        #如果有之前的表则直接删除
        if 'tableName' in self.dbInformation.keys():
            print("hhh")
            print(self.dbInformation['tableName'])
            qe = f"DROP TABLE {self.dbInformation['tableName']};"
            dbInterface.update(qe)

        if 'tableName' in self.dbInformation.keys() and tableSetting==None:
            tableName = self.dbInformation['tableName']
        elif tableName == None:
            raise Exception("Unable to find tableName")
        self.dbInformation['tableName'] = tableName

        if 'tableSetting' in self.dbInformation.keys() and tableSetting==None:
            tableSetting = self.dbInformation['tableSetting']
        elif tableSetting == None:
            raise Exception("Unable to find tableSetting")

        self.dbInformation['tableSetting'] = tableSetting
        
        return tableName, tableSetting


    def mem2database(self, tableName, tableSetting):
        dbInterface = DataBaseInterface('postgresql', 'postgres', 'localhost', 5432, {'user': 'postgres', 'password': 'postgres'})

        tableName, tableSetting = self.preAction(tableName, tableSetting, dbInterface)

        #首先要查看数据库中是否有这个表
        qe = f"select count(*) from information_schema.tables where table_name = '{tableName}';"
        print(qe)
        result = dbInterface.query(qe)[0][0]
        print(result)
        if result > 0:
            raise Exception("Table name conflict")
        qe = f"CREATE TABLE {tableName} ({tableSetting});"
        dbInterface.update(qe)

        for i in range(len(self.items)):
            print(self.items[i])
            keys = ""
            values = ""
            for key, value in self.items[i].items():
                keys += (key+", ")
                values += ("'"+value+ "', ")
            keys = keys[:-2]
            values = values[:-2]
            qe = f"INSERT INTO {tableName} ({keys}) VALUES ({values});"
            dbInterface.update(qe)
        dbInterface.close()
    
    def database2mem(self, keys=None):
        dbInterface = DataBaseInterface('postgresql', 'postgres', 'localhost', 5432, {'user': 'postgres', 'password': 'postgres'})

        results = []
        cur = dbInterface.cursor
        if keys == None:
            cur.execute(f"SELECT * FROM {self.dbInformation['tableName']};")
        else:
            temp = ""
            for i in range(len(keys)):
                print(keys[i])
                temp += (keys[i]+", ")
                print(temp)
            temp = temp[:-2]
            cur.execute(f"SELECT {temp} FROM {self.dbInformation['tableName']};")

        columns = [col[0] for col in cur.description]
        rows = cur.fetchall()
        for row in rows:
            result = dict(zip(columns, row))
            results.append(result)
        self.items = results
        dbInterface.close()


if __name__ == '__main__':
    rm = RelationalMemory('id')
    rm.add_item({'id': 1, 'name': 'Alice', 'age': 25})
    rm.add_item({'idd': 2, 'name': 'Bob', 'age': 30})
    rm.add_item({'id': 3, 'namee': 'Charlie', 'age': 35})
    rm.add_item({'idd': 4, 'namee': 'Dave', 'age': 40})
    print(rm.select_keys(['id', 'name'], type='or'))
    print(rm.select_keys(['id', 'name'], type='and'))

