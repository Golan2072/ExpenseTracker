import sqlite3
from datetime import date
import pandas as pd


def create_database():
    with sqlite3.connect("expense_base.db") as connection:
        cursor = connection.cursor()
        create_expense_table_query = """CREATE TABLE IF NOT EXISTS Expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, sum REAL, type TEXT, payment TEXT, date TEXT);"""
        create_income_table_query = """CREATE TABLE IF NOT EXISTS Incomes (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, sum REAL, type TEXT, date TEXT);"""
        cursor.execute(create_expense_table_query)
        cursor.execute(create_income_table_query)
        connection.commit()


def insert_query_func(command, data):
    with sqlite3.connect("expense_base.db") as connection:
        cursor = connection.cursor()
        cursor.execute(command, data)
        connection.commit()


def insert_expense(description, sum, type, payment, date):
    insert_query = """INSERT INTO Expenses (description, sum, type, payment, date) VALUES (?, ?, ?, ?, ?);"""
    data = (description, sum, type, payment, date)
    insert_query_func(insert_query, data)


def insert_income(description, sum, type, date):
    insert_query = """INSERT INTO Incomes (description, sum, type, date) VALUES (?, ?, ?, ?);"""
    data = (description, sum, type, date)
    insert_query_func(insert_query, data)


def retrieve_multiple_expenses(number):
    with sqlite3.connect("expense_base.db") as connection:
        cursor = connection.cursor()
        select_query = """SELECT * FROM Expenses;"""
        cursor.execute(select_query)
        if number == 0:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(number)


def retrieve_multiple_incomes(number):
    with sqlite3.connect("expense_base.db") as connection:
        cursor = connection.cursor()
        select_query = """SELECT * FROM Incomes;"""
        cursor.execute(select_query)
        if number == 0:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(number)

def expenses_dataframe():
    with sqlite3.connect("expense_base.db") as connection:
        cursor = connection.cursor()
        select_query = """SELECT * FROM Expenses WHERE date >= date('now', '-1 month');"""
        return pd.read_sql_query(select_query, connection)

def expenses_dataframe_annual():
    with sqlite3.connect("expense_base.db") as connection:
        cursor = connection.cursor()
        select_query = """SELECT * FROM Expenses WHERE date >= date('now', '-1 year');"""
        return pd.read_sql_query(select_query, connection)

def incomes_dataframe():
    with sqlite3.connect("expense_base.db") as connection:
        cursor = connection.cursor()
        select_query = """SELECT * FROM Incomes WHERE date >= date("now", "-1 month");"""
        return pd.read_sql_query(select_query, connection)
    
def incomes_dataframe_annual():
    with sqlite3.connect("expense_base.db") as connection:
        cursor = connection.cursor()
        select_query = """SELECT * FROM Incomes WHERE date >= date("now", "-1 year");"""
        return pd.read_sql_query(select_query, connection)