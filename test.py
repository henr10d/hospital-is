import unittest
from DoctorUI import calculate_age
from datetime import datetime

class TestDoctorUI(unittest.TestCase):
    def test_calculate_age(self):
        # Test case for calculating age correctly
        birthdate = datetime(1980, 5, 4)
        expected_age = datetime.now().year - 1980 - (datetime.now().month, datetime.now().day < (5, 4))
        self.assertEqual(calculate_age(birthdate), expected_age)

if __name__ == '__main__':
    unittest.main()

import pytest
import mysql.connector

def test_insert_doctor(db_connection):
    cursor = db_connection.cursor()
    sql = "INSERT INTO doctors (name, specialty, birthdate) VALUES (%s, %s, %s)"
    values = ('John Doe', 'Cardiology', '1980-05-04')
    cursor.execute(sql, values)
    db_connection.commit()

    cursor.execute("SELECT * FROM doctors WHERE name = 'John Doe'")
    result = cursor.fetchone()
    assert result is not None

@pytest.fixture
def db_connection():
    connection = mysql.connector.connect(user='user', password='password', host='127.0.0.1', database='test_db')
    yield connection
    connection.rollback()
    connection.close()


import pytest
import mysql.connector

def test_insert_doctor(db_connection):
    cursor = db_connection.cursor()
    sql = "INSERT INTO doctors (name, specialty, birthdate) VALUES (%s, %s, %s)"
    values = ('John Doe', 'Cardiology', '1980-05-04')
    cursor.execute(sql, values)
    db_connection.commit()

    cursor.execute("SELECT * FROM doctors WHERE name = 'John Doe'")
    result = cursor.fetchone()
    assert result is not None

@pytest.fixture
def db_connection():
    connection = mysql.connector.connect(user='user', password='password', host='127.0.0.1', database='test_db')
    yield connection
    connection.rollback()
    connection.close()



