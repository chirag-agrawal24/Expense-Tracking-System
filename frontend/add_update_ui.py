import streamlit as st
from datetime import date
import requests

BACKEND_URL="http://localhost:8000"


def add_update_tab():
    selected_date= st.date_input("Enter Date:",date.today(),label_visibility="collapsed")
    response= requests.get(f"{BACKEND_URL}/expenses/{selected_date}")

    if response.status_code==200:
        existing_expense=response.json()
        
    else:
        st.error("Failed to retrieve expenses")
        existing_expense=[]
    
    with st.form(key="expense_form"):

        categories=["Rent","Food","Shopping","Entertainment","Other"]# make it dynamic( user can add more category)
        col1,col2,col3=st.columns(3)
        col1.subheader("Amount")
        col2.subheader("Category")
        col3.subheader("Note")
        n=len(existing_expense)
        updated_expenses=[]

        for i in range((5 if 5>n else n+1)): #change it
            if i<n:
                amount=existing_expense[i]['amount']
                category=existing_expense[i]['category']
                note=existing_expense[i]['notes']
            else:
                amount,category,note=0.0,categories[-1],""
            
            category_index=categories.index(category)
            
            with col1:
                amount_input=st.number_input(label="Amount",min_value=0.0,step=1.0,value=amount,key=f"amount_{i}",label_visibility="collapsed")
            with col2:
                category_input=st.selectbox(label="Category",options=categories,index=category_index,key=f"categories_{i}",label_visibility="collapsed",)
            with col3:
                notes_input=st.text_input(label="Notes",value=note,key=f"notes_{i}",label_visibility="collapsed")

            updated_expenses.append({
                'amount':amount_input,
                'category':category_input,
                'notes':notes_input
            })

        submit_button=st.form_submit_button()

        if submit_button:
            filtered_expenses=[expense for expense in updated_expenses if expense['amount']>0]

            response=requests.post(f"{BACKEND_URL}/expenses/{selected_date}",json=filtered_expenses)

            if response.status_code==200:
                st.success("Expenses Updated Successfully")
            else:
                st.error("Failed to update Expenses")