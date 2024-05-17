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
        print("error while working with database:")
        if exception.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access to the database was denied")
            pass
        elif exception.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
            pass
        else:
            # throw other error
            print("database query failed")

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

    def get_patient(self, params):
        """
        Method for getting data about a patient based on id
        :param params: tuple with id of a patient
        :return: data about the doctor or none
        """
        statement = "SELECT * FROM patients WHERE patient_id = %s"
        result = self.database_query(statement, params, False)
        if result:
            return result[0]
        return None

    def login(self, params):
        user_id = self.get_user_id(params)
        if id is None:
            return None
        if params[2] == "doctor":
            return self.get_doctor((user_id, ))
        elif params[2] == "patient":
            return self.get_patient((user_id, ))

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

    def fetch_patient_medical_records(self, patient_id):
        """
        Method that fetches the medical history of patient with user_id
        :param patient_id: id of the user for whom to fetch the medical history
        :return: the medical history of the patient or None if the user has
        no medical history
        """
        statement = "SELECT * FROM medical_history WHERE patient_id = %s"
        result = self.database_query(statement, (patient_id,), False)
        if result:
            return result
        return None

    def update_medical_record(self, params):
        """
        Method for updating a medical record of a patient based on given parameters
        :param params: tuple with new details and medical_record id
        :return: None
        """
        statement = "UPDATE medical_history SET details = %s WHERE id = %s"
        self.database_query(statement, params, True)

    def add_medical_record(self, params):
        """
        Method for inserting new medical record into the database
        :param params: parameters of the medical record
        :return: None
        """
        statement = "INSERT INTO medical_history (details, patient_id, appointment_time) VALUES (%s, %s, %s)"
        self.database_query(statement, params, True)

    def add_appointment(self, params):
        """
        Method for adding an appointment with a doctor
        :param params: parameters of the appointment
        :return: None
        """
        statement = ("INSERT INTO appointments (patient_id, doctor_id, appointment_details,"
                     " appointment_time, status) VALUES (%s, %s, %s, %s, %s))")
        self.database_query(statement, params + ("waiting", ), True)

    def fetch_patient_appointments(self, patient_id):
        """
        Method that fetches the medical history of patient with user_id
        :param patient_id: id of the user for whom to fetch the medical history
        :return: the medical history of the patient or None if the user has
        no medical history
        """
        statement = "SELECT * FROM appointments WHERE patient_id = %s"
        result = self.database_query(statement, (patient_id,), False)
        if result:
            return result
        return None

    def fetch_doctor_appointments(self, doctor_id):
        """
       Method that fetches the medical history of patient with user_id
       :param doctor_id: id of the user for whom to fetch the medical history
       :return: the medical history of the patient or None if the user has
       no medical history
       """
        statement = "SELECT * FROM appointments WHERE doctor_id = %s"
        result = self.database_query(statement, (doctor_id,), False)
        if result:
            return result
        return None

    def approved_appointment(self, appointment_id):
        """
       Method that fetches the medical history of patient with user_id
       :param appointment_id: id of the appointment to be accepted
       :return: the medical history of the patient or None if the user has
       no medical history
       """
        statement = "UPDATE appointments SET status = %s WHERE id = %s"
        result = self.database_query(statement, ("approved", appointment_id), False)
        if result:
            return result
        return None
