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
    margin_data = df.groupby('Product Name')['Gross Margin (%)'].mean().reset_index()
    margin_data = margin_data.sort_values('Gross Margin (%)', ascending=True)
    fig1 = px.bar(
        margin_data, 
        x='Gross Margin (%)', 
        y='Product Name', 
        orientation='h',
        color='Gross Margin (%)',
        color_continuous_scale='RdYlGn',
        text_auto='.2f'
    )
    fig1.update_layout(xaxis_title="Gross Margin (%)", yaxis_title="")
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    st.subheader("Revenue vs Profit by Division")
    div_data = df.groupby('Division')[['Sales', 'Gross Profit']].sum().reset_index()
    fig2 = px.bar(
        div_data, 
        x='Division', 
        y=['Sales', 'Gross Profit'],
        barmode='group',
        color_discrete_sequence=['#34495e', '#27ae60'],
        labels={'value': 'Amount ($)', 'variable': 'Metric'}
    )
    fig2.update_layout(yaxis_title="Total Value ($)")
    st.plotly_chart(fig2, use_container_width=True)
with tab3:
    fig3 = px.scatter(
        df, 
        x='Cost', 
        y='Sales', 
        color='Division', 
        hover_data=['Product Name', 'Gross Margin (%)'],
        size_max=10
    )
    st.plotly_chart(fig3, use_container_width=True)