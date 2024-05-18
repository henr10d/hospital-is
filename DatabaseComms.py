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
        statement = "SELECT id FROM users WHERE username = %s AND password = %s AND role = %s"
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

    def add_user_to_database(self, name, birth, username, password, role, insurance):
        """
        Adds new user to the database
        :param name: personal name of the new user as string
        :param birth: date of birth of the user
        :param username: username of the new user as string
        :param password: password of the new user as string
        :param role: role of the user as string, can be one of ('patient', 'doctor')
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
            statement = ("INSERT INTO patients (patient_id, name, birth, insurance) "
                         "VALUES (%s, %s, %s, %s)")
        elif role == "doctor":
            statement = ("INSERT INTO doctors (doctor_id, name, birth, insurance) "
                         "VALUES (%s, %s, %s, %s)")
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
        statement = ("SELECT appointment_time, details "
                     "FROM medical_history "
                     "WHERE patient_id = %s "
                     "ORDER BY appointment_time DESC")
        result = self.database_query(statement, (patient_id,), False)
        return result

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
        statement = """
                    INSERT INTO appointments (patient_id, doctor_id, details, appointment_time, status)
                    VALUES (%s, %s, %s, %s, %s);
                    """
        self.database_query(statement, params, True)

    def fetch_patient_appointments(self, patient_id):
        """
        Method that fetches the medical history of patient with user_id
        :param patient_id: id of the user for whom to fetch the medical history
        :return: the medical history of the patient or None if the user has
        no medical history
        """
        statement = ("SELECT id, appointment_time, details, status "
                     "FROM appointments "
                     "WHERE patient_id = %s "
                     "ORDER BY appointment_time DESC")
        result = self.database_query(statement, (patient_id,), False)
        return result

    def fetch_doctor_appointments(self, doctor_id):
        """
       Method that fetches the medical history of patient with user_id
       :param doctor_id: id of the user for whom to fetch the medical history
       :return: the medical history of the patient or None if the user has
       no medical history
       """
        statement = ("SELECT id, appointment_time, details, status "
                     "FROM appointments "
                     "WHERE doctor_id = %s "
                     "ORDER BY appointment_time DESC")
        result = self.database_query(statement, (doctor_id,), False)
        return result

    def update_appointment_status(self, params):
        """
       Method that approves declines with appointment_id
       :param params: id of appointment and new status
       :return: None
       """
        statement = "UPDATE appointments SET status = %s WHERE id = %s"
        self.database_query(statement, params, True)

    def update_personal_info(self, params):
        """
        Method to update the personal information of a patient
        :param params: new name and age and id of the patient
        :return: None
        """
        statement = "UPDATE patients SET name = %s WHERE patient_id = %s"
        self.database_query(statement, params, True)

    def update_patient_picture(self, patient_id, image_path):
        """
        Method to update path to an image for patient
        :param patient_id: id of the patient
        :param image_path: path to the image
        :return: None
        """
        statement = "UPDATE patients SET image_path = %s WHERE patient_id = %s"
        self.database_query(statement, (image_path, patient_id), True)

    def fetch_patient_picture(self, patient_id):
        """
        Method to get path to an image of a patient
        :param patient_id: id of the patient
        :return: path to the image or None if the path does not exist
        """
        statement = "SELECT image_path FROM patients WHERE patient_id = %s"
        result = self.database_query(statement, (patient_id, ), False)
        if result is not None:
            return result[0]
        return None

    def get_login_credentials(self, user_id):
        statement = "SELECT username, password FROM users WHERE id = %s"
        result = self.database_query(statement, (user_id,), False)
        if result is not None:
            return result[0]
        return None

    def update_login_credentials(self, params):
        statement = "UPDATE users SET username = %s, password = %s WHERE id = %s"
        self.database_query(statement, params, True)

    def fetch_NULL_patients(self):
        statement = ("SELECT patient_id, name, birth, insurance "
                     "FROM patients where doctor_id IS NULL")
        result = self.database_query(statement, None, False)
        return result

    def add_doctor_to_patient(self, patient_id, doctor_id):
        statement = "UPDATE patients SET doctor_id = %s WHERE patient_id = %s"
        self.database_query(statement, (doctor_id, patient_id), True)
        statement = "UPDATE appointments SET doctor_id = %s WHERE patient_id = %s"
        self.database_query(statement, (doctor_id, patient_id), True)

