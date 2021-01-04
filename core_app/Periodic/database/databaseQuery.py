import psycopg2
from decouple import config


class DBQuery:

    class BloodDonor:
        def __init__(self):
            self.conn = psycopg2.connect(config('DATABASE_URL'))
            self.schema = 'codeblood'
            self.table = 'blood_donor'

        def __check_table__(self):
            with self.conn.cursor() as cur:
                sql = "SELECT EXISTS(SELECT * FROM information_schema.tables " \
                      "WHERE table_schema = '{}' AND table_name = '{}');".format(self.schema, self.table)
                cur.execute(sql)
                return True if cur.fetchone()[0] else False

        def check_entry(self, user_id):
            if self.__check_table__():
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{} WHERE user_id={})".format(self.schema, self.table, user_id)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False

        def check_appointment(self, user_id):
            if self.__check_table__():
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{} WHERE user_id={} and first_donation IS NULL)".format(
                        self.schema, self.table, user_id)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False

        def make_donor_account(self, blood_type, eligible, is_active, user_id):
            with self.conn.cursor() as cur:
                sql = "INSERT INTO {}.{} (blood_type, eligible, is_active, user_id) VALUES ('{}', {}, {}, {})".format(
                    self.schema, self.table, blood_type, eligible, is_active, user_id)
                cur.execute(sql)
            self.conn.commit()

        def set_appointment(self, user_id, appointment):
            with self.conn.cursor() as cur:
                sql = "UPDATE {}.{} SET first_donation = '{}' WHERE user_id = {}".format(self.schema, self.table,
                                                                                         appointment, user_id)
                cur.execute(sql)
            self.conn.commit()

        def check_appointment_attendance(self, user_id):
            if self.__check_table__():
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{} WHERE user_id={} and first_donation = last_donation)".format(
                        self.schema, self.table, user_id)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False

        def get_appointment(self, user_id):
            with self.conn.cursor() as cur:
                sql = "SELECT first_donation FROM {}.{} WHERE user_id = '{}'".format(self.schema, self.table, user_id)
                cur.execute(sql)
                first_donation = cur.fetchone()[0]
            return first_donation

        def get_last_donation(self, user_id):
            with self.conn.cursor() as cur:
                sql = "SELECT last_donation FROM {}.{} WHERE user_id = '{}'".format(self.schema, self.table, user_id)
                cur.execute(sql)
                try:
                    last_donation = cur.fetchone()[0]
                except TypeError:
                    last_donation = cur.fetchone()
            return last_donation

        def get_patient_id(self, user_id):
            with self.conn.cursor() as cur:
                sql = "SELECT patient_id FROM {}.{} WHERE user_id = '{}'".format(self.schema, self.table, user_id)
                cur.execute(sql)
                first_donation = cur.fetchone()[0]
            return first_donation

        def set_last_donation(self, patient_id, last_donation):
            with self.conn.cursor() as cur:
                sql = "UPDATE {}.{} SET last_donation = '{}' WHERE patient_id = {}".format(self.schema, self.table,
                                                                                           last_donation, patient_id)
                cur.execute(sql)
            self.conn.commit()

        def __del__(self):
            self.conn.close()

    class MedicalStaff:
        def __init__(self):
            self.conn = psycopg2.connect(config('DATABASE_URL'))
            self.schema = 'codeblood'
            self.table = 'medical_staff'

        def get_medical_id(self, user_id):
            with self.conn.cursor() as cur:
                sql = "SELECT medical_id FROM {}.{} WHERE user_id = '{}'".format(self.schema, self.table, user_id)
                cur.execute(sql)
                facility_id = cur.fetchone()[0]
            return facility_id

        def __get_facility_id__(self, facility_name):
            with self.conn.cursor() as cur:
                sql = "SELECT facility_id FROM {}.{} WHERE facility_name = '{}'".format(self.schema, 'facilities', facility_name)
                cur.execute(sql)
                facility_id = cur.fetchone()[0]
            return facility_id

        def get_facility_id(self, medical_id):
            with self.conn.cursor() as cur:
                sql = "SELECT facility_id FROM {}.{} WHERE medical_id = '{}'".format(self.schema, self.table, medical_id)
                cur.execute(sql)
                facility_id = cur.fetchone()[0]
            return facility_id

        def __check_table__(self):
            with self.conn.cursor() as cur:
                sql = "SELECT EXISTS(SELECT * FROM information_schema.tables " \
                      "WHERE table_schema = '{}' AND table_name = '{}');".format(self.schema, self.table)
                cur.execute(sql)
                return True if cur.fetchone()[0] else False

        def check_entry(self, user_id):
            if self.__check_table__():
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{} WHERE user_id={})".format(self.schema, self.table, user_id)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False

        def is_active(self, user_id):
            if self.__check_table__():
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{} WHERE user_id={} AND is_active=TRUE)".format(self.schema, self.table, user_id)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False

        def check_appointment(self, user_id):
            if self.__check_table__():
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{} WHERE user_id={} and first_donation IS NULL)".format(
                        self.schema, self.table, user_id)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False

        def add_staff_entry(self, start_date, facility_name, level, job, user_id):
            facility_id = self.__get_facility_id__(facility_name)
            with self.conn.cursor() as cur:
                sql = "INSERT INTO {}.{}(start_date, job, is_active, level, vacation_days, on_vacation, facility_id, user_id) VALUES ('{}', '{}', {}, {}, {}, {}, {}, {})".format(self.schema, self.table, start_date, job, False, level, 0, False, facility_id, user_id)
                cur.execute(sql)
            self.conn.commit()

        def activate_account(self, user_id):
            with self.conn.cursor() as cur:
                sql = "UPDATE {}.{} SET is_active = '{}' WHERE user_id = {}".format(self.schema, self.table, True, user_id)
                cur.execute(sql)
            self.conn.commit()

        def __del__(self):
            self.conn.close()

        def get_staff_name(self, medical_id):
            with self.conn.cursor() as cur:
                sql = 'SELECT user_id FROM {}.{} WHERE medical_id={}'.format(self.schema, self.table, medical_id)
                cur.execute(sql)
                user_id = cur.fetchone()[0]
                sql = "SELECT first_name FROM public.auth_user WHERE id={}".format(user_id)
                cur.execute(sql)
                first_name = cur.fetchone()[0]
                sql = "SELECT last_name FROM public.auth_user WHERE id={}".format(user_id)
                cur.execute(sql)
                last_name = cur.fetchone()[0]
            return first_name + ' ' + last_name

    class PatientForms:
        def __init__(self):
            self.conn = psycopg2.connect(config('DATABASE_URL'))
            self.schema = 'codeblood'
            self.table = 'patient_forms'

        def __check_table__(self):
            with self.conn.cursor() as cur:
                sql = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = '{}' AND table_name = '{}');".format(self.schema, self.table)
                cur.execute(sql)
                return True if cur.fetchone()[0] else False

        def check_entry(self, patient_id):
            if self.__check_table__():
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{} WHERE patient_id={})".format(self.schema, self.table, patient_id)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False

        def add_entry(self, amount_donated, appointment_date, next_eligible, next_appointment_date, special_instructions, patient_id, facility_id, medical_id):
            print(amount_donated, appointment_date, next_eligible, next_appointment_date, special_instructions, patient_id, facility_id, medical_id)
            if self.check_entry(patient_id):
                with self.conn.cursor() as cur:
                    sql = "UPDATE {}.{} SET last_editor = '{}', next_eligible = '{}', amount_donated = '{}', next_appointment_date = '{}', last_appointment_date = '{}', special_instructions = '{}', WHERE patient_id = {}".format(self.schema, self.table,  medical_id, next_eligible, amount_donated, next_appointment_date, appointment_date, special_instructions, patient_id)
                    cur.execute(sql)
                self.conn.commit()
            else:
                if self.__check_table__():
                    with self.conn.cursor() as cur:
                        sql = "INSERT INTO {}.{}(last_editor, next_eligible, amount_donated, next_appointment_date, last_appointment_date, special_instructions, patient_id, facility_id, medical_id) VALUES ({}, '{}', {}, '{}', '{}', '{}', {}, {}, {})" \
                            "".format(self.schema, self.table, medical_id, next_eligible, amount_donated, next_appointment_date, appointment_date, special_instructions, patient_id, facility_id, medical_id)
                        cur.execute(sql)
                    self.conn.commit()

        def get_facility_id(self, patient_id):
            with self.conn.cursor() as cur:
                sql = 'SELECT facility_id FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_medical_id(self, patient_id):
            with self.conn.cursor() as cur:
                sql = 'SELECT medical_id FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_next_appointment_date(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT next_appointment_date FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                try:
                    last_appointment = cur.fetchone()[0]
                except TypeError:
                    last_appointment = cur.fetchone()
                return last_appointment

        def get_last_appointment_date(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT last_appointment_date FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                try:
                    last_appointment = cur.fetchone()[0]
                except TypeError:
                    last_appointment = cur.fetchone()
                return last_appointment

        def get_last_editor(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT last_editor FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_next_eligible(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT next_eligible FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_amount_donated(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT amount_donated FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_special_instructions(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT special_instructions FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_upcoming_appointments(self):
            with self.conn.cursor() as cur:
                sql = 'SELECT patient_id, first_donation FROM codeblood.blood_donor'
                cur.execute(sql)
                return cur.fetchall()

    class PatientReviews:
        def __init__(self):
            self.conn = psycopg2.connect(config('DATABASE_URL'))
            self.schema = 'codeblood'
            self.table = 'patient_reviews'

        def __check_table__(self):
            with self.conn.cursor() as cur:
                sql = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = '{}' AND table_name = '{}');".format(self.schema, self.table)
                cur.execute(sql)
                return True if cur.fetchone()[0] else False

        def check_entry(self, patient_id):
            if self.__check_table__():
                with self.conn.cursor() as cur:
                    sql = "SELECT EXISTS(SELECT 1 FROM {}.{} WHERE patient_id={})".format(self.schema, self.table, patient_id)
                    cur.execute(sql)
                    return True if cur.fetchone()[0] else False
            else:
                return False

        def create_review(self, date_reviewed, title, rating, review, patient_id, facility_id, medical_id):
            if self.__check_table__:
                if self.check_entry(patient_id) is False:
                    with self.conn.cursor() as cur:
                        sql = "INSERT INTO {}.{}(date_reviewed, title, rating, review, patient_id, facility_id, medical_id) VALUES ('{}', '{}', {}, '{}', {}, {}, {})" \
                            "".format(self.schema, self.table, date_reviewed, title, rating, review, patient_id, facility_id, medical_id)
                        cur.execute(sql)
                    self.conn.commit()

        def get_all_reviews(self):
            if self.__check_table__:
                with self.conn.cursor() as cur:
                    sql = 'SELECT * FROM codeblood.patient_reviews'
                    cur.execute(sql)
                    data = cur.fetchall()
                    return data

        def get_username(self, patient_id):
            with self.conn.cursor() as cur:
                sql = 'SELECT user_id FROM codeblood.blood_donor WHERE patient_id={}'.format(patient_id)
                cur.execute(sql)
                user_id = cur.fetchone()[0]
                sql = 'SELECT username FROM public.auth_user WHERE id={}'.format(user_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_facility(self, facility_id):
            with self.conn.cursor() as cur:
                sql = 'SELECT facility_name FROM codeblood.facilities WHERE facility_id={}'.format(facility_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_medical_staff(self, medical_id):
            with self.conn.cursor() as cur:
                sql = 'SELECT user_id FROM codeblood.medical_staff WHERE medical_id={}'.format(medical_id)
                cur.execute(sql)
                user_id = cur.fetchone()[0]
                sql = 'SELECT first_name, last_name FROM public.auth_user WHERE id={}'.format(user_id)
                cur.execute(sql)
                name = cur.fetchall()
                return '{} {}'.format(name[0][0], name[0][1])

    class Vials:
        def __init__(self):
            self.conn = psycopg2.connect(config('DATABASE_URL'))
            self.schema = 'codeblood'
            self.table = 'vials'

        def add_vial(self, vial_type, points, amount_donated, patient_id):
            with self.conn.cursor() as cur:
                sql = "INSERT INTO {}.{}(vial_type, points, amount_donated, patient_id) VALUES ('{}', {}, {}, {})".format(self.schema, self.table, vial_type, points, amount_donated, patient_id)
                cur.execute(sql)
            self.conn.commit()

        def get_vial_type(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT vial_type FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_points(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT points FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]

        def get_amount_donated(self, user_id):
            patient_id = DBQuery().BloodDonor().get_patient_id(user_id)
            with self.conn.cursor() as cur:
                sql = 'SELECT amount_donated FROM {}.{} WHERE patient_id={}'.format(self.schema, self.table, patient_id)
                cur.execute(sql)
                return cur.fetchone()[0]
