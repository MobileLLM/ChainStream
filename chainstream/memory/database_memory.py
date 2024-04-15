import pymysql
import psycopg2
import sqlite3


class DataBaseInterface:
    def __init__(self, type, database, host=None, port=None, user_config: dict = None):
        self.type = type
        self.database = database
        self.host = host
        self.port = port
        self.user_config = user_config

        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            if self.type == 'mysql':
                self.connection = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user_config['user'],
                    password=self.user_config['password'],
                )
                self.cursor = self.connection.cursor()
            elif self.type == 'postgresql':
                self.connection = psycopg2.connect(
                    database=self.database,
                    host=self.host,
                    port=self.port,
                    user=self.user_config['user'],
                    password=self.user_config['password']
                )
                self.cursor = self.connection.cursor()
            elif self.type == 'sqlite':
                self.connection = sqlite3.connect(self.database)
                self.cursor = self.connection.cursor()
            else:
                raise ValueError("Unsupported database type: {}".format(self.type))
        except Exception as e:
            print("Failed to connect to the database: {}".format(str(e)))

    def query(self, sql):
        try:
            if not self.cursor:
                raise Exception("Database connection is not established.")
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Failed to execute query: {}".format(str(e)))

    def update(self, sql):
        try:
            if not self.cursor:
                raise Exception("Database connection is not established.")
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print("Failed to execute update: {}".format(str(e)))

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            print("Failed to close the database connection: {}".format(str(e)))
