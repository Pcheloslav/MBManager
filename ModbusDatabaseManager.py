import sqlite3
from datetime import datetime


class ModbusDatabaseManager:
    def __init__(self):
        self.db_connection_point = None
        self.cursor = None

    def open_connection(self):
        self.db_connection_point = sqlite3.connect('modbus.db')
        self.cursor = self.db_connection_point.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Modbus(
            Ua REAL, 
            Ub REAL, 
            Uc REAL, 
            Ia REAL, 
            Ib REAL, 
            Ic REAL,
            DateTime TEXT);
        """)
        self.db_connection_point.commit()

    def add_record(self, register_list):
        date = datetime.now()
        input_list = []
        input_list.extend(register_list[6:9])
        input_list.extend(register_list[13:16])
        input_list.append(date)
        tuple(input_list)
        self.cursor.execute("INSERT INTO Modbus VALUES(?, ?, ?, ?, ?, ?, ?);", input_list)
        self.db_connection_point.commit()

    def fetch_last_n_raws(self, n):
        self.cursor.execute("SELECT * FROM Modbus LIMIT ? OFFSET (SELECT count(*) FROM Modbus)-?", (n, n))
        return self.cursor.fetchmany(n)

    def close_connection(self):
        self.db_connection_point.close()


if __name__ == "__ModbusDatabaseManager__":
    mylist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    lol = ModbusDatabaseManager()
    lol.open_connection()
    lol.add_record(mylist)
    my_list = lol.fetch_last_n_raws(1)
    print(my_list)
    lol.close_connection()
