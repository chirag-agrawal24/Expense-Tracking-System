import streamlit as st
from add_update_ui import add_update_tab
from analytics_by_categories_ui import analytics_by_categories_tab
from analytics_by_month_ui import analytics_by_month_tab
from update_category_ui import manage_categories

BACKEND_URL="http://localhost:8000"

st.title("Expense Management System")

tab1 , tab2,tab3, tab4 =st.tabs(["Add/Update","Analytics By category","Analytics Monthly","Manage Categories"])

with tab1:
    add_update_tab()
    

with tab2:
    analytics_by_categories_tab()

with tab3:
    analytics_by_month_tab()

with tab4:
    manage_categories()