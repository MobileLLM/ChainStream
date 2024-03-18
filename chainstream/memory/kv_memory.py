from chainstream.interfaces import MemoryInterface
import cv2
import json
from database_memory import DataBaseInterface



class KV_Memory(MemoryInterface):
    def __init__(self, memory_id) -> None:
        super().__init__()
        self.memory_id = memory_id  # known_people
        self.items = {}

    # add or change
    def add_item(self, data_item):
        self.items[data_item[0]] = data_item[1]

    def delete_item(self, data_key):
        if data_key in self.items.keys():
            del self.items[data_key]
        else:
            print('there is no ' + str(data_key))
            raise RuntimeError("Item not found")

    def find_item(self, data_key):
        if data_key in self.items.keys():
            return self.items[data_key]
        else:
            print('there is no ' + str(data_key))
            return None

    def get_keys(self):
        return self.items.keys()

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

        keys = ""
        values = ""
        for key, value in self.items.items():
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


def main():
    image = cv2.imread('image.jpeg')
    temp = KV_Memory('known_people')
    temp.add_item('face', image)
    temp.add_item('name', 'image')
    print(temp.get_keys())
    image_1 = temp.find_item('face')
    temp.delete_item('name')
    print(temp.get_keys())
    temp.find_item('name')
    print(temp.get_keys())


if __name__ == "__main__":
    main()
