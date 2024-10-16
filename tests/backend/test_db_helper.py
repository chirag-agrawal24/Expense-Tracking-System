from backend import db_helper


def test_fetch_expenses_for_date():
    expense=db_helper.fetch_expenses_for_date("2024-08-01")

    assert len(expense)==4

def test_fetch_expenses_for_date_invalid_date():
    expense=db_helper.fetch_expenses_for_date("2420-8-01")

    assert len(expense)==0

def test_fetch_expense_summary():
    summary=db_helper.fetch_expense_summary("2024-08-01","2024-08-02")
    
    assert len(summary)==5

def test_fetch_expense_summary_invalid_range():
    summary=db_helper.fetch_expense_summary("2024-08-10","2024-08-02")
    
    assert len(summary)==0

if __name__=="__main__":
    test_fetch_expense_summary()