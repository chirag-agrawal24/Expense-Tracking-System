import streamlit as st
import json

# Load categories from the JSON file
def load_categories():
    with open("../categories.json", "r") as file:
        data = json.load(file)
    return data['categories']

# Save updated categories to the JSON file
def save_categories(categories):
    with open("../categories.json", "w") as file:
        json.dump({"categories": categories}, file)

# Function to manage the categories
@st.fragment()
def manage_categories():
    st.title("Manage Categories")  # Title for the categories tab

    # Load categories from the JSON file
    categories = load_categories()

    # Display existing categories
    st.subheader("Existing Categories")
    for i, category in enumerate(categories):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.text_input(f"Category {i + 1}", value=category, key=f"category_{i}")
        with col2:
            if st.button("❌", key=f"delete_category_{i}"):
                categories.pop(i)  # Remove the category
                save_categories(categories)  # Save the updated list to the file
                st.success(f"Category '{category}' deleted!")
                st.rerun(scope="fragment")  # Rerun to update UI

    # Section to add a new category
    st.subheader("Add New Category")
    new_category = st.text_input("New Category Name", key="new_category")

    # Button to add the new category
    if st.button("Add Category"):
        if new_category:
            if new_category not in categories:
                categories.append(new_category)  # Add the new category to the list
                save_categories(categories)  # Save the updated list to the file
                st.success(f"Category '{new_category}' added!")
                st.rerun(scope="fragment")
                 # Rerun to update UI
            else:
                st.warning(f"Category '{new_category}' already exists!")
        else:
            st.error("Category name cannot be empty!")

if __name__=='__main__':
    #  the category management tab
    manage_categories()
