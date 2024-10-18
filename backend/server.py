from fastapi import FastAPI
from datetime import date
import db_helper
from pydantic import BaseModel
from typing import List

app=FastAPI()


class Expenses(BaseModel):
    amount :float
    category :str
    notes : str

@app.get("/expenses/{expense_date}",response_model=List[Expenses])
def get_expensed(expense_date: date):
    expenses=db_helper.fetch_expenses_for_date(expense_date)
    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date:date,expenses:List[Expenses]):
    db_helper.delete_expenses_for_date(expense_date)

    for exp in expenses:
        db_helper.insert_expense(expense_date,exp.amount,exp.category,exp.notes)
    return {"Message":"Expense updated successfully"}