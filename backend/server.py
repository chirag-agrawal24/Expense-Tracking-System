from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from pydantic import BaseModel, conint
from typing import List

app=FastAPI()


class Expenses(BaseModel):
    amount :float
    category :str
    notes : str

class DateRange(BaseModel):
    start_date : date
    end_date :date


# Define a Pydantic model for year validation
class YearRequest(BaseModel):
    year: conint(ge=1900, le=2100)  # Year must be an integer between 1900 and 2100

@app.get("/expenses/{expense_date}",response_model=List[Expenses])
def get_expensed(expense_date: date):
    expenses=db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(500,"Failed to retrieve data")

    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date:date,expenses:List[Expenses]):
    db_helper.delete_expenses_for_date(expense_date)

    for exp in expenses:
        db_helper.insert_expense(expense_date,exp.amount,exp.category,exp.notes)
    return {"Message":"Expense updated successfully"}

@app.post('/analytics/')
def get_analytics(date_range : DateRange):
    summary_data=db_helper.fetch_expense_summary(date_range.start_date,date_range.end_date)

    if summary_data is None:
        raise HTTPException(500,"Failed to retrieve data")

    total=sum([row['total_expense'] for row in summary_data])

    breakdown={}
    if total>0:
        for row in summary_data:
            percent=row['total_expense']/total *100
            breakdown[row['category']]={
                "total":row['total_expense'],
                "percentage": round(percent,2)
            }

    return breakdown

@app.post("/analytics_by_month/")
def get_analytics_by_month(year:YearRequest):
    summary_data=db_helper.fetch_expense_by_month(year.year)
    
    if summary_data is None:
        raise HTTPException(500,"Failed to retrieve data")
    
    return summary_data