import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Nassau Candy Analytics", layout="wide")
st.title("Nassau Candy Distributor Dashboard 🍬")
@st.cache_data
def load_data():
    return pd.read_csv('data/Cleaned_Nassau_Data.csv')
df = load_data()
st.sidebar.header("User Controls")
selected_division = st.sidebar.multiselect("Select Division", df['Division'].unique())
margin_threshold = st.sidebar.slider("Minimum Gross Margin (%)", 0, 100, 10)
if selected_division:
    df = df[df['Division'].isin(selected_division)]
df = df[df['Gross Margin (%)'] >= margin_threshold]
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${df['Gross Profit'].sum():,.2f}")
col3.metric("Avg Gross Margin", f"{df['Gross Margin (%)'].mean():.2f}%")
tab1, tab2, tab3 = st.tabs(["Product Profitability", "Division Performance", "Cost Diagnostics"])
with tab1:
    st.subheader("Product-Level Margin Leaderboard")
with tab2:
    st.subheader("Revenue vs Profit by Division")  
with tab3:
    st.subheader("Cost vs Sales Scatter Analysis")
    fig = px.scatter(df, x='Cost', y='Sales', color='Division', hover_data=['Product Name'])
    st.plotly_chart(fig)
