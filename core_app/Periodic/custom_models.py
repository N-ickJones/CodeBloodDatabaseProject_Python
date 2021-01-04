import psycopg2
from psycopg2.extensions import AsIs
from decouple import config
# noinspection PyCompatibility
from http import cookies

from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models


class CustomSession(AbstractBaseSession):
    account_id = models.IntegerField(null=True, db_index=True)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore


# noinspection PyCompatibility
class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        return CustomSession

    def create_model_instance(self, data):
        obj = super().create_model_instance(data)
        try:
            account_id = int(data.get('_auth_user_id'))
        except (ValueError, TypeError):
            account_id = None
        obj.account_id = account_id
        return obj


class UserSessions:
    def __init__(self):
        self.__session = cookies.SimpleCookie()


class UserAccounts:
    def __init__(self, username, password_hash, first_name, last_name, blood_group, street_name, city_name,
                 state_name, zip_code, mobile_number, email, security_question, security_answer_hash,
                 last_blood_donation, subscribe_request):
        # NOTE : PRIVATE CLASSES DON'T CLOSE CURSOR
        # Retrieve Database & Schema
        self.__db = DataBuilder()
        self.__conn = self.__db.connect()
        self.__cur = self.__db.get_cursor()
        self.__schema_name = self.__db.get_schema()
        if self.__db.table_exist():
            self.__table_exist = True
        else:
            self.__db.create_table('user_accounts')
            if self.__db.table_exist() is False:
                self.__table_exist = False

        # User Accounts Table Settings
        self.__table_name = 'user_accounts'
        self.__remove_type = 'RESTRICT'

        # User Account Fields
        self.__user_id = 'test'  # TODO Build ID Assignment
        self.__username = username
        self.__password = password_hash
        self.__first_name = first_name
        self.__last_name = last_name
        self.__blood_group = blood_group
        self.__street_name = street_name
        self.__city_name = city_name
        self.__state_name = state_name
        self.__zip_code = zip_code
        self.__mobile_number = mobile_number
        self.__email = email
        self.__security_question = security_question
        self.__security_answer = security_answer_hash
        self.__last_blood_donation = last_blood_donation
        self.__subscribe_request = subscribe_request

        self.__user_added = True

        def __init__(self, username, password_hash, first_name, last_name, blood_group, street_name, city_name,
                     state_name, zip_code, mobile_number, email, security_question, security_answer_hash,
                     last_blood_donation, subscribe_request):
            # NOTE : PRIVATE CLASSES DON'T CLOSE CURSOR
            # Retrieve Database & Schema
            self.__db = DataBuilder()
            self.__conn = self.__db.connect()
            self.__cur = self.__db.get_cursor()
            self.__schema_name = self.__db.get_schema()
            if self.__db.table_exist():
                self.__table_exist = True
            else:
                self.__db.create_table('user_accounts')
                if self.__db.table_exist() is False:
                    self.__table_exist = False

            # User Accounts Table Settings
            self.__table_name = 'user_accounts'
            self.__remove_type = 'RESTRICT'

            # User Account Fields
            self.__user_id = 'test'  # TODO Build ID Assignment
            self.__username = username
            self.__password = password_hash
            self.__first_name = first_name
            self.__last_name = last_name
            self.__blood_group = blood_group
            self.__street_name = street_name
            self.__city_name = city_name
            self.__state_name = state_name
            self.__zip_code = zip_code
            self.__mobile_number = mobile_number
            self.__email = email
            self.__security_question = security_question
            self.__security_answer = security_answer_hash
            self.__last_blood_donation = last_blood_donation
            self.__subscribe_request = subscribe_request

            self.__user_added = True

    def add_entry(self):
        if self.__check_entry() is False:
            sql = '''INSERT INTO %s.%s (id, username, password, first_name, last_name, blood_group,
              street_name, city_name, state_name, zip_code, mobile_number, email, security_question, security_answer,
              last_blood_donation, subscribe_request) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
               %s, %s, %s);'''
            data = (AsIs(self.__schema_name), AsIs(self.__table_name), self.__user_id, self.__username, self.__password,
                    self.__first_name, self.__last_name, self.__blood_group, self.__street_name, self.__city_name,
                    self.__state_name, self.__zip_code, self.__mobile_number, self.__email, self.__security_question,
                    self.__security_answer, self.__last_blood_donation, self.__subscribe_request,)
            self.__cur.execute(sql, data)
            print("User Created in DB Successfully")
            self.__conn.commit()
            self.__conn.close()
            self.__user_added = True
        else:
            self.__user_added = False
            print("Couldn't add User")

    def __check_entry(self):
        if self.__table_exist is True:
            sql = '''SELECT EXISTS(SELECT 1 FROM codeblood.user_accounts WHERE username = %s)'''
            data = (self.__username,)
            self.__cur.execute(sql, data)
            validated = self.__cur.fetchone()
            self.__conn.commit()
            if validated[0]:
                return True
            else:
                return False
        else:
            print("Table Doesn't exist")
            return False

    def authenticate(self):
        if self.__table_exist is True:
            sql = '''SELECT password FROM %s.%s WHERE username = %s'''
            data = (AsIs(self.__schema_name), AsIs(self.__table_name), self.__username)
            self.__cur.execute(sql, data)
            password = self.__cur.fetchone()
            self.__conn.commit()
            self.__conn.close()
            if password is not None:
                if password[0] == self.__password:
                    print('Password Match')
                    return True
                else:
                    print('Password MisMatch')
                    return False
            else:
                print('Password None')
                return False
        else:
            print("Table Doesn't exist")
            return False

    def table_exist(self):
        return self.__table_exist

    def was_added(self):
        return self.__user_added


class DataBuilder:
    def __init__(self):
        self.__conn = psycopg2.connect(config('DATABASE_URL'))
        self.__cur = self.__conn.cursor()
        self.__schema_name = 'codeblood'
        self.__table_name = 'user_accounts'
        self.__remove_type = 'RESTRICT'

    def __table_exist(self):
        sql = "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = %s AND table_name = %s);"
        data = (self.__schema_name, self.__table_name,)

        self.__cur.execute(sql, data)
        result = self.__cur.fetchone()
        # print(result)
        if 'True' in str(result):
            return True
        elif 'False' in str(result):
            return False

    def __create_user_accounts(self):
        # TODO Assign ID
        sql = """CREATE TABLE codeblood.user_accounts(
                            id                  VARCHAR(50) ,
                            username            VARCHAR(50) PRIMARY KEY,
                            password            VARCHAR(128),
                            first_name          VARCHAR(30) ,
                            last_name           VARCHAR(30) ,
                            blood_group         VARCHAR(50) ,
                            street_name         VARCHAR(50) ,
                            city_name           VARCHAR(50) ,
                            state_name          VARCHAR(50) ,
                            zip_code            VARCHAR(50) ,
                            mobile_number       VARCHAR(50) ,
                            email               VARCHAR(100),
                            security_question   VARCHAR(100),
                            security_answer     VARCHAR(128),
                            last_blood_donation VARCHAR(100),
                            subscribe_request   VARCHAR(100)
                            );"""

        data = (AsIs(self.__schema_name), AsIs(self.__table_name))
        self.__cur.execute(sql, data)
        print("Table created successfully")
        self.__conn.commit()
        self.__conn.close()

    def table_exist(self):
        if self.__table_exist():
            return True
        else:
            return False

    def create_table(self, table):
        self.__table_name = table
        if self.__table_exist() is False:
            self.__create_user_accounts()

    def connect(self):
        return self.__conn

    def get_cursor(self):
        return self.__cur

    def get_schema(self):
        return self.__schema_name

    def set_table(self, table_name):
        self.__table_name = table_name
