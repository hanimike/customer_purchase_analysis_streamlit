import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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