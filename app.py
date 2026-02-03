import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# App title
st.title("Customer Purchasing Behavior Datataset Analysis")

# Load data
st.header("Load Dataset")
data = pd.read_csv("Customer-Purchasing-Behaviors.csv")

# Show raw data
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(data)
    
# Basic statistics
st.subheader("Summary Statistics")
st.write(data.describe())

st.subheader("Shape")
st.write(data.shape)

st.subheader("Head")
st.write(data.head())

st.subheader("Tail")
st.write(data.tail())

st.subheader("Sample")
st.write(data.sample(10))

st.subheader("Columns")
st.write(data.columns)

st.subheader("Data types")
st.write(data.dtypes)

st.subheader("Missing values")
st.write(data.isnull().sum())

# keep only numeric columns
num_df = data.select_dtypes(include="number")

# correlation matrix
corr = num_df.corr()

st.subheader("Correlation Matrix")
st.write(corr)


st.subheader("Regional sale performance")
regional_sales = data.groupby('region')['purchase_amount'].sum() 
st.write("Total Sales by Region:") 
st.write(regional_sales) 
# Identify the region with highest total sales 
st.write(f"Highest purchasing region: {regional_sales.idxmax()} with ${regional_sales.max():,.2f}") 
st.write()


# Customer Region frequency count
freq = data['region'].value_counts()
st.subheader("Customers Per Region") 
st.write(freq) 

# age and purchase  frequency
young_freq = data[data['age'] < 30]['purchase_frequency'].mean() 
senior_freq = data[data['age'] > 50]['purchase_frequency'].mean() 
st.subheader("Purchase Frequency by Age:") 
st.write(f"Under 30: {young_freq:.2f}") 
st.write(f"Over 50: {senior_freq:.2f}") 
st.write(f"More frequent group: {'Young' if young_freq > senior_freq else 
'Senior'}") 
st.write() 

# frequency vs loyalty correlation
freq_loyalty_corr = data['purchase_frequency'].corr(data['loyalty_score']) 
st.subheader("Correlation between frequency and loyalty")
st.write(f"Correlation between frequency and loyalty: {freq_loyalty_corr:.3f}")

# spend per visit
# Spending_per_visit = purchase_amount / purchase_frequency 
for col in ['purchase_amount', 'purchase_frequency', 'loyalty_score']: 
    if col in data.columns: data[col] = pd.to_numeric(data[col], errors='coerce')
data = data.dropna(subset=['purchase_amount', 'purchase_frequency']) 
data = data[data['purchase_frequency'] > 0]
data['spending_per_visit'] = data['purchase_amount'] / data['purchase_frequency'] 
# Top 5 customers who spend the most per visit 
top_spender_per_visit = data.nlargest(5, 'spending_per_visit') 
st.subheader("Top 5 Customers by Spending per Visit:") 
st.write(top_spender_per_visit[['user_id', 'spending_per_visit', 'purchase_amount', 'purchase_frequency']]) 

# LOYALTY TIER CLASSIFICATION
for col in ['purchase_amount', 'purchase_frequency', 'loyalty_score']: 
    if col in data.columns: data[col] = pd.to_numeric(data[col], errors='coerce').astype('float64')
for col in data.select_dtypes(include=['object']).columns: data[col] = data[col].astype(str)
loyalty_bins = [0, 5, 7, 10] 
loyalty_labels = ['Low', 'Medium', 'High'] 
data['loyalty_tier'] = pd.cut(data['loyalty_score'], bins=loyalty_bins, labels=loyalty_labels) 
loyalty_tier_counts = data['loyalty_tier'].value_counts() 
st.subheader(" Customers per Loyalty Tier:") 
st.write(loyalty_tier_counts) 

# CUSTOMER RETENTION INSIGHT
data['purchase_frequency'] = pd.to_numeric(data['purchase_frequency'], errors='coerce')
data['region'] = data['region'].astype(str)
data = data.dropna(subset=['purchase_frequency', 'region'])
north_freq = data[data['region'] == 'North']['purchase_frequency'].mean() 
south_freq = data[data['region'] == 'South']['purchase_frequency'].mean() 
st.subheader("Purchase Frequency by Region:") 
st.write(f"North: {north_freq:.2f}") 
st.write(f"South: {south_freq:.2f}") 
st.write(f"Difference: {abs(north_freq - south_freq):.2f}") 

#  Age Distribution (Histogram)
plt.figure(figsize=(10, 6)) 
plt.hist(data['age'], bins=15, edgecolor='black', alpha=0.7, color='skyblue')
plt.title('Age Distribution of Customers', fontsize=16) 
plt.xlabel('Age', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.grid(alpha=0.3) 
st.pyplot(plt)

# Annual Income vs Purchase Amount (Scatter Plot) 
fig = px.scatter( data, x='annual_income', y='purchase_amount', color='loyalty_score', hover_data=['age', 'region', 'purchase_frequency'], title='Annual Income vs Purchase Amount', labels={ 'annual_income': 'Annual Income ($)', 'purchase_amount': 'Purchase Amount ($)', 'loyalty_score': 'Loyalty Score' } )
st.subheader("Annual Income vs Purchase Amount")
st.plotly_chart(fig)
