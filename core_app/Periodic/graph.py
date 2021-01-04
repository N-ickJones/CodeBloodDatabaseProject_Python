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
import numpy as np
# from psycopg2.extensions import AsIs
# from datetime import datetime
# from django.utils import timezone
from random import randint
import matplotlib.pyplot as plt


class Graph:

    def __init__(self):
        self.conn = psycopg2.connect(config('DATABASE_URL'))
        self.entries = []
        self.donate_date_var = []
        self.donate_date_label = []
        self.donate_data = ()
        self.total_donations = []
        self.__fill_entries()

    def build_graph(self):
        # plt.style.use('dark_background')
        plt.figure(figsize=(20, 10))
        plt.plot(self.donate_date_label, self.total_donations, linewidth=3)
        plt.suptitle('', fontsize=20)
        plt.xlabel('YEAR', fontsize=20)
        plt.xticks(fontsize=16, rotation=0)
        plt.ylabel('PINTS OF BLOOD DONATED', fontsize=20)
        plt.yticks(fontsize=20, rotation=0)
        plt.grid(True)
        plt.savefig('../../core_static/assets/images/example.png')

    def build_bar_graph(self):
        plt.style.use('dark_background')
        plt.figure(figsize=(20, 10))
        dates = ('09-2018', '10-2018', '11-2018')
        y_pos = np.arange(len(dates))
        donate_array = self.total_donations
        plt.bar(y_pos, donate_array, width=1, align='edge', alpha=.8, color='red')
        plt.xticks(y_pos, dates, fontsize=16)
        plt.yticks(fontsize=20, rotation=0)
        plt.xlabel('Donation Dates')
        plt.ylabel('Units Of Blood')
        plt.title('Blood Donations')
        plt.savefig('../core_static/assets/images/example_bar_graph.png')
        plt.show()

    def get_donations(self):
        with self.conn.cursor() as cur:
            for date in self.donate_date_var:
                sql = "SELECT donate_amount FROM donations WHERE donate_date Between %s And %s;"
                data = (date[0], date[1])
                add_donations = 0.0
                cur.execute(sql, data)
                self.donate_data = cur.fetchall()
                for data in self.donate_data:
                    add_donations += float(data[0])
                self.total_donations.append(add_donations)

    def check_table(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = 'donations');")
            return True if cur.fetchone()[0] else False

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE public.donations(
                        donate_amount FLOAT,
                        donate_date TIMESTAMP WITH TIME ZONE); """)
        self.conn.commit()

    def fill_table(self):
        sql = "INSERT INTO public.donations (donate_amount, donate_date) VALUES (%s, %s)"
        with self.conn.cursor() as cur:
            for entry in self.entries:
                data = (entry[0], entry[1])
                cur.execute(sql, data)
        self.conn.commit()

    def drop_table(self):
        with self.conn.cursor() as cur:
            cur.execute("drop table donations;")
        self.conn.commit()

    def __fill_entries(self):
        for i in range(2000, 2018, 1):
            for j in range(1, 12, 1):
                amount, year, month = randint(500, 1000), i, j
                day, hour, minute, second = randint(1, 25), randint(0, 23), randint(0, 59), randint(0, 59)
                mill_second = randint(271954, 271955)
                if month < 10:
                    month = '0{}'.format(month)
                if day < 10:
                    day = '0{}'.format(day)
                if hour < 10:
                    hour = '0{}'.format(hour)
                if minute < 10:
                    minute = '0{}'.format(minute)
                if second < 10:
                    second = '0{}'.format(second)
                if len(str(mill_second)) < 6:
                    padding = ''
                    for h in range(len(str(mill_second)), 6):
                        padding = '0{}'.format(padding)
                    mill_second = '{}{}'.format(padding, mill_second)
                timestamp = "{}-{}-{} {}:{}:{}.{}".format(year, month, day, hour,
                            minute, second, mill_second)
                self.entries.append((str(amount), timestamp))
            self.donate_date_var.append(('{}-01-01'.format(i), '{}-12-31'.format(i)))
            self.donate_date_label.append(str(i))

    def __del__(self):
        self.conn.close()
