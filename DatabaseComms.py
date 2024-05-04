import mysql.connector
from mysql.connector import errorcode


class DatabaseCommunicator:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        except mysql.connector.Error as err:
            self.handle_exception(err)

    def handle_exception(self, exception):
        if exception.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            # Print access denied message
            pass
        elif exception.errno == errorcode.ER_BAD_DB_ERROR:
            # Print database non existent message
            pass
        else:
            # throw other error
            pass

    def disconnect(self):
        self.connection.close()

    def fetch_medical_history(self, person_id):
        statement = "SELECT details FROM medical_history WHERE user_id = %s"
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement, person_id)
            return cursor.fetchone()
        except mysql.connector.Error as err:
            self.handle_exception(err)
        finally:
            if cursor is not None:
                cursor.close()

    def login_user(self, params):
        statement = "SELECT id FROM users WHERE name = %s AND password = %s AND role = %s"
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement, params)
            result = cursor.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            self.handle_exception(err)
        finally:
            if cursor is not None:
                cursor.close()

    def register_user(self, params):
        statement = "INSERT INTO users (name, password, role) VALUES (%s, %s, %s)"
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement, params)
        except mysql.connector.Error as err:
            self.handle_exception(err)
        finally:
            if cursor is not None:
                cursor.close()