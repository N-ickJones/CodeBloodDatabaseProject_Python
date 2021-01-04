"""
Retrieves user donation information from donations table and
Creates a graph as example.png in /assets/images folder
Developer: Andrew Warren

Revision Started : 10/27/2018
Revision Developer: Nicholas Jones
Revision Date Complete 10/31/2018
Revision Notes: Made Program Object Oriented and Dynamic
"""

from decouple import config
import psycopg2
# from psycopg2.extensions import AsIs
# from datetime import datetime
# from django.utils import timezone
# from random import randint
# import matplotlib.pyplot as plt


class Tables:

    def __init__(self, schema='codeblood'):
        self.schema = schema
        self.table = TableBuilder()
        # self.auth_user(True)
        self.facilities(True)
        self.blood_donor(True)
        # self.money_donor(True)
        # self.time_donor(True)
        self.medical_staff(True)
        self.patient_reviews(True)
        self.patient_forms(True)
        self.vials(True)
        self.donation_stats(True)

    """
    def auth_user(self, create=True):
        table_name = 'auth_user'
        if create:
            attributes = (
                ('"id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"password"', 'VARCHAR(128)', 'NOT NULL'),
                ('"last_login"', 'TIMESTAMP WITH TIME ZONE', 'NOT NULL'),
                ('"username"', 'VARCHAR(150)', 'NOT NULL'),
                ('"first_name"', 'VARCHAR(30)', 'NOT NULL'),
                ('"username"', 'VARCHAR(150)', 'NOT NULL'),
                ('"email"', 'VARCHAR(254)', 'NOT NULL'),
                ('"is_staff"', 'BOOLEAN', 'NOT NULL'),
                ('"is_active"', 'BOOLEAN', 'NOT NULL'),
                ('"date_joined"', 'TIMESTAMP WITH TIME ZONE', 'NOT NULL'),
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)
    """
    def facilities(self, create=True):
        table_name = 'facilities'
        if create:
            attributes = (
                ('"facility_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"facility_type"', 'VARCHAR(30)', 'NOT NULL'),
                ('"facility_name"', 'VARCHAR(50)', 'NOT NULL'),
                ('"is_active"', 'BOOLEAN', 'NOT NULL'),
                ('"rating"', 'FLOAT', 'CHECK(rating > 0)'),
                ('"established"', 'TIMESTAMP WITH TIME ZONE'),
                ('"closed"', 'BOOLEAN'),
                ('"last_open"', 'TIMESTAMP WITH TIME ZONE'),
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)

    def blood_donor(self, create=True):
        table_name = 'blood_donor'
        if create:
            attributes = (
                ('"patient_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"eligible"', 'BOOLEAN', 'NOT NULL'),
                ('"blood_type"', 'VARCHAR(30)'),
                ('"is_active"', 'BOOLEAN', 'NOT NULL'),
                ('"first_donation"', 'TIMESTAMP WITH TIME ZONE'),
                ('"last_donation"', 'TIMESTAMP WITH TIME ZONE'),
                ('"amount_donated"', 'FLOAT', 'CHECK(amount_donated > 0.0)'),
                ('"times_donated"', 'INT', 'CHECK(times_donated > 0)'),
                ('"user_id"', 'INT', 'REFERENCES auth_user(id)')
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)
    """
    def money_donor(self, create=True):
        table_name = 'money_donor'
        if create:
            attributes = (
                ('"money_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"account_type"', 'VARCHAR(30)', 'NOT NULL'),
                ('"is_active"', 'BOOLEAN', 'NOT NULL'),
                ('"first_donation"', 'TIMESTAMP WITH TIME ZONE'),
                ('"last_donation"', 'TIMESTAMP WITH TIME ZONE'),
                ('"times_donated"', 'INT', 'CHECK(times_donated > 0)'),
                ('"amount_donated"', 'FLOAT', 'CHECK(amount_donated > 0.0)'),
                ('"user_id"', 'INT', 'REFERENCES auth_user(id)')
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)

    def time_donor(self, create=True):
        table_name = 'time_donor'
        if create:
            attributes = (
                ('"volunteer_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"volunteer_type"', 'VARCHAR(30)', 'NOT NULL'),
                ('"is_active"', 'BOOLEAN', 'NOT NULL'),
                ('"first_donation"', 'TIMESTAMP WITH TIME ZONE'),
                ('"last_donation"', 'TIMESTAMP WITH TIME ZONE'),
                ('"times_donated"', 'INT', 'CHECK(times_donated > 0)'),
                ('"amount_donated"', 'FLOAT', 'CHECK(amount_donated > 0.0)'),
                ('"user_id"', 'INT', 'REFERENCES auth_user(id)')
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)
    """
    def medical_staff(self, create=True):
        table_name = 'medical_staff'
        if create:
            attributes = (
                ('"medical_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"start_date"', 'TIMESTAMP WITH TIME ZONE', 'NOT NULL'),
                ('"job"', 'VARCHAR(30)', 'NOT NULL'),
                ('"is_active"', 'BOOLEAN', 'NOT NULL'),
                ('"level"', 'INT', 'CHECK(level > 0)'),
                ('"vacation_days"', 'FLOAT'),
                ('"on_vacation"', 'BOOLEAN'),
                ('"facility_id"', 'INT', 'REFERENCES codeblood.facilities(facility_id)'),
                ('"user_id"', 'INT', 'REFERENCES auth_user(id)')
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)

    def patient_reviews(self, create=True):
        table_name = 'patient_reviews'
        if create:
            attributes = (
                ('"review_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"date_reviewed"', 'TIMESTAMP WITH TIME ZONE', 'NOT NULL'),
                ('"title"', 'VARCHAR(30)', 'NOT NULL'),
                ('"rating"', 'INT', 'NOT NULL', 'CHECK(rating > 0)'),
                ('"review"', 'VARCHAR(500)'),
                ('"is_edited"', 'BOOLEAN'),
                ('"patient_id"', 'INT', 'REFERENCES codeblood.blood_donor(patient_id)'),
                ('"facility_id"', 'INT', 'REFERENCES codeblood.facilities(facility_id)'),
                ('"medical_id"', 'INT', 'REFERENCES codeblood.medical_staff(medical_id)'),
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)

    def patient_forms(self, create=True):
        table_name = 'patient_forms'
        if create:
            attributes = (
                ('"form_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"last_editor"', 'SERIAL', 'NOT NULL'),
                ('"next_eligible"', 'TIMESTAMP WITH TIME ZONE', 'NOT NULL'),
                ('"amount_donated"', 'FLOAT', 'NOT NULL', 'CHECK(amount_donated > 0.0)'),
                ('"next_appointment_date"', 'TIMESTAMP WITH TIME ZONE'),
                ('"last_appointment_date"', 'TIMESTAMP WITH TIME ZONE'),
                ('"special_instructions"', 'VARCHAR(500)'),
                ('"patient_id"', 'INT', 'REFERENCES codeblood.blood_donor(patient_id)'),
                ('"facility_id"', 'INT', 'REFERENCES codeblood.facilities(facility_id)'),
                ('"medical_id"', 'INT', 'REFERENCES codeblood.medical_staff(medical_id)'),
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)

    def vials(self, create=True):
        table_name = 'vials'
        if create:
            attributes = (
                ('"vial_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"vial_type"', 'VARCHAR(30)', 'NOT NULL'),
                ('"points"', 'INT', 'NOT NULL', 'CHECK(points > 0)'),
                ('"amount_donated"', 'FLOAT', 'NOT NULL'),
                ('"patient_id"', 'INT', 'REFERENCES codeblood.blood_donor(patient_id)'),
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)

    def donation_stats(self, create=True):
        table_name = 'donation_stats'
        if create:
            attributes = (
                ('"donation_id"', 'SERIAL', 'NOT NULL', 'PRIMARY KEY'),
                ('"blood_type"', 'VARCHAR(30)', 'NOT NULL'),
                ('"amount_donated"', 'FLOAT', 'NOT NULL', 'CHECK(amount_donated > 0.0)'),
                ('"form_id"', 'INT', 'REFERENCES codeblood.patient_forms(form_id)'),
            )
            self.table.build(self.schema, table_name, attributes)
        else:
            self.table.drop(self.schema, table_name)


class TableBuilder:
    # TODO Build Schema if doesn't exist and delete schema if empty after table removal

    def __init__(self):
        self.conn = psycopg2.connect(config('DATABASE_URL'))
        self.write = False
        if self.write:
            open('output.txt', 'w').close()

    def build(self, schema, table, attributes):
        if self.__check__(schema):
            if self.__check__(schema, table) is False:
                sql = 'CREATE TABLE {}.{}('.format(schema, table)
                for attrib in attributes:
                    for item in attrib:
                        sql += '{} '.format(item)
                    sql = sql.rstrip()
                    sql += '{} '.format(',')
                sql = sql.rstrip(' ,')
                sql += ');'
                if self.write:
                    with open('output.txt', 'a') as file:
                        file.write('{}\n'.format(sql))
                else:
                    with self.conn.cursor() as cur:
                        print(sql)
                        cur.execute(sql)
                    self.conn.commit()
                print("SUCCESS: Schema {} now has the {} relation.".format(schema, table))
            else:
                print("ERROR: Schema {} already has the {} relation.".format(schema, table))
        else:
            print("ERROR: Schema {} doesn't exist.".format(schema))

    def drop(self, schema, table):
        if self.__check__(schema):
            if self.__check__(schema, table):
                sql = "drop table {}.{}".format(schema, table)
                with self.conn.cursor() as cur:
                    cur.execute(sql)
                self.conn.commit()
                print("SUCCESS: Schema {} no longer has the {} relation.".format(schema, table))
            else:
                print("ERROR: Schema {} does not have the {} relation.".format(schema, table))
        else:
            print("ERROR: Schema {} doesn't exist.".format(schema))

    def __check_schema__(self, schema_name):
        with self.conn.cursor() as cur:
            sql = "SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = '{}');".format(schema_name)
            cur.execute(sql)
            return True if cur.fetchone()[0] else False

    def __check_table__(self, table_schema, table_name):
        with self.conn.cursor() as cur:
            sql = "SELECT EXISTS(SELECT * FROM information_schema.tables " \
                  "WHERE table_schema = '{}' AND table_name = '{}');".format(table_schema, table_name)
            cur.execute(sql)
            return True if cur.fetchone()[0] else False

    def __check__(self, schema_name, table_name=None):
        if self.__check_schema__(schema_name):
            if table_name is not None:
                if self.__check_table__(schema_name, table_name):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def __del__(self):
        self.conn.close()

    def fill(self, schema, table, entries):
        if self.__check__(schema):
            if self.__check__(schema, table):
                insert = "INSERT INTO {}.{}".format(schema, table)
                with self.conn.cursor() as cur:
                    for entry in entries:
                        attributes, values = '', ''
                        for item in entry:
                            attributes += "{}, ".format(item[0])
                            values += "'{}', ".format(item[1])
                        attributes = attributes.rstrip(', ')
                        values = values.rstrip(', ')
                        sql = "{} ({}) {} ({});".format(insert, attributes, 'VALUES', values)
                        cur.execute(sql)
                self.conn.commit()
                print("SUCCESS: Schema {} now has the {} relation with entries.".format(schema, table))
            else:
                print("ERROR: Schema {} does not have the {} relation.".format(schema, table))
        else:
            print("ERROR: Schema {} doesn't exist.".format(schema))

    def is_filled(self, schema, table):
        if self.__check__(schema):
            if self.__check__(schema, table):
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{});".format(schema, table)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False
        else:
            return False



"""

    def get_donations(self):
        with self.conn.cursor() as cur:
            for date in self.donate_date_var:
                sql = "SELECT donate_amount FROM donations WHERE donate_date Between %s And %s;"
                data = (date[0], date[1])
                add_donations = 0.0
                cur.execute(sql, data)
                self.donate_data = cur.fetchall()
                for data in self.donate_data:
                    print(data[0])
                    add_donations += float(data[0])
                self.total_donations.append(add_donations)
                print(self.total_donations)
"""


