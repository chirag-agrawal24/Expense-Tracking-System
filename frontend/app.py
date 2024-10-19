import streamlit as st
from add_update_ui import add_update_tab
from analytics_by_categories_ui import analytics_by_categories_tab
from analytics_by_month_ui import analytics_by_month_tab


BACKEND_URL="http://localhost:8000"

st.title("Expense Management System")

tab1 , tab2,tab3=st.tabs(["Add/Update","Analytics By category","Analytics Monthly"])

with tab1:
    add_update_tab()
    

with tab2:
    analytics_by_categories_tab()

with tab3:
    analytics_by_month_tab()