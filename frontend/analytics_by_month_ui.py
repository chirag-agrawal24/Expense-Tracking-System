import streamlit as st
from datetime import date,timedelta
import requests
import pandas as pd

BACKEND_URL="http://localhost:8000"


def analytics_by_month_tab():
    select_year=st.number_input("Select the Year", min_value=2000, max_value=2100, value=date.today().year)

    response=requests.post(f'{BACKEND_URL}/analytics_by_month/',json={"year":select_year})
    
    if response.status_code==200:
        data=response.json()
        if len(data)>0:
            df=pd.DataFrame(data)
            df.rename(columns={"month_name":"Month"},inplace=True)
            df_sorted = df.sort_values(by="month_no")
            df_sorted.set_index("month_no", inplace=True)
            
            months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']
            df_sorted['Month'] = pd.Categorical(df_sorted['Month'], categories=months_order, ordered=True)


            st.bar_chart(df_sorted,x='Month',y='Amount',)
            st.table(df_sorted.style.format(precision=2))
            
        else:
            st.info("No Data for this Year")
    else:
        st.error("Failed to retrive data")
        