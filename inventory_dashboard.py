import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objects as go

st.set_page_config(page_title="Inventory Dashboard", layout="wide")
sns.set_style("whitegrid")

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_master_inventory.csv", parse_dates=["salesdate", "startdate", "enddate"])

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("🔍 Filters")
brands = st.sidebar.multiselect("Select Brand(s)", df['brand'].dropna().unique())
abcs = st.sidebar.multiselect("Select ABC Category", ['A', 'B', 'C'])

# Apply Filters
if brands:
    df = df[df['brand'].isin(brands)]
if abcs:
    df = df[df['ABC'].isin(abcs)]

# --- Header & KPIs ---
st.title("📦 Inventory Intelligence Dashboard")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total SKUs", df['inventoryid'].nunique())
col2.metric("Avg Turnover", round(df['inventory_turnover'].mean(), 2))
col3.metric("Avg DIO", round(df['DIO'].mean(), 1))
col4.metric("C-Item Overstock", df[(df['ABC'] == 'C') & (df['inventory_health'] == 'Overstock')].shape[0])

st.divider()

# --- Inventory Health Pie ---
st.subheader("🩺 Inventory Health")
fig1, ax1 = plt.subplots()
df['inventory_health'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#ffcccb', '#c2f0c2', '#d9d9d9'], ax=ax1)
ax1.set_ylabel("")
st.pyplot(fig1)

# --- ABC Category Count ---
st.subheader("🔠 ABC Classification")
fig2, ax2 = plt.subplots()
sns.countplot(data=df, x='ABC', palette='pastel', ax=ax2)
st.pyplot(fig2)

# --- Overstocked C-Items Table ---
st.subheader("📛 Overstocked C-Items")
c_over = df[(df['ABC'] == 'C') & (df['inventory_health'] == 'Overstock')]
st.dataframe(c_over[['inventoryid', 'brand', 'description', 'onhand', 'salesquantity', 'inventory_age_days']].reset_index(drop=True))

# --- Vendor Performance Table ---
st.subheader("🚚 Vendor Scorecard")
if 'vendorname' in df.columns:
    vendor_perf = df.groupby('vendorname')[['avg_lead_time', 'on_time_delivery_pct']].mean().dropna()
    vendor_perf = vendor_perf.sort_values(by='on_time_delivery_pct', ascending=False)
    st.dataframe(vendor_perf.reset_index())

# --- Reorder Point Breaches ---
st.subheader("⏰ Procurement Triggers")
reorders = df[df['trigger_reorder']]
st.dataframe(reorders[['inventoryid', 'brand', 'description', 'onhand', 'ROP', 'EOQ', 'reorder_qty']].reset_index(drop=True))

# --- Forecast Monthly Demand (Prophet) ---
st.subheader("📈 Forecast Monthly Demand (Prophet)")
sku_list = df['inventoryid'].dropna().unique()
sku_choice = st.selectbox("Select Inventory ID", sku_list)

sku_df = df[df['inventoryid'] == sku_choice]
ts = sku_df.groupby('salesdate')['salesquantity'].sum().reset_index().rename(columns={'salesdate': 'ds', 'salesquantity': 'y'})

if len(ts) >= 6:
    model = Prophet()
    model.fit(ts)
    future = model.make_future_dataframe(periods=6, freq='M')
    forecast = model.predict(future)
    st.plotly_chart(plot_plotly(model, forecast), use_container_width=True)
    st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(6))
else:
    st.warning("⚠️ Not enough sales data for Prophet (min 6 months required).")

# --- Footer ---
st.markdown("📊 Built with ❤️ by [Your Name] – Inventory Analytics Toolkit")
