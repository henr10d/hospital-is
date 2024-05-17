import mysql.connector
from mysql.connector import errorcode


class DatabaseCommunicator:
    def __init__(self, host, user, password, database):
        """
        Initializer for DatabaseCommunicator
        :param host: address where the server is hosted
        :param user: username under which the connection is to be made
        :param password: password associated with the username
        :param database: the name of the database to be connected to
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def handle_exception(self, exception):
        """
        Method for handling exception that arise while working with the database
        :param exception: exception to be handled
        :return: None
        """
        if exception.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            # Print access denied message
            pass
        elif exception.errno == errorcode.ER_BAD_DB_ERROR:
            # Print database non existent message
            pass
        else:
            # throw other error
            pass

    def connect(self):
        """
        Method that creates connection to the database
        :return: None
        """
        if self.connection is not None:
            return
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            self.handle_exception(err)

    def disconnect(self):
        """
        Method that closes the connection to the database
        :return: None
        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def database_query(self, statement, params, update):
        """
        Method that safely sends query to the database and returns the result
        :param statement: query to be sent to the database
        :param params: tuple with parameters for the query
        :param update: boolean indicating whether the flushing of the database is needed
        :return: List of tuples with data representing the result of the query
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement, params)
            if update:
                self.connection.commit()
            return cursor.fetchall()
        except mysql.connector.Error as err:
            if update:
                self.connection.rollback()
            self.handle_exception(err)
        finally:
            if cursor is not None:
                cursor.close()

    def get_user_id(self, params):
        """
        Get method for user_id from database based on username and password
        :param params: tuple with username and password
        :return: user_id or None if there is no such user_id in the database
        """
        statement = "SELECT id FROM users WHERE name = %s AND password = %s AND role = %s"
        result = self.database_query(statement, params, False)
        if result:
            return result[0][0]
        return None

    def get_doctor(self, params):
        """
        Method for getting data about a doctor based on id
        :param params: tuple with id of a doctor
        :return: data about the doctor or none
        """
        statement = "SELECT * FROM doctors WHERE doctor_id = %s"
        result = self.database_query(statement, params, False)
        if result:
            return result[0]
        return None

    def add_user_to_database(self, username, password, role, name, birth, insurance):
        """
        Adds new user to the database
        :param username: username of the new user as string
        :param password: password of the new user as string
        :param role: role of the user as string, can be one of ('patient', 'doctor')
        :param name: personal name of the new user as string
        :param birth: date of birth of the user
        :param insurance: insurance company covering the user
        :return: None
        """
        statement = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        self.database_query(statement, (username, password, role), True)
        user_id = self.get_user_id((username, password, role))
        if user_id is None:
            # throw some error
            pass
        if role == "patient":
            statement = "INSERT INTO patients (patient_id, name, birth, insurance) VALUES (%s, %s, %s, %s)"
        elif role == "doctor":
            statement = "INSERT INTO doctors (doctor_id, name, birth, insurance) VALUES (%s, %s, %s, %s)"
        else:
            # throw some error
            pass
        self.database_query(statement, (user_id, name, birth, insurance), True)

    def fetch_medical_record(self, user_id):
        """
        Method that fetches the medical history of patient with user_id
        :param user_id: id of the user for whom to fetch the medical history
        :return: the medical history of the patient or None if the user has
        no medical history
        """
        statement = "SELECT details FROM medical_history WHERE user_id = %s"
        result = self.database_query(statement, (user_id,), False)
        if result:
            return result[0]
        return None

    def update_medical_record(self, params):
        """
        Method for updating a medical record of a patient based on given parameters
        :param params: tuple with data based on which to update the record
        :return: None
        """
        statement = "UPDATE medical_history SET details = %s WHERE user_id = %s"
        self.database_query(statement, params, True)

    def insert_medical_record(self, params):
        """
        Method for inserting new medical record into the database
        :param params: parameters of the medical record
        :return: None
        """
        statement = "INSERT INTO medical_history (details, user_id) VALUES (%s, %s)"
        self.database_query(statement, params, True)

    def add_appointment(self, params):
        """
        Method for adding an appointment with a doctor
        :param params: parameters of the appointment
        :return: None
        """
        statement = ("INSERT INTO appointments (user_id, appointment_details,"
                     " appointment_time) VALUES (%s, %s, %s)")
        self.database_query(statement, params, True)
