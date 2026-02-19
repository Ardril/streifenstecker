import sqlite3 as s3




class DatabaseConnection:

    def __init__(self,name="data.db"):
        self.connection = s3.connect(name)
        cursor = self.connection.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master").fetchone()
        if not tables or "data_entry" not in tables:
            cursor.execute("CREATE TABLE data_entry (timestamp ,type, measurements_box_1, measurements_box_2)")

    def __del__(self):
        self.connection.close()

    def insert_record(self, record):
        # record_schema = {
        #   "timestamp":    datetime_tuple,
        #   "box1":         List_of_measurements,
        #   "box2":         List_of_measurements,
        # }
        cursor = self.connection.cursor()
        m1 = record["box1"]
        m2 = record["box2"]
        ts = record["timestamp"]
        ty = record["type"]
        cursor.execute("INSERT INTO data_entry VALUES (?, ?, ?, ?)", (ts, ty, m1, m2))
        self.connection.commit()
