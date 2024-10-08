import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Load the dataset
df = pd.read_csv(r'Imports_Exports_Dataset (1).csv')

# Sample the dataset
df_sample = df.sample(n=3001, random_state=55023)

# Set the title of the dashboard
st.title('Imports and Exports Dashboard')

# Count the number of Import and Export transactions
transaction_counts = df_sample['Import_Export'].value_counts()

# Plot the pie chart
fig1, ax1 = plt.subplots()
ax1.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%', startangle=90, colors=['purple', 'pink'])
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Group the data by Category and Import_Export, then count the number of transactions
category_transaction_counts = df_sample.groupby(['Category', 'Import_Export']).size().unstack()

# Plot a stacked bar chart
fig2, ax2 = plt.subplots()
category_transaction_counts.plot(kind='bar', stacked=True, ax=ax2, color=['purple', 'pink'])
ax2.set_title('Transactions by Category (Stacked by Import/Export)')
ax2.set_xlabel('Category')
ax2.set_ylabel('Number of Transactions')
ax2.legend(title='Transaction Type')

# Count the occurrences of each payment mode
payment_mode_counts = df_sample['Payment_Terms'].value_counts()

# Plot a horizontal bar chart
fig3, ax3 = plt.subplots()
payment_mode_counts.plot(kind='barh', ax=ax3)
ax3.set_title('Most Preferred Payment Modes')
ax3.set_xlabel('Number of Transactions')
ax3.set_ylabel('Payment Mode')

# Convert 'Date' column to datetime format
df_sample['Date'] = pd.to_datetime(df_sample['Date'], format='%d-%m-%Y')

# Extract month from the date
df_sample['Month'] = df_sample['Date'].dt.month

# Group by month and Import_Export, then calculate the average transaction value
monthly_avg_value = df_sample.groupby(['Month', 'Import_Export'])['Value'].mean().unstack()

# Plot the line graph
fig4, ax4 = plt.subplots()

# Plot each import and export line
for column in monthly_avg_value.columns:
    ax4.plot(monthly_avg_value.index, monthly_avg_value[column], marker='o', label=column)

ax4.set_title('Average Value of Transactions by Month')
ax4.set_xlabel('Month')
ax4.set_ylabel('Average Transaction Value')
ax4.grid(True)
ax4.legend(title='Transaction Type')

# Arrange 2 graphs per row and align subheaders
col1, col2 = st.columns(2)

# First row: Pie chart and Stacked bar chart
with col1:
    st.subheader('Percentage of Import and Export Transactions')
    st.pyplot(fig1)

with col2:
    st.subheader('Transactions by Category (Stacked by Import/Export)')
    st.pyplot(fig2)

# Second row: Bar chart of Payment Modes and Line graph of Average Transaction Value
col3, col4 = st.columns(2)

with col3:
    st.subheader('Most Preferred Payment Modes')
    st.pyplot(fig3)

with col4:
    st.subheader('Average Value of Transactions by Month')
    st.pyplot(fig4)
