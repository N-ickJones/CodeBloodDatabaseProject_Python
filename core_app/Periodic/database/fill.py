import sys
from core_app.Periodic.database.tables import TableBuilder
# from decouple import config
# import psycopg2
# from psycopg2.extensions import AsIs
# from datetime import datetime
# from django.utils import timezone
# from random import randint
# import matplotlib.pyplot as plt


class TableFill:

    def __init__(self):
        self.builder = TableBuilder()
        self.schema_name = 'codeblood'
        self.blood_donor_entries()
        self.medical_staff_entries()
        self.patient_reviews_entries()
        self.patient_sheets_entries()

    def blood_donor_entries(self):
        table_name = 'blood_donor'
        if self.builder.is_filled(self.schema_name, table_name) is False:
            entries = (
                (('"patient_id"', '1'),
                ('"eligible"', 'True'),
                ('"blood_type"', 'A-Positive'),
                ('"first_donation"', '2018-09-22 21:48:31.582940'),
                ('"last_donation"', '2018-09-22 21:48:31.582940'),
                ('"times_donated"', '5'),
                ('"amount_donated"', '100'),
                ('"is_active"', 'True')),

                (('"patient_id"', '2'),
                ('"eligible"', 'False'),
                ('"blood_type"', 'B-Positive'),
                ('"first_donation"', '2018-10-22 21:48:31.582940'),
                ('"last_donation"', '2018-12-22 21:48:31.582940'),
                ('"times_donated"', '2'),
                ('"amount_donated"', '40'),
                ('"is_active"', 'True'))
            )
            self.builder.fill(self.schema_name, table_name, entries)
        else:
            print("ERROR: {} table is already has data.".format(table_name))

    def medical_staff_entries(self):
        table_name = 'medical_staff'
        if self.builder.is_filled(self.schema_name, table_name) is False:
            entries = (
                (('"id"', '3'),
                 ('"start_date"', '2018-10-22 21:48:31.582940'),
                 ('"job"', 'doctor'),
                 ('"is_active"', 'True'),
                 ('"level"', '6'),
                 ('"rating"', '7'),
                 ('"vacation_days"', '5'),
                 ('"on_vacation"', 'False')),

                (('"id"', '4'),
                 ('"start_date"', '2018-01-22 21:48:31.582940'),
                 ('"job"', 'Nurse'),
                 ('"is_active"', 'True'),
                 ('"level"', '4'),
                 ('"rating"', '9'),
                 ('"vacation_days"', '20'),
                 ('"on_vacation"', 'False'))
            )
            self.builder.fill(self.schema_name, table_name, entries)
        else:
            print("ERROR: {} table is already has data.".format(table_name))

    def patient_reviews_entries(self):
        table_name = 'patient_reviews'
        if self.builder.is_filled(self.schema_name, table_name) is False:
            entries = (
                (('"patient_id"', '1'),
                 ('"facility_id"', '100'),
                 ('"medical_id"', '3'),
                 ('"date_reviewed"', '2018-01-22 21:48:31.582940'),
                 ('"title"', 'Decent Experience'),
                 ('"rating"', '6'),
                 ('"review"', 'Good Price and decent service!'),
                 ('"is_edited"', 'False')),

                (('"patient_id"', '2'),
                 ('"facility_id"', '100'),
                 ('"medical_id"', '2'),
                 ('"date_reviewed"', '2018-02-22 21:48:31.582940'),
                 ('"title"', 'Great Staff'),
                 ('"rating"', '10'),
                 ('"review"', 'The Best Place On Earth!'),
                 ('"is_edited"', 'True'))
            )
            self.builder.fill(self.schema_name, table_name, entries)
        else:
            print("ERROR: {} table is already has data.".format(table_name))

    def patient_sheets_entries(self):
        table_name = 'patient_sheets'
        if self.builder.is_filled(self.schema_name, table_name) is False:
            entries = (
                (('"patient_id"', '1'),
                 ('"facility_id"', '100'),
                 ('"last_editor"', '2'),
                 ('"next_eligible"', '2018-03-11 21:48:31.582940'),
                 ('"next_appointment_date"', '2018-03-11 21:48:31.582940'),
                 ('"last_appointment_date"', '2018-01-13 21:48:31.582940'),
                 ('"special_instructions"', '')),

                (('"patient_id"', '2'),
                 ('"facility_id"', '100'),
                 ('"last_editor"', '2'),
                 ('"next_eligible"', '2018-02-22 21:48:31.582940'),
                 ('"next_appointment_date"', '2018-02-22 21:48:31.582940'),
                 ('"last_appointment_date"', '2018-01-22 21:48:31.582940'),
                 ('"special_instructions"', 'Needs Bandage'))
            )
            self.builder.fill(self.schema_name, table_name, entries)
        else:
            print("ERROR: {} table is already has data.".format(table_name))


def main():
    TableFill()


main()
