import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_db_cursor(commit=False):

    connection=mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="expense_manager"
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
    with get_db_cursor() as cursor:

        cursor.execute("SELECT * FROM expenses where expense_date = %s; ",(expense_date,))
        expenses=cursor.fetchall()
        return expenses

def delete_expenses_for_date(expense_date):
    with get_db_cursor(commit=True) as cursor:
        
        cursor.execute("DELETE FROM expenses where expense_date= %s;",(expense_date,))


def insert_expense(expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s,%s,%s,%s);",
        (expense_date, amount, category, notes))


def fetch_expense_summary(start_date, end_date):
    with get_db_cursor() as cursor:
        
        cursor.execute("""SELECT category,SUM(amount) as total_expense
        FROM expenses
        WHERE expense_date BETWEEN %s and %s
        GROUP BY category;
        """,(start_date, end_date))
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
