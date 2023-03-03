import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_tables(self):
        sql = """
        CREATE TABLE Users (
            id INTEGER UNIQUE,
            ism TEXT,
            tel TEXT
            );
        """
        self.execute(sql, commit=True)
        
        sql = """
        CREATE TABLE Kurslar (
	    "id"	INTEGER,
	    "nom"	TEXT UNIQUE,
	    "tarif"	TEXT,
	    PRIMARY KEY("id")
        );
        """
        
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):#
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id, ism, tel): #
        sql = """
        INSERT INTO Users(id, ism, tel) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, ism, tel), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users WHERE id > 100
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, id):
        sql = "SELECT * FROM Users WHERE id = ?"

        return self.execute(sql, parameters=(id,), fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_name(self, name, id):
        sql = f"""
        UPDATE Users SET ism = ? WHERE id = ?
        """
        return self.execute(sql, parameters=(name, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)
        
    def update_user_number(self, raqam, id):
        sql = f"""
        UPDATE Users SET tel = ? WHERE id = ?
        """
        return self.execute(sql, parameters=(raqam, id), commit=True)
        
        
        
    def select_all_kurs(self):
        return self.execute(sql="SELECT * FROM Kurslar WHERE TRUE", fetchall=True)
    
    def select_kurs(self, id):
        return self.execute(sql="SELECT * FROM Kurslar WHERE id = ?", parameters=(id,), fetchone=True)
    
    def add_kurs(self, nom, tarif):
        sql = "INSERT INTO Kurslar(nom, tarif) VALUES (?, ?)"
        self.execute(sql, parameters=(nom, tarif), commit=True)
        
    def delete_kurs(self, id):
        self.execute(sql="DELETE FROM Kurslar WHERE id = ?", parameters=(id,), commit=True)
        
    def update_tarif(self, id, tarif):
        self.execute(sql="UPDATE Kurslar SET tarif = ? WHERE id = ?", parameters=(tarif, id), commit=True)

# def logger(statement):
#     print(f"""
# _____________________________________________________        
# Executing: 
# {statement}
# _____________________________________________________
# """)