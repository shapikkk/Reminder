import pyodbc

class Database:
    conn = None
    cursor = None

    def __init__(self):
        server = "localhost"
        database = "Reminder"

        connection_string = f"DRIVER={{ODBC Driver 11 for SQL Server}}; SERVER={server}; DATABASE={database}; Trusted_Connection=yes"
        if Database.conn is None:
            Database.conn = pyodbc.connect(connection_string)
            Database.cursor = Database.conn.cursor()

    def get_all_tasks(self):
        Database.cursor.execute("SELECT * FROM reminderPy WHERE status between 0 and 1")
        select_data = Database.cursor.fetchall()
        return select_data

    def save_task(self, data):
        Database.cursor.execute("INSERT INTO reminderPy (description, date, status) VALUES (?, ?, ?)", data)
        self.conn.commit()

    def update_task(self, data):
        Database.cursor.execute("UPDATE reminderPy SET description = ?, date = ? WHERE id = ?", data)
        self.conn.commit()

    def delete_task(self, data):
        Database.cursor.execute("DELETE FROM reminderPy WHERE id = ?", data)
        self.conn.commit()