import streamlit as st
from datetime import date,timedelta
import requests
import pandas as pd

BACKEND_URL="http://localhost:8000"


def analytics_tab():
    col1,col2=st.columns(2)
    with col1:
        start_date=st.date_input("From",date.today()-timedelta(days=6))
    with col2:
        end_date=st.date_input("To",date.today())
    
    if st.button("Get Analytics"):
        payload={
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date':end_date.strftime('%Y-%m-%d')
        }

        response=requests.post(f'{BACKEND_URL}/analytics/',json=payload)
        
        if response.status_code==200:
            data=response.json()
            if len(data)>0:
                df=pd.DataFrame(data,).T
                df.rename(columns={'total':'Amount','percentage':'Percentage'},inplace=True)
                df_sorted=df.sort_values('Percentage',ascending=False)

                st.bar_chart(df_sorted['Percentage'],y_label='Percentage')

                st.table(df_sorted.style.format(precision=2))
            else:
                st.info("No Data for this Date Range")
        else:
            st.error("Failed to retrive data")
            