import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
import json

logger=setup_logger("db_helper")

@contextmanager
def get_db_cursor(commit=False):
    with open("sql.json") as con:
        connection_dict=json.load(con)

    connection=mysql.connector.connect(
        **connection_dict
    )
    # cursor is to read / write data
    cursor = connection.cursor(dictionary=True)
    yield cursor

    #commit if there is any data update
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date is called with date: {expense_date}")

    with get_db_cursor() as cursor:

        cursor.execute("SELECT * FROM expenses where expense_date = %s; ",(expense_date,))
        expenses=cursor.fetchall()
        return expenses

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date is called with date: {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        
        cursor.execute("DELETE FROM expenses where expense_date= %s;",(expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense is called with date: {expense_date},amount: {amount},category: {category} ,notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s,%s,%s,%s);",
        (expense_date, amount, category, notes))


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary is called with start date: {start_date} , end date : {end_date}")
    with get_db_cursor() as cursor:
        
        cursor.execute("""SELECT category,SUM(amount) as total_expense
        FROM expenses
        WHERE expense_date BETWEEN %s and %s
        GROUP BY category;
        """,(start_date, end_date))
        data = cursor.fetchall()
        return data
    
def fetch_expense_by_month(year):
    logger.info(f"fetch_expense_by_month is called with YEAR:{year}")
    with get_db_cursor() as cursor:
        
        cursor.execute("""select
            month(expense_date) as month_no,
            monthname(expense_date) as month_name,
            sum(amount) as Amount
            from expenses
            where YEAR(expense_date)=%s
            group by month(expense_date),monthname(expense_date);""",(year,))
        
        data = cursor.fetchall()
        return data

def fetch_expense_monthly_trend(year):
    logger.info(f"fetch_expense_by_monthly_trend is called with YEAR:{year}")
    with get_db_cursor() as cursor:
        
        cursor.execute("""select
                                month(expense_date) as month_no,
                                monthname(expense_date) as month_name,
                                category,
                                sum(amount) as Amount
                            from expenses
                            where YEAR(expense_date)=%s
                            group by month(expense_date),monthname(expense_date),category
                            order by month_no
                            """,(year,))
        data = cursor.fetchall()
        return data
    


if __name__=="__main__":
    # expenses=fetch_expenses_for_date("2024-08-02")
    # print(expenses)

    insert_expense("2025-09-01",45,'FOOD','Ice Cream')
    expenses=fetch_expenses_for_date("2025-09-01")
    print(expenses)

    delete_expenses_for_date("2025-09-01")
    expenses=fetch_expenses_for_date("2025-09-01")
    print(expenses)

    summary=fetch_expense_summary("2024-08-01","2024-08-05")
    for record in summary:
        print(record)
    data=fetch_expense_by_month(2024)
    print(data)
