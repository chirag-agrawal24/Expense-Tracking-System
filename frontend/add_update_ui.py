import streamlit as st
from datetime import date
import requests
import json

BACKEND_URL = "http://localhost:8000"

def load_categories():
    # Load the categories and permanent categories from the JSON file
    data = json.load(open("../categories.json"))
    return data["categories"], data["permanent_categories"]

@st.fragment
def add_update_tab():
    # Initialize session state for tracking the number of rows
    if 'num_rows' not in st.session_state:
        st.session_state.num_rows = 5  # Default number of rows
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = date.today()

    selected_date = st.date_input("Enter Date:", value=st.session_state.selected_date, label_visibility="collapsed")
    response = requests.get(f"{BACKEND_URL}/expenses/{selected_date}")

    if response.status_code == 200:
        existing_expense = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expense = []
    
    # Add Row button
    add_row_button = st.button("Add Row")
    if add_row_button:
        st.session_state.num_rows += 1  # Increment the number of rows
        st.rerun(scope="fragment") 

    with st.form(key="expense_form"):

        # Load categories and permanent categories
        categories, permanent_categories = load_categories()
        all_categories = categories + permanent_categories  # Combine both regular and permanent categories

        col1, col2, col3 = st.columns(3)
        col1.subheader("Amount")
        col2.subheader("Category")
        col3.subheader("Note")

        n = len(existing_expense)
        updated_expenses = []

        # Loop through the rows and populate inputs
        for i in range(max(st.session_state.num_rows, n+1)):  # Use session state for controlling rows
            if i < n:
                amount = existing_expense[i]['amount']
                category = existing_expense[i]['category']
                note = existing_expense[i]['notes']
            else:
                amount, category, note = 0.0, permanent_categories[-1], ""  # Default category is 'Other'

            # Check if the fetched category exists in the regular categories list
            if category not in categories:
                category = permanent_categories[-1]  # Default to 'Other' if the category is not in the list

            category_index = all_categories.index(category)  # Index in combined list of categories

            # Input fields
            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
                                               label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=all_categories, index=category_index,
                                              key=f"categories_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=note, key=f"notes_{i}", label_visibility="collapsed")

            updated_expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        # Submit button
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Filter out empty expenses and submit updated expenses
            filtered_expenses = [expense for expense in updated_expenses if expense['amount'] > 0]

            response = requests.post(f"{BACKEND_URL}/expenses/{selected_date}", json=filtered_expenses)

            if response.status_code == 200:
                st.success("Expenses Updated Successfully")
            else:
                st.error("Failed to update Expenses")

if __name__ == "__main__":
    # Call the function to display the form
    add_update_tab()
