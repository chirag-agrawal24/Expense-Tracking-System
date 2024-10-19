import streamlit as st
from datetime import date
import requests

BACKEND_URL = "http://localhost:8000"



def add_update_tab():
    # Initialize session state for tracking the number of rows
    if 'num_rows' not in st.session_state:
        st.session_state.num_rows = 5  # Default number of rows
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = date.today()

    selected_date = st.date_input("Enter Date:", st.session_state.selected_date, label_visibility="collapsed",key="selected_date")
    response = requests.get(f"{BACKEND_URL}/expenses/{selected_date}")

    if response.status_code == 200:
        existing_expense = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expense = []
    add_row_button = st.button("Add Row")
    if add_row_button:
        st.session_state.num_rows += 1  # Increment the number of rows
        st.rerun()

    with st.form(key="expense_form"):

        categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]  # make it dynamic (user can add more categories)
        col1, col2, col3 = st.columns(3)
        col1.subheader("Amount")
        col2.subheader("Category")
        col3.subheader("Note")
        
        n = len(existing_expense)
        updated_expenses = []

        # Make sure the number of rows reflects either the number of existing expenses or default rows in session state
        for i in range(max(st.session_state.num_rows, n)):  # Use session state for controlling rows
            if i < n:
                amount = existing_expense[i]['amount']
                category = existing_expense[i]['category']
                note = existing_expense[i]['notes']
            else:
                amount, category, note = 0.0, categories[-1], ""

            category_index = categories.index(category)

            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
                                               label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=category_index,
                                              key=f"categories_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=note, key=f"notes_{i}", label_visibility="collapsed")

            updated_expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        # Add button to allow user to add more rows


        submit_button = st.form_submit_button("Submit")

        if submit_button:
            filtered_expenses = [expense for expense in updated_expenses if expense['amount'] > 0]

            response = requests.post(f"{BACKEND_URL}/expenses/{selected_date}", json=filtered_expenses)

            if response.status_code == 200:
                st.success("Expenses Updated Successfully")
            else:
                st.error("Failed to update Expenses")


# Call the function to display the form
add_update_tab()
