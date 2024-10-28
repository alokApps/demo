import streamlit as st
import pandas as pd
from optimization import get_optimal_portfolio,get_invested_amount



############  side bar 
# st.sidebar.title("Revolutionizing Investment")
st.set_page_config(
     page_title="Revolutionizing Investment",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.google.com',
         #'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "AI managed investment portfolio"
     }
 )

st.sidebar.title("Input requirements")
term_list = ["short","mid","long"]
risk_list = ['low','mid','high']

with st.container():
    capital = st.sidebar.number_input("Total Capital",min_value=500)
    term = st.sidebar.selectbox("Choose Term:",term_list)
    risk = st.sidebar.selectbox("Risk Apetite:",risk_list)

    submit = st.sidebar.button("Get Recommendation")

##########  body 
flag = False
col1, col2,col3 = st.columns(3)


def on_subscribe():
    st.write("Subscription successful")

if submit:
    with st.spinner("Please wait"): 
        recommendation = get_optimal_portfolio(capital, term, risk)
        with col1:
            st.write(f"Recommended stocks for {term } term ")

            st.dataframe(recommendation, use_container_width=True,height= 35*len(recommendation)+38)

            #########  submit button to subscribe 
            flag = True
            subs = st.button("subscribe",on_click=on_subscribe,)             


            
            
         
        
        with col2:
            st.write(f'Total investment: {get_invested_amount(recommendation)}')
            



