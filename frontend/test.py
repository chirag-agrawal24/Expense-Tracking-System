import streamlit as st

# Initialize session state for categories if not already done
if 'categories' not in st.session_state:
    st.session_state['categories'] = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

def manage_categories():
    st.title("Manage Categories")  # Title for the categories tab

    # Display existing categories
    st.subheader("Existing Categories")
    for i, category in enumerate(st.session_state['categories']):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.text_input(f"Category {i + 1}", value=category, key=f"category_{i}")
        with col2:
            if st.button("❌", key=f"delete_category_{i}"):
                st.session_state['categories'].pop(i)  # Remove category from session state
                st.rerun()  # Rerun to update UI

    # Section to add a new category
    st.subheader("Add New Category")
    new_category = st.text_input("New Category Name", key="new_category")

    # Button to add the new category
    if st.button("Add Category"):
        if new_category:
            st.session_state['categories'].append(new_category)  # Add new category to the list
            st.success(f"Category '{new_category}' added!")
            st.rerun()  # Rerun to show the new category
        else:
            st.error("Category name cannot be empty!")

# Display the category management tab
manage_categories()
